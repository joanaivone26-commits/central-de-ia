#!/usr/bin/env python3
"""Painel admin local da Central Trip Angle.

Uso:
  python3 tools/admin.py [--port N] [--no-open]

Escuta só em 127.0.0.1 (porta padrão: adminPort do hub.config.json, 4545). Serve o site gerado (dist/),
o painel (/admin) e a API /admin-api/*. Toda escrita reconstrói o catálogo.
Só usa a biblioteca padrão do Python 3.9+.
"""
import argparse
import datetime
import json
import mimetypes
import re
import shlex
import shutil
import subprocess
import sys
import threading
import time
import traceback
import urllib.parse
import webbrowser
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hubcore as hc  # noqa: E402
import build  # noqa: E402
import importers as imp  # noqa: E402

MAX_BODY = 25 * 1024 * 1024
WRITE_LOCK = threading.RLock()
STATE = {"port": 4545}
SIDE_KEYS = ("title", "description", "tags", "author", "license", "version", "source", "scan", "featured",
             "addedAt", "notes")
CONFIG_KEYS = ("name", "shortName", "tagline", "description", "siteUrl", "githubRepo", "branch",
               "marketplaceName", "socials", "cta")
MIME = {
    ".html": "text/html", ".htm": "text/html", ".css": "text/css", ".js": "text/javascript",
    ".mjs": "text/javascript", ".json": "application/json", ".map": "application/json",
    ".webmanifest": "application/manifest+json", ".md": "text/markdown", ".txt": "text/plain",
    ".py": "text/x-python", ".sh": "text/x-shellscript", ".bash": "text/x-shellscript", ".ts": "text/plain",
    ".yaml": "text/yaml", ".yml": "text/yaml", ".toml": "text/plain", ".csv": "text/csv",
    ".xml": "application/xml", ".xsd": "application/xml", ".svg": "image/svg+xml", ".png": "image/png",
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp",
    ".ico": "image/x-icon", ".avif": "image/avif", ".woff": "font/woff", ".woff2": "font/woff2",
    ".ttf": "font/ttf", ".otf": "font/otf", ".pdf": "application/pdf", ".zip": "application/zip",
    ".mp4": "video/mp4", ".webm": "video/webm", ".mp3": "audio/mpeg", ".wasm": "application/wasm",
}
TEXT_TYPES = ("application/json", "application/manifest+json", "application/xml", "image/svg+xml",
              "text/javascript")


class ApiError(Exception):
    def __init__(self, status, msg, **extra):
        super().__init__(msg)
        self.status = status
        self.extra = extra


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def base_url():
    return f"http://localhost:{STATE['port']}"


# ---------------------------------------------------------------- utilidades

def rebuild():
    res = build.build(quiet=True)
    return {"count": len(res["items"]), "warnings": res["warnings"][:50]}


def catalog_items():
    path = hc.DIST / "api" / "catalog.json"
    data = hc.load_json(path)
    if data is None:
        with WRITE_LOCK:
            rebuild()
        data = hc.load_json(path, {"items": []})
    return data.get("items", [])


def find_item(item_id):
    for it in catalog_items():
        if it["id"] == item_id:
            return it
    return None


def mime_for(path):
    ext = Path(path).suffix.lower()
    ctype = MIME.get(ext) or (mimetypes.guess_type(str(path))[0] if ext else "text/plain") or "application/octet-stream"
    if ctype.startswith("text/") or ctype in TEXT_TYPES:
        ctype += "; charset=utf-8"
    return ctype


def run_git(args, timeout=60):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", LC_ALL="C")
    try:
        p = subprocess.run(["git"] + list(args), cwd=str(hc.ROOT), capture_output=True, text=True,
                           timeout=timeout, env=env)
        return p.returncode, p.stdout, p.stderr
    except FileNotFoundError:
        return 127, "", "git não encontrado"
    except subprocess.TimeoutExpired:
        return 124, "", f"git {' '.join(args)}: tempo esgotado"


def git_is_root():
    if not shutil.which("git"):
        return False, "git não encontrado"
    rc, out, err = run_git(["rev-parse", "--show-toplevel"])
    if rc != 0:
        return False, None
    top = Path(out.strip()).resolve()
    if top != hc.ROOT.resolve():
        return False, str(top)
    return True, None


def git_info():
    info = {"repo": False, "remote": None, "branch": None, "dirty": None, "lastCommit": None}
    ok, other = git_is_root()
    if not ok:
        if other:
            info["note"] = ("git não encontrado" if other == "git não encontrado"
                            else f"a raiz da Central fica dentro de outro repositório git ({other})")
        return info
    info["repo"] = True
    rc, out, _ = run_git(["remote", "get-url", "origin"])
    info["remote"] = out.strip() if rc == 0 and out.strip() else None
    rc, out, _ = run_git(["symbolic-ref", "--short", "HEAD"])
    if rc != 0:
        rc, out, _ = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    info["branch"] = out.strip() if rc == 0 else None
    rc, out, _ = run_git(["status", "--porcelain"])
    info["dirty"] = bool(out.strip()) if rc == 0 else None
    rc, out, _ = run_git(["log", "-1", "--format=%h %cI %s"])
    if rc == 0 and out.strip():
        sha, date, subject = (out.strip().split(" ", 2) + ["", ""])[:3]
        info["lastCommit"] = {"sha": sha, "date": date, "message": subject}
    return info


def side_path_for(item):
    base = hc.ROOT / item["base"]
    if item.get("kind") == "dir":
        return base / hc.SIDE
    return base.parent / (base.stem + hc.SIDE)


def yaml_scalar(text):
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    if not text:
        return '""'
    if re.search(r"[:#\[\]{},&*!|>'\"%@`]", text) or text[0] in "-?" or text.lower() in ("true", "false", "null", "yes", "no"):
        return json.dumps(text, ensure_ascii=False)
    return text


def clean_meta(meta):
    if meta is None:
        return {}
    if not isinstance(meta, dict):
        raise ApiError(400, "meta precisa ser um objeto.")
    out = {}
    for k in SIDE_KEYS:
        if k not in meta:
            continue
        v = meta[k]
        if k == "tags":
            if isinstance(v, str):
                v = [t.strip() for t in v.split(",") if t.strip()]
            elif isinstance(v, list):
                v = [str(t).strip() for t in v if str(t).strip()]
            elif v is not None:
                raise ApiError(400, "tags precisa ser uma lista ou texto separado por vírgulas.")
        elif k == "featured":
            v = bool(v) if v is not None else None
        elif k in ("source", "scan"):
            if v is not None and not isinstance(v, dict):
                raise ApiError(400, f"{k} precisa ser um objeto.")
        elif v is not None:
            v = str(v).strip()
        out[k] = v
    return out


def parse_json_text(text, what="JSON"):
    try:
        return json.loads(text)
    except ValueError as exc:
        line = getattr(exc, "lineno", None)
        col = getattr(exc, "colno", None)
        where = f" (linha {line}, coluna {col})" if line else ""
        raise ApiError(400, f"{what} inválido{where}: {getattr(exc, 'msg', exc)}")


def no_dots(*values):
    for v in values:
        if v is not None and ".." in str(v):
            raise ApiError(400, f"Caminho inválido: {v}")


# ---------------------------------------------------------------- rotas: leitura

def api_ping(q, body=None):
    return {"ok": True, "config": hc.load_config(), "root": str(hc.ROOT), "port": STATE["port"],
            "adminUrl": base_url() + "/admin", "git": git_info()}


def api_item(q, body=None):
    item_id = (q.get("id") or "").strip()
    if not item_id:
        raise ApiError(400, "Informe o id (ex.: skills/copy/copywriting).")
    item = find_item(item_id)
    if not item:
        raise ApiError(404, f"Componente não encontrado: {item_id}")
    base = hc.ROOT / item["base"]
    main = base / item["main"] if item.get("kind") == "dir" else base
    content = None
    if main.is_file():
        content = main.read_bytes()[:3 * 1024 * 1024].decode("utf-8", "replace")
    side = None if item.get("partOf") else hc.load_json(side_path_for(item))
    out = {"ok": True}
    out.update(item)
    out.update({"item": item, "content": content, "side": side})
    return out


def api_aitmpl_search(q, body=None):
    try:
        limit = int(q.get("limit") or 50)
    except ValueError:
        limit = 50
    res = imp.aitmpl_search(q.get("q") or "", q.get("type") or None, limit)
    return dict({"ok": True}, **res)


# ---------------------------------------------------------------- rotas: escrita

def api_component(q, body):
    type_id = str(body.get("type") or "").strip()
    category = str(body.get("category") or "").strip()
    name = str(body.get("name") or "").strip()
    no_dots(type_id, category, name)
    if type_id not in hc.TYPE_BY_ID:
        raise ApiError(400, f"Tipo inválido: {type_id or '(vazio)'}. Use: {', '.join(t['id'] for t in hc.TYPES)}.")
    imp.validate_ids(type_id, category, name)
    imp.ensure_category(category)
    overwrite = bool(body.get("overwrite"))
    meta = clean_meta(body.get("meta"))
    content = body.get("content")
    if content is not None and not isinstance(content, str):
        raise ApiError(400, "content precisa ser texto.")
    files = body.get("files")
    kind = hc.TYPE_BY_ID[type_id]["kind"]
    exists = imp.component_main(type_id, category, name).exists()
    if exists and not overwrite:
        raise ApiError(409, f"Já existe: {type_id}/{category}/{name}. Marque sobrescrever para atualizar.")
    if files is not None:
        if kind != "dir":
            raise ApiError(400, "files só vale para skills, templates e plugins.")
        if not isinstance(files, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in files.items()):
            raise ApiError(400, 'files precisa ser {"caminho/relativo": "texto"}.')
        if len(files) > 500:
            raise ApiError(400, "Arquivos demais (máximo 500).")
        clean = {}
        for k, v in files.items():
            no_dots(k)
            rk = imp.safe_rel(k)
            if Path(rk).name == hc.SIDE:
                raise ApiError(400, f"Use meta em vez de {hc.SIDE}.")
            clean[rk] = v.encode("utf-8")
        files = clean
    if (content is None or not content.strip()) and not exists:
        raise ApiError(400, "Conteúdo vazio.")
    warnings = []
    data = None
    if content is not None and content.strip():
        if kind == ".json" or type_id == "plugins":
            data = parse_json_text(content)
            if not isinstance(data, dict):
                raise ApiError(400, "O JSON precisa ser um objeto { ... }.")
            if type_id == "mcps":
                servers = data.get("mcpServers")
                if not isinstance(servers, dict) or not servers:
                    raise ApiError(400, 'MCP precisa ter "mcpServers" com ao menos um servidor.')
                bad = [k for k, v in servers.items() if not isinstance(v, dict) or not (v.get("command") or v.get("url"))]
                if bad:
                    raise ApiError(400, f"Servidor MCP sem command ou url: {', '.join(bad)}")
            elif type_id == "hooks":
                hooks = data.get("hooks")
                if not isinstance(hooks, dict) or not hooks:
                    raise ApiError(400, 'Hook precisa ter "hooks" com ao menos um evento (ex.: Stop, PreToolUse).')
                unknown = [k for k in hooks if k not in imp.HOOK_EVENTS]
                if unknown:
                    warnings.append("evento(s) desconhecido(s) do Claude Code: " + ", ".join(unknown))
                if not all(isinstance(v, list) for v in hooks.values()):
                    raise ApiError(400, "Cada evento de hook precisa ser uma lista.")
            elif type_id in ("repos", "sites"):
                if not re.match(r"^https?://\S+$", str(data.get("url") or "")):
                    raise ApiError(400, 'Informe "url" começando com http(s)://.')
            elif type_id == "plugins":
                if not data.get("name"):
                    data["name"] = name
                    content = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        elif type_id in ("skills", "agents", "commands", "templates"):
            fm, _ = hc.parse_frontmatter(content)
            has_fm = content.startswith("---") and bool(fm)
            desc = meta.get("description") or ""
            if type_id in ("skills", "agents") and not has_fm:
                content = f"---\nname: {name}\ndescription: {yaml_scalar(desc)}\n---\n\n" + content.lstrip("\n")
                if not desc:
                    warnings.append("sem descrição: preencha meta.description para o Claude saber quando usar")
            elif type_id == "commands" and not has_fm and desc:
                content = f"---\ndescription: {yaml_scalar(desc)}\n---\n\n" + content.lstrip("\n")
            elif has_fm and type_id in ("skills", "agents") and isinstance(fm.get("name"), str) and fm["name"] != name:
                warnings.append(f"o frontmatter diz name: {fm['name']}, diferente do nome {name}")
        elif type_id in ("prompts", "frameworks"):
            fm, body = hc.parse_frontmatter(content)
            if not (content.startswith("---") and fm):
                titulo = meta.get("title") or hc.humanize(name)
                desc = meta.get("description") or ""
                content = (f"---\ntitle: {yaml_scalar(titulo)}\ndescription: {yaml_scalar(desc)}\n---\n\n"
                           + content.lstrip("\n"))
                if not desc:
                    warnings.append("sem descrição: preencha a descrição para aparecer bem no site")
            if type_id == "prompts":
                declarados = fm.get("variables") if isinstance(fm.get("variables"), dict) else {}
                soltas = sorted(set(hc.VAR_RE.findall(body)) - set(declarados))
                if soltas:
                    warnings.append("variáveis sem rótulo em variables: " + ", ".join(soltas))
        main = content.encode("utf-8")
    else:
        main = None
    with WRITE_LOCK:
        res = imp.write_component(type_id, category, name, main=main, files=files, side=meta,
                                  overwrite=overwrite, mode="update")
        b = rebuild()
    log(f"{'criado' if res['created'] else 'atualizado'} {res['id']}")
    return {"ok": True, "id": res["id"], "created": res["created"], "path": res["path"],
            "item": find_item(res["id"]), "warnings": warnings, "build": b}


def api_delete(q, body):
    item_id = str(body.get("id") or "").strip().strip("/")
    no_dots(item_id)
    parts = item_id.split("/")
    if len(parts) != 3 or parts[0] not in hc.TYPE_BY_ID:
        raise ApiError(400, "id inválido (use tipo/categoria/nome).")
    item = find_item(item_id)
    if item and item.get("partOf"):
        raise ApiError(400, f"Este item faz parte do plugin {item['partOf']}: apague ou edite o plugin.")
    if item:
        base = hc.ROOT / item["base"]
        if item.get("kind") == "dir":
            paths = [base]
        else:
            paths = imp.component_paths(item["type"], base.parent.name, base.stem)
    else:
        paths = imp.component_paths(parts[0], parts[1], parts[2])
    if not paths:
        raise ApiError(404, f"Componente não encontrado: {item_id}")
    for p in paths:
        if hc.COMPONENTS.resolve() not in Path(p).resolve().parents:
            raise ApiError(400, "Só dá para apagar itens de components/.")
    with WRITE_LOCK:
        moved = [hc.rel(p) for p in paths]
        parents = {Path(p).parent for p in paths}
        trash = imp.move_to_trash(paths)
        for d in parents:
            try:
                if d.is_dir() and d.parent.parent == hc.COMPONENTS and not any(d.iterdir()):
                    d.rmdir()
            except OSError:
                pass
        b = rebuild()
    log(f"apagado {item_id} → {trash}")
    return {"ok": True, "id": item_id, "trash": trash, "moved": moved, "build": b}


def _write_categories(cats):
    lines = ",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in cats)
    (hc.ROOT / "categories.json").write_text("[\n" + lines + "\n]\n", encoding="utf-8")


def api_category(q, body):
    cid = str(body.get("id") or "").strip()
    no_dots(cid)
    if not cid or not hc.NAME_RE.match(cid):
        raise ApiError(400, f"id de categoria inválido: {cid or '(vazio)'}. Use minúsculas e hífens (sugestão: {hc.slugify(cid)}).")
    with WRITE_LOCK:
        cats = hc.load_json(hc.ROOT / "categories.json", []) or []
        entry = next((c for c in cats if c.get("id") == cid), None)
        created = entry is None
        label = body.get("label")
        if created and not str(label or "").strip():
            raise ApiError(400, "Informe o rótulo (label) da categoria.")
        if created:
            entry = {"id": cid, "label": "", "icon": "•", "description": ""}
            cats.append(entry)
        for k in ("label", "icon", "description"):
            if body.get(k) is not None:
                v = str(body[k]).strip()
                if k == "label" and not v:
                    raise ApiError(400, "O rótulo não pode ficar vazio.")
                entry[k] = v or ("•" if k == "icon" else "")
        if body.get("order") is not None:
            try:
                entry["order"] = int(body["order"])
            except (TypeError, ValueError):
                raise ApiError(400, "order precisa ser um número.")
        _write_categories(cats)
        b = rebuild()
    log(f"categoria {'criada' if created else 'atualizada'}: {cid}")
    return {"ok": True, "category": entry, "created": created, "build": b}


def api_config(q, body):
    unknown = [k for k in body if k not in CONFIG_KEYS]
    changes = {}
    for k in CONFIG_KEYS:
        if k not in body:
            continue
        v = body[k]
        if k == "cta":
            if not isinstance(v, dict):
                raise ApiError(400, "cta precisa ser um objeto com youtube, site e produtos.")
            def link(x, onde):
                u = str((x or {}).get("url") or "").strip()
                if u and not re.match(r"^https://[^\s]+$", u):
                    raise ApiError(400, f"{onde}: o link precisa começar com https://")
                return u
            limpo = {}
            for chave in ("youtube", "site"):
                x = v.get(chave) or {}
                if isinstance(x, dict) and link(x, chave):
                    limpo[chave] = {"url": link(x, chave), "titulo": str(x.get("titulo") or "")[:120],
                                    "texto": str(x.get("texto") or "")[:300]}
            prods = []
            for i, x in enumerate(v.get("produtos") or []):
                if not isinstance(x, dict) or not link(x, f"produto {i + 1}"):
                    continue
                prods.append({"titulo": str(x.get("titulo") or "")[:120], "descricao": str(x.get("descricao") or "")[:300],
                              "url": link(x, f"produto {i + 1}"), "selo": str(x.get("selo") or "")[:30]})
            limpo["produtos"] = prods[:6]
            changes[k] = limpo
            continue
        if k == "socials":
            if isinstance(v, str):
                v = [s.strip() for s in v.split(",") if s.strip()]
            if not isinstance(v, list) or not all(isinstance(s, str) for s in v):
                raise ApiError(400, "socials precisa ser uma lista de textos.")
            v = [s.strip() for s in v if s.strip()][:20]
        else:
            v = "" if v is None else str(v).strip()
            if len(v) > 1000:
                raise ApiError(400, f"{k} longo demais.")
        if k == "githubRepo" and v:
            m = imp.parse_github_url(v)
            if m and m.get("mode") is None:
                v = f"{m['owner']}/{m['repo']}"
            if not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", v) or v.endswith(".git"):
                raise ApiError(400, "githubRepo precisa estar no formato dono/repo (ex.: tripangle/central).")
        if k == "siteUrl" and v:
            if not re.match(r"^https?://[^\s/$.?#][^\s]*$", v):
                raise ApiError(400, "siteUrl precisa começar com http:// ou https:// (ou ficar vazio).")
            v = v.rstrip("/")
        if k == "branch" and v and not re.match(r"^[A-Za-z0-9._/-]+$", v):
            raise ApiError(400, "branch inválido.")
        if k == "marketplaceName" and v and not hc.NAME_RE.match(v):
            raise ApiError(400, "marketplaceName precisa ser minúsculas e hífens (ex.: trip-angle).")
        if k in ("name", "shortName", "branch", "marketplaceName") and not v:
            raise ApiError(400, f"{k} não pode ficar vazio.")
        changes[k] = v
    remote_added = False
    note = None
    with WRITE_LOCK:
        cfg_path = hc.ROOT / "hub.config.json"
        raw = hc.load_json(cfg_path, {}) or {}
        raw.update(changes)
        hc.write_json(cfg_path, raw)
        b = rebuild()
        repo = changes.get("githubRepo") or ""
        if repo:
            ok, _ = git_is_root()
            if ok:
                rc, out, _ = run_git(["remote", "get-url", "origin"])
                if rc != 0 or not out.strip():
                    url = f"https://github.com/{repo}.git"
                    rc, out, err = run_git(["remote", "add", "origin", url])
                    if rc == 0:
                        remote_added = True
                        log(f"remoto origin adicionado: {url}")
                    else:
                        note = f"não consegui adicionar o remoto origin: {(err or out).strip()}"
            else:
                note = "a pasta da Central não é um repositório git; o remoto não foi configurado"
    log("configuração atualizada: " + (", ".join(changes) or "nada"))
    info = git_info()
    res = {"ok": True, "config": hc.load_config(), "remoteAdded": remote_added, "remote": info.get("remote"),
           "build": b}
    if unknown:
        res["ignored"] = unknown
    if note:
        res["note"] = note
    return res


def api_repo(q, body):
    url = str(body.get("url") or "").strip()
    if not url:
        raise ApiError(400, "Informe a URL do repositório.")
    with WRITE_LOCK:
        res = imp.add_repo(url, body.get("category"), body.get("name"), body.get("description"),
                           body.get("tags"), bool(body.get("overwrite")))
        b = rebuild()
    log(f"repositório {res['id']}")
    return {"ok": True, "id": res["id"], "path": res["path"], "created": res["created"], "repo": res["repo"],
            "item": find_item(res["id"]), "build": b}


def api_scan(q, body):
    res = imp.scan(body.get("source"))
    log(f"scan {res['source'].get('repo')}: {len(res['items'])} candidato(s)")
    return {"ok": True, "source": res["source"], "items": res["items"], "candidates": res["items"],
            "warnings": res["warnings"]}


def _import_response(res, key):
    imported, errors = res["imported"], res["errors"]
    warnings = [f"{it['id']}: {w}" for it in imported for w in it.get("warnings", [])]
    warnings += [f"não importado {e.get(key)}: {e['error']}" for e in errors]
    out = {"ok": bool(imported) or not errors, "imported": imported, "errors": errors, "warnings": warnings}
    if not imported and errors:
        out["error"] = errors[0]["error"] if len(errors) == 1 else f"{len(errors)} itens falharam: " + "; ".join(
            f"{e.get(key)}: {e['error']}" for e in errors[:5])
    return out


def api_apply(q, body):
    items = body.get("items")
    if not isinstance(items, list) or not items:
        raise ApiError(400, "Escolha ao menos um item.")
    for it in items:
        if not isinstance(it, dict):
            raise ApiError(400, "Cada item precisa ser {kind, path, name?, category}.")
        no_dots(it.get("path"), it.get("name"), it.get("category"))
    with WRITE_LOCK:
        res = imp.apply(body.get("source"), items, overwrite=bool(body.get("overwrite")),
                        category=body.get("category"))
        out = _import_response(res, "path")
        if res["imported"]:
            out["build"] = rebuild()
    log(f"importados {len(res['imported'])}, erros {len(res['errors'])}")
    out["source"] = res["source"]
    if not out["ok"]:
        raise ApiError(400 if all("Já existe" not in e["error"] for e in res["errors"]) else 409, out["error"], **out)
    return out


def api_aitmpl_import(q, body):
    ids = body.get("ids")
    if isinstance(ids, str):
        ids = [ids]
    if not isinstance(ids, list) or not ids:
        raise ApiError(400, "Informe ids, ex.: [\"skills/business-marketing/copywriting\"].")
    for i in ids:
        no_dots(i)
    with WRITE_LOCK:
        res = imp.aitmpl_import(ids, body.get("category") or None, bool(body.get("overwrite")))
        out = _import_response(res, "id")
        if res["imported"]:
            out["build"] = rebuild()
    log(f"aitmpl: importados {len(res['imported'])}, erros {len(res['errors'])}")
    if not out["ok"]:
        raise ApiError(409 if any("Já existe" in e["error"] for e in res["errors"]) else 400, out["error"], **out)
    return out


def api_rebuild(q, body):
    with WRITE_LOCK:
        b = rebuild()
    log(f"build: {b['count']} componentes")
    return {"ok": True, "build": b, "count": b["count"], "warnings": b["warnings"]}


def api_publish(q, body):
    msg = str(body.get("message") or "").strip() or ("Atualiza a Central (" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ")")
    ok, other = git_is_root()
    if not ok:
        if other and other != "git não encontrado":
            raise ApiError(400, f"A pasta da Central não é a raiz de um repositório git (achei {other}). Rode git init na pasta da Central.")
        raise ApiError(400, "Esta pasta não é um repositório git. Rode git init e configure o remoto.")
    out_lines = []

    def step(args, timeout=60):
        rc, out, err = run_git(args, timeout)
        out_lines.append("$ git " + " ".join(shlex.quote(a) for a in args))
        text = (out + err).strip()
        if text:
            out_lines.append(text)
        return rc, out, err

    with WRITE_LOCK:
        b = rebuild()
        rc, _, _ = step(["add", "-A"])
        if rc != 0:
            raise ApiError(500, "git add falhou.", output="\n".join(out_lines))
        rc, out, _ = run_git(["status", "--porcelain"])
        committed = False
        if out.strip():
            rc, _, _ = step(["commit", "-m", msg])
            if rc != 0:
                hint = ""
                joined = "\n".join(out_lines)
                if "user.email" in joined or "Please tell me who you are" in joined:
                    hint = " Configure: git config user.name \"Seu Nome\" e git config user.email voce@exemplo.com."
                raise ApiError(500, "O commit falhou." + hint, output=joined, committed=False, pushed=False)
            committed = True
        rc, remotes, _ = run_git(["remote"])
        remotes = [r for r in remotes.split() if r]
        pushed = False
        push_error = None
        if remotes:
            rc_up, _, _ = run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
            remote = "origin" if "origin" in remotes else remotes[0]
            args = ["push"] if rc_up == 0 else ["push", "-u", remote, "HEAD"]
            rc, _, _ = step(args, timeout=180)
            pushed = rc == 0
            if not pushed:
                push_error = "O push falhou" + (" (commit feito só local)." if committed else ".")
    if committed and pushed:
        message = "Publicado: commit feito e enviado (git push)."
    elif committed and not remotes:
        message = "Commit feito. Sem remoto configurado: nada foi enviado."
    elif committed:
        message = "Commit feito, mas o push falhou."
    elif pushed:
        message = "Nada mudou desde o último commit. Push conferido."
    elif not remotes:
        message = "Nada mudou desde o último commit. Sem remoto configurado."
    else:
        message = "Nada mudou desde o último commit."
    log(message)
    output = "\n".join(out_lines)
    if push_error:
        raise ApiError(502, push_error, output=output, committed=committed, pushed=False, message=message)
    return {"ok": True, "committed": committed, "pushed": pushed, "message": message, "output": output,
            "build": b, "git": git_info()}


def api_plugin(q, body):
    category = str(body.get("category") or "").strip()
    name = str(body.get("name") or "").strip()
    description = str(body.get("description") or "").strip()
    version = str(body.get("version") or "1.0.0").strip()
    members = body.get("members")
    no_dots(category, name)
    imp.validate_ids("plugins", category, name)
    imp.ensure_category(category)
    if not description:
        raise ApiError(400, "Informe a descrição do plugin.")
    if not re.match(r"^[0-9A-Za-z.+-]{1,40}$", version):
        raise ApiError(400, "Versão inválida (ex.: 1.0.0).")
    if not isinstance(members, list) or not members:
        raise ApiError(400, "Escolha ao menos uma skill, agente, comando, prompt ou framework (members).")
    overwrite = bool(body.get("overwrite"))
    if imp.component_main("plugins", category, name).exists() and not overwrite:
        raise ApiError(409, f"Já existe: plugins/{category}/{name}. Marque sobrescrever para substituir.")
    items = {it["id"]: it for it in catalog_items()}
    payload, used, lines, missing = {}, set(), [], []
    for mid in members:
        mid = str(mid).strip()
        it = items.get(mid)
        if not it:
            missing.append(mid)
            continue
        if it["type"] not in ("skills", "agents", "commands", "prompts", "frameworks"):
            raise ApiError(400, f"Plugins aceitam só skills, agentes, comandos, prompts e frameworks: {mid}")
        destino = {"prompts": "commands", "frameworks": "skills"}.get(it["type"], it["type"])
        nome = hc.framework_skill_name(it["name"]) if it["type"] == "frameworks" else it["name"]
        key = (destino, nome)
        if key in used:
            raise ApiError(400, f"Nome repetido no plugin: {destino}/{nome}")
        used.add(key)
        base = hc.ROOT / it["base"]
        if it["type"] == "skills":
            for f in hc.list_files(base):
                payload[f"skills/{it['name']}/{f.relative_to(base).as_posix()}"] = f.read_bytes()
        elif it["type"] == "prompts":
            payload[f"commands/{nome}.md"] = hc.prompt_to_command(base.read_text(encoding="utf-8"), it).encode("utf-8")
        elif it["type"] == "frameworks":
            payload[f"skills/{nome}/SKILL.md"] = hc.framework_to_skill(base.read_text(encoding="utf-8"), it).encode("utf-8")
        else:
            payload[f"{it['type']}/{it['name']}.md"] = base.read_bytes()
        label = {"skills": "Skill", "agents": "Agente", "commands": "Comando", "prompts": "Prompt",
                 "frameworks": "Framework"}[it["type"]]
        lines.append(f"- **{label} {it['name']}**: {it.get('description', '')[:200]}")
    if missing:
        raise ApiError(400, "Não encontrei: " + ", ".join(missing))
    cfg = hc.load_config()
    keywords = body.get("keywords") or body.get("tags") or []
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    manifest = {"name": name, "version": version, "description": description,
                "author": {"name": str(body.get("author") or cfg.get("owner", {}).get("name") or "Trip Angle")}}
    if keywords:
        manifest["keywords"] = [str(k) for k in keywords][:20]
    payload[".claude-plugin/plugin.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    title = hc.humanize(name)
    readme = f"# {title}\n\n{description}\n\n## Conteúdo\n\n" + "\n".join(lines) + "\n"
    payload["README.md"] = readme.encode("utf-8")
    side = {"addedAt": imp.today(), "tags": manifest.get("keywords"),
            "notes": "Montado no painel a partir de: " + ", ".join(str(m) for m in members)}
    with WRITE_LOCK:
        res = imp.write_component("plugins", category, name, files=payload, side=side, overwrite=overwrite,
                                  mode="replace")
        b = rebuild()
    log(f"plugin {res['id']} com {len(members)} item(ns)")
    return {"ok": True, "id": res["id"], "path": res["path"], "created": res["created"], "members": members,
            "item": find_item(res["id"]), "build": b}


GET_ROUTES = {
    "/admin-api/ping": api_ping,
    "/admin-api/item": api_item,
    "/admin-api/aitmpl/search": api_aitmpl_search,
}
POST_ROUTES = {
    "/admin-api/component": api_component,
    "/admin-api/component/delete": api_delete,
    "/admin-api/category": api_category,
    "/admin-api/config": api_config,
    "/admin-api/repo": api_repo,
    "/admin-api/import/scan": api_scan,
    "/admin-api/import/apply": api_apply,
    "/admin-api/aitmpl/import": api_aitmpl_import,
    "/admin-api/rebuild": api_rebuild,
    "/admin-api/publish": api_publish,
    "/admin-api/plugin": api_plugin,
}


# ---------------------------------------------------------------- servidor HTTP

class Handler(BaseHTTPRequestHandler):
    server_version = "CentralTA-Admin/1.0"
    sys_version = ""

    def log_request(self, code="-", size="-"):
        path = self.path.split("?", 1)[0]
        if path.startswith("/admin-api/") or (isinstance(code, int) and code >= 400):
            log(f"{code} {self.command} {path}")

    def log_message(self, fmt, *args):  # silencia o log padrão
        pass

    # -------- respostas
    def _send(self, status, body, ctype, extra_headers=None, head=False):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        for k, v in (extra_headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if not head:
            self.wfile.write(body)

    def _json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8",
                   {"Cache-Control": "no-store", "X-Frame-Options": "DENY"}, head=self.command == "HEAD")

    def _error(self, status, msg, **extra):
        data = {"ok": False, "error": msg}
        data.update({k: v for k, v in extra.items() if k not in ("ok", "error")})
        self._json(status, data)

    # -------- segurança
    def _host_ok(self):
        host = (self.headers.get("Host") or "").strip().lower()
        port = STATE["port"]
        return host in (f"localhost:{port}", f"127.0.0.1:{port}")

    def _origin_ok(self):
        origin = self.headers.get("Origin")
        if origin is None:
            return True
        port = STATE["port"]
        return origin.strip().lower() in (f"http://localhost:{port}", f"http://127.0.0.1:{port}")

    # -------- métodos
    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        if not self._host_ok():
            return self._error(403, "Host não permitido. Acesse por http://localhost:%d" % STATE["port"])
        parsed = urllib.parse.urlsplit(self.path)
        path = urllib.parse.unquote(parsed.path)
        if path.startswith("/admin-api/"):
            if self.command == "HEAD" and path not in GET_ROUTES:
                return self._error(405, "Método não permitido.")
            fn = GET_ROUTES.get(path)
            if not fn:
                if path in POST_ROUTES:
                    return self._error(405, "Use POST nesta rota.")
                return self._error(404, f"Rota não encontrada: {path}")
            q = {k: v[-1] for k, v in urllib.parse.parse_qs(parsed.query, keep_blank_values=True).items()}
            return self._call(fn, q, None)
        return self._static(path)

    def do_POST(self):
        if not self._host_ok():
            return self._error(403, "Host não permitido. Acesse por http://localhost:%d" % STATE["port"])
        if not self._origin_ok():
            return self._error(403, "Origem não permitida.")
        path = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
        fn = POST_ROUTES.get(path)
        if not fn:
            if path in GET_ROUTES:
                return self._error(405, "Use GET nesta rota.")
            return self._error(404, f"Rota não encontrada: {path}")
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if ctype != "application/json":
            return self._error(415, "Envie o corpo como JSON (Content-Type: application/json).")
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return self._error(400, "Content-Length inválido.")
        if length > MAX_BODY:
            return self._error(413, "Corpo grande demais (máximo 25 MB).")
        raw = self.rfile.read(length) if length > 0 else b""
        if raw.strip():
            try:
                body = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                return self._error(400, "JSON inválido no corpo da requisição.")
        else:
            body = {}
        if not isinstance(body, dict):
            return self._error(400, "O corpo precisa ser um objeto JSON.")
        return self._call(fn, {}, body)

    def do_PUT(self):
        self._error(405, "Método não permitido.")

    do_DELETE = do_PATCH = do_OPTIONS = do_PUT

    def _call(self, fn, q, body):
        try:
            data = fn(q, body)
            self._json(200, data)
        except ApiError as exc:
            self._error(exc.status, str(exc), **exc.extra)
        except imp.ImportFailure as exc:
            status = exc.status if 400 <= exc.status <= 599 else 400
            self._error(status, str(exc))
        except Exception as exc:  # noqa: BLE001
            traceback.print_exc()
            self._error(500, f"Erro interno: {exc}")

    # -------- arquivos
    def _static(self, path):
        head = self.command == "HEAD"
        if path == "/admin/":
            return self._redirect("/admin")
        if path in ("/admin", "/admin.html"):
            return self._file(hc.SITE / "admin.html", no_store=True, missing="site/admin.html ainda não existe.")
        if path == "/assets/admin.js":
            return self._file(hc.SITE / "assets" / "admin.js", no_store=True, missing="site/assets/admin.js ainda não existe.")
        if path == "/tahub.py":
            cli = hc.ROOT / "tools" / "tahub.py"
            if not cli.is_file():
                return self._text(404, "tools/tahub.py ainda não existe.")
            text = cli.read_text(encoding="utf-8").replace(build.SOURCE_PLACEHOLDER, base_url())
            return self._send(200, text.encode("utf-8"), "text/x-python; charset=utf-8",
                              {"Cache-Control": "no-store"}, head=head)
        dist = hc.DIST.resolve()
        if not dist.is_dir():
            return self._text(503, "dist/ não existe: o build falhou. Veja o terminal ou rode python3 tools/build.py.")
        relp = path.lstrip("/")
        target = (dist / relp).resolve() if relp else dist
        if target != dist and dist not in target.parents:
            return self._text(404, "Não encontrado.")
        if target.is_dir():
            if not path.endswith("/") and relp:
                return self._redirect(path + "/")
            target = target / "index.html"
        no_store = relp.startswith("api/") or relp in ("marketplace.json", "llms.txt")
        return self._file(target, no_store=no_store)

    def _redirect(self, location):
        self.send_response(301)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _text(self, status, msg):
        self._send(status, (msg + "\n").encode("utf-8"), "text/plain; charset=utf-8",
                   {"Cache-Control": "no-store"}, head=self.command == "HEAD")

    def _file(self, path, no_store=False, missing="Não encontrado."):
        path = Path(path)
        if not path.is_file():
            return self._text(404, missing)
        data = path.read_bytes()
        headers = {"Cache-Control": "no-store" if no_store else "no-cache"}
        if path.suffix in (".html", ".htm") and path.parent == hc.SITE:
            headers["X-Frame-Options"] = "DENY"
        return self._send(200, data, mime_for(path), headers, head=self.command == "HEAD")


class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main(argv=None):
    cfg = hc.load_json(hc.ROOT / "hub.config.json", {}) or {}
    ap = argparse.ArgumentParser(prog="admin.py", description="Painel admin local da Central Trip Angle.")
    ap.add_argument("--port", type=int, default=int(cfg.get("adminPort") or 4545))
    ap.add_argument("--no-open", action="store_true", help="não abre o navegador")
    args = ap.parse_args(argv)
    STATE["port"] = args.port
    try:
        server = Server(("127.0.0.1", args.port), Handler)
    except OSError as exc:
        print(f"erro: não consegui usar a porta {args.port} ({exc.strerror or exc}). Tente --port {args.port + 1}.",
              file=sys.stderr)
        return 1
    try:
        b = rebuild()
        log(f"Catálogo gerado: {b['count']} componentes, {len(b['warnings'])} aviso(s).")
    except Exception as exc:  # noqa: BLE001
        traceback.print_exc()
        log(f"aviso: o build falhou ({exc}). O painel abre mesmo assim.")
    url = base_url() + "/admin"
    log(f"Painel da Central: {url}  (site: {base_url()}/)  Ctrl+C para sair.")
    if not args.no_open:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        log("Painel encerrado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
