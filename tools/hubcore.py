"""Núcleo da Central Trip Angle: tipos, leitura de componentes e montagem do catálogo.

Usado por build.py, admin.py e importers.py. Só usa a biblioteca padrão do Python 3.9+.
"""
import datetime
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPONENTS = ROOT / "components"
DIST = ROOT / "dist"
SITE = ROOT / "site"
BUNDLES = ROOT / "bundles"

# id, rótulo, flag do CLI, formato ("dir" = pasta, ou extensão do arquivo único)
TYPES = [
    {"id": "prompts", "label": "Prompts", "singular": "Prompt", "flag": "--prompts", "kind": ".md"},
    {"id": "skills", "label": "Skills", "singular": "Skill", "flag": "--skill", "kind": "dir", "main": "SKILL.md"},
    {"id": "agents", "label": "Agentes", "singular": "Agente", "flag": "--agent", "kind": ".md"},
    {"id": "frameworks", "label": "Frameworks", "singular": "Framework", "flag": "--framework", "kind": ".md"},
    {"id": "commands", "label": "Comandos", "singular": "Comando", "flag": "--command", "kind": ".md"},
    {"id": "mcps", "label": "MCPs", "singular": "MCP", "flag": "--mcp", "kind": ".json"},
    {"id": "hooks", "label": "Hooks", "singular": "Hook", "flag": "--hook", "kind": ".json"},
    {"id": "settings", "label": "Settings", "singular": "Setting", "flag": "--setting", "kind": ".json"},
    {"id": "plugins", "label": "Plugins", "singular": "Plugin", "flag": "--plugin", "kind": "dir", "main": ".claude-plugin/plugin.json"},
    {"id": "templates", "label": "Templates", "singular": "Template", "flag": "--template", "kind": "dir", "main": "CLAUDE.md"},
    {"id": "repos", "label": "Repositórios", "singular": "Repositório", "flag": "--repo", "kind": ".json"},
    {"id": "sites", "label": "Ferramentas & Sites", "singular": "Ferramenta", "flag": "", "kind": ".json"},
]
STATUS = ("rascunho", "testado", "controle")
TYPE_BY_ID = {t["id"]: t for t in TYPES}
SIDE = ".hub.json"  # metadados extras da Central (nunca instalados)
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
IGNORED = {".DS_Store", "__pycache__", ".git", "node_modules", ".venv"}


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def load_config():
    cfg = load_json(ROOT / "hub.config.json", {}) or {}
    env_url = os.environ.get("TAHUB_SITE_URL")
    if env_url:
        cfg["siteUrl"] = env_url
    env_repo = os.environ.get("TAHUB_GITHUB_REPO")
    if env_repo:
        cfg["githubRepo"] = env_repo
    cfg["siteUrl"] = (cfg.get("siteUrl") or "").rstrip("/")
    return cfg


def load_categories():
    cats = load_json(ROOT / "categories.json", []) or []
    for i, c in enumerate(cats):
        c.setdefault("order", i)
    return cats


def slugify(text):
    text = (text or "").strip().lower()
    table = str.maketrans("áàâãäéèêëíìîïóòôõöúùûüçñ", "aaaaaeeeeiiiiooooouuuucn")
    text = text.translate(table)
    text = re.sub(r"[^a-z0-9._-]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-.")[:80] or "item"


ACENTOS = {
    "producao": "produção", "trafego": "tráfego", "analise": "análise", "conteudo": "conteúdo",
    "estrategia": "estratégia", "anuncio": "anúncio", "anuncios": "anúncios", "lancamento": "lançamento",
    "operacao": "operação", "pagina": "página", "paginas": "páginas", "video": "vídeo", "videos": "vídeos",
    "configuracao": "configuração", "automacao": "automação", "pos": "pós", "midia": "mídia", "publico": "público",
}


def humanize(slug):
    words = [ACENTOS.get(w.lower(), w) for w in re.split(r"[-_]+", slug)]
    small = {"de", "da", "do", "e", "com", "para", "em", "a", "o"}
    out = []
    for i, w in enumerate(words):
        if w.lower() in {"ai", "ia", "seo", "cro", "mcp", "ui", "ux", "api", "pdf", "crm", "trm", "dr", "vsl", "ga4", "utm"}:
            out.append(w.upper())
        elif i and w in small:
            out.append(w)
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


# ---------------------------------------------------------------- frontmatter

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
            # mapa ou lista aninhada
            sub, lst = {}, []
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].startswith("\t")):
                s = lines[i].strip()
                if s.startswith("- "):
                    lst.append(_scalar(s[2:]))
                else:
                    sm = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", s)
                    if sm:
                        sub[sm.group(1)] = _scalar(sm.group(2))
                i += 1
            data[key] = lst if lst else sub
        else:
            data[key] = _scalar(val)
    return data, body


def _scalar(val):
    val = val.strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
        return val[1:-1]
    if val.startswith("[") and val.endswith("]"):
        return [_scalar(x) for x in val[1:-1].split(",") if x.strip()]
    if val.lower() in ("true", "false"):
        return val.lower() == "true"
    return val


def first_paragraph(body, limit=300):
    for block in re.split(r"\n\s*\n", body or ""):
        b = block.strip()
        if b and not b.startswith("#") and not b.startswith("```") and not b.startswith("|"):
            b = re.sub(r"\s+", " ", b)
            return b[:limit]
    return ""


# ---------------------------------------------------------------- scanning

def rel(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def list_files(base):
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED)
        for fn in sorted(filenames):
            if fn in IGNORED or fn == SIDE or fn.endswith(".pyc"):
                continue
            out.append(Path(dirpath) / fn)
    return out


def _date(path):
    try:
        return datetime.date.fromtimestamp(Path(path).stat().st_mtime).isoformat()
    except OSError:
        return datetime.date.today().isoformat()


def _apply_side(item, side):
    if not side:
        return
    for key in ("title", "description", "tags", "author", "license", "version", "source", "scan",
                "featured", "addedAt", "repo", "notes", "status", "testedWith", "testedAt"):
        if side.get(key) not in (None, "", []):
            item[key] = side[key]


def _base_item(type_id, category, name):
    return {
        "id": f"{type_id}/{category}/{name}",
        "type": type_id,
        "category": category,
        "name": name,
        "title": humanize(name),
        "description": "",
        "tags": [],
        "author": None,
        "license": None,
        "version": None,
        "kind": "file",
        "base": "",
        "main": "",
        "files": [],
        "extras": [],
        "partOf": None,
        "children": [],
        "source": None,
        "scan": None,
        "featured": False,
        "addedAt": None,
        "size": 0,
        "bundle": None,
        "status": None,
    }


def _md_item(type_id, category, path, part_of=None):
    name = path.stem
    item = _base_item(type_id, category, name)
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_frontmatter(text)
    item["description"] = str(fm.get("description") or first_paragraph(body))
    if fm.get("name") and isinstance(fm.get("name"), str):
        item["title"] = humanize(fm["name"]) if NAME_RE.match(fm["name"]) else fm["name"]
    item["license"] = fm.get("license") if isinstance(fm.get("license"), str) else None
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    item["version"] = fm.get("version") or meta.get("version") or meta.get("versao")
    item["author"] = fm.get("author") or meta.get("author") or meta.get("autor")
    if type_id == "agents":
        item["model"] = fm.get("model")
        item["tools"] = fm.get("tools")
    if type_id == "commands":
        item["argumentHint"] = fm.get("argument-hint")
    if isinstance(fm.get("status"), str):
        item["status"] = fm["status"]
    if type_id in ("prompts", "frameworks"):
        if isinstance(fm.get("title"), str):
            item["title"] = fm["title"]
        item["tags"] = [str(t) for t in fm.get("tags", [])] if isinstance(fm.get("tags"), list) else []
        item["preview"] = re.sub(r"\s+", " ", body).strip()[:320]
    if type_id == "prompts":
        item["level"] = fm.get("level") if fm.get("level") in ("mestre", "modulo") else "modulo"
        item["stage"] = fm.get("stage") if isinstance(fm.get("stage"), str) else None
        nums = {int(n) for n in re.findall(r"^###\s+Etapa\s+(\d+)", body, re.M)} - {0}
        item["etapas"] = len(nums) or (int(fm["etapas"]) if str(fm.get("etapas", "")).isdigit() else None)
        item["tempo"] = fm.get("tempo") if isinstance(fm.get("tempo"), str) else None
        item["next"] = [str(x) for x in fm.get("next", [])] if isinstance(fm.get("next"), list) else []
        item["lines"] = body.count("\n") + 1
        item["secoes"] = sorted({int(n) for n in re.findall(r"^##\s+(\d)\.", body, re.M)})
        item["variables"] = prompt_variables(fm, body)
        item["tools"] = [str(t) for t in fm.get("tools", [])] if isinstance(fm.get("tools"), list) else []
        item["output"] = fm.get("output") if isinstance(fm.get("output"), str) else None
    if type_id == "frameworks":
        item["when"] = fm.get("when") if isinstance(fm.get("when"), str) else None
        item["origin"] = fm.get("origin") if isinstance(fm.get("origin"), str) else None
    item["base"] = rel(path)
    item["main"] = path.name
    item["files"] = [rel(path)]
    item["size"] = path.stat().st_size
    item["addedAt"] = _date(path)
    item["partOf"] = part_of
    return item


def _skill_item(category, folder, part_of=None, type_id="skills"):
    t = TYPE_BY_ID[type_id]
    name = folder.name
    item = _base_item(type_id, category, name)
    item["kind"] = "dir"
    item["base"] = rel(folder)
    files = list_files(folder)
    item["files"] = [rel(f) for f in files]
    item["size"] = sum(f.stat().st_size for f in files)
    main = folder / t.get("main", "SKILL.md")
    item["main"] = t.get("main", "")
    if type_id == "plugins":
        pj = load_json(main, {}) or {}
        item["description"] = pj.get("description", "")
        item["version"] = pj.get("version")
        author = pj.get("author")
        item["author"] = author.get("name") if isinstance(author, dict) else author
        item["tags"] = pj.get("keywords") or []
        item["pluginName"] = pj.get("name") or name
        readme = folder / "README.md"
        if readme.exists():
            item["main"] = "README.md"
    elif main.exists():
        fm, body = parse_frontmatter(main.read_text(encoding="utf-8", errors="replace"))
        item["description"] = str(fm.get("description") or first_paragraph(body))
        item["license"] = fm.get("license") if isinstance(fm.get("license"), str) else None
        meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
        item["version"] = fm.get("version") or meta.get("version") or meta.get("versao")
        item["author"] = fm.get("author") or meta.get("author") or meta.get("autor")
    else:
        # template sem CLAUDE.md: usa o primeiro .md
        mds = [f for f in files if f.suffix == ".md"]
        if mds:
            item["main"] = mds[0].relative_to(folder).as_posix()
            item["description"] = first_paragraph(parse_frontmatter(mds[0].read_text(encoding="utf-8", errors="replace"))[1])
    item["addedAt"] = _date(main if main.exists() else folder)
    item["partOf"] = part_of
    return item


def _json_item(type_id, category, path):
    name = path.stem
    item = _base_item(type_id, category, name)
    data = load_json(path, {}) or {}
    item["base"] = rel(path)
    item["main"] = path.name
    item["files"] = [rel(path)]
    item["size"] = path.stat().st_size
    item["addedAt"] = _date(path)
    item["description"] = str(data.get("description") or "")
    if type_id == "repos":
        item["title"] = data.get("title") or data.get("name") or humanize(name)
        item["repo"] = {k: data.get(k) for k in ("url", "stars", "language", "license", "updatedAt", "homepage") if data.get(k) is not None}
        if isinstance(data.get("detalhes"), dict):
            item["detalhes"] = data["detalhes"]
        if data.get("subcategoria"):
            item["subcategoria"] = data["subcategoria"]
        if isinstance(data.get("fontes"), list):
            item["fontes"] = [str(x) for x in data["fontes"]][:8]
        item["tags"] = data.get("tags") or []
        item["license"] = data.get("license")
    if type_id == "sites":
        item["title"] = data.get("title") or humanize(name)
        item["site"] = {k: data.get(k) for k in ("url", "pricing", "lang", "verified") if data.get(k) is not None}
        item["tags"] = data.get("tags") or []
    if type_id == "mcps":
        servers = data.get("mcpServers") or {}
        item["servers"] = list(servers.keys())
        needs = set()
        for s in servers.values():
            blob = json.dumps(s)
            needs.update(re.findall(r"<([A-Za-z0-9_ -]{2,40})>", blob))
            needs.update(re.findall(r"\$\{([A-Z0-9_]+)\}", blob))
            needs.update(re.findall(r"\b((?:YOUR|SEU|SUA)_[A-Z0-9_]+)\b", blob))
            needs.update(f"caminho {m}" for m in re.findall(r"(/path/to/[^\"\s]*)", blob))
            for k, v in (s.get("env") or {}).items():
                if isinstance(v, str) and (v.startswith("<") or v.startswith("${") or not v
                                           or re.search(r"your|seu|sua|xxx|\*\*\*", v, re.I)):
                    needs.add(k)
        item["requires"] = sorted(needs)
    if type_id == "hooks":
        item["events"] = sorted((data.get("hooks") or {}).keys())
    # scripts de apoio com o mesmo nome (ex.: notify.json + notify.sh)
    extras = []
    for f in sorted(path.parent.iterdir()):
        if f.is_file() and f.stem == name and f.suffix not in (".json",) and not f.name.endswith(SIDE):
            extras.append(rel(f))
    scripts_dir = path.parent / name
    if scripts_dir.is_dir():
        extras += [rel(f) for f in list_files(scripts_dir)]
    item["extras"] = extras
    return item


def scan_components(warn=None):
    """Lê components/ e devolve a lista de itens do catálogo."""
    warn = warn or (lambda msg: None)
    items = []
    for t in TYPES:
        tdir = COMPONENTS / t["id"]
        if not tdir.is_dir():
            continue
        for cdir in sorted(p for p in tdir.iterdir() if p.is_dir() and p.name not in IGNORED):
            category = cdir.name
            for entry in sorted(cdir.iterdir()):
                if entry.name in IGNORED or entry.name.endswith(SIDE) or entry.name.startswith("."):
                    continue
                try:
                    if t["kind"] == "dir":
                        if not entry.is_dir():
                            continue
                        item = _skill_item(category, entry, type_id=t["id"])
                        side = load_json(entry / SIDE)
                    else:
                        if not entry.is_file() or entry.suffix != t["kind"]:
                            continue
                        item = (_md_item(t["id"], category, entry) if t["kind"] == ".md"
                                else _json_item(t["id"], category, entry))
                        side = load_json(entry.with_name(entry.stem + SIDE))
                    _apply_side(item, side)
                    if not NAME_RE.match(item["name"]):
                        warn(f"nome fora do padrão (use minúsculas e hífens): {item['id']}")
                    items.append(item)
                    if t["id"] == "plugins":
                        items.extend(_plugin_children(item, entry, category))
                except Exception as exc:  # noqa: BLE001
                    warn(f"falha ao ler {rel(entry)}: {exc}")
    # filho de plugin que é cópia de um componente solto (mesmo tipo e nome): aponta para o solto
    soltos = {(it["type"], it["name"]): it["id"] for it in items if not it["partOf"]}
    plugins = {it["id"]: it for it in items if it["type"] == "plugins"}
    final = []
    for it in items:
        alvo = soltos.get((it["type"], it["name"])) if it["partOf"] else None
        if alvo:
            pai = plugins.get(it["partOf"])
            if pai:
                pai["children"] = [alvo if c == it["id"] else c for c in pai["children"]]
            continue
        final.append(it)
    items = final
    # ids únicos
    seen = {}
    for it in items:
        if it["id"] in seen:
            n = 2
            while f"{it['id']}-{n}" in seen:
                n += 1
            warn(f"id repetido {it['id']} → {it['id']}-{n}")
            it["id"] = f"{it['id']}-{n}"
        seen[it["id"]] = it
    return items


def _plugin_children(plugin, folder, category):
    kids = []
    for sk in sorted((folder / "skills").glob("*/SKILL.md")) if (folder / "skills").is_dir() else []:
        kids.append(_skill_item(category, sk.parent, part_of=plugin["id"]))
    for ty in ("agents", "commands"):
        d = folder / ty
        if d.is_dir():
            for md in sorted(d.glob("*.md")):
                kids.append(_md_item(ty, category, md, part_of=plugin["id"]))
    for k in kids:
        k["author"] = k["author"] or plugin.get("author")
        k["license"] = k["license"] or plugin.get("license")
        k["source"] = k["source"] or plugin.get("source")
        k["tags"] = k["tags"] or plugin.get("tags", [])[:6]
    plugin["children"] = [k["id"] for k in kids]
    return kids


def item_install_path(item):
    """Onde o componente fica dentro de components/ (para o admin apagar/editar)."""
    return ROOT / item["base"]


# ---------------------------------------------------------------- prompts e frameworks

VAR_RE = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*\}\}")


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
        lines.append("argument-hint: " + json.dumps(" ".join(f"[{v['name']}]" for v in variables), ensure_ascii=False))
    lines += ["---", "", f"<!-- Central Trip Angle · prompt {item.get('category')}/{item.get('name')} -->",
              "Dados enviados pelo usuário: $ARGUMENTS", ""]
    if variables and any(v.get("required") is not None for v in variables):
        obr = "; ".join(f"{v['name']} ({v['label']})" for v in variables if v.get("required"))
        opc = "; ".join(f"{v['name']} ({v['label']}" + (f"; padrão: {v['default']}" if v.get("default") else "") + ")"
                        for v in variables if not v.get("required"))
        partes = [f"Obrigatórios: {obr}." if obr else "", f"Opcionais: {opc}." if opc else ""]
        lines += ["Antes de começar, confira os insumos. " + " ".join(x for x in partes if x)
                  + " Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.", ""]
    elif variables:
        need = "; ".join(f"{v['name']} ({v['label']})" for v in variables)
        lines += [f"Antes de começar, confira se você tem: {need}. Se faltar algum, pergunte ao usuário.", ""]
    lines.append(VAR_RE.sub(lambda m: f"[{m.group(1)}]", body.strip()))
    return "\n".join(lines) + "\n"


def framework_skill_name(name):
    return name if name.startswith("framework-") else f"framework-{name}"


def framework_to_skill(text, item):
    """Converte um framework da Central em skill (.claude/skills/framework-<nome>/SKILL.md)."""
    fm, body = parse_frontmatter(text)
    title = str(fm.get("title") or item.get("title") or item.get("name"))
    desc = str(fm.get("description") or item.get("description") or "").strip()
    when = str(fm.get("when") or "").strip()
    full = f"Framework {title}: {desc} {when}".replace("\n", " ").strip()
    return ("---\n" + f"name: {framework_skill_name(item['name'])}\n" + "description: "
            + json.dumps(full[:1000], ensure_ascii=False) + "\n---\n\n" + f"# {title}\n\n" + body.strip() + "\n")
