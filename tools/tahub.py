#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Central Trip Angle: instalador de componentes para o Claude Code.

Um arquivo só. Python 3.9+ e só a biblioteca padrão.

    python3 tahub.py                              modo interativo
    python3 tahub.py --skill copy/copywriting     instala uma skill
    python3 tahub.py --help                       todas as opções
"""
import argparse
import copy
import datetime
import difflib
import errno
import glob
import hashlib
import json
import os
import platform
import re
import shlex
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import textwrap
import threading
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath

VERSION = "1.0.0"
DEFAULT_SOURCE = "__TAHUB_DEFAULT_SOURCE__"
_MARKER = "__TAHUB_" + "DEFAULT_SOURCE__"  # montado em partes para o build não trocar
USER_AGENT = "trip-angle-hub-cli"
TIMEOUT = 20
MAX_FILE = 25 * 1024 * 1024
MAX_CATALOG = 64 * 1024 * 1024
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
CENTRAL_KEYS = ("description", "scripts", "$schema")
SCOPES = ("local", "project", "user")
ANALYTICS_PORT = 3333
CHATS_PORT = 9876
EXIT_OK, EXIT_ERR, EXIT_USAGE, EXIT_CANCEL = 0, 1, 2, 130

# id, flag, rótulo, singular (mesma ordem de hubcore.TYPES)
TYPES = [
    ("prompts", "prompts", "Prompts", "Prompt"),
    ("skills", "skill", "Skills", "Skill"),
    ("agents", "agent", "Agentes", "Agente"),
    ("frameworks", "framework", "Frameworks", "Framework"),
    ("commands", "command", "Comandos", "Comando"),
    ("mcps", "mcp", "MCPs", "MCP"),
    ("hooks", "hook", "Hooks", "Hook"),
    ("settings", "setting", "Settings", "Setting"),
    ("plugins", "plugin", "Plugins", "Plugin"),
    ("templates", "template", "Templates", "Template"),
    ("repos", "repo", "Repositórios", "Repositório"),
]
TYPE_IDS = [t[0] for t in TYPES]
FLAG = {t[0]: t[1] for t in TYPES}
LABEL = {t[0]: t[2] for t in TYPES}
SINGULAR = {t[0]: t[3] for t in TYPES}


# ================================================================ terminal

def _isatty(stream):
    try:
        return bool(stream.isatty())
    except Exception:  # noqa: BLE001
        return False


def _color_ok(stream):
    return _isatty(stream) and not os.environ.get("NO_COLOR") and os.environ.get("TERM") != "dumb"


for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except Exception:  # noqa: BLE001
        pass

COLOR = _color_ok(sys.stdout)
ECOLOR = _color_ok(sys.stderr)


def paint(text, code, on=None):
    on = COLOR if on is None else on
    return "\033[%sm%s\033[0m" % (code, text) if on else str(text)


def red(t):
    return paint(t, "1;31")


def bold(t):
    return paint(t, "1")


def dim(t):
    return paint(t, "2")


def green(t):
    return paint(t, "32")


def yellow(t):
    return paint(t, "33")


def tag(t):
    return red("[") + " " + bold(t) + " " + red("]")


def banner(sub="instalador"):
    return red("▲") + " " + bold("CENTRAL TRIP ANGLE") + dim("  ·  " + sub)


def sym(s):
    return {"+": green("+"), "~": yellow("~"), "!": yellow("!"), "=": dim("="), "$": dim("$"),
            "·": dim("·")}.get(s, s)


def warn(msg):
    print(yellow("!") + " " + msg)


def print_error(msg, hint=None):
    try:
        sys.stdout.flush()
    except Exception:  # noqa: BLE001
        pass
    print(paint("✗ erro:", "1;31", ECOLOR) + " " + msg, file=sys.stderr)
    if hint:
        for line in str(hint).split("\n"):
            print("  " + line, file=sys.stderr)


class HubError(Exception):
    def __init__(self, msg, hint=None, code=EXIT_ERR):
        super().__init__(msg)
        self.msg = msg
        self.hint = hint
        self.code = code


def short(text, n=90):
    t = re.sub(r"\s+", " ", str(text or "")).strip()
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def _fold_table():
    table = {c: chr(c + 32) for c in range(0x41, 0x5B)}
    for c in range(0xC0, 0x250):
        ch = chr(c)
        base = "".join(x for x in unicodedata.normalize("NFKD", ch) if not unicodedata.combining(x)).lower()
        if len(base) == 1 and base != ch:
            table[c] = base
        elif len(ch.lower()) == 1 and ch.lower() != ch:
            table[c] = ch.lower()
    return table


FOLD = _fold_table()


def fold(s):
    """Minúsculas sem acento, mantendo o tamanho do texto (índices continuam valendo)."""
    return str(s or "").translate(FOLD)


ALIAS = {}
for _tid, _flag, _label, _sing in TYPES:
    for _a in (_tid, _flag, "--" + _flag, _label, _sing):
        ALIAS[fold(_a)] = _tid
ALIAS.update({"agente": "agents", "agentes": "agents", "comando": "commands", "comandos": "commands",
              "repositorio": "repos", "repositorios": "repos", "pacote": "plugins", "pacotes": "plugins",
              "bundle": "plugins", "bundles": "plugins"})


def type_alias(s):
    return ALIAS.get(fold(str(s or "").strip()))


def ask(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        raise KeyboardInterrupt


def confirm(question):
    return ask("%s [S/n] " % question).lower() in ("", "s", "sim", "y", "yes")


# ================================================================ caminhos

def claude_user_dir():
    env = os.environ.get("CLAUDE_CONFIG_DIR", "").strip()
    if env:
        return Path(os.path.abspath(os.path.expanduser(env)))
    return Path(os.path.expanduser("~")) / ".claude"


def _inside(path, root):
    p = os.path.realpath(str(path))
    r = os.path.realpath(str(root))
    return p == r or p.startswith(r.rstrip(os.sep) + os.sep)


def guard(path, roots):
    for r in roots:
        if _inside(path, r):
            return
    raise HubError("caminho fora da pasta de destino recusado: %s" % path,
                   hint="Confira se .claude ou alguma subpasta é um link para fora do projeto.")


def safe_rel(p):
    """Caminho relativo vindo do catálogo: sem '..', sem absoluto, sem truques."""
    if not isinstance(p, str) or not p.strip() or "\x00" in p or "\\" in p:
        raise HubError("caminho inválido no catálogo: %r" % (p,))
    if p.startswith("/") or p.startswith("~") or re.match(r"^[A-Za-z]:", p):
        raise HubError("caminho absoluto recusado no catálogo: %s" % p)
    parts = [x for x in p.split("/") if x not in ("", ".")]
    if not parts or any(x == ".." for x in parts):
        raise HubError("caminho com '..' recusado no catálogo: %s" % p)
    return "/".join(parts)


def script_path():
    f = globals().get("__file__")
    if not f:
        return None
    try:
        p = Path(os.path.abspath(f))
        if str(p).startswith(("/dev/", "/proc/")) or not p.is_file():
            return None
        return p.resolve()
    except (OSError, RuntimeError, ValueError):
        return None


def project_dir(d):
    p = Path(os.path.abspath(os.path.expanduser(d or os.getcwd())))
    if os.path.realpath(str(p)) == os.path.abspath(os.sep):
        raise HubError("não instalo na raiz do sistema (-d /).", hint="Use -d com a pasta do seu projeto.")
    if p.exists() and not p.is_dir():
        raise HubError("-d precisa ser uma pasta: %s" % p)
    return p


# ================================================================ origem e catálogo

def http_get(url, limit=MAX_FILE, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    host = urllib.parse.urlsplit(url).netloc
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read(limit + 1)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise HubError("não encontrado na origem (HTTP 404): %s" % url)
        raise HubError("a origem respondeu HTTP %s: %s" % (e.code, url))
    except urllib.error.URLError as e:
        reason = str(getattr(e, "reason", e))
        hint = None
        if "CERTIFICATE_VERIFY_FAILED" in reason:
            hint = "Faltam certificados SSL no Python. No macOS rode 'Install Certificates.command' da pasta do Python."
        raise HubError("sem conexão com %s (%s)" % (host, reason), hint)
    except socket.timeout:
        raise HubError("tempo esgotado ao baixar %s" % url)
    except OSError as e:
        raise HubError("falha de rede ao baixar %s: %s" % (url, e))
    if len(data) > limit:
        raise HubError("arquivo grande demais na origem: %s" % url)
    return data


class Source:
    def __init__(self, spec, origin):
        self.origin = origin
        spec = str(spec).strip()
        if re.match(r"^https?://", spec, re.I):
            self.kind = "url"
            self.base = spec.rstrip("/")
        else:
            if spec.lower().startswith("file://"):
                spec = urllib.parse.unquote(urllib.parse.urlsplit(spec).path)
            p = Path(os.path.abspath(os.path.expanduser(spec)))
            if (p / "api" / "catalog.json").is_file():
                pass
            elif (p / "dist" / "api" / "catalog.json").is_file():
                p = p / "dist"
            elif p.name == "catalog.json" and p.parent.name == "api" and p.is_file():
                p = p.parent.parent
            elif not p.exists():
                raise HubError("origem não encontrada: %s" % spec,
                               hint="Use --source com uma URL http(s) ou uma pasta que tenha api/catalog.json.")
            self.kind = "dir"
            self.base = p
        self._catalog = None

    def describe(self):
        return self.base if self.kind == "url" else "%s (pasta local)" % self.base

    def url_for(self, rel):
        return self.base + "/" + urllib.parse.quote(rel, safe="/-._~")

    def read(self, rel, limit=MAX_FILE):
        rel = safe_rel(rel)
        if self.kind == "url":
            return http_get(self.url_for(rel), limit)
        path = self.base / rel
        if not _inside(path, self.base):
            raise HubError("arquivo fora da origem recusado: %s" % rel)
        try:
            if os.path.getsize(path) > limit:
                raise HubError("arquivo grande demais na origem: %s" % rel)
            with open(path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise HubError("arquivo não encontrado na origem: %s" % rel,
                           hint="O catálogo pode estar desatualizado. Rode o build de novo.")
        except IsADirectoryError:
            raise HubError("esperava um arquivo e achei uma pasta na origem: %s" % rel)
        except OSError as e:
            raise HubError("não consegui ler %s: %s" % (rel, e.strerror or e))

    def catalog(self):
        if self._catalog is None:
            raw = self.read("api/catalog.json", MAX_CATALOG)
            try:
                data = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                raise HubError("catálogo inválido em %s" % self.describe())
            if not isinstance(data, dict) or not isinstance(data.get("items"), list):
                raise HubError("catálogo sem a lista de itens em %s" % self.describe())
            self._catalog = Catalog(data)
        return self._catalog


def pick_source(arg):
    if arg:
        return Source(arg, "--source")
    env = os.environ.get("TAHUB_SOURCE", "").strip()
    if env:
        return Source(env, "TAHUB_SOURCE")
    d = (DEFAULT_SOURCE or "").strip()
    if d and d != _MARKER:
        return Source(d, "padrão")
    sp = script_path()
    if sp:
        for cand in (sp.parent.parent / "dist", sp.parent):
            if (cand / "api" / "catalog.json").is_file():
                return Source(str(cand), "repositório")
    raise HubError("nenhuma origem de catálogo configurada.",
                   hint="Use --source <url-ou-pasta> ou defina a variável TAHUB_SOURCE.")


class Catalog:
    def __init__(self, data):
        self.data = data
        self.hub = data.get("hub") if isinstance(data.get("hub"), dict) else {}
        self.items = []
        for it in data.get("items") or []:
            if not isinstance(it, dict) or it.get("type") not in TYPE_IDS or not isinstance(it.get("name"), str):
                continue
            it.setdefault("category", "geral")
            it["category"] = str(it["category"])
            it.setdefault("id", "%s/%s/%s" % (it["type"], it["category"], it["name"]))
            if not isinstance(it.get("description"), str):
                it["description"] = str(it.get("description") or "")
            if not isinstance(it.get("tags"), list):
                it["tags"] = []
            self.items.append(it)
        self.by_id = {i["id"]: i for i in self.items}
        self.by_type = {t: [] for t in TYPE_IDS}
        for it in self.items:
            self.by_type[it["type"]].append(it)
        self.bundles = [b for b in (data.get("bundles") or [])
                        if isinstance(b, dict) and isinstance(b.get("name"), str) and b["name"]]
        self.categories = {}
        for i, c in enumerate(data.get("categories") or []):
            if isinstance(c, dict) and c.get("id"):
                c.setdefault("order", i)
                self.categories[c["id"]] = c

    def of_type(self, t):
        return self.by_type.get(t, [])

    def count(self, t):
        return len(self.of_type(t))

    def cat_label(self, cid):
        return (self.categories.get(cid) or {}).get("label") or cid

    def cat_order(self, cid):
        o = (self.categories.get(cid) or {}).get("order", 999)
        return o if isinstance(o, (int, float)) else 999

    def marketplace(self):
        return str(self.hub.get("marketplaceName") or "trip-angle")


def item_spec(it):
    return "%s/%s" % (it["category"], it["name"])


def cli_prefix(src):
    if src.kind == "url":
        return "python3 <(curl -fsSL %s/tahub.py)" % src.base
    sp = script_path()
    if sp:
        try:
            rel = os.path.relpath(str(sp))
            show = rel if not rel.startswith(".." + os.sep + "..") else str(sp)
        except ValueError:
            show = str(sp)
        pre = "python3 " + shlex.quote(show)
    else:
        pre = "python3 tahub.py"
    if src.origin == "--source":
        pre += " --source " + shlex.quote(str(src.base))
    return pre


def install_cmd(src, tid, spec):
    return "%s --%s %s" % (cli_prefix(src), FLAG[tid], spec)


# ================================================================ busca de itens

def find_items(cat, tid, spec):
    s = str(spec or "").strip().strip("/")
    if not s:
        return []
    if s in cat.by_id and (tid is None or cat.by_id[s]["type"] == tid):
        return [cat.by_id[s]]
    parts = s.split("/")
    pool = cat.of_type(tid) if tid else cat.items
    if len(parts) >= 3:
        t = type_alias(parts[0])
        if not t or (tid and t != tid):
            return []
        name = "/".join(parts[2:])
        return [i for i in cat.of_type(t) if i["category"] == parts[1] and i["name"] == name]
    if len(parts) == 2:
        a, b = parts
        res = [i for i in pool if i["category"] == a and i["name"] == b]
        if not res:
            t = type_alias(a)
            if t and (tid is None or t == tid):
                res = [i for i in cat.of_type(t) if i["name"] == b]
        return res
    n = parts[0]
    res = [i for i in pool if i["name"] == n or (i["type"] == "plugins" and i.get("pluginName") == n)]
    if not res:
        res = [i for i in pool if i["name"].lower() == n.lower()]
    return res


def _suggest(cat, tid, spec):
    pool = cat.of_type(tid) if tid else cat.items
    specs = [item_spec(i) for i in pool]
    names = [i["name"] for i in pool]
    sug = difflib.get_close_matches(spec, specs, n=3, cutoff=0.5)
    if not sug:
        last = spec.split("/")[-1]
        hits = difflib.get_close_matches(last, names, n=3, cutoff=0.55)
        sug = [item_spec(i) for i in pool if i["name"] in hits][:3]
    return sug


def resolve_item(cat, tid, spec):
    res = find_items(cat, tid, spec)
    if len(res) == 1:
        return res[0]
    if not res:
        hint = []
        sug = _suggest(cat, tid, spec)
        if sug:
            hint.append("Talvez: " + ", ".join(sug))
        hint.append('Busque com --search "%s" ou veja a lista com --list %s' % (spec.split("/")[-1], tid))
        raise HubError('nada encontrado para --%s "%s"' % (FLAG[tid], spec), "\n".join(hint))
    lines = ["  --%s %-36s %s" % (FLAG[tid], item_spec(i), short(i.get("description"), 56)) for i in res]
    raise HubError('"%s" existe em mais de uma categoria de %s. Escolha uma:' % (spec, LABEL[tid].lower()),
                   "\n".join(lines) + "\nRode de novo com categoria/nome.")


def plugin_target(it):
    return {"kind": "plugin", "id": it["id"], "label": item_spec(it), "item": it,
            "name": str(it.get("marketplaceName") or it.get("pluginName") or it["name"])}


def bundle_target(b, cat):
    return {"kind": "bundle", "id": "bundle:" + b["name"], "name": b["name"], "bundle": b,
            "label": "%s (pacote %s)" % (b["name"], cat.cat_label(b.get("category") or ""))}


def plugin_targets(cat, spec):
    s = str(spec or "").strip().strip("/")
    out = [plugin_target(i) for i in find_items(cat, "plugins", s)]
    parts = s.split("/")
    for b in cat.bundles:
        if b["name"] == s or (len(parts) == 2 and b["name"] == parts[1] and b.get("category") == parts[0]):
            out.append(bundle_target(b, cat))
    return out


def resolve_plugin(cat, spec):
    res = plugin_targets(cat, spec)
    if len(res) == 1:
        return res[0]
    if not res:
        names = [item_spec(i) for i in cat.of_type("plugins")] + [b["name"] for b in cat.bundles]
        sug = difflib.get_close_matches(spec, names, n=3, cutoff=0.5)
        hint = ("Talvez: " + ", ".join(sug) + "\n") if sug else ""
        hint += "Veja plugins e pacotes com --list plugins"
        raise HubError('nada encontrado para --plugin "%s"' % spec, hint)
    lines = ["  --plugin %s" % (item_spec(t["item"]) if t["kind"] == "plugin" else t["name"]) for t in res]
    raise HubError('"%s" bate com mais de um plugin. Escolha um:' % spec, "\n".join(lines))


# ================================================================ mescla de JSON

_MISSING = object()
DETAIL_KEYS = ("hooks", "permissions", "mcpServers", "enabledPlugins", "extraKnownMarketplaces", "env")


def jeq(a, b):
    return json.dumps(a, sort_keys=True, ensure_ascii=False) == json.dumps(b, sort_keys=True, ensure_ascii=False)


def _fmt(v):
    return short(json.dumps(v, ensure_ascii=False), 48)


def strip_central(data):
    return {k: v for k, v in data.items() if k not in CENTRAL_KEYS}


def merge_into(dst, src, changes, mode="settings", path=()):
    """Mescla src em dst (no lugar) e anota as mudanças como (símbolo, chave, nota)."""
    for key, val in src.items():
        p = path + (key,)
        name = ".".join(p)
        cur = dst.get(key, _MISSING)
        if mode == "mcp" and len(p) == 2 and p[0] == "mcpServers":
            if cur is _MISSING:
                changes.append(("+", name, "servidor novo"))
            elif jeq(cur, val):
                changes.append(("=", name, "igual"))
                continue
            else:
                changes.append(("!", name, "já existia com outra configuração e será substituído"))
            dst[key] = copy.deepcopy(val)
            continue
        if len(p) == 2 and p[0] == "hooks" and isinstance(val, list):
            if not isinstance(cur, list):
                if cur is not _MISSING:
                    changes.append(("~", name, "valor anterior não era lista e foi trocado"))
                dst[key] = copy.deepcopy(val)
                changes.append(("+", name, "%d entrada(s)" % len(val)))
                continue
            added = 0
            for entry in val:
                if not any(jeq(entry, old) for old in cur):
                    cur.append(copy.deepcopy(entry))
                    added += 1
            changes.append(("+", name, "+%d entrada(s)" % added) if added else ("=", name, "já existe"))
            continue
        if len(p) == 2 and p[0] == "permissions" and key in ("allow", "deny", "ask") and isinstance(val, list):
            base = cur if isinstance(cur, list) else []
            if cur is not _MISSING and not isinstance(cur, list):
                changes.append(("~", name, "valor anterior não era lista e foi trocado"))
            out = list(base)
            added = 0
            for x in val:
                if not any(jeq(x, y) for y in out):
                    out.append(copy.deepcopy(x))
                    added += 1
            dst[key] = out
            changes.append(("+", name, "+%d regra(s)" % added) if added else ("=", name, "já existe"))
            continue
        replace_whole = len(p) == 3 and p[0] == "extraKnownMarketplaces" and key == "source"
        if isinstance(val, dict) and not replace_whole:
            if isinstance(cur, dict):
                merge_into(cur, val, changes, mode, p)
                continue
            if cur is _MISSING:
                if len(p) == 1 and key in DETAIL_KEYS and val:
                    dst[key] = {}
                    merge_into(dst[key], val, changes, mode, p)
                else:
                    dst[key] = copy.deepcopy(val)
                    changes.append(("+", name, _fmt(val)))
                continue
            dst[key] = copy.deepcopy(val)
            changes.append(("~", name, "substitui o valor anterior"))
            continue
        if cur is _MISSING:
            dst[key] = copy.deepcopy(val)
            changes.append(("+", name, _fmt(val)))
        elif jeq(cur, val):
            changes.append(("=", name, "igual"))
        else:
            dst[key] = copy.deepcopy(val)
            changes.append(("~", name, "%s → %s" % (_fmt(cur), _fmt(val))))


def read_json_file(path):
    """dict, None (não existe) ou HubError (inválido)."""
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except UnicodeDecodeError:
        raise HubError("%s não está em UTF-8" % path)
    except OSError as e:
        raise HubError("não consegui ler %s: %s" % (path, e.strerror or e))
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except ValueError as e:
        pos = " (linha %d, coluna %d)" % (e.lineno, e.colno) if hasattr(e, "lineno") else ""
        raise HubError("JSON inválido em %s%s" % (path, pos),
                       hint="Corrija o arquivo (ou restaure um backup de .tahub-backups/) e rode de novo.")
    if not isinstance(data, dict):
        raise HubError("%s precisa ser um objeto JSON { ... }" % path)
    return data


def write_atomic(path, data, umask, executable=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        mode = stat.S_IMODE(os.stat(str(path)).st_mode)
    except OSError:
        mode = 0o666 & ~umask
    if executable:
        mode |= 0o111 & ~umask | 0o100
    fd, tmp = tempfile.mkstemp(prefix=".tahub-", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.chmod(tmp, mode)
        os.replace(tmp, str(path))
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def make_executable(path, umask):
    try:
        mode = stat.S_IMODE(os.stat(str(path)).st_mode)
        os.chmod(str(path), mode | (0o111 & ~umask) | 0o100)
    except OSError:
        pass


# ================================================================ prompts e frameworks
# Cópia fiel de tools/hubcore.py (parse_frontmatter, prompt_to_command, framework_to_skill):
# o resultado precisa ser idêntico, byte a byte, ao que o build gera nos kits do marketplace.

VAR_RE = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")


def parse_frontmatter(text):
    """Lê o bloco YAML simples entre '---'. Retorna (dict, corpo)."""
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not m:
        return {}, text
    block, body = m.group(1), text[m.end():]
    data, lines, i = {}, block.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not km:
            i += 1
            continue
        key, val = km.group(1), km.group(2).strip()
        i += 1
        if val in ("|", ">", "|-", ">-", "|+", ">+"):
            buf = []
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].startswith("\t") or not lines[i].strip()):
                buf.append(lines[i].strip())
                i += 1
            data[key] = ("\n" if val.startswith("|") else " ").join(buf).strip()
        elif val == "":
            sub, lst = {}, []
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].startswith("\t")):
                s = lines[i].strip()
                if s.startswith("- "):
                    lst.append(_fm_scalar(s[2:]))
                else:
                    sm = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", s)
                    if sm:
                        sub[sm.group(1)] = _fm_scalar(sm.group(2))
                i += 1
            data[key] = lst if lst else sub
        else:
            data[key] = _fm_scalar(val)
    return data, body


def _fm_scalar(val):
    val = val.strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
        return val[1:-1]
    if val.startswith("[") and val.endswith("]"):
        return [_fm_scalar(x) for x in val[1:-1].split(",") if x.strip()]
    if val.lower() in ("true", "false"):
        return val.lower() == "true"
    return val


def source_text(data):
    """Bytes da origem → texto como o build lê (UTF-8 e quebras de linha normalizadas para \\n)."""
    return data.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")


def prompt_variables(fm, body):
    """Variáveis do prompt: as declaradas no frontmatter (com rótulo) + as achadas no texto."""
    declared = fm.get("variables") if isinstance(fm.get("variables"), dict) else {}
    out, seen = [], set()
    for name, label in declared.items():
        label = str(label or name)
        req, default = None, None
        m = re.match(r"^\s*\[(obrigat[oó]rio|opcional|padr[aã]o\s*=\s*([^\]]*))\]\s*", label, re.I)
        if m:
            req = m.group(1).lower().startswith("obrig")
            default = m.group(2).strip() if m.group(2) else None
            label = label[m.end():]
        out.append({"name": name, "label": label, "required": req, "default": default})
        seen.add(name)
    for name in VAR_RE.findall(body or ""):
        if name not in seen:
            out.append({"name": name, "label": name.replace("_", " "), "required": None, "default": None})
            seen.add(name)
    return out


def prompt_to_command(text, item):
    """Converte um prompt da Central em comando do Claude Code (.claude/commands/<nome>.md)."""
    fm, body = parse_frontmatter(text)
    variables = prompt_variables(fm, body)
    desc = str(fm.get("description") or item.get("description") or item.get("title") or "").replace("\n", " ").strip()
    lines = ["---", "description: " + json.dumps(desc, ensure_ascii=False)]
    if variables:
        lines.append("argument-hint: " + json.dumps(" ".join("[%s]" % v["name"] for v in variables), ensure_ascii=False))
    lines += ["---", "", "<!-- Central Trip Angle · prompt %s/%s -->" % (item.get("category"), item.get("name")),
              "Dados enviados pelo usuário: $ARGUMENTS", ""]
    if variables and any(v.get("required") is not None for v in variables):
        obr = "; ".join("%s (%s)" % (v["name"], v["label"]) for v in variables if v.get("required"))
        opc = "; ".join("%s (%s%s)" % (v["name"], v["label"], ("; padrão: %s" % v["default"]) if v.get("default") else "")
                        for v in variables if not v.get("required"))
        partes = ["Obrigatórios: %s." % obr if obr else "", "Opcionais: %s." % opc if opc else ""]
        lines += ["Antes de começar, confira os insumos. " + " ".join(x for x in partes if x)
                  + " Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.", ""]
    elif variables:
        need = "; ".join("%s (%s)" % (v["name"], v["label"]) for v in variables)
        lines += ["Antes de começar, confira se você tem: %s. Se faltar algum, pergunte ao usuário." % need, ""]
    lines.append(VAR_RE.sub(lambda m: "[%s]" % m.group(1), body.strip()))
    return "\n".join(lines) + "\n"


def framework_skill_name(name):
    return name if name.startswith("framework-") else "framework-" + name


def framework_to_skill(text, item):
    """Converte um framework da Central em skill (.claude/skills/framework-<nome>/SKILL.md)."""
    fm, body = parse_frontmatter(text)
    title = str(fm.get("title") or item.get("title") or item.get("name"))
    desc = str(fm.get("description") or item.get("description") or "").strip()
    when = str(fm.get("when") or "").strip()
    full = ("Framework %s: %s %s" % (title, desc, when)).replace("\n", " ").strip()
    return ("---\n" + "name: %s\n" % framework_skill_name(item["name"]) + "description: "
            + json.dumps(full[:1000], ensure_ascii=False) + "\n---\n\n" + "# %s\n\n" % title + body.strip() + "\n")


def fill_variables(text, values):
    """Troca {{nome}} pelos valores dados. Devolve (texto, nomes que ficaram sem valor)."""
    missing = []

    def rep(m):
        name = m.group(1)
        if name in values:
            return values[name]
        if name not in missing:
            missing.append(name)
        return "{{%s}}" % name

    return VAR_RE.sub(rep, text), missing


# ================================================================ plano de instalação

class Entry:
    def __init__(self, kind, spec, dest=None):
        self.kind, self.spec, self.dest = kind, spec, dest
        self.lines = []  # (símbolo, texto, nota)
        self.json = []   # (rótulo do arquivo, mudanças)
        self.notes = []  # avisos que valem depois de instalar


class FileOp:
    def __init__(self, dest, data, root, executable, status):
        self.dest, self.data, self.root, self.executable, self.status = dest, data, root, executable, status


class JsonTarget:
    def __init__(self, path, root, label, backup_root):
        guard(path, [root])
        self.path, self.root, self.label, self.backup_root = path, root, label, backup_root
        self.original = read_json_file(path)
        self.work = copy.deepcopy(self.original) if self.original is not None else {}
        self.patches = []

    @property
    def changed(self):
        return self.original is None or not jeq(self.original, self.work)


class Ctx:
    def __init__(self, args, src, cat, scope):
        self.args, self.src, self.cat = args, src, cat
        self.project = project_dir(args.directory)
        self.scope = scope or "local"
        self.force = bool(args.force)
        self.user_dir = claude_user_dir()
        self.stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    def scope_root(self):
        return self.user_dir if self.scope == "user" else self.project

    def scope_base(self):
        return self.user_dir if self.scope == "user" else self.project / ".claude"

    def settings_path(self):
        if self.scope == "user":
            return self.user_dir / "settings.json"
        if self.scope == "project":
            return self.project / ".claude" / "settings.json"
        return self.project / ".claude" / "settings.local.json"

    def show(self, p):
        p = os.path.abspath(str(p))
        home = os.path.expanduser("~")
        ud = os.path.abspath(str(self.user_dir))
        pr = os.path.abspath(str(self.project))
        if p == ud or p.startswith(ud + os.sep):
            return "~" + p[len(home):] if p.startswith(home + os.sep) else p
        if p == pr:
            return "."
        if p.startswith(pr + os.sep):
            return os.path.relpath(p, pr)
        return p


class Plan:
    def __init__(self, ctx):
        self.ctx = ctx
        self.entries, self.files, self.clones, self.commands, self.after = [], [], [], [], []
        self.usage = []
        self.targets = {}
        self._dests = {}

    def entry(self, kind, spec, dest=None):
        e = Entry(kind, spec, dest)
        self.entries.append(e)
        return e

    def add_file(self, entry, dest, data, root, executable=False):
        dest = Path(os.path.abspath(str(dest)))
        guard(dest, [root])
        key = str(dest)
        if key in self._dests:
            if self._dests[key] == data:
                return
            raise HubError("dois itens gravariam o mesmo arquivo: %s" % self.ctx.show(dest),
                           hint="Instale um de cada vez.")
        self._dests[key] = data
        if dest.is_dir():
            raise HubError("já existe uma pasta onde iria o arquivo %s" % self.ctx.show(dest))
        if dest.exists() or dest.is_symlink():
            try:
                same = dest.read_bytes() == data
            except OSError:
                same = False
            status = "same" if same else ("overwrite" if self.ctx.force else "skip")
        else:
            status = "new"
        self.files.append(FileOp(dest, data, root, executable, status))
        mark = {"new": "+", "same": "=", "overwrite": "~", "skip": "!"}[status]
        note = {"new": "", "same": "já existe igual", "overwrite": "sobrescreve (--force)",
                "skip": "já existe e é diferente: mantido (use --force para sobrescrever)"}[status]
        if executable and status in ("new", "overwrite"):
            note = (note + " · " if note else "") + "executável"
        entry.lines.append((mark, self.ctx.show(dest), note))

    def target(self, path, root, backup_root):
        key = str(path)
        if key not in self.targets:
            self.targets[key] = JsonTarget(Path(path), root, self.ctx.show(path), backup_root)
        return self.targets[key]

    def settings_target(self):
        c = self.ctx
        broot = c.user_dir if c.scope == "user" else c.project / ".claude"
        return self.target(c.settings_path(), c.scope_root(), broot)

    def merge(self, entry, target, patch, mode):
        changes = []
        merge_into(target.work, patch, changes, mode)
        target.patches.append((patch, mode))
        entry.json.append((target.label, changes))

    def counts(self):
        c = {"new": 0, "same": 0, "overwrite": 0, "skip": 0}
        for f in self.files:
            c[f.status] += 1
        return c

    def pending(self):
        return bool(any(f.status in ("new", "overwrite") for f in self.files) or self.clones or self.commands
                    or any(t.changed for t in self.targets.values()))


def safe_name(it):
    n = it.get("name")
    if not isinstance(n, str) or not NAME_RE.match(n):
        raise HubError("nome inválido no catálogo: %r" % (n,))
    return n


def item_files(it):
    base = safe_rel(it.get("base") or "")
    files = it.get("files") or [base]
    out = []
    for f in files:
        f = safe_rel(f)
        if it.get("kind") == "dir":
            if not f.startswith(base + "/"):
                raise HubError("arquivo fora da pasta do item no catálogo: %s" % f)
            out.append((f, f[len(base) + 1:]))
        else:
            out.append((f, PurePosixPath(f).name))
    return out


def load_item_json(ctx, it):
    rel = safe_rel(it.get("base") or (it.get("files") or [""])[0])
    raw = ctx.src.read(rel)
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        raise HubError("JSON inválido no catálogo: %s (%s)" % (rel, e))
    if not isinstance(data, dict):
        raise HubError("JSON do item precisa ser um objeto: %s" % rel)
    return data


def plan_skill(plan, it):
    ctx = plan.ctx
    dest = ctx.project / ".claude" / "skills" / safe_name(it)
    e = plan.entry("skills", item_spec(it), ctx.show(dest) + "/")
    for src_rel, rel in item_files(it):
        plan.add_file(e, dest / rel, ctx.src.read(src_rel), ctx.project)


def plan_md(plan, it, folder):
    ctx = plan.ctx
    dest = ctx.project / ".claude" / folder / (safe_name(it) + ".md")
    src_rel = item_files(it)[0][0] if it.get("kind") == "dir" else safe_rel(it.get("base") or it["files"][0])
    e = plan.entry(it["type"], item_spec(it), ctx.show(dest))
    plan.add_file(e, dest, ctx.src.read(src_rel), ctx.project)


def plan_prompt(plan, it):
    """Prompt → comando do Claude Code, no mesmo formato do build (prompt_to_command)."""
    ctx = plan.ctx
    name = safe_name(it)
    dest = ctx.project / ".claude" / "commands" / (name + ".md")
    src_rel = safe_rel(it.get("base") or (it.get("files") or [""])[0])
    text = source_text(ctx.src.read(src_rel))
    e = plan.entry("prompts", item_spec(it), ctx.show(dest))
    plan.add_file(e, dest, prompt_to_command(text, it).encode("utf-8"), ctx.project)
    fm, body = parse_frontmatter(text)
    names = [v["name"] for v in prompt_variables(fm, body)]
    use = "/%s %s" % (name, " ".join("<%s>" % n for n in names)) if names else "/%s <dados>" % name
    plan.usage.append("prompt %s: no Claude Code digite %s" % (name, use.strip()))


def plan_framework(plan, it):
    """Framework → skill framework-<nome>, no mesmo formato do build (framework_to_skill)."""
    ctx = plan.ctx
    skill = framework_skill_name(safe_name(it))
    dest = ctx.project / ".claude" / "skills" / skill / "SKILL.md"
    src_rel = safe_rel(it.get("base") or (it.get("files") or [""])[0])
    text = source_text(ctx.src.read(src_rel))
    e = plan.entry("frameworks", item_spec(it), ctx.show(dest.parent) + "/")
    plan.add_file(e, dest, framework_to_skill(text, it).encode("utf-8"), ctx.project)
    plan.usage.append("framework %s: vira a skill %s; peça \"use o framework %s\" ou deixe o Claude escolher"
                      % (it["name"], skill, it.get("title") or it["name"]))


def plan_template(plan, it):
    ctx = plan.ctx
    e = plan.entry("templates", item_spec(it), "raiz do projeto")
    for src_rel, rel in item_files(it):
        plan.add_file(e, ctx.project / rel, ctx.src.read(src_rel), ctx.project)


def plan_extras(plan, e, it, folder):
    ctx = plan.ctx
    extras = it.get("extras") or []
    if not extras:
        return
    base = safe_rel(it.get("base") or "")
    stem = base[:-5] if base.endswith(".json") else base
    dest_dir = ctx.scope_base() / folder
    for x in extras:
        x = safe_rel(x)
        rel = x[len(stem) + 1:] if x.startswith(stem + "/") else PurePosixPath(x).name
        plan.add_file(e, dest_dir / rel, ctx.src.read(x), ctx.scope_root(),
                      executable=rel.endswith((".sh", ".py")))


def mcp_needs(servers, requires):
    out = []
    for sname, s in servers.items():
        blob = json.dumps(s, ensure_ascii=False)
        envs = sorted(set(re.findall(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}", blob)))
        phs = sorted(set(re.findall(r"<([A-Za-z0-9_ .-]{2,40})>", blob)))
        env = s.get("env") if isinstance(s, dict) and isinstance(s.get("env"), dict) else {}
        empty = sorted(k for k, v in env.items() if isinstance(v, str) and not v.strip())
        if phs:
            out.append("troque no .mcp.json (%s): %s" % (sname, ", ".join("<%s>" % x for x in phs)))
        if empty:
            out.append("preencha no .mcp.json (%s): %s" % (sname, ", ".join("env." + k for k in empty)))
        if envs:
            out.append("defina a variável de ambiente (%s): %s" % (sname, ", ".join(envs)))
    if not out and requires:
        out.append("preencha antes de usar: " + ", ".join(str(r) for r in requires))
    return out


def plan_mcp(plan, it):
    ctx = plan.ctx
    data = strip_central(load_item_json(ctx, it))
    servers = data.get("mcpServers")
    if not isinstance(servers, dict) or not servers:
        raise HubError("o MCP %s não tem a chave mcpServers" % item_spec(it))
    e = plan.entry("mcps", item_spec(it), ".mcp.json")
    t = plan.target(ctx.project / ".mcp.json", ctx.project, ctx.project / ".claude")
    plan.merge(e, t, {"mcpServers": servers}, "mcp")
    req = it.get("requires") if isinstance(it.get("requires"), list) else []
    e.notes.extend(mcp_needs(servers, req))


def plan_hook(plan, it):
    ctx = plan.ctx
    data = strip_central(load_item_json(ctx, it))
    hooks = data.get("hooks")
    if not isinstance(hooks, dict) or not hooks:
        raise HubError("o hook %s não tem a chave hooks" % item_spec(it))
    e = plan.entry("hooks", item_spec(it), "%s (escopo %s)" % (ctx.show(ctx.settings_path()), ctx.scope))
    plan_extras(plan, e, it, "hooks")
    plan.merge(e, plan.settings_target(), {"hooks": hooks}, "settings")
    ignored = [k for k in data if k != "hooks"]
    if ignored:
        e.notes.append("chaves ignoradas no hook: " + ", ".join(ignored))
    if ctx.scope == "user" and it.get("extras") and "CLAUDE_PROJECT_DIR" in json.dumps(hooks):
        e.notes.append("o hook usa $CLAUDE_PROJECT_DIR, mas no escopo user os scripts ficam em %s"
                       % ctx.show(ctx.scope_base() / "hooks"))


def plan_setting(plan, it):
    ctx = plan.ctx
    data = strip_central(load_item_json(ctx, it))
    if not data:
        raise HubError("o setting %s não tem nenhuma chave para mesclar" % item_spec(it))
    e = plan.entry("settings", item_spec(it), "%s (escopo %s)" % (ctx.show(ctx.settings_path()), ctx.scope))
    plan_extras(plan, e, it, "scripts")
    plan.merge(e, plan.settings_target(), data, "settings")


def marketplace_source(ctx):
    repo = str(ctx.cat.hub.get("githubRepo") or "").strip()
    if repo:
        if not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", repo):
            raise HubError("hub.githubRepo inválido no catálogo: %s" % repo)
        return {"source": "github", "repo": repo}, repo
    if ctx.src.kind == "dir":
        for cand in (ctx.src.base, ctx.src.base.parent):
            if (cand / ".claude-plugin" / "marketplace.json").is_file():
                p = str(Path(cand).resolve())
                return {"source": "directory", "path": p}, p
    raise HubError("a Central ainda não foi publicada no GitHub (hub.githubRepo está vazio), "
                   "então não há marketplace para instalar plugins por esta origem.",
                   hint="Quem mantém a Central: publique o repositório e preencha githubRepo em hub.config.json.\n"
                        "Para testar agora: use --source com a pasta dist/ do repositório "
                        "(ao lado de .claude-plugin/marketplace.json).")


def plan_plugin(plan, tgt):
    ctx = plan.ctx
    mp = ctx.cat.marketplace()
    if not NAME_RE.match(mp) or not NAME_RE.match(tgt["name"]):
        raise HubError("nome de plugin ou marketplace inválido no catálogo: %s@%s" % (tgt["name"], mp))
    msource, add_arg = marketplace_source(ctx)
    ref = "%s@%s" % (tgt["name"], mp)
    e = plan.entry("plugins", tgt["label"], "%s (escopo %s)" % (ctx.show(ctx.settings_path()), ctx.scope))
    claude = shutil.which("claude")
    if claude:
        add = [claude, "plugin", "marketplace", "add", add_arg]
        if add not in plan.commands:
            plan.commands.append(add)
            e.lines.append(("$", "claude plugin marketplace add " + shlex.quote(add_arg), ""))
        plan.commands.append([claude, "plugin", "install", ref, "--scope", ctx.scope])
        e.lines.append(("$", "claude plugin install %s --scope %s" % (ref, ctx.scope), ""))
    else:
        e.lines.append(("·", "comando claude não encontrado: só o settings será gravado", ""))
    plan.merge(e, plan.settings_target(),
               {"extraKnownMarketplaces": {mp: {"source": msource}}, "enabledPlugins": {ref: True}}, "settings")
    for line in ("/plugin marketplace add %s" % add_arg, "/plugin install %s" % ref):
        if line not in plan.after:
            plan.after.append(line)


def valid_git_url(u):
    if not u or u.startswith("-") or re.search(r"\s", u):
        return False
    return bool(re.match(r"^(https?|ssh|git|file)://\S+$", u) or re.match(r"^[A-Za-z0-9_.-]+@[A-Za-z0-9_.-]+:\S+$", u))


def plan_repo(plan, it):
    ctx = plan.ctx
    name = safe_name(it)
    url = str((it.get("repo") or {}).get("url") or "").strip()
    if not valid_git_url(url):
        raise HubError("URL de repositório inválida no catálogo (%s): %r" % (item_spec(it), url))
    dest = ctx.project / name
    guard(dest, [ctx.project])
    e = plan.entry("repos", item_spec(it), ctx.show(dest) + "/")
    if dest.exists() or any(str(d) == str(dest) for _, d in plan.clones):
        e.lines.append(("=", ctx.show(dest) + "/", "já existe, pulando"))
        return
    if not shutil.which("git"):
        raise HubError("git não encontrado no PATH (necessário para --repo).", hint="Instale o git e rode de novo.")
    plan.clones.append((url, dest))
    e.lines.append(("$", "git clone %s %s" % (url, ctx.show(dest)), ""))


def build_plan(ctx, selection):
    plan = Plan(ctx)
    seen = set()
    for tid, obj in selection:
        key = (tid, obj.get("id"))
        if key in seen:
            continue
        seen.add(key)
        if tid == "prompts":
            plan_prompt(plan, obj)
        elif tid == "frameworks":
            plan_framework(plan, obj)
        elif tid == "skills":
            plan_skill(plan, obj)
        elif tid == "agents":
            plan_md(plan, obj, "agents")
        elif tid == "commands":
            plan_md(plan, obj, "commands")
        elif tid == "mcps":
            plan_mcp(plan, obj)
        elif tid == "hooks":
            plan_hook(plan, obj)
        elif tid == "settings":
            plan_setting(plan, obj)
        elif tid == "plugins":
            plan_plugin(plan, obj)
        elif tid == "templates":
            plan_template(plan, obj)
        elif tid == "repos":
            plan_repo(plan, obj)
    return plan


def print_plan(plan, full=False):
    ctx = plan.ctx
    print()
    print(tag("PLANO") + "  " + dim("%d item(ns)" % len(plan.entries)))
    for e in plan.entries:
        print()
        print("  " + red(SINGULAR[e.kind].upper()) + "  " + bold(e.spec) + (dim("  → " + e.dest) if e.dest else ""))
        lines = e.lines
        shown = lines if full or len(lines) <= 14 else lines[:12]
        for s, text, note in shown:
            print("    %s %s%s" % (sym(s), text, dim("  " + note) if note else ""))
        if len(shown) < len(lines):
            print(dim("    … e mais %d arquivo(s) (veja tudo com --dry-run)" % (len(lines) - len(shown))))
        for label, changes in e.json:
            real = [c for c in changes if c[0] != "="]
            if not real:
                print("    " + dim("= %s: nada muda (já aplicado)" % label))
                continue
            print("    " + dim("mesclar em %s:" % label))
            for s, name, note in real:
                print("      %s %s%s" % (sym(s), name, dim("  " + note) if note else ""))
            same = len(changes) - len(real)
            if same:
                print(dim("      = %d chave(s) já iguais" % same))
        for n in e.notes:
            print("    " + yellow("!") + " " + n)
    c = plan.counts()
    parts = []
    if c["new"]:
        parts.append("%d arquivo(s) novo(s)" % c["new"])
    if c["overwrite"]:
        parts.append("%d sobrescrito(s)" % c["overwrite"])
    if c["same"]:
        parts.append("%d igual(is)" % c["same"])
    if c["skip"]:
        parts.append("%d mantido(s)" % c["skip"])
    nj = sum(1 for t in plan.targets.values() if t.changed)
    nb = sum(1 for t in plan.targets.values() if t.changed and t.original is not None)
    if nj:
        parts.append("%d JSON a mesclar%s" % (nj, " (backup de %d antes)" % nb if nb else ""))
    if plan.clones:
        parts.append("%d clone(s)" % len(plan.clones))
    if plan.commands:
        parts.append("%d comando(s) do claude" % len(plan.commands))
    print()
    print(dim("Resumo: ") + (" · ".join(parts) if parts else "nada a mudar"))
    if c["skip"]:
        warn("%d arquivo(s) já existem com outro conteúdo e não serão alterados. Use --force para sobrescrever."
             % c["skip"])


def backup_file(ctx, t):
    d = Path(t.backup_root) / ".tahub-backups" / ctx.stamp
    guard(d, [t.root])
    d.mkdir(parents=True, exist_ok=True)
    dest = d / t.path.name
    n = 2
    while dest.exists():
        dest = d / ("%s.%d" % (t.path.name, n))
        n += 1
    shutil.copy2(str(t.path), str(dest))
    return dest


def execute(plan):
    ctx = plan.ctx
    errors, written, backups, jsons = 0, 0, [], 0
    um = os.umask(0)
    os.umask(um)
    print()
    for op in plan.files:
        if op.status not in ("new", "overwrite"):
            if op.status == "same" and op.executable:
                make_executable(op.dest, um)
            continue
        try:
            guard(op.dest, [op.root])
            write_atomic(op.dest, op.data, um, op.executable)
            written += 1
        except (OSError, HubError) as e:
            errors += 1
            print(red("✗") + " não gravei %s: %s" % (ctx.show(op.dest), getattr(e, "msg", None) or e))
    if written:
        print(green("✓") + " %d arquivo(s) gravado(s)" % written)
    for url, dest in plan.clones:
        print(dim("$ git clone %s %s" % (url, ctx.show(dest))))
        sys.stdout.flush()
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            r = subprocess.run(["git", "clone", "--", url, str(dest)], timeout=900)
            if r.returncode != 0:
                errors += 1
                print(red("✗") + " git clone falhou (código %d)" % r.returncode)
            else:
                print(green("✓") + " clonado em %s" % ctx.show(dest))
        except (OSError, subprocess.TimeoutExpired) as e:
            errors += 1
            print(red("✗") + " git clone falhou: %s" % e)
    for cmd in plan.commands:
        print(dim("$ " + " ".join(["claude"] + [shlex.quote(c) for c in cmd[1:]])))
        sys.stdout.flush()
        try:
            ctx.project.mkdir(parents=True, exist_ok=True)
            r = subprocess.run(cmd, cwd=str(ctx.project), timeout=300)
            if r.returncode != 0:
                warn("o comando terminou com código %d; o settings será gravado mesmo assim." % r.returncode)
        except (OSError, subprocess.TimeoutExpired) as e:
            warn("não consegui rodar o claude (%s); o settings será gravado mesmo assim." % e)
    for t in plan.targets.values():
        try:
            cur = read_json_file(t.path)  # relê: o claude pode ter mexido no arquivo
            work = copy.deepcopy(cur) if cur is not None else {}
            for patch, mode in t.patches:
                merge_into(work, patch, [], mode)
            if cur is not None and jeq(cur, work):
                print(dim("= %s sem mudanças" % t.label))
                continue
            if cur is not None:
                b = backup_file(ctx, t)
                backups.append(b)
            guard(t.path, [t.root])
            write_atomic(t.path, (json.dumps(work, ensure_ascii=False, indent=2) + "\n").encode("utf-8"), um)
            jsons += 1
            print(green("✓") + " %s %s" % (t.label, "atualizado" if cur is not None else "criado"))
        except HubError as e:
            errors += 1
            print(red("✗") + " " + e.msg)
        except OSError as e:
            errors += 1
            print(red("✗") + " não gravei %s: %s" % (t.label, e))
    return errors, written, backups, jsons


def run_prompt(text, cwd):
    claude = shutil.which("claude")
    cmd_show = "claude " + shlex.quote(text)
    if not claude:
        print()
        warn("o comando claude não está no PATH. Rode você mesmo:")
        print("  cd %s && %s" % (shlex.quote(str(cwd)), cmd_show))
        return EXIT_OK
    print()
    print(dim("Abrindo o Claude Code com o prompt…"))
    argv = [claude, text] if not text.startswith("-") else [claude, "--", text]
    sys.stdout.flush()
    try:
        cwd = str(cwd) if Path(str(cwd)).is_dir() else None
        return subprocess.call(argv, cwd=cwd)
    except OSError as e:
        raise HubError("não consegui abrir o claude: %s" % e)


def print_header(ctx, show_scope=False):
    print(banner())
    print(dim("  origem   ") + str(ctx.src.describe()))
    print(dim("  projeto  ") + str(ctx.project) + ("" if ctx.project.exists() else dim("  (pasta será criada)")))
    if show_scope:
        print(dim("  escopo   ") + "%s (%s)" % (ctx.scope, ctx.show(ctx.settings_path())))


def run_install(args, src, cat, selection, scope):
    ctx = Ctx(args, src, cat, scope)
    print_header(ctx, any(t in ("hooks", "settings", "plugins") for t, _ in selection))
    if src.kind == "url" and selection:
        print(dim("  baixando arquivos da origem…"))
    plan = build_plan(ctx, selection)
    if plan.entries:
        print_plan(plan, full=bool(args.dry_run))
    if not plan.pending():
        print()
        c = plan.counts()
        if c["skip"]:
            print(green("✓") + " Nada novo para gravar. Arquivos diferentes foram mantidos (use --force).")
        elif selection:
            print(green("✓") + " Nada a fazer: tudo já está instalado.")
        if args.prompt and not args.dry_run:
            return run_prompt(args.prompt, ctx.project)
        return EXIT_OK
    if args.dry_run:
        print()
        warn("simulação (--dry-run): nada foi gravado.")
        return EXIT_OK
    if not args.yes:
        print()
        if not confirm("Instalar agora?"):
            print("Cancelado. Nada foi gravado.")
            return EXIT_OK
    errors, written, backups, jsons = execute(plan)
    for b in backups:
        print(dim("  backup: %s" % ctx.show(b)))
    print()
    if errors:
        print(red("✗") + " Terminou com %d erro(s)." % errors)
    else:
        in_project = any(op.status in ("new", "overwrite") and op.root == ctx.project for op in plan.files)
        print(green("✓") + " Pronto!" + (" Projeto: %s" % ctx.project if in_project or plan.clones else ""))
    notes = [n for e in plan.entries for n in e.notes]
    if notes or plan.after or plan.usage:
        print()
        print(tag("PRÓXIMOS PASSOS"))
        for n in notes:
            print("  " + yellow("!") + " " + n)
        for u in plan.usage:
            print("  " + red("›") + " " + u)
        if plan.after:
            print("  No Claude Code, se o plugin ainda não aparecer:")
            for line in plan.after:
                print("    " + bold(line))
    if not args.prompt:
        print(dim("  Abra o Claude Code na pasta: cd %s && claude" % shlex.quote(str(ctx.project))))
    if not errors:
        cta = cat.hub.get("cta") if isinstance(cat.hub.get("cta"), dict) else {}
        yt = cta.get("youtube") if isinstance(cta.get("youtube"), dict) else {}
        prods = [x for x in (cta.get("produtos") or []) if isinstance(x, dict) and str(x.get("url", "")).startswith("https://")]
        if str(yt.get("url", "")).startswith("https://") or prods:
            print()
        if str(yt.get("url", "")).startswith("https://"):
            print(red("▲") + " " + (yt.get("titulo") or "Acompanhe no YouTube") + ": " + bold(yt["url"]))
        if prods:
            print(red("▲") + " " + str(prods[0].get("titulo") or "Material completo") + ": " + bold(prods[0]["url"]))
    code = EXIT_ERR if errors else EXIT_OK
    if args.prompt:
        pc = run_prompt(args.prompt, ctx.project)
        code = code or pc
    return code


def collect(args):
    req = []
    for tid, flag, _, _ in TYPES:
        for v in getattr(args, flag) or []:
            for s in str(v).split(","):
                if s.strip():
                    req.append((tid, s.strip()))
    return req


def cmd_install(args, requests):
    src = pick_source(args.source)
    cat = src.catalog()
    selection = []
    for tid, spec in requests:
        selection.append((tid, resolve_plugin(cat, spec) if tid == "plugins" else resolve_item(cat, tid, spec)))
    return run_install(args, src, cat, selection, args.scope or "local")


# ================================================================ interativo

def parse_selection(text, n):
    t = fold(text).strip()
    if t in ("todos", "todas", "tudo", "t", "*", "all"):
        return list(range(1, n + 1))
    out = []
    for part in re.split(r"[,\s;]+", t):
        if not part:
            continue
        m = re.match(r"^(\d+)-(\d+)$", part)
        if m:
            a, b = sorted((int(m.group(1)), int(m.group(2))))
            out.extend(range(a, b + 1))
        elif part.isdigit():
            out.append(int(part))
        else:
            return None
    if not out or any(x < 1 or x > n for x in out):
        return None
    seen, res = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


def type_entries(cat, tid):
    if tid == "plugins":
        out = [(i["category"], plugin_target(i), item_spec(i), i.get("description")) for i in cat.of_type("plugins")]
        out += [(b.get("category") or "geral", bundle_target(b, cat), b["name"], b.get("description"))
                for b in cat.bundles]
    else:
        out = [(i["category"], i, i["name"], i.get("description")) for i in cat.of_type(tid)]
    return sorted(out, key=lambda x: (cat.cat_order(x[0]), x[0], x[2]))


def pick_items(tid, sel, keys):
    print()
    for n, (_, obj, label, desc) in enumerate(sel, 1):
        mk = green("✓") if (tid, obj["id"]) in keys else " "
        print("  %s %s %s  %s" % (red("%3d)" % n), mk, bold(label), dim(short(desc, 64))))
    while True:
        a = ask("Itens (ex.: 1,3,5 · 2-4 · todos · 0 volta): ")
        if a in ("0", ""):
            return None
        idx = parse_selection(a, len(sel))
        if idx is None:
            warn("seleção inválida")
            continue
        return [sel[i - 1][1] for i in idx]


def pick_from_type(cat, tid, keys):
    entries = type_entries(cat, tid)
    cats = []
    for cid, _, _, _ in entries:
        if not cats or cats[-1][0] != cid:
            cats.append([cid, 0])
        cats[-1][1] += 1
    while True:
        print()
        print(tag(LABEL[tid].upper()) + dim("  categorias"))
        for n, (cid, cnt) in enumerate(cats, 1):
            print("  %s %s %s" % (red("%2d)" % n), cat.cat_label(cid), dim("(%d)" % cnt)))
        print("  %s todas" % red(" T)"))
        print("  %s voltar" % red(" 0)"))
        a = ask("Categoria: ").lower()
        if a in ("0", ""):
            return []
        if a in ("t", "todas", "todos"):
            sel = entries
        elif a.isdigit() and 1 <= int(a) <= len(cats):
            sel = [x for x in entries if x[0] == cats[int(a) - 1][0]]
        else:
            warn("opção inválida")
            continue
        got = pick_items(tid, sel, keys)
        if got is not None:
            return got


def cmd_interactive(args):
    src = pick_source(args.source)
    cat = src.catalog()
    print(banner())
    print(dim("  %d itens no catálogo · origem %s" % (len(cat.items), src.describe())))
    chosen, keys = [], set()
    while True:
        types = [t for t in TYPE_IDS if cat.count(t) or (t == "plugins" and cat.bundles)]
        print()
        print(tag("O QUE VOCÊ QUER INSTALAR?"))
        for n, t in enumerate(types, 1):
            extra = " + %d pacotes" % len(cat.bundles) if t == "plugins" and cat.bundles else ""
            print("  %s %s %s" % (red("%2d)" % n), LABEL[t], dim("(%d%s)" % (cat.count(t), extra))))
        if chosen:
            print("  %s continuar com %d item(ns)" % (red(" C)"), len(chosen)))
        print("  %s sair" % red(" 0)"))
        a = ask("Escolha: ").lower()
        if a in ("0", "q", "sair"):
            print("Saindo. Nada foi instalado.")
            return EXIT_OK
        if a == "c" and chosen:
            break
        if not a.isdigit() or not 1 <= int(a) <= len(types):
            warn("opção inválida")
            continue
        tid = types[int(a) - 1]
        added = 0
        for obj in pick_from_type(cat, tid, keys):
            k = (tid, obj["id"])
            if k not in keys:
                keys.add(k)
                chosen.append((tid, obj))
                added += 1
        if added:
            print(green("✓") + " %d adicionado(s). Total: %d. Escolha mais ou digite C para continuar." % (added, len(chosen)))
    scope = args.scope
    if not scope and any(t in ("hooks", "settings", "plugins") for t, _ in chosen):
        print()
        print(tag("ESCOPO") + dim("  vale para settings, hooks e plugins"))
        print("  %s local    .claude/settings.local.json  %s" % (red("1)"), dim("só você, neste projeto")))
        print("  %s project  .claude/settings.json        %s" % (red("2)"), dim("todo o time do projeto")))
        print("  %s user     ~/.claude/settings.json      %s" % (red("3)"), dim("todos os seus projetos")))
        a = ask("Escopo [1]: ").lower() or "1"
        scope = {"1": "local", "2": "project", "3": "user"}.get(a, a if a in SCOPES else "local")
    if not args.directory:
        d = ask("Pasta do projeto [%s]: " % os.getcwd())
        if d:
            args.directory = d
    print()
    return run_install(args, src, cat, chosen, scope or "local")


# ================================================================ explorar: busca, lista, info

def search_catalog(cat, q, category=None):
    words = [w for w in re.split(r"\s+", fold(q).strip()) if w]
    out = []
    for it in cat.items:
        if category and it["category"] != category:
            continue
        extra = " ".join([str(it.get("preview") or ""), str(it.get("output") or ""), str(it.get("when") or ""),
                          " ".join(map(str, it.get("tools") or [])) if isinstance(it.get("tools"), list) else ""])
        fields = [(fold(it["name"]), 5), (fold(it.get("title")), 4), (fold(" ".join(map(str, it["tags"]))), 3),
                  (fold(it["category"] + " " + cat.cat_label(it["category"])), 2), (fold(it["description"]), 1),
                  (fold(extra), 1)]
        hits, score = 0, 0
        for w in words:
            best = max([wt for txt, wt in fields if w in txt] or [0])
            if best:
                hits += 1
                score += best
        if hits:
            if fold(it["name"]) == fold(q).strip():
                score += 10
            score -= 0.5 if it.get("partOf") else 0
            out.append((hits, score, "item", it))
    for b in cat.bundles:
        if category and b.get("category") != category:
            continue
        txt = fold(" ".join([b["name"], str(b.get("label") or ""), str(b.get("description") or ""),
                             str(b.get("category") or "")]))
        hits = sum(1 for w in words if w in txt)
        if hits:
            out.append((hits, hits * 1.5, "bundle", b))
    out.sort(key=lambda x: (-x[0], -x[1], x[3].get("name", "")))
    return out


def cmd_search(args):
    q = (args.search or "").strip()
    if not q:
        raise HubError('informe o que buscar, por exemplo: --search "copy vsl"', code=EXIT_USAGE)
    src = pick_source(args.source)
    cat = src.catalog()
    res = search_catalog(cat, q, args.category)
    print(banner("busca"))
    print(tag("BUSCA") + '  "%s" · %d resultado(s)%s' % (q, len(res), ", mostrando 10" if len(res) > 10 else ""))
    if not res:
        print()
        print("Nada encontrado. Tente outras palavras ou veja tudo com --list.")
        return EXIT_OK
    for n, (_, _, kind, obj) in enumerate(res[:10], 1):
        print()
        if kind == "bundle":
            print("%s %s  %s" % (red("%2d." % n), bold("pacote " + obj["name"]), dim("plugin · " + cat.cat_label(obj.get("category") or ""))))
            print("    " + short(obj.get("description"), 100))
            print("    " + dim("%s --plugin %s" % (cli_prefix(src), obj["name"])))
            continue
        extra = " · do plugin %s" % obj["partOf"].split("/")[-1] if obj.get("partOf") else ""
        print("%s %s  %s" % (red("%2d." % n), bold(obj["id"]), dim(SINGULAR[obj["type"]] + extra)))
        print("    " + short(obj.get("description"), 100))
        print("    " + dim(install_cmd(src, obj["type"], item_spec(obj))))
    return EXIT_OK


def cmd_list(args):
    src = pick_source(args.source)
    cat = src.catalog()
    want = (args.list or "").strip()
    tid = None
    if want and fold(want) not in ("all", "todos", "tudo"):
        tid = type_alias(want)
        if not tid:
            raise HubError("tipo desconhecido: %s" % want,
                           hint="Tipos: " + ", ".join(TYPE_IDS), code=EXIT_USAGE)
    catf = args.category
    if catf and catf not in cat.categories and not any(i["category"] == catf for i in cat.items):
        raise HubError("categoria desconhecida: %s" % catf,
                       hint="Categorias: " + ", ".join(sorted(cat.categories)), code=EXIT_USAGE)
    print(banner("catálogo"))
    total = 0
    for t in ([tid] if tid else TYPE_IDS):
        items = [i for i in cat.of_type(t) if not catf or i["category"] == catf]
        bundles = [b for b in cat.bundles if t == "plugins" and (not catf or b.get("category") == catf)]
        if not items and not bundles:
            if tid:
                print()
                print(tag(LABEL[t].upper()) + "  " + dim("nenhum item" + (" nesta categoria" if catf else "")))
            continue
        total += len(items) + len(bundles)
        print()
        print(tag(LABEL[t].upper()) + "  " + dim(str(len(items) + len(bundles))))
        items.sort(key=lambda i: (cat.cat_order(i["category"]), i["category"], i["name"]))
        lastc = None
        width = min(44, max([len(item_spec(i)) for i in items] + [10]))
        for it in items:
            if it["category"] != lastc:
                lastc = it["category"]
                print("  " + bold(cat.cat_label(lastc)) + dim("  (%s)" % lastc))
            extra = dim("  · plugin " + it["partOf"].split("/")[-1]) if it.get("partOf") else ""
            print("    %-*s  %s%s" % (width, item_spec(it), dim(short(it["description"], 70)), extra))
        if bundles:
            print("  " + bold("Pacotes por categoria") + dim("  (--plugin ta-<categoria>)"))
            for b in sorted(bundles, key=lambda x: x["name"]):
                print("    %-*s  %s" % (width, b["name"], dim(short(b.get("description"), 70))))
    print()
    if not total:
        print("Nada para listar.")
    else:
        ft = tid or "skills"
        print(dim("Instale: %s --%s categoria/nome   ·   detalhes: --info %s/categoria/nome"
                  % (cli_prefix(src), FLAG[ft], ft)))
    return EXIT_OK


def install_target_text(cat, it):
    t, n = it["type"], it["name"]
    mp = cat.marketplace()
    return {
        "prompts": ".claude/commands/%s.md (comando /%s)" % (n, n),
        "frameworks": ".claude/skills/%s/SKILL.md" % framework_skill_name(n),
        "skills": ".claude/skills/%s/" % n,
        "agents": ".claude/agents/%s.md" % n,
        "commands": ".claude/commands/%s.md" % n,
        "mcps": ".mcp.json (mcpServers)",
        "hooks": "settings do escopo (hooks) + .claude/hooks/",
        "settings": "settings do escopo + .claude/scripts/",
        "plugins": "marketplace %s: /plugin install %s@%s" % (mp, it.get("marketplaceName") or it.get("pluginName") or n, mp),
        "templates": "raiz do projeto (não sobrescreve sem --force)",
        "repos": "git clone em ./%s" % n,
    }.get(t, "")


def cmd_info(args):
    src = pick_source(args.source)
    cat = src.catalog()
    spec = args.info.strip()
    res = [("item", i) for i in find_items(cat, None, spec)]
    res += [("bundle", b) for b in cat.bundles if b["name"] == spec.strip("/").split("/")[-1]]
    if not res:
        sug = _suggest(cat, None, spec)
        raise HubError('nada encontrado para --info "%s"' % spec,
                       ("Talvez: " + ", ".join(sug) + "\n" if sug else "") + "Use o formato tipo/categoria/nome, por exemplo skills/copy/copywriting.")
    if len(res) > 1:
        lines = ["  --info %s" % (o["id"] if k == "item" else o["name"]) for k, o in res]
        raise HubError('"%s" bate com mais de um item. Escolha um:' % spec, "\n".join(lines))
    kind, o = res[0]
    print(banner("detalhes"))
    print()
    wrap = lambda s: textwrap.fill(re.sub(r"\s+", " ", str(s or "")).strip(), width=88,
                                   initial_indent="  ", subsequent_indent="  ")
    if kind == "bundle":
        print(tag("PACOTE") + "  " + bold(o["name"]))
        print(wrap(o.get("description")))
        print()
        print(dim("  categoria  ") + cat.cat_label(o.get("category") or ""))
        print(dim("  contém     ") + "%s skills · %s agentes · %s comandos" % (o.get("skills", 0), o.get("agents", 0), o.get("commands", 0)))
        for m in (o.get("members") or [])[:30]:
            print("    · " + str(m))
        print()
        print(dim("  instalar   ") + "%s --plugin %s" % (cli_prefix(src), o["name"]))
        print(dim("  no claude  ") + "/plugin install %s@%s" % (o["name"], cat.marketplace()))
        return EXIT_OK
    it = o
    print(tag(SINGULAR[it["type"]].upper()) + "  " + bold(it.get("title") or it["name"]))
    print(wrap(it.get("description")))
    print()
    row = lambda k, v: print(dim("  %-12s" % k) + str(v)) if v not in (None, "", [], {}) else None
    row("id", it["id"])
    row("categoria", "%s (%s)" % (cat.cat_label(it["category"]), it["category"]))
    row("autor", it.get("author"))
    row("licença", it.get("license"))
    row("versão", it.get("version"))
    row("tags", ", ".join(map(str, it.get("tags") or [])))
    if it["type"] == "prompts":
        tools = it.get("tools") if isinstance(it.get("tools"), list) else []
        row("ferramentas", ", ".join(map(str, tools)) or "qualquer IA de texto")
        row("saída", it.get("output") or "não informada")
        variables = [v for v in (it.get("variables") or []) if isinstance(v, dict) and v.get("name")]
        row("variáveis", "%d" % len(variables) if variables else "nenhuma")
        for v in variables:
            print("    · %s%s" % (bold("{{%s}}" % v["name"]), dim("  " + str(v.get("label") or ""))))
    if it["type"] == "frameworks":
        row("quando usar", it.get("when"))
        row("origem", it.get("origin"))
    if it["type"] == "agents":
        row("modelo", it.get("model"))
        row("ferramentas", it.get("tools"))
    if it["type"] == "commands":
        row("argumentos", it.get("argumentHint"))
    if it["type"] == "mcps":
        row("servidores", ", ".join(it.get("servers") or []))
        row("requer", ", ".join(it.get("requires") or []))
    if it["type"] == "hooks":
        row("eventos", ", ".join(it.get("events") or []))
    if it["type"] == "repos":
        r = it.get("repo") or {}
        row("url", r.get("url"))
        row("estrelas", r.get("stars"))
        row("linguagem", r.get("language"))
    src_info = it.get("source") or {}
    if isinstance(src_info, dict):
        row("fonte", src_info.get("url") or src_info.get("repo") or src_info.get("note"))
    if it.get("partOf"):
        row("plugin", it["partOf"])
    if it.get("children"):
        row("filhos", "%d itens (skills, agentes e comandos)" % len(it["children"]))
    row("pacote", it.get("bundle"))
    files = it.get("files") or []
    size = it.get("size") or 0
    row("arquivos", "%d · %.1f KB" % (len(files), size / 1024.0) if files else None)
    if it.get("kind") == "dir" and it["type"] != "plugins":
        base = str(it.get("base") or "")
        for f in files[:20]:
            print("    · " + (f[len(base) + 1:] if f.startswith(base + "/") else f))
        if len(files) > 20:
            print(dim("    … e mais %d" % (len(files) - 20)))
    row("instala em", install_target_text(cat, it))
    if it.get("preview") and it["type"] in ("prompts", "frameworks"):
        row("prévia", short(it["preview"], 160))
    print()
    if it["type"] in ("prompts", "frameworks"):
        print(dim("  ver texto  ") + "%s --show %s" % (cli_prefix(src), it["id"]))
    if it["type"] == "plugins":
        print(dim("  instalar   ") + "%s --plugin %s" % (cli_prefix(src), item_spec(it)))
    else:
        print(dim("  instalar   ") + install_cmd(src, it["type"], item_spec(it)))
    return EXIT_OK


def main_file(it):
    """Arquivo principal do item (relativo à raiz da origem)."""
    base = safe_rel(it.get("base") or (it.get("files") or [""])[0])
    if it.get("kind") != "dir":
        return base
    main = str(it.get("main") or "").strip("/")
    if main:
        return safe_rel(base + "/" + main)
    files = it.get("files") or []
    if not files:
        raise HubError("o item %s não tem arquivos no catálogo" % it["id"])
    return safe_rel(files[0])


def parse_vars(pairs):
    values = {}
    for p in pairs or []:
        if "=" not in p:
            raise HubError("use --var nome=valor (recebi %r)" % p, code=EXIT_USAGE)
        k, v = p.split("=", 1)
        k = k.strip().strip("{} ")
        if not re.match(r"^[A-Za-z0-9_]+$", k):
            raise HubError("nome de variável inválido em --var: %r" % k, code=EXIT_USAGE)
        values[k] = v
    return values


def cmd_show(args):
    values = parse_vars(args.var)
    src = pick_source(args.source)
    cat = src.catalog()
    spec = args.show.strip()
    res = find_items(cat, None, spec)
    if not res:
        sug = _suggest(cat, None, spec)
        raise HubError('nada encontrado para --show "%s"' % spec,
                       ("Talvez: " + ", ".join(sug) + "\n" if sug else "")
                       + "Use tipo/categoria/nome ou categoria/nome, por exemplo prompts/copy/extrair-vsl.")
    if len(res) > 1:
        raise HubError('"%s" bate com mais de um item. Escolha um:' % spec,
                       "\n".join("  --show %s" % i["id"] for i in res))
    it = res[0]
    rel = main_file(it)
    data = src.read(rel)
    if b"\x00" in data[:4096]:
        raise HubError("o arquivo principal de %s não é texto: %s" % (it["id"], rel))
    text = source_text(data)
    if it["type"] == "prompts":
        text = parse_frontmatter(text)[1].strip() + "\n"
    missing = []
    if it["type"] == "prompts" or values:
        used = set(VAR_RE.findall(text))
        text, missing = fill_variables(text, values)
        unused = [k for k in values if k not in used]
        if unused:
            print(paint("!", "33", ECOLOR) + " variável que não aparece no texto: " + ", ".join(unused), file=sys.stderr)
    sys.stdout.write(text if text.endswith("\n") else text + "\n")
    sys.stdout.flush()
    if missing:
        print(paint("!", "33", ECOLOR) + " variáveis sem valor (ficaram como {{nome}}): " + ", ".join(missing)
              + ". Preencha com --var nome=valor.", file=sys.stderr)
    return EXIT_OK


# ================================================================ health check

def count_installed(base):
    base = Path(base)
    sk = len(list((base / "skills").glob("*/SKILL.md"))) if (base / "skills").is_dir() else 0
    ag = len(list((base / "agents").rglob("*.md"))) if (base / "agents").is_dir() else 0
    cm = len(list((base / "commands").rglob("*.md"))) if (base / "commands").is_dir() else 0
    return sk, ag, cm


def cmd_health(args):
    rows = []

    def add(kind, text, fix=None):
        rows.append((kind, text, fix))

    pv = platform.python_version()
    if sys.version_info >= (3, 9):
        add("ok", "Python %s" % pv)
    else:
        add("bad", "Python %s (precisa 3.9 ou mais novo)" % pv, "instale o Python 3.9+ em python.org")
    claude = shutil.which("claude")
    if claude:
        try:
            r = subprocess.run([claude, "--version"], capture_output=True, text=True, timeout=20)
            v = (r.stdout or r.stderr or "").strip().splitlines()
            add("ok", "claude %s (%s)" % (v[0] if v else "?", claude))
        except (OSError, subprocess.TimeoutExpired) as e:
            add("warn", "claude encontrado em %s, mas não respondeu (%s)" % (claude, e), "reinstale o Claude Code")
    else:
        add("warn", "comando claude não está no PATH",
            "instale o Claude Code: npm install -g @anthropic-ai/claude-code (ou veja docs.claude.com)")
    if shutil.which("git"):
        add("ok", "git disponível")
    else:
        add("warn", "git não encontrado (só é preciso para --repo)", "instale o git")
    ud = claude_user_dir()
    label_ud = ("CLAUDE_CONFIG_DIR " if os.environ.get("CLAUDE_CONFIG_DIR") else "") + str(ud)
    if ud.is_dir():
        add("ok", "pasta do usuário: %s" % label_ud)
    else:
        add("warn", "pasta do usuário não existe: %s" % label_ud, "abra o Claude Code uma vez para criá-la")
    proj = project_dir(args.directory) if args.directory else Path(os.getcwd())
    for label, path in (("~/.claude/settings.json", ud / "settings.json"),
                        (".claude/settings.json", proj / ".claude" / "settings.json"),
                        (".claude/settings.local.json", proj / ".claude" / "settings.local.json"),
                        (".mcp.json", proj / ".mcp.json")):
        if not path.exists():
            add("ok", "%s não existe (opcional)" % label)
            continue
        try:
            read_json_file(path)
            add("ok", "%s: JSON válido" % label)
        except HubError as e:
            add("bad", e.msg, "corrija o JSON; o instalador guarda backups em .tahub-backups/")
    sk, ag, cm = count_installed(proj / ".claude")
    add("ok", "projeto %s: %d skills · %d agentes · %d comandos" % (proj, sk, ag, cm))
    sk, ag, cm = count_installed(ud)
    add("ok", "usuário: %d skills · %d agentes · %d comandos" % (sk, ag, cm))
    try:
        src = pick_source(args.source)
        cat = src.catalog()
        add("ok", "catálogo responde: %d itens · %s" % (len(cat.items), src.describe()))
    except HubError as e:
        add("bad", "catálogo: " + e.msg, "use --source <url-ou-pasta> ou a variável TAHUB_SOURCE")
    print(banner("diagnóstico"))
    print()
    print(tag("HEALTH CHECK"))
    icons = {"ok": green("✓"), "bad": red("✗"), "warn": yellow("!")}
    for kind, text, fix in rows:
        print("  %s %s" % (icons[kind], text))
        if fix and kind != "ok":
            print(dim("      → " + fix))
    nb = sum(1 for r in rows if r[0] == "bad")
    nw = sum(1 for r in rows if r[0] == "warn")
    print()
    if nb:
        print(red("✗") + " %d problema(s) e %d aviso(s)." % (nb, nw))
    elif nw:
        print(yellow("!") + " Funciona, com %d aviso(s)." % nw)
    else:
        print(green("✓") + " Tudo certo.")
    return EXIT_ERR if nb else EXIT_OK


# ================================================================ leitura das conversas (~/.claude/projects)

SYSTEM_PREFIXES = ("<system-reminder", "<command-", "<local-command", "<task-notification", "<bash-",
                   "<user-prompt-submit-hook", "<teammate", "<peer", "Caveat:", "[Request interrupted",
                   "Base directory for this skill", "This session is being continued")
TOKEN_KEYS = (("input_tokens", "input"), ("output_tokens", "output"),
              ("cache_read_input_tokens", "cacheRead"), ("cache_creation_input_tokens", "cacheCreation"))
TS_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2})(?:[.,](\d+))?\s*(Z|[+-]\d{2}:?\d{2})?$")
HAY_MAX = 1500000
ID_RE = re.compile(r"^[A-Za-z0-9._-]{1,200}$")


def parse_ts(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v) / 1000.0 if v > 1e12 else float(v)
    if not isinstance(v, str):
        return None
    m = TS_RE.match(v.strip())
    if not m:
        return None
    y, mo, d, h, mi, s = (int(x) for x in m.groups()[:6])
    micro = int(((m.group(7) or "0") + "000000")[:6])
    tz = m.group(8)
    if tz in (None, "Z"):
        tzinfo = datetime.timezone.utc
    else:
        sign = 1 if tz[0] == "+" else -1
        tzinfo = datetime.timezone(sign * datetime.timedelta(hours=int(tz[1:3]), minutes=int(tz[-2:])))
    try:
        return datetime.datetime(y, mo, d, h, mi, s, micro, tzinfo).timestamp()
    except (ValueError, OverflowError):
        return None


def local_date(ts):
    try:
        return datetime.date.fromtimestamp(ts).isoformat()
    except (ValueError, OverflowError, OSError):
        return None


def _int(v):
    try:
        return max(0, int(v))
    except (TypeError, ValueError):
        return 0


def content_blocks(content):
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    out = []
    if isinstance(content, list):
        for b in content:
            if isinstance(b, dict):
                out.append(b)
            elif isinstance(b, str):
                out.append({"type": "text", "text": b})
    return out


def is_system_text(s):
    return str(s).lstrip().startswith(SYSTEM_PREFIXES)


def one_line(s, n):
    return short(s, n)


def command_title(texts):
    for t in texts:
        m = re.search(r"<command-name>(.*?)</command-name>", t, re.S)
        if m:
            name = m.group(1).strip()
            a = re.search(r"<command-args>(.*?)</command-args>", t, re.S)
            return one_line(("/" + name.lstrip("/")) + (" " + a.group(1).strip() if a and a.group(1).strip() else ""), 140)
    return ""


def session_key(stem, sid):
    if sid == stem and ID_RE.match(sid):
        return sid
    return "%s--%s" % (stem if ID_RE.match(stem) else hashlib.sha1(stem.encode()).hexdigest()[:12],
                       hashlib.sha1(sid.encode("utf-8", "replace")).hexdigest()[:10])


def _zero_tokens():
    return {"input": 0, "output": 0, "cacheRead": 0, "cacheCreation": 0}


def summarize_file(path):
    path = Path(path)
    stem = path.stem
    sessions, seen = {}, set()

    def sess(sid):
        s = sessions.get(sid)
        if s is None:
            s = sessions[sid] = {"id": session_key(stem, sid), "sid": sid, "file": str(path),
                                 "projectDir": path.parent.name, "cwd": "", "title": "", "cmdTitle": "",
                                 "customTitle": "", "first": None, "last": None, "user": 0, "assistant": 0,
                                 "tokens": _zero_tokens(), "models": {}, "days": {}, "_hay": [], "_n": 0}
        return s

    def hay(s, texts):
        for t in texts:
            if s["_n"] >= HAY_MAX:
                return
            t = t[: HAY_MAX - s["_n"]]
            s["_hay"].append(t)
            s["_n"] += len(t) + 1

    def day(s, d):
        x = s["days"].get(d)
        if x is None:
            x = s["days"][d] = dict(_zero_tokens(), messages=0)
        return x

    with open(str(path), encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"user"' not in line and '"assistant"' not in line and "custom-title" not in line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if not isinstance(d, dict):
                continue
            t = d.get("type")
            sid = d.get("sessionId") if isinstance(d.get("sessionId"), str) and d.get("sessionId") else stem
            if t == "custom-title":
                if isinstance(d.get("customTitle"), str):
                    sess(sid)["customTitle"] = d["customTitle"][:200]
                continue
            if t not in ("user", "assistant"):
                continue
            m = d.get("message") if isinstance(d.get("message"), dict) else {}
            s = sess(sid)
            ts = parse_ts(d.get("timestamp"))
            if ts is not None:
                if s["first"] is None or ts < s["first"]:
                    s["first"] = ts
                if s["last"] is None or ts > s["last"]:
                    s["last"] = ts
            if not s["cwd"] and isinstance(d.get("cwd"), str):
                s["cwd"] = d["cwd"]
            dd = local_date(ts) if ts is not None else None
            blocks = content_blocks(m.get("content"))
            texts = [b["text"] for b in blocks if b.get("type") == "text" and isinstance(b.get("text"), str)
                     and b["text"].strip()]
            if t == "user":
                if d.get("isMeta") or not texts:
                    continue
                human = [x for x in texts if not is_system_text(x)]
                if not human:
                    if not s["cmdTitle"]:
                        s["cmdTitle"] = command_title(texts)
                    continue
                s["user"] += 1
                if not s["title"]:
                    s["title"] = one_line(human[0], 140)
                if dd:
                    day(s, dd)["messages"] += 1
                hay(s, human)
                continue
            mid = m.get("id")
            if not (isinstance(mid, str) and mid) and not blocks:
                continue
            if isinstance(mid, str) and mid:
                if mid in seen:
                    hay(s, texts)
                    continue
                seen.add(mid)
            s["assistant"] += 1
            usage = m.get("usage") if isinstance(m.get("usage"), dict) else {}
            tok = {k2: _int(usage.get(k1)) for k1, k2 in TOKEN_KEYS}
            for k, v in tok.items():
                s["tokens"][k] += v
            model = m.get("model") if isinstance(m.get("model"), str) else ""
            if model and model != "<synthetic>":
                mm = s["models"].setdefault(model, dict(_zero_tokens(), messages=0))
                for k, v in tok.items():
                    mm[k] += v
                mm["messages"] += 1
            if dd:
                x = day(s, dd)
                x["messages"] += 1
                for k, v in tok.items():
                    x[k] += v
            hay(s, texts)
    out = {}
    for sid, s in sessions.items():
        s["hay"] = "\n".join(s.pop("_hay"))
        s.pop("_n", None)
        s["messages"] = s["user"] + s["assistant"]
        if not s["messages"]:
            continue
        s["title"] = s["title"] or s["customTitle"] or s["cmdTitle"] or "(sem título)"
        cwd = s["cwd"].rstrip("/\\")
        s["project"] = os.path.basename(cwd) if cwd else s["projectDir"]
        s["tokensTotal"] = sum(s["tokens"].values())
        out[sid] = s
    return out


class SessionIndex:
    def __init__(self, claude_dir):
        self.claude_dir = Path(claude_dir)
        self.root = self.claude_dir / "projects"
        self.cache = {}
        self.by_key = {}
        self.nfiles = 0
        self.lock = threading.Lock()

    def snapshot(self):
        with self.lock:
            pattern = os.path.join(glob.escape(str(self.root)), "*", "*.jsonl")
            files = sorted(glob.glob(pattern))
            alive = set()
            for f in files:
                try:
                    st = os.stat(f)
                except OSError:
                    continue
                sig = (st.st_mtime_ns, st.st_size)
                alive.add(f)
                c = self.cache.get(f)
                if c and c[0] == sig:
                    continue
                try:
                    self.cache[f] = (sig, summarize_file(f))
                except (OSError, MemoryError):
                    continue
            for f in list(self.cache):
                if f not in alive:
                    del self.cache[f]
            sessions, by_key = [], {}
            for f in files:
                for s in (self.cache.get(f) or (None, {}))[1].values():
                    sessions.append(s)
                    by_key[s["id"]] = s
            self.by_key = by_key
            self.nfiles = len(alive)
            return sessions


def public_session(s):
    return {"id": s["id"], "title": s["title"], "project": s["project"], "cwd": s["cwd"],
            "start": s["first"], "last": s["last"], "messages": s["messages"], "user": s["user"],
            "assistant": s["assistant"], "tokens": s["tokensTotal"]}


def build_stats(index):
    sessions = index.snapshot()
    today = datetime.date.today()
    days = [(today - datetime.timedelta(days=i)).isoformat() for i in range(29, -1, -1)]
    dmap = {d: dict(_zero_tokens(), date=d, total=0, messages=0, sessions=0) for d in days}
    tot = _zero_tokens()
    models, projects = {}, {}
    nuser = nassist = 0
    for s in sessions:
        nuser += s["user"]
        nassist += s["assistant"]
        for k in tot:
            tot[k] += s["tokens"][k]
        for name, mm in s["models"].items():
            x = models.setdefault(name, dict(_zero_tokens(), model=name, messages=0))
            for k in _zero_tokens():
                x[k] += mm[k]
            x["messages"] += mm["messages"]
        for d, v in s["days"].items():
            if d in dmap:
                x = dmap[d]
                for k in _zero_tokens():
                    x[k] += v[k]
                x["messages"] += v["messages"]
                x["sessions"] += 1
        key = s["cwd"] or s["projectDir"]
        p = projects.setdefault(key, {"name": s["project"], "path": key, "sessions": 0, "messages": 0,
                                      "tokens": 0, "last": None})
        p["sessions"] += 1
        p["messages"] += s["messages"]
        p["tokens"] += s["tokensTotal"]
        if s["last"] and (p["last"] is None or s["last"] > p["last"]):
            p["last"] = s["last"]
    for x in list(dmap.values()) + list(models.values()):
        x["total"] = x["input"] + x["output"] + x["cacheRead"] + x["cacheCreation"]
    recent = sorted(sessions, key=lambda s: s["last"] or 0, reverse=True)[:15]
    return {
        "ok": True,
        "generatedAt": datetime.datetime.now().timestamp(),
        "claudeDir": str(index.claude_dir),
        "files": index.nfiles,
        "totals": {"sessions": len(sessions), "messages": nuser + nassist, "userMessages": nuser,
                   "assistantMessages": nassist, "tokens": dict(tot, total=sum(tot.values()))},
        "models": sorted(models.values(), key=lambda x: -x["total"]),
        "days": [dmap[d] for d in days],
        "projects": sorted(projects.values(), key=lambda p: (-p["messages"], -(p["last"] or 0)))[:10],
        "recent": [public_session(s) for s in recent],
    }


def _cut(s, n):
    s = str(s or "")
    return s if len(s) <= n else s[:n] + "\n… (cortado: mais %d caracteres)" % (len(s) - n)


def _result_text(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        parts = []
        for b in c:
            if isinstance(b, dict):
                if b.get("type") == "text":
                    parts.append(str(b.get("text") or ""))
                elif b.get("type") == "image":
                    parts.append("[imagem]")
                else:
                    parts.append(json.dumps(b, ensure_ascii=False)[:2000])
            else:
                parts.append(str(b))
        return "\n".join(parts)
    return "" if c is None else json.dumps(c, ensure_ascii=False)


def view_blocks(content, role):
    out = []
    for b in content_blocks(content):
        bt = b.get("type")
        if bt == "text":
            tx = b.get("text") if isinstance(b.get("text"), str) else ""
            if not tx.strip():
                continue
            if role == "user" and is_system_text(tx):
                out.append({"t": "meta", "text": _cut(tx, 20000)})
            else:
                out.append({"t": "text", "text": _cut(tx, 100000)})
        elif bt == "thinking":
            tx = b.get("thinking") or b.get("text") or ""
            if isinstance(tx, str) and tx.strip():
                out.append({"t": "thinking", "text": _cut(tx, 20000)})
        elif bt == "tool_use":
            try:
                inp = json.dumps(b.get("input"), ensure_ascii=False, indent=2)
            except (TypeError, ValueError):
                inp = str(b.get("input"))
            out.append({"t": "tool_use", "name": str(b.get("name") or ""), "input": _cut(inp, 12000)})
        elif bt == "tool_result":
            out.append({"t": "tool_result", "text": _cut(_result_text(b.get("content")), 12000),
                        "error": bool(b.get("is_error"))})
        elif bt == "image":
            out.append({"t": "image"})
    return out


def load_conversation(s, max_msgs=5000):
    msgs, by_id, truncated = [], {}, False
    stem = Path(s["file"]).stem
    with open(s["file"], encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if '"user"' not in line and '"assistant"' not in line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if not isinstance(d, dict) or d.get("type") not in ("user", "assistant"):
                continue
            sid = d.get("sessionId") if isinstance(d.get("sessionId"), str) and d.get("sessionId") else stem
            if sid != s["sid"]:
                continue
            t = d["type"]
            m = d.get("message") if isinstance(d.get("message"), dict) else {}
            blocks = view_blocks(m.get("content"), t)
            if not blocks:
                continue
            ts = parse_ts(d.get("timestamp"))
            if t == "assistant":
                mid = m.get("id") if isinstance(m.get("id"), str) else None
                if mid and mid in by_id:
                    by_id[mid]["blocks"].extend(blocks)
                    continue
                model = m.get("model") if isinstance(m.get("model"), str) and m.get("model") != "<synthetic>" else None
                entry = {"role": "assistant", "ts": ts, "model": model, "blocks": blocks}
                if mid:
                    by_id[mid] = entry
            else:
                kinds = {b["t"] for b in blocks}
                if d.get("isMeta"):
                    role = "meta"
                    blocks = [dict(b, t="meta") if b["t"] == "text" else b for b in blocks]
                elif kinds <= {"meta"}:
                    role = "meta"
                elif kinds <= {"tool_result"}:
                    role = "tool"
                else:
                    role = "user"
                entry = {"role": role, "ts": ts, "blocks": blocks}
            if len(msgs) >= max_msgs:
                truncated = True
                break
            msgs.append(entry)
    return msgs, truncated


def api_sessions(index, q):
    sessions = index.snapshot()
    try:
        limit = max(1, min(2000, int((q.get("limit") or ["300"])[0])))
    except ValueError:
        limit = 300
    query = (q.get("q") or [""])[0].strip()[:200]
    sessions = sorted(sessions, key=lambda s: s["last"] or 0, reverse=True)
    if not query:
        return {"ok": True, "query": "", "total": len(sessions), "sessions": [public_session(s) for s in sessions[:limit]]}
    words = [w for w in fold(query).split() if w]
    out = []
    for s in sessions:
        if "_fold" not in s:
            s["_fold"] = fold(s["hay"])
        low = s["_fold"]
        head = fold(s["title"] + " " + s["project"])
        if not all(w in low or w in head for w in words):
            continue
        ps = public_session(s)
        i = low.find(words[0])
        if i >= 0:
            a = max(0, i - 60)
            b = min(len(s["hay"]), i + len(words[0]) + 110)
            pre = "…" if a else ""
            txt = s["hay"][a:b].replace("\n", " ").replace("\r", " ").replace("\t", " ")
            ps["snippet"] = {"text": pre + txt + ("…" if b < len(s["hay"]) else ""),
                             "start": len(pre) + (i - a), "end": len(pre) + (i - a) + len(words[0])}
        out.append(ps)
    return {"ok": True, "query": query, "total": len(out), "sessions": out[:limit]}


def api_session(index, q):
    sid = (q.get("id") or [""])[0]
    if not ID_RE.match(sid):
        return {"ok": False, "error": "id inválido"}, 400
    s = index.by_key.get(sid)
    if s is None:
        index.snapshot()
        s = index.by_key.get(sid)
    if s is None:
        return {"ok": False, "error": "sessão não encontrada"}, 404
    try:
        msgs, truncated = load_conversation(s)
    except OSError as e:
        return {"ok": False, "error": "não consegui ler a sessão: %s" % e}, 500
    return {"ok": True, "session": public_session(s), "messages": msgs, "truncated": truncated}, 200


# ================================================================ páginas locais (analytics e chats)

LOGO_SVG = ('<svg class="logo" viewBox="190 190 710 612" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            '<polygon fill="#CE0103" points="543,211 736,548 673,664 478,325"/>'
            '<polygon fill="#CE0103" points="406,434 532,434 334,782 210,782"/>'
            '<polygon fill="#CE0103" points="411,671 815,671 880,783 474,783"/></svg>')
FAVICON = ('<svg viewBox="190 190 710 612" xmlns="http://www.w3.org/2000/svg">'
           '<polygon fill="#CE0103" points="543,211 736,548 673,664 478,325"/>'
           '<polygon fill="#CE0103" points="406,434 532,434 334,782 210,782"/>'
           '<polygon fill="#CE0103" points="411,671 815,671 880,783 474,783"/></svg>')
FONTS = ("https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700"
         "&family=JetBrains+Mono:wght@400;600&display=swap")
CSP = ("default-src 'none'; style-src 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; script-src 'unsafe-inline'; connect-src 'self'; "
       "img-src 'self' data:; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")

BASE_CSS = r"""
:root{--bg:#050505;--card:#111113;--line:#26262A;--red:#CE0103;--neon:#FF2B2B;--tx:#F5F5F5;--mut:#A1A1A1;--soft:#1a1a1d}
*{box-sizing:border-box}
html,body{margin:0;background:var(--bg);color:var(--tx)}
body{font:14px/1.55 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.top{position:sticky;top:0;z-index:10;display:flex;align-items:center;gap:14px;padding:14px 24px;background:rgba(5,5,5,.94);border-bottom:1px solid var(--line);backdrop-filter:blur(8px)}
.logo{width:30px;height:26px;display:block;flex:none}
.brand{font-family:Anton,Impact,"Arial Narrow",sans-serif;text-transform:uppercase;font-size:20px;letter-spacing:.03em;line-height:1;white-space:nowrap}
.lbl{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--tx);white-space:nowrap}
.lbl b{color:var(--red);font-weight:700}
.sp{flex:1}
.live{display:flex;align-items:center;gap:8px;color:var(--mut);font-size:12px;font-family:"JetBrains Mono",ui-monospace,monospace;white-space:nowrap}
.dot{width:8px;height:8px;border-radius:50%;background:var(--neon);box-shadow:0 0 8px var(--neon)}
.dot.off{background:var(--mut);box-shadow:none}
h1,h2,h3{font-family:Anton,Impact,sans-serif;font-weight:400;text-transform:uppercase;letter-spacing:.03em;margin:0}
h2{font-size:17px;margin-bottom:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;min-width:0}
.mut{color:var(--mut)}
.mono,code,pre{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{padding:9px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{color:var(--mut);font-weight:500;font-size:11px;text-transform:uppercase;letter-spacing:.08em}
tr:last-child td{border-bottom:0}
.n{text-align:right;font-family:"JetBrains Mono",ui-monospace,monospace;font-variant-numeric:tabular-nums;white-space:nowrap}
.empty{color:var(--mut);padding:28px;text-align:center}
::selection{background:var(--red);color:#fff}
@media (max-width:640px){.top{padding:12px 16px;gap:10px}.brand{display:none}}
"""

COMMON_JS = r"""
const $=s=>document.querySelector(s);
const E=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const NF=new Intl.NumberFormat('pt-BR');
const N=n=>NF.format(n||0);
let CF=null;try{CF=new Intl.NumberFormat('pt-BR',{notation:'compact',maximumFractionDigits:1});}catch(e){}
const C=n=>CF?CF.format(n||0):N(n);
const D=t=>t?new Date(t*1000).toLocaleString('pt-BR',{day:'2-digit',month:'2-digit',year:'2-digit',hour:'2-digit',minute:'2-digit'}):'';
async function getJSON(u){const r=await fetch(u,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);return r.json();}
"""


def html_page(title, label, css, body, js, body_class=""):
    head = ('<header class="top"><a href="/" aria-label="Início">' + LOGO_SVG + '</a>'
            '<div class="brand">Central Trip Angle</div><div class="lbl"><b>[</b> ' + label + ' <b>]</b></div>'
            '<div class="sp"></div><div class="live"><span class="dot off" id="dot"></span>'
            '<span id="st">carregando…</span></div></header>')
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="color-scheme" content="dark"><title>' + title + '</title>'
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="' + FONTS + '">'
            '<style>' + BASE_CSS + css + '</style></head><body class="' + body_class + '">' + head + body +
            '<script>' + COMMON_JS + js + '</script></body></html>')


ANALYTICS_CSS = r"""
main{max-width:1200px;margin:0 auto;padding:24px;display:grid;gap:16px}
.kpis{display:grid;gap:16px;grid-template-columns:repeat(6,minmax(0,1fr))}
@media (max-width:1100px){.kpis{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:560px){.kpis{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}}
.kpi .l{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin-bottom:6px}
.kpi .v{font-family:Anton,Impact,sans-serif;font-size:32px;line-height:1.1;white-space:nowrap}
.kpi .s{color:var(--mut);font-size:12px;margin-top:4px}
.two{display:grid;gap:16px;grid-template-columns:1fr 1fr}
@media (max-width:860px){.two{grid-template-columns:1fr}}
.ch{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:6px}
.ch h2{margin:0}
svg.chart{width:100%;height:auto;display:block}
.chart .b{fill:var(--red)}
.chart .b:hover{opacity:.7}
.chart .gl{stroke:var(--line);stroke-width:1}
.chart .ax{fill:var(--mut);font:11px "JetBrains Mono",ui-monospace,monospace}
.row{display:grid;grid-template-columns:130px 1fr 80px;gap:12px;align-items:center;padding:9px 0;border-bottom:1px solid var(--line)}
.row:last-child{border-bottom:0}
.meter{height:6px;border-radius:3px;background:var(--soft);overflow:hidden}
.meter i{display:block;height:100%;background:var(--red)}
.ttl{max-width:440px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.scroll{overflow-x:auto}
footer{color:var(--mut);font-size:12px;padding:4px 2px 32px}
@media (max-width:640px){main{padding:16px}.kpi .v{font-size:28px}.row{grid-template-columns:96px 1fr 64px}}
"""

ANALYTICS_BODY = r"""
<main>
  <section class="kpis" id="kpis"></section>
  <section class="card"><div class="ch"><h2>Tokens por dia</h2><span class="mut mono">últimos 30 dias</span></div><div id="chart"></div></section>
  <div class="two">
    <section class="card"><h2>Tokens por tipo</h2><div id="types"></div></section>
    <section class="card"><h2>Tokens por modelo</h2><div id="models" class="scroll"></div></section>
  </div>
  <section class="card"><h2>Projetos mais ativos</h2><div id="projects" class="scroll"></div></section>
  <section class="card"><h2>Sessões recentes</h2><div id="recent" class="scroll"></div></section>
  <footer id="foot"></footer>
</main>
"""

ANALYTICS_JS = r"""
const fd=s=>s.slice(8,10)+'/'+s.slice(5,7);
function kpi(l,v,s){return '<div class="card kpi"><div class="l">'+E(l)+'</div><div class="v">'+E(v)+'</div><div class="s">'+E(s)+'</div></div>';}
function chart(days){
  const W=900,H=240,L=70,R=8,T=12,B=28,ih=H-T-B;
  const max=Math.max(1,...days.map(d=>d.total));
  const bw=(W-L-R)/days.length;
  let s='<svg class="chart" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Tokens por dia">';
  for(let i=0;i<=4;i++){const y=T+ih*i/4;s+='<line class="gl" x1="'+L+'" x2="'+(W-R)+'" y1="'+y+'" y2="'+y+'"/><text class="ax" x="'+(L-8)+'" y="'+(y+4)+'" text-anchor="end">'+E(C(max*(1-i/4)))+'</text>';}
  days.forEach((d,i)=>{
    const h=d.total?Math.max(1.5,ih*d.total/max):0,x=L+i*bw+bw*.16,y=T+ih-h;
    s+='<rect class="b" x="'+x.toFixed(1)+'" y="'+y.toFixed(1)+'" width="'+(bw*.68).toFixed(1)+'" height="'+h.toFixed(1)+'" rx="2"><title>'+E(fd(d.date))+': '+E(N(d.total))+' tokens · '+E(N(d.messages))+' mensagens · entrada '+E(N(d.input))+' · saída '+E(N(d.output))+' · cache '+E(N(d.cacheRead+d.cacheCreation))+'</title></rect>';
    if(i%5===0||i===days.length-1)s+='<text class="ax" x="'+(x+bw*.34).toFixed(1)+'" y="'+(H-8)+'" text-anchor="middle">'+E(fd(d.date))+'</text>';
  });
  return s+'</svg>';
}
function table(head,rows){return '<table><thead><tr>'+head.map(h=>'<th'+(h[1]?' class="n"':'')+'>'+E(h[0])+'</th>').join('')+'</tr></thead><tbody>'+rows.join('')+'</tbody></table>';}
function render(d){
  const t=d.totals,k=t.tokens;
  $('#kpis').innerHTML=[
    kpi('Sessões',N(t.sessions),N(d.files)+' arquivo(s) de conversa'),
    kpi('Mensagens',N(t.messages),N(t.userMessages)+' suas · '+N(t.assistantMessages)+' do Claude'),
    kpi('Tokens',C(k.total),N(k.total)+' no total'),
    kpi('Entrada',C(k.input),N(k.input)+' tokens'),
    kpi('Saída',C(k.output),N(k.output)+' tokens'),
    kpi('Cache',C(k.cacheRead+k.cacheCreation),'leitura '+C(k.cacheRead)+' · criação '+C(k.cacheCreation))
  ].join('');
  $('#chart').innerHTML=t.sessions?chart(d.days):'<div class="empty">Nenhuma conversa encontrada ainda.</div>';
  const tt=[['Entrada',k.input],['Saída',k.output],['Cache leitura',k.cacheRead],['Cache criação',k.cacheCreation]];
  const tm=Math.max(1,...tt.map(x=>x[1]));
  $('#types').innerHTML=tt.map(x=>'<div class="row"><span>'+E(x[0])+'</span><div class="meter"><i style="width:'+(100*x[1]/tm).toFixed(1)+'%"></i></div><span class="n">'+E(C(x[1]))+'</span></div>').join('');
  $('#models').innerHTML=d.models.length?table([['Modelo'],['Entrada',1],['Saída',1],['Cache',1],['Total',1]],d.models.map(m=>'<tr><td class="mono">'+E(m.model)+'</td><td class="n">'+E(C(m.input))+'</td><td class="n">'+E(C(m.output))+'</td><td class="n">'+E(C(m.cacheRead+m.cacheCreation))+'</td><td class="n">'+E(C(m.total))+'</td></tr>')):'<div class="empty">Sem dados de modelo.</div>';
  $('#projects').innerHTML=d.projects.length?table([['Projeto'],['Sessões',1],['Mensagens',1],['Tokens',1],['Última atividade',1]],d.projects.map(p=>'<tr><td title="'+E(p.path)+'"><div class="ttl">'+E(p.name)+'</div></td><td class="n">'+E(N(p.sessions))+'</td><td class="n">'+E(N(p.messages))+'</td><td class="n">'+E(C(p.tokens))+'</td><td class="n">'+E(D(p.last))+'</td></tr>')):'<div class="empty">Sem projetos.</div>';
  $('#recent').innerHTML=d.recent.length?table([['Sessão'],['Projeto'],['Mensagens',1],['Tokens',1],['Quando',1]],d.recent.map(s=>'<tr><td><div class="ttl" title="'+E(s.title)+'">'+E(s.title)+'</div></td><td>'+E(s.project)+'</td><td class="n">'+E(N(s.messages))+'</td><td class="n">'+E(C(s.tokens))+'</td><td class="n">'+E(D(s.last))+'</td></tr>')):'<div class="empty">Sem sessões.</div>';
  $('#foot').innerHTML='Fonte: <span class="mono">'+E(d.claudeDir)+'/projects</span> · atualiza a cada 30 s · tudo fica no seu computador.';
}
async function load(){
  try{const d=await getJSON('/api/stats');render(d);$('#dot').classList.remove('off');$('#st').textContent='ao vivo · '+new Date().toLocaleTimeString('pt-BR');}
  catch(e){$('#dot').classList.add('off');$('#st').textContent='sem conexão';}
}
load();setInterval(load,30000);
"""

CHATS_CSS = r"""
body.app{height:100vh;display:flex;flex-direction:column}
.wrap{flex:1;min-height:0;display:grid;grid-template-columns:minmax(280px,380px) 1fr}
aside{border-right:1px solid var(--line);display:flex;flex-direction:column;min-height:0}
.search{padding:14px;border-bottom:1px solid var(--line)}
.search input{width:100%;background:var(--card);border:1px solid var(--line);border-radius:10px;color:var(--tx);padding:10px 12px;font:inherit;outline:none}
.search input:focus{border-color:var(--red)}
.list{overflow:auto;flex:1}
.it{display:block;padding:12px 16px;border-bottom:1px solid var(--line)}
.it:hover{background:var(--card)}
.it.on{background:var(--card);box-shadow:inset 3px 0 0 var(--red)}
.it .t{font-weight:600;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;word-break:break-word}
.it .m{color:var(--mut);font-size:12px;margin-top:3px}
.it .sn{color:var(--mut);font-size:12px;margin-top:6px;font-family:"JetBrains Mono",ui-monospace,monospace;word-break:break-word}
mark{background:var(--red);color:#fff;border-radius:2px;padding:0 2px}
.conv{overflow:auto;padding:24px;min-width:0}
.head{max-width:880px;margin:0 auto 18px}
.head h1{font-size:24px;line-height:1.15;margin-top:6px;word-break:break-word}
.head .m{color:var(--mut);font-size:12px;margin-top:8px;font-family:"JetBrains Mono",ui-monospace,monospace;word-break:break-all}
.msg{max-width:880px;margin:0 auto 12px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.msg.user{border-left:3px solid var(--red)}
.msg.tool,.msg.meta{background:transparent;border:0;padding:0 4px;margin-top:-4px}
.who{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:8px;display:flex;gap:10px;flex-wrap:wrap}
.who b{color:var(--red)}
.who span{color:var(--mut);letter-spacing:.02em;text-transform:none}
.txt{white-space:pre-wrap;overflow-wrap:anywhere}
.txt+.txt{margin-top:8px}
details{margin-top:8px;border:1px solid var(--line);border-radius:10px;background:#0b0b0c}
details>summary{cursor:pointer;padding:7px 12px;font:12px "JetBrains Mono",ui-monospace,monospace;color:var(--mut);list-style:none}
details>summary::-webkit-details-marker{display:none}
details>summary:before{content:"▸ ";color:var(--red)}
details[open]>summary:before{content:"▾ "}
details pre{margin:0;padding:10px 12px;border-top:1px solid var(--line);overflow:auto;max-height:460px;font-size:12px;white-space:pre-wrap;word-break:break-word}
details.err>summary{color:#ff9b9b}
.back{display:none}
@media (max-width:760px){body.app{height:auto}.wrap{display:block}aside{border-right:0}.list{overflow:visible}.conv{display:none;padding:16px}body.reading aside{display:none}body.reading .conv{display:block}.back{display:inline-block;margin-bottom:12px;color:var(--mut);font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12px}}
"""

CHATS_BODY = r"""
<div class="wrap">
  <aside><div class="search"><input id="q" type="search" placeholder="Buscar nas conversas…" autocomplete="off" aria-label="Buscar nas conversas"></div><div id="list" class="list"><div class="empty">carregando…</div></div></aside>
  <section id="conv" class="conv"><div class="empty">Escolha uma conversa.</div></section>
</div>
"""

CHATS_JS = r"""
let cur=null,seq=0,tm=null;
function row(s){
  let sn='';
  if(s.snippet){const t=s.snippet.text,a=s.snippet.start,b=s.snippet.end;sn='<div class="sn">'+E(t.slice(0,a))+'<mark>'+E(t.slice(a,b))+'</mark>'+E(t.slice(b))+'</div>';}
  return '<a class="it" href="#/s/'+encodeURIComponent(s.id)+'" data-id="'+E(s.id)+'"><div class="t">'+E(s.title)+'</div><div class="m">'+E(s.project)+' · '+E(D(s.last))+' · '+E(N(s.messages))+' msgs</div>'+sn+'</a>';
}
function markOn(){document.querySelectorAll('.it').forEach(a=>a.classList.toggle('on',a.dataset.id===cur));}
async function loadList(){
  const q=$('#q').value.trim(),my=++seq;
  $('#st').textContent=q?'buscando…':'carregando…';
  try{
    const d=await getJSON('/api/sessions?limit=400&q='+encodeURIComponent(q));
    if(my!==seq)return;
    $('#dot').classList.remove('off');
    $('#st').textContent=q?N(d.total)+' resultado(s)':N(d.total)+' sessões';
    $('#list').innerHTML=d.sessions.length?d.sessions.map(row).join(''):'<div class="empty">Nada encontrado.</div>';
    markOn();
  }catch(e){$('#dot').classList.add('off');$('#st').textContent='sem conexão';}
}
function det(label,body,cls){return '<details'+(cls?' class="'+cls+'"':'')+'><summary>'+E(label)+'</summary><pre>'+E(body)+'</pre></details>';}
function blocks(bs){return bs.map(b=>{
  if(b.t==='text')return '<div class="txt">'+E(b.text)+'</div>';
  if(b.t==='thinking')return det('raciocínio',b.text);
  if(b.t==='tool_use')return det('ferramenta · '+(b.name||'?'),b.input);
  if(b.t==='tool_result')return det(b.error?'resultado da ferramenta · erro':'resultado da ferramenta',b.text,b.error?'err':'');
  if(b.t==='meta')return det('contexto do sistema',b.text);
  if(b.t==='image')return '<div class="mut mono">[ imagem ]</div>';
  return '';}).join('');}
function msg(m){
  if(m.role==='tool'||m.role==='meta')return '<div class="msg '+m.role+'">'+blocks(m.blocks)+'</div>';
  const who=m.role==='user'?'você':'claude';
  return '<article class="msg '+m.role+'"><div class="who"><b>[</b> '+who+' <b>]</b><span>'+E(D(m.ts))+'</span>'+(m.model?'<span>'+E(m.model)+'</span>':'')+'</div>'+blocks(m.blocks)+'</article>';
}
async function openS(id){
  cur=id;markOn();
  const c=$('#conv');c.innerHTML='<div class="empty">carregando…</div>';
  try{
    const d=await getJSON('/api/session?id='+encodeURIComponent(id));
    if(cur!==id)return;
    const s=d.session;
    c.innerHTML='<a class="back" href="#/">← conversas</a><div class="head"><div class="lbl"><b>[</b> '+E(s.project)+' <b>]</b></div><h1>'+E(s.title)+'</h1><div class="m">'+E(D(s.start))+' → '+E(D(s.last))+' · '+E(N(s.messages))+' mensagens · '+E(s.id)+'</div></div>'+(d.messages.length?d.messages.map(msg).join(''):'<div class="empty">Sem mensagens.</div>')+(d.truncated?'<div class="empty">Conversa longa: mostrando as primeiras '+E(N(d.messages.length))+' mensagens.</div>':'');
    c.scrollTop=0;
  }catch(e){c.innerHTML='<a class="back" href="#/">← conversas</a><div class="empty">Não consegui abrir esta conversa.</div>';}
}
function route(){
  const m=location.hash.match(/^#\/s\/(.+)$/);
  if(m){document.body.classList.add('reading');openS(decodeURIComponent(m[1]));}
  else{document.body.classList.remove('reading');cur=null;markOn();$('#conv').innerHTML='<div class="empty">Escolha uma conversa.</div>';}
}
$('#q').addEventListener('input',()=>{clearTimeout(tm);tm=setTimeout(loadList,280);});
window.addEventListener('hashchange',route);
loadList();route();
"""


def host_allowed(host):
    if not host:
        return False
    h = host.strip().lower()
    if h.startswith("["):
        return False
    name, _, port = h.partition(":")
    if port and not port.isdigit():
        return False
    return name in ("localhost", "127.0.0.1")


def make_handler(mode, index):
    if mode == "analytics":
        page = html_page("Analytics · Central Trip Angle", "ANALYTICS", ANALYTICS_CSS, ANALYTICS_BODY, ANALYTICS_JS)
    else:
        page = html_page("Chats · Central Trip Angle", "CHATS", CHATS_CSS, CHATS_BODY, CHATS_JS, "app")
    page_bytes = page.encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        server_version = "tahub/" + VERSION
        sys_version = ""

        def log_message(self, fmt, *args):  # silencioso
            pass

        def _send(self, code, body, ctype):
            if isinstance(body, str):
                body = body.encode("utf-8")
            try:
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("X-Frame-Options", "DENY")
                self.send_header("Referrer-Policy", "no-referrer")
                if ctype.startswith("text/html"):
                    self.send_header("Content-Security-Policy", CSP)
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def _json(self, obj, code=200):
            self._send(code, json.dumps(obj, ensure_ascii=False, separators=(",", ":")),
                       "application/json; charset=utf-8")

        def do_GET(self):
            if not host_allowed(self.headers.get("Host")):
                return self._send(403, "Host não permitido.\n", "text/plain; charset=utf-8")
            u = urllib.parse.urlsplit(self.path)
            q = urllib.parse.parse_qs(u.query)
            p = u.path
            try:
                if p in ("/", "/index.html"):
                    return self._send(200, page_bytes, "text/html; charset=utf-8")
                if p in ("/favicon.svg", "/favicon.ico"):
                    return self._send(200, FAVICON, "image/svg+xml")
                if mode == "analytics" and p == "/api/stats":
                    return self._json(build_stats(index))
                if mode == "chats" and p == "/api/sessions":
                    return self._json(api_sessions(index, q))
                if mode == "chats" and p == "/api/session":
                    obj, code = api_session(index, q)
                    return self._json(obj, code)
                if p.startswith("/api/"):
                    return self._json({"ok": False, "error": "rota não encontrada"}, 404)
                return self._send(404, "Não encontrado.\n", "text/plain; charset=utf-8")
            except Exception as e:  # noqa: BLE001
                return self._json({"ok": False, "error": "falha interna: %s" % e}, 500)

        do_HEAD = do_GET

        def _not_allowed(self):
            if not host_allowed(self.headers.get("Host")):
                return self._send(403, "Host não permitido.\n", "text/plain; charset=utf-8")
            return self._send(405, "Método não permitido.\n", "text/plain; charset=utf-8")

        do_POST = do_PUT = do_DELETE = do_PATCH = _not_allowed

    return Handler


def serve(mode, args):
    port = args.port if args.port is not None else (ANALYTICS_PORT if mode == "analytics" else CHATS_PORT)
    if not 0 <= port <= 65535:
        raise HubError("porta inválida: %s" % port, code=EXIT_USAGE)
    cdir = claude_user_dir()
    index = SessionIndex(cdir)
    try:
        httpd = ThreadingHTTPServer(("127.0.0.1", port), make_handler(mode, index))
    except OSError as e:
        if e.errno in (errno.EADDRINUSE, 48, 98):
            raise HubError("a porta %d já está em uso." % port, hint="Use --port com outra porta, por exemplo --port %d." % (port + 1))
        raise HubError("não consegui abrir o servidor na porta %d: %s" % (port, e))
    httpd.daemon_threads = True
    url = "http://127.0.0.1:%d/" % httpd.server_address[1]
    print(banner(mode))
    print()
    print(tag(mode.upper()) + "  " + bold(url))
    print(dim("  lendo %s" % (index.root)))
    if not index.root.is_dir():
        warn("a pasta %s não existe ainda: o painel vai aparecer vazio." % index.root)
    print(dim("  só escuta em 127.0.0.1 · Ctrl+C para encerrar"))
    sys.stdout.flush()
    threading.Thread(target=index.snapshot, daemon=True).start()
    if not args.no_open:
        threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        print()
        print("Servidor encerrado.")
    finally:
        httpd.server_close()
    return EXIT_OK


# ================================================================ linha de comando

def help_text():
    site = DEFAULT_SOURCE.strip() if DEFAULT_SOURCE.strip() and DEFAULT_SOURCE != _MARKER else "https://SEU-SITE"
    return """%s  %s

Uso
  python3 tahub.py                              modo interativo (menus)
  python3 tahub.py --skill copy/copywriting
  python3 <(curl -fsSL %s/tahub.py) --agent conteudo/content-marketer

Instalar  (vários itens separados por vírgula; use categoria/nome ou só o nome)
  --prompts  --skill  --agent  --framework  --command  --mcp  --hook  --setting
  --plugin  --template  --repo
  --prompts vira comando /nome · --framework vira a skill framework-nome
  --plugin aceita plugin (categoria/nome) ou pacote de categoria (ta-copy)

Opções de instalação
  -d, --directory PASTA   pasta do projeto (padrão: pasta atual)
  --scope ESCOPO          local | project | user  (settings, hooks e plugins; padrão local)
  -y, --yes               instala sem perguntar
  --dry-run               só mostra o plano, não grava nada
  --force                 sobrescreve arquivos que já existem
  --prompt "TEXTO"        depois de instalar, abre o claude com esse texto

Explorar
  --search "PALAVRAS"     busca no catálogo (top 10)
  --list [TIPO]           lista os itens; filtre com --category CATEGORIA
  --info TIPO/CAT/NOME    detalhes de um item (ex.: skills/copy/copywriting)
  --show TIPO/CAT/NOME    imprime o texto (prompt sem frontmatter) para copiar e colar
  --var NOME=VALOR        com --show: troca {{NOME}} pelo valor (repita para cada variável)

Ferramentas
  --health-check          diagnóstico do ambiente (alias --health)
  --analytics             painel de uso em http://127.0.0.1:%d
  --chats                 navegador de conversas em http://127.0.0.1:%d
  --port N  --no-open     porta do painel · não abrir o navegador

Outros
  --source URL|PASTA      origem do catálogo (ou variável TAHUB_SOURCE)
  --version  -h, --help
""" % (bold("CENTRAL TRIP ANGLE"), dim("instalador para o Claude Code · tahub " + VERSION), site,
       ANALYTICS_PORT, CHATS_PORT)


ARG_ERRORS = [
    ("unrecognized arguments: ", "opção não reconhecida: "),
    ("expected one argument", "falta o valor"),
    ("invalid choice: ", "valor inválido: "),
    ("(choose from ", "(use "),
    ("invalid int value: ", "número inválido: "),
    ("ignored explicit argument ", "valor não esperado "),
    ("ambiguous option: ", "opção ambígua: "),
    ("could match", "pode ser"),
    ("argument ", "opção "),
]


class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        for en, pt in ARG_ERRORS:
            message = message.replace(en, pt)
        raise HubError(message, hint="Use --help para ver as opções.", code=EXIT_USAGE)


def build_parser():
    p = ArgParser(prog="tahub", add_help=False, allow_abbrev=False)
    for _tid, flag, _l, _s in TYPES:
        p.add_argument("--" + flag, action="append", metavar="ITENS")
    p.add_argument("-d", "--directory")
    p.add_argument("-y", "--yes", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--scope", choices=SCOPES)
    p.add_argument("--force", action="store_true")
    p.add_argument("--search")
    p.add_argument("--list", nargs="?", const="")
    p.add_argument("--category")
    p.add_argument("--info")
    p.add_argument("--show")
    p.add_argument("--var", action="append", metavar="NOME=VALOR")
    p.add_argument("--prompt")
    p.add_argument("--health-check", "--health", dest="health", action="store_true")
    p.add_argument("--analytics", action="store_true")
    p.add_argument("--chats", action="store_true")
    p.add_argument("--port", type=int)
    p.add_argument("--no-open", action="store_true")
    p.add_argument("--source")
    p.add_argument("--version", action="store_true")
    p.add_argument("-h", "--help", action="store_true")
    return p


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        args = build_parser().parse_args(argv)
        if args.help:
            print(help_text())
            return EXIT_OK
        if args.version:
            print("tahub %s · Central Trip Angle · Python %s" % (VERSION, platform.python_version()))
            return EXIT_OK
        if args.analytics and args.chats:
            raise HubError("use --analytics ou --chats, um de cada vez.", code=EXIT_USAGE)
        if args.var and not args.show:
            raise HubError("--var só vale junto com --show.", hint='Exemplo: --show prompts/copy/extrair-vsl --var nicho="emagrecimento"',
                           code=EXIT_USAGE)
        if args.show:
            return cmd_show(args)
        if args.health:
            return cmd_health(args)
        if args.analytics:
            return serve("analytics", args)
        if args.chats:
            return serve("chats", args)
        if args.search is not None:
            return cmd_search(args)
        if args.list is not None:
            return cmd_list(args)
        if args.info:
            return cmd_info(args)
        requests = collect(args)
        tty = _isatty(sys.stdin)
        if not requests and not args.prompt:
            if not tty:
                print(help_text())
                return EXIT_OK
            return cmd_interactive(args)
        if not tty:
            args.yes = True
        if not requests:
            return run_prompt(args.prompt, project_dir(args.directory))
        return cmd_install(args, requests)
    except HubError as e:
        print_error(e.msg, e.hint)
        return e.code
    except KeyboardInterrupt:
        print()
        print("Cancelado.")
        return EXIT_CANCEL


if __name__ == "__main__":
    sys.exit(main())
