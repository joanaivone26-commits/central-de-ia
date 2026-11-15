#!/usr/bin/env python3
"""Importadores da Central Trip Angle: repositórios do GitHub, pastas locais e o catálogo do aitmpl.com.

Uso:
  python3 tools/importers.py scan <url-github-ou-pasta> [--json]
  python3 tools/importers.py apply <origem> (--all | --pick caminho1,caminho2) [--category <id>] [--overwrite]
  python3 tools/importers.py aitmpl search <termos> [--type skills] [--limit 30] [--json]
  python3 tools/importers.py aitmpl import <id> [<id>...] [--category <id>] [--overwrite]
  python3 tools/importers.py repo <url-github> --category <id> [--name x] [--overwrite]

Depois de gravar, o catálogo é reconstruído (use --no-build para pular).
Variável opcional: GITHUB_TOKEN (aumenta o limite da API do GitHub de 60 para 5000 requisições/hora).
Só usa a biblioteca padrão do Python 3.9+.
"""
import argparse
import concurrent.futures
import datetime
import json
import os
import re
import shutil
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hubcore as hc  # noqa: E402

UA = "central-trip-angle-importer/1.0"
CACHE = hc.ROOT / ".cache"
TRASH = hc.ROOT / ".trash"
GH_TTL = 600            # repo/branch em cache por 10 min (scan e apply usam o mesmo commit)
AITMPL_TTL = 86400      # catálogo do aitmpl.com em cache por 1 dia
AITMPL_CATALOG_URL = "https://www.aitmpl.com/api/v1/catalog.json"
AITMPL_CONTENT_URL = "https://www.aitmpl.com/component-content/{id}.json"
AITMPL_REPO = "davila7/claude-code-templates"
AITMPL_REPO_LICENSE = "MIT"
AITMPL_BASE = "cli-tool/components"
AITMPL_TYPES = ("skills", "agents", "commands", "mcps", "hooks", "settings")
MAX_FILE = 20 * 1024 * 1024
MAX_JSON_PROBE = 300
MAX_DESCRIBE = 500
SCRIPT_EXTS = (".sh", ".bash", ".zsh", ".py", ".js", ".mjs", ".cjs", ".ts", ".ps1", ".rb")
IGNORED_DIRS = {".git", "node_modules", ".venv", "__pycache__"}
SKIP_JSON = {
    "package.json", "package-lock.json", "tsconfig.json", "jsconfig.json", "composer.json", "renovate.json",
    ".eslintrc.json", ".prettierrc.json", "plugin.json", "marketplace.json", "manifest.json", "deno.json",
    "vercel.json", "app.json", "firebase.json", "lerna.json", "nx.json", "turbo.json", "biome.json",
    "components.json", "angular.json", "pyrightconfig.json", "cspell.json", "evals.json", ".hub.json",
}
NOT_COMPONENT_MD = {"readme", "contributing", "changelog", "license", "index", "code_of_conduct", "security"}
HOOK_EVENTS = {
    "PreToolUse", "PostToolUse", "PostToolUseFailure", "PostToolBatch", "Notification", "UserPromptSubmit",
    "UserPromptExpansion", "Stop", "StopFailure", "SubagentStart", "SubagentStop", "PreCompact", "PostCompact",
    "SessionStart", "SessionEnd", "PermissionRequest", "PermissionDenied", "Setup", "TeammateIdle",
    "TaskCreated", "TaskCompleted", "ConfigChange", "CwdChanged", "FileChanged", "WorktreeCreate",
    "WorktreeRemove", "InstructionsLoaded", "Elicitation", "ElicitationResult",
}
KIND_TO_TYPE = {"skill": "skills", "plugin": "plugins", "agent": "agents", "command": "commands",
                "mcp": "mcps", "hook": "hooks"}
TYPE_TO_KIND = {v: k for k, v in KIND_TO_TYPE.items()}

_lock = threading.RLock()


class ImportFailure(Exception):
    """Erro com mensagem para o usuário (pt-BR) e status HTTP sugerido."""

    def __init__(self, msg, status=400):
        super().__init__(msg)
        self.status = status


class NotFound(ImportFailure):
    def __init__(self, msg):
        super().__init__(msg, 404)


def today():
    return datetime.date.today().isoformat()


def pjoin(a, b):
    return b if a in ("", ".") else f"{a}/{b}"


def pdir(p):
    return p.rsplit("/", 1)[0] if "/" in p else "."


def pbase(p):
    return p.rsplit("/", 1)[-1]


def pstem(p):
    b = pbase(p)
    return b.rsplit(".", 1)[0] if "." in b else b


def under(path, folder):
    return folder in ("", ".") or path == folder or path.startswith(folder + "/")


def safe_rel(p):
    """Normaliza um caminho relativo e recusa '..' e caminhos absolutos."""
    raw = str(p or "").replace("\\", "/")
    parts = [x for x in raw.split("/") if x not in ("", ".")]
    if raw.startswith("/") or not parts or any(x == ".." for x in parts) or re.match(r"^[A-Za-z]:", raw):
        raise ImportFailure(f"Caminho inválido: {p}")
    return "/".join(parts)


# ---------------------------------------------------------------- HTTP

def _rate_message(host, headers):
    reset = headers.get("X-RateLimit-Reset") if headers else None
    retry = headers.get("Retry-After") if headers else None
    when = ""
    if reset and reset.isdigit():
        when = " Tente de novo às " + datetime.datetime.fromtimestamp(int(reset)).strftime("%H:%M") + "."
    elif retry and retry.isdigit():
        when = f" Tente de novo em {int(retry)} s."
    if host == "api.github.com":
        tip = "" if os.environ.get("GITHUB_TOKEN") else " Sem token o limite é 60 por hora: defina GITHUB_TOKEN."
        return "Limite de requisições da API do GitHub atingido." + when + tip
    return f"{host} limitou as requisições (429).{when or ' Tente de novo em alguns minutos.'}"


def http_get(url, headers=None, timeout=30, retries=2):
    """GET que devolve bytes. Erros viram ImportFailure com mensagem clara."""
    hdrs = {"User-Agent": UA}
    if headers:
        hdrs.update(headers)
    host = urllib.parse.urlparse(url).hostname or ""
    token = os.environ.get("GITHUB_TOKEN")
    if token and host == "api.github.com":
        hdrs["Authorization"] = "Bearer " + token
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            try:
                body = exc.read(4000).decode("utf-8", "replace").lower()
            except Exception:  # noqa: BLE001
                body = ""
            if exc.code == 404:
                raise NotFound(f"Não encontrado: {url}")
            limited = (exc.code == 429 or (exc.headers or {}).get("X-RateLimit-Remaining") == "0"
                       or "rate limit" in body)
            if exc.code in (403, 429) and limited:
                raise ImportFailure(_rate_message(host, exc.headers), 429)
            if exc.code == 401:
                raise ImportFailure("GITHUB_TOKEN inválido ou expirado (401).", 401)
            if exc.code == 403:
                raise ImportFailure(f"Acesso negado por {host} (403): {url}", 403)
            if exc.code >= 500 and attempt < retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise ImportFailure(f"{host} respondeu {exc.code} para {url}", exc.code if exc.code < 500 else 502)
        except (urllib.error.URLError, socket.timeout, ConnectionError) as exc:
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            reason = getattr(exc, "reason", exc)
            raise ImportFailure(f"Sem conexão com {host}: {reason}", 502)
    raise ImportFailure(f"Falha ao baixar {url}", 502)


def http_json(url, **kw):
    data = http_get(url, **kw)
    try:
        return json.loads(data.decode("utf-8"))
    except ValueError:
        raise ImportFailure(f"Resposta inválida (não é JSON) de {url}", 502)


def gh_api(path, accept="application/vnd.github+json"):
    return http_get("https://api.github.com" + path,
                    headers={"Accept": accept, "X-GitHub-Api-Version": "2022-11-28"})


def raw_url(repo, commit, path):
    return f"https://raw.githubusercontent.com/{repo}/{commit}/{urllib.parse.quote(path, safe='/')}"


# ---------------------------------------------------------------- categorias

# (categoria, palavras). "x*" casa como prefixo (copy* → copywriting); sem "*" casa a palavra inteira (com plural).
CATEGORY_RULES = [
    ("copy", ["copy", "copywrit*", "copys", "headline*", "vsl", "sales letter", "carta de vendas", "persuas*", "hook writing"]),
    ("trafego", ["ads", "meta ads", "facebook ads", "google ads", "tiktok ads", "linkedin ads", "campaign*",
                 "campanha*", "ppc", "paid media", "paid social", "trafego", "tráfego", "adwords", "ad account"]),
    ("seo", ["seo", "serp", "keyword research", "search engine", "sitemap", "aeo", "schema markup"]),
    ("email-whatsapp", ["email*", "e-mail*", "whatsapp", "crm", "mailchimp", "klaviyo", "hubspot", "sms",
                        "drip"]),
    ("analytics", ["analytic*", "tracking", "pixel", "utm", "ga4", "tag manager", "attribution", "mixpanel",
                   "posthog", "conversions api", "capi"]),
    ("criativos", ["video*", "vídeo*", "image", "imagem", "thumbnail*", "creative*", "criativo*", "youtube",
                   "remotion", "ffmpeg", "midjourney", "storyboard*", "b-roll", "gif", "animated", "animation"]),
    ("funil", ["landing*", "funnel*", "funil*", "checkout*", "quiz*", "advertorial*", "sales page",
               "página de vendas", "pre-lander", "signup"]),
    ("cro", ["cro", "conversion rate", "a/b", "ab test*", "split test*", "onboarding", "paywall*"]),
    ("conteudo", ["content", "conteúdo", "social media", "linkedin", "instagram", "twitter", "tweet", "blog*",
                  "post", "editorial", "newsletter*", "publisher"]),
    ("documentos", ["pdf", "docx", "xlsx", "pptx", "word document", "spreadsheet*", "planilha*", "powerpoint",
                    "excel"]),
    ("pesquisa", ["research*", "pesquisa*", "competitor*", "concorrente*", "market research", "espionagem",
                  "trend*"]),
    ("vendas", ["sales", "vendas", "churn", "retention", "referral*", "upsell*", "customer success"]),
    ("estrategia", ["pricing", "offer", "oferta*", "positioning", "posicionamento", "strategy", "estratégia",
                    "go-to-market", "product marketing"]),
    ("compliance", ["compliance", "legal", "lgpd", "gdpr", "privacy policy", "terms of service", "jurídico",
                    "contract*", "contrato*"]),
    ("design", ["design", "ui", "ux", "figma", "brand*", "logo", "identidade visual"]),
    ("produto", ["ebook*", "course*", "curso*", "membership", "área de membros"]),
    ("automacao", ["scrap*", "browser*", "playwright", "puppeteer", "selenium", "notion", "api", "apis",
                   "webhook*", "zapier", "n8n", "integration*", "integração", "automat*", "automação",
                   "google drive", "slack", "airtable", "crawl*"]),
    ("dev", ["react", "frontend", "front-end", "backend", "back-end", "code", "código", "typescript",
             "javascript", "python", "git", "github", "deploy*", "database*", "sql", "docker", "debug*",
             "refactor*", "nextjs", "next.js", "programming"]),
    ("produtividade", ["statusline", "status line", "notification*", "notificação", "productivity",
                       "produtividade", "settings", "permission*", "context window"]),
    ("ia", ["skill*", "prompt*", "agent*", "agente*", "llm*", "gpt", "ai", "ia", "machine learning", "rag"]),
]
_RULES = []
for _cat, _words in CATEGORY_RULES:
    pats = []
    for w in _words:
        if w.endswith("*"):
            pats.append(re.compile(r"(?<![a-z0-9])" + re.escape(w[:-1])))
        else:
            pats.append(re.compile(r"(?<![a-z0-9])" + re.escape(w) + r"(?:s|es)?(?![a-z0-9])"))
    _RULES.append((_cat, pats))

# categorias do aitmpl.com que dão uma boa pista da categoria da Central
AITMPL_HINTS = {
    "document-processing": "documentos", "statusline": "produtividade", "monitoring": "produtividade",
    "automation": "automacao", "workflow-automation": "automacao", "web-data": "automacao",
    "browser_automation": "automacao", "git": "dev", "development": "dev", "web-development": "dev",
    "development-tools": "dev", "database": "dev", "devops-infrastructure": "dev", "testing": "dev",
    "quality-gates": "dev", "security": "dev", "creative-design": "design", "video": "criativos",
    "media": "criativos", "analytics": "analytics", "ai-research": "ia", "ai-specialists": "ia",
    "productivity": "produtividade", "telemetry": "analytics",
}
TYPE_DEFAULT = {"mcps": "automacao", "hooks": "produtividade", "settings": "produtividade", "repos": "dev"}
TYPE_PRIOR = {"mcps": ("automacao", 1.0), "hooks": ("produtividade", 1.5), "settings": ("produtividade", 1.5)}


def _norm(text):
    text = (text or "").lower()
    text = re.sub(r"claude[ -]code", " ", text)
    return re.sub(r"[-_/]+", " ", text)


def suggest_category(type_id, name, description="", hint=None):
    """Sugere a categoria da Central por palavras-chave no nome e na descrição."""
    name_t, desc_t = _norm(name), _norm(description)
    scores = {}
    for cat, pats in _RULES:
        weight_desc = 0.5 if cat == "ia" else 1.0
        s = 0.0
        for pat in pats:
            if pat.search(name_t):
                s += 3
            elif pat.search(desc_t):
                s += weight_desc
        if s:
            scores[cat] = s
    if hint and AITMPL_HINTS.get(hint):
        c = AITMPL_HINTS[hint]
        scores[c] = scores.get(c, 0) + 2
    if type_id in TYPE_PRIOR:
        c, w = TYPE_PRIOR[type_id]
        scores[c] = scores.get(c, 0) + w
    known = set(category_ids())
    order = [c for c, _ in CATEGORY_RULES]
    ranked = sorted((c for c in scores if c in known), key=lambda c: (-scores[c], order.index(c)))
    if ranked:
        return ranked[0]
    return TYPE_DEFAULT.get(type_id, "ia")


_cats_mem = {"mtime": None, "ids": []}


def category_ids():
    path = hc.ROOT / "categories.json"
    try:
        mtime = path.stat().st_mtime
    except OSError:
        mtime = None
    if mtime is None or _cats_mem["mtime"] != mtime:
        _cats_mem["ids"] = [c["id"] for c in hc.load_categories()]
        _cats_mem["mtime"] = mtime
    return list(_cats_mem["ids"])


def ensure_category(cat):
    cat = (cat or "").strip()
    if not cat:
        raise ImportFailure("Informe a categoria.")
    ids = category_ids()
    if cat not in ids:
        raise ImportFailure(f"Categoria desconhecida: {cat}. Use uma de: {', '.join(ids)}.")
    return cat


def guess_license(text):
    head = (text or "")[:600].lower()
    for key, spdx in (("mit license", "MIT"), ("apache license", "Apache-2.0"), ("gnu general public license", "GPL"),
                      ("bsd 3-clause", "BSD-3-Clause"), ("bsd 2-clause", "BSD-2-Clause"),
                      ("mozilla public license", "MPL-2.0"), ("isc license", "ISC"), ("unlicense", "Unlicense"),
                      ("creative commons", "CC")):
        if key in head:
            return spdx
    return None


# ---------------------------------------------------------------- gravação em components/

def type_ext(type_id):
    kind = hc.TYPE_BY_ID[type_id]["kind"]
    return None if kind == "dir" else kind


def validate_ids(type_id, category, name):
    if type_id not in hc.TYPE_BY_ID:
        raise ImportFailure(f"Tipo inválido: {type_id}. Use um de: {', '.join(t['id'] for t in hc.TYPES)}.")
    if not category or not hc.NAME_RE.match(category):
        raise ImportFailure(f"Categoria inválida: {category}")
    if not name or not hc.NAME_RE.match(name) or ".." in name:
        raise ImportFailure(f"Nome inválido: {name}. Use minúsculas, números e hífens (sugestão: {hc.slugify(name)}).")


def component_main(type_id, category, name):
    """Pasta (dir) ou arquivo principal (file) do componente em components/."""
    ext = type_ext(type_id)
    base = hc.COMPONENTS / type_id / category
    return base / name if ext is None else base / (name + ext)


def component_side(type_id, category, name):
    main = component_main(type_id, category, name)
    return main / hc.SIDE if type_ext(type_id) is None else main.parent / (name + hc.SIDE)


def component_paths(type_id, category, name):
    """Tudo que pertence ao componente (para apagar ou substituir)."""
    main = component_main(type_id, category, name)
    if type_ext(type_id) is None:
        return [main] if main.exists() else []
    out = [p for p in (main, component_side(type_id, category, name)) if p.exists()]
    if type_ext(type_id) == ".json" and main.parent.is_dir():
        for f in sorted(main.parent.iterdir()):
            if f.is_file() and f.stem == name and f.suffix != ".json" and not f.name.endswith(hc.SIDE):
                out.append(f)
        folder = main.parent / name
        if folder.is_dir():
            out.append(folder)
    return out


def find_existing(type_id, name):
    """ids de componentes do mesmo tipo e nome (em qualquer categoria)."""
    tdir = hc.COMPONENTS / type_id
    if not tdir.is_dir():
        return []
    ext = type_ext(type_id)
    out = []
    for cdir in sorted(p for p in tdir.iterdir() if p.is_dir()):
        target = cdir / name if ext is None else cdir / (name + ext)
        if target.exists():
            out.append(f"{type_id}/{cdir.name}/{name}")
    return out


def move_to_trash(paths, stamp=None):
    """Move caminhos de dentro da raiz para .trash/<AAAAMMDD-HHMMSS>/<caminho original>."""
    stamp = stamp or datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    dest_root = TRASH / stamp
    for p in paths:
        p = Path(p)
        if not p.exists():
            continue
        relp = p.resolve().relative_to(hc.ROOT.resolve())
        dest = dest_root / relp
        n = 2
        while dest.exists():
            dest = dest_root / relp.parent / f"{relp.name}.{n}"
            n += 1
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(p), str(dest))
    return dest_root.relative_to(hc.ROOT).as_posix()


def _clean_side(side):
    return {k: v for k, v in (side or {}).items() if v not in (None, "", [], {})}


def write_component(type_id, category, name, main=None, files=None, extras=None, side=None,
                    overwrite=False, mode="replace", executable=()):
    """Grava um componente.

    main: bytes do arquivo principal (SKILL.md, .md, .json; para plugins o plugin.json).
    files: {caminho relativo: bytes} para tipos em pasta (inclui o principal se main=None).
    extras: {caminho relativo à pasta da categoria: bytes} para tipos em arquivo (scripts de apoio).
    side: dados do .hub.json. mode "replace" manda o antigo para a lixeira; "update" edita no lugar
    (mantém arquivos de apoio que não vieram) e mescla o .hub.json.
    """
    validate_ids(type_id, category, name)
    ext = type_ext(type_id)
    target = component_main(type_id, category, name)
    side_path = component_side(type_id, category, name)
    exists = target.exists()
    if exists and not overwrite:
        raise ImportFailure(f"Já existe: {type_id}/{category}/{name}. Use sobrescrever (--overwrite) para substituir.", 409)
    trash = None
    old_side = hc.load_json(side_path, {}) if exists else {}
    if exists and mode == "replace":
        trash = move_to_trash(component_paths(type_id, category, name))
    written = []
    if ext is None:
        target.mkdir(parents=True, exist_ok=True)
        payload = dict(files or {})
        if main is not None:
            payload[hc.TYPE_BY_ID[type_id].get("main", "SKILL.md")] = main
        for relp, data in payload.items():
            relp = safe_rel(relp)
            if pbase(relp) == hc.SIDE:
                continue
            dest = target / relp
            dest.parent.mkdir(parents=True, exist_ok=True)
            data = data if isinstance(data, bytes) else str(data).encode("utf-8")
            dest.write_bytes(data)
            if relp in executable or data[:2] == b"#!":
                dest.chmod(0o755)
            written.append(relp)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        if main is not None:
            target.write_bytes(main if isinstance(main, bytes) else str(main).encode("utf-8"))
            written.append(target.name)
        elif not target.exists():
            raise ImportFailure("Conteúdo vazio.")
        for relp, data in (extras or {}).items():
            relp = safe_rel(relp)
            dest = target.parent / relp
            dest.parent.mkdir(parents=True, exist_ok=True)
            data = data if isinstance(data, bytes) else str(data).encode("utf-8")
            dest.write_bytes(data)
            if relp in executable or data[:2] == b"#!" or dest.suffix in (".sh", ".bash", ".zsh"):
                dest.chmod(0o755)
            written.append(relp)
    if side is not None or (mode == "update" and old_side):
        merged = dict(old_side) if mode == "update" else {}
        for k, v in (side or {}).items():
            if v is None:
                merged.pop(k, None)
            else:
                merged[k] = v
        merged.setdefault("addedAt", today())
        hc.write_json(side_path, _clean_side(merged))
    return {"id": f"{type_id}/{category}/{name}", "path": hc.rel(target), "created": not exists,
            "files": written, "trash": trash}


# ---------------------------------------------------------------- origens (GitHub e pasta local)

GH_RE = re.compile(r"^(?:https?://)?(?:www\.)?github\.com[/:]([^/\s]+)/([^/\s#?]+?)(?:\.git)?(?:/(tree|blob)/(.+?))?/?(?:[#?].*)?$")
GH_SSH_RE = re.compile(r"^git@github\.com:([^/\s]+)/([^/\s]+?)(?:\.git)?$")
SHORT_RE = re.compile(r"^([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)$")


def parse_github_url(url):
    url = (url or "").strip()
    m = GH_RE.match(url)
    if m:
        return {"owner": m.group(1), "repo": m.group(2), "mode": m.group(3), "rest": urllib.parse.unquote(m.group(4) or "")}
    m = GH_SSH_RE.match(url)
    if m:
        return {"owner": m.group(1), "repo": m.group(2), "mode": None, "rest": ""}
    return None


class Source:
    """Origem com uma lista de arquivos (caminhos relativos em posix) e leitura sob demanda."""
    kind = "local"
    repo = None
    commit = None
    license = None
    owner = None
    truncated = False
    scope = "."
    scope_is_file = False

    def __init__(self):
        self.files = {}  # caminho -> tamanho
        self._cache = {}

    def read(self, path):
        raise NotImplementedError

    def read_text(self, path):
        if path not in self._cache:
            self._cache[path] = self.read(path).decode("utf-8", "replace")
        return self._cache[path]

    def url_for(self, path, is_dir):
        return None

    def source_meta(self, path, is_dir):
        return {"kind": self.kind, "repo": self.repo, "path": path, "commit": self.commit,
                "url": self.url_for(path, is_dir)}

    def info(self):
        return {"kind": self.kind, "repo": self.repo, "commit": self.commit, "scope": self.scope,
                "license": self.license, "files": len(self.files), "truncated": self.truncated,
                "url": self.url_for(self.scope, not self.scope_is_file)}

    def set_scope(self, scope):
        scope = (scope or "").strip("/") or "."
        if scope != "." and scope not in self.files and not any(p.startswith(scope + "/") for p in self.files):
            raise NotFound(f"Caminho não encontrado na origem: {scope}")
        if scope in self.files:
            if pbase(scope) == "SKILL.md":
                scope = pdir(scope)
            elif scope.endswith(".claude-plugin/plugin.json"):
                scope = pdir(pdir(scope))
            else:
                self.scope_is_file = True
        self.scope = scope

    def scoped(self):
        if self.scope_is_file:
            return [self.scope]
        return sorted(p for p in self.files if under(p, self.scope))


class LocalSource(Source):
    kind = "local"

    def __init__(self, path):
        super().__init__()
        p = Path(os.path.expanduser(str(path))).resolve()
        if not p.exists():
            raise NotFound(f"Pasta não encontrada: {path}")
        scope = "."
        if p.is_file():
            parent = p.parent
            if p.name == "plugin.json" and parent.name == ".claude-plugin":
                parent = parent.parent
            self.root = parent.parent if parent.parent != parent else parent
            scope = p.relative_to(self.root).as_posix()
        else:
            self.root = p
        self.repo = self.root.name
        try:
            os.listdir(self.root)
        except PermissionError:
            raise ImportFailure(
                f"Sem permissão para ler {self.root}. No macOS, libere o acesso do Terminal (ou do app que "
                "rodou o admin) em Ajustes do Sistema → Privacidade e Segurança → Arquivos e Pastas.")
        for dirpath, dirnames, filenames in os.walk(self.root, onerror=self._erro_walk):
            dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not os.path.islink(os.path.join(dirpath, d))]
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                if fn in hc.IGNORED or fn.endswith(".pyc") or os.path.islink(full):
                    continue
                relp = Path(full).relative_to(self.root).as_posix()
                try:
                    self.files[relp] = os.path.getsize(full)
                except OSError:
                    continue
        if not self.files and self._negados:
            raise ImportFailure(
                f"Sem permissão para ler {self.root}. No macOS, libere o acesso do Terminal (ou do app que "
                "rodou o admin) em Ajustes do Sistema → Privacidade e Segurança → Arquivos e Pastas.")
        lic = next((self.root / n for n in ("LICENSE", "LICENSE.md", "LICENSE.txt") if (self.root / n).is_file()), None)
        if lic:
            self.license = guess_license(lic.read_text(encoding="utf-8", errors="replace"))
        self.set_scope(scope)

    _negados = 0

    def _erro_walk(self, exc):
        if isinstance(exc, PermissionError):
            self._negados += 1

    def read(self, path):
        full = (self.root / safe_rel(path)).resolve()
        if self.root.resolve() not in full.parents:
            raise ImportFailure(f"Caminho inválido: {path}")
        return full.read_bytes()

    def info(self):
        d = super().info()
        d["path"] = str(self.root)
        return d


def _gh_cache_file(owner, repo):
    return CACHE / "github" / f"{hc.slugify(owner)}__{hc.slugify(repo)}.json"


class GitHubSource(Source):
    kind = "github"

    def __init__(self, url, parsed=None):
        super().__init__()
        parsed = parsed or parse_github_url(url)
        if not parsed:
            raise ImportFailure(f"URL do GitHub inválida: {url}")
        self.owner, self.name = parsed["owner"], parsed["repo"]
        self.repo = f"{self.owner}/{self.name}"
        with _lock:
            cache = hc.load_json(_gh_cache_file(self.owner, self.name), {}) or {}
        now = time.time()
        meta = cache.get("repo")
        if not meta or now - meta.get("at", 0) > GH_TTL:
            try:
                data = json.loads(gh_api(f"/repos/{self.repo}"))
            except NotFound:
                raise NotFound(f"Repositório não encontrado (ou privado): {self.repo}")
            lic = data.get("license") or {}
            spdx = lic.get("spdx_id")
            meta = {
                "at": now, "default_branch": data.get("default_branch") or "main",
                "license": (spdx if spdx and spdx != "NOASSERTION" else lic.get("name")) or None,
                "description": data.get("description"), "stars": data.get("stargazers_count"),
                "language": data.get("language"), "homepage": data.get("homepage") or None,
                "updatedAt": data.get("pushed_at") or data.get("updated_at"), "topics": data.get("topics") or [],
                "html_url": data.get("html_url"), "full_name": data.get("full_name") or self.repo,
                "owner": (data.get("owner") or {}).get("login") or self.owner,
            }
            cache["repo"] = meta
        self.meta = meta
        self.license = meta.get("license")
        refs = cache.setdefault("refs", {})
        ref, sub = self._resolve_ref(parsed, meta["default_branch"], refs, now)
        self.ref = ref
        self.commit = refs[ref]["sha"]
        trees = cache.setdefault("trees", {})
        tree = trees.get(self.commit)
        if not tree:
            data = json.loads(gh_api(f"/repos/{self.repo}/git/trees/{self.commit}?recursive=1"))
            entries = [[e["path"], e.get("size", 0)] for e in data.get("tree", [])
                       if e.get("type") == "blob" and e.get("mode") != "120000"]
            tree = {"entries": entries, "truncated": bool(data.get("truncated")), "at": now}
            trees[self.commit] = tree
            for old in sorted(trees, key=lambda k: trees[k].get("at", 0))[:-3]:
                trees.pop(old, None)
        self.truncated = tree.get("truncated", False)
        for path, size in tree["entries"]:
            parts = path.split("/")
            if any(p in IGNORED_DIRS for p in parts[:-1]) or parts[-1] in hc.IGNORED:
                continue
            self.files[path] = size
        with _lock:
            hc.write_json(_gh_cache_file(self.owner, self.name), cache)
        self.set_scope(sub)

    def _resolve_ref(self, parsed, default_branch, refs, now):
        candidates = []
        if parsed.get("rest"):
            parts = parsed["rest"].split("/")
            for i in range(1, min(len(parts), 4) + 1):
                candidates.append(("/".join(parts[:i]), "/".join(parts[i:])))
        else:
            candidates.append((default_branch, ""))
        for ref, sub in candidates:
            hit = refs.get(ref)
            if hit and now - hit.get("at", 0) <= GH_TTL:
                return ref, sub
            try:
                sha = gh_api(f"/repos/{self.repo}/commits/{urllib.parse.quote(ref, safe='')}",
                             accept="application/vnd.github.sha").decode().strip()
            except NotFound:
                continue
            except ImportFailure as exc:
                if exc.status == 422:
                    continue
                raise
            if re.match(r"^[0-9a-f]{40}$", sha):
                refs[ref] = {"sha": sha, "at": now}
                return ref, sub
        raise NotFound(f"Branch ou commit não encontrado em {self.repo}: {parsed.get('rest') or default_branch}")

    def read(self, path):
        return http_get(raw_url(self.repo, self.commit, path), timeout=60)

    def url_for(self, path, is_dir):
        base = f"https://github.com/{self.repo}"
        if path in ("", "."):
            return f"{base}/tree/{self.commit}"
        return f"{base}/{'tree' if is_dir else 'blob'}/{self.commit}/{urllib.parse.quote(path, safe='/')}"

    def info(self):
        d = super().info()
        d.update({"ref": self.ref, "description": self.meta.get("description"), "stars": self.meta.get("stars")})
        return d


def open_source(source):
    """Abre uma origem: pasta local, URL do GitHub ou dono/repo."""
    s = str(source or "").strip()
    if not s:
        raise ImportFailure("Informe a origem (URL do GitHub ou caminho de uma pasta).")
    expanded = os.path.expanduser(s)
    if os.path.exists(expanded):
        return LocalSource(expanded)
    parsed = parse_github_url(s)
    if not parsed and SHORT_RE.match(s) and not s.startswith("."):
        parsed = {"owner": s.split("/")[0], "repo": s.split("/")[1], "mode": None, "rest": ""}
    if parsed:
        return GitHubSource(s, parsed)
    if s.startswith(("/", "~", ".")):
        raise NotFound(f"Pasta não encontrada: {s}")
    raise ImportFailure(f"Origem não reconhecida: {s}. Use uma URL do GitHub ou o caminho de uma pasta.")


# ---------------------------------------------------------------- detecção

def _is_hooks_map(h):
    return isinstance(h, dict) and bool(h) and all(k in HOOK_EVENTS for k in h)


def classify_json(path, text):
    """Devolve ("mcp"|"hook"|None, dados normalizados) para um arquivo JSON."""
    try:
        data = json.loads(text)
    except ValueError:
        return None, None
    if not isinstance(data, dict):
        return None, None
    servers = data.get("mcpServers")
    if isinstance(servers, dict) and servers:
        return "mcp", data
    if pbase(path) == ".mcp.json" and data and all(isinstance(v, dict) and ("command" in v or "url" in v)
                                                   for v in data.values()):
        return "mcp", {"mcpServers": data}
    if _is_hooks_map(data.get("hooks")):
        return "hook", data
    if path.endswith("hooks/hooks.json") and _is_hooks_map(data):
        return "hook", {"hooks": data}
    return None, None


def _json_name(src, path, kind, data):
    base = pbase(path)
    parent = pbase(pdir(path)) if pdir(path) != "." else ""
    root_name = getattr(src, "name", None) or src.repo or "item"
    if kind == "mcp" and base == ".mcp.json":
        servers = list((data.get("mcpServers") or {}).keys())
        return hc.slugify(servers[0] if len(servers) == 1 else (parent or root_name))
    if kind == "hook" and path.endswith("hooks/hooks.json"):
        owner_dir = pdir(pdir(path))
        return hc.slugify(pbase(owner_dir) if owner_dir != "." else root_name)
    stem = pstem(path)
    if stem.lower() in ("mcp", "config", "settings", "settings.local", "hooks", ".mcp") and (parent or root_name):
        return hc.slugify((parent if parent not in (".claude", "hooks") else root_name) + ("-hooks" if kind == "hook" else ""))
    return hc.slugify(stem)


def detect(src, describe=True):
    """Lista candidatos a componente na origem (respeitando a subpasta escolhida)."""
    files = src.scoped()
    fileset = set(src.files)
    warnings = []
    if src.truncated:
        warnings.append("A árvore do repositório veio incompleta (muito grande). Use uma URL /tree/<branch>/<subpasta>.")
    plugins = sorted({pdir(pdir(p)) for p in files if p.endswith(".claude-plugin/plugin.json")},
                     key=lambda d: (d.count("/"), d))
    plugin_dirs = []
    for d in plugins:
        if not any(under(d, o) for o in plugin_dirs):
            plugin_dirs.append(d)
    skill_dirs = []
    for d in sorted({pdir(p) for p in files if pbase(p) == "SKILL.md"}, key=lambda d: (d.count("/"), d)):
        if any(under(d, o) for o in plugin_dirs) or any(under(d, o) for o in skill_dirs):
            continue
        skill_dirs.append(d)
    taken = plugin_dirs + skill_dirs
    for d in plugin_dirs:
        inner = sum(1 for p in files if under(p, d) and pbase(p) == "SKILL.md")
        if inner > 1:
            where = "A origem inteira é um plugin" if d == "." else f"O plugin {d} tem {inner} skills"
            warnings.append(f"{where}: ele entra como um item só. Para importar as skills soltas, "
                            f"escaneie a subpasta delas (URL /tree/<branch>/<subpasta> ou a pasta local).")

    def free(p):
        return not any(under(p, o) for o in taken)

    cands = []
    for d in plugin_dirs:
        cands.append({"kind": "plugin", "path": d, "main": pjoin(d, ".claude-plugin/plugin.json")})
    for d in skill_dirs:
        cands.append({"kind": "skill", "path": d, "main": pjoin(d, "SKILL.md")})
    for p in files:
        if not p.endswith(".md") or not free(p) or pstem(p).lower() in NOT_COMPONENT_MD:
            continue
        m = re.search(r"(?:^|/)(agents|commands)/[^/]+\.md$", p)
        if m:
            cands.append({"kind": "agent" if m.group(1) == "agents" else "command", "path": p, "main": p})
    jsons = [p for p in files if p.endswith(".json") and free(p) and pbase(p) not in SKIP_JSON
             and src.files.get(p, 0) <= 256 * 1024]
    if len(jsons) > MAX_JSON_PROBE:
        warnings.append(f"{len(jsons)} arquivos JSON na origem; só os primeiros {MAX_JSON_PROBE} foram verificados.")
        jsons = sorted(jsons, key=lambda p: (pbase(p) not in (".mcp.json", "hooks.json"), p.count("/"), p))[:MAX_JSON_PROBE]
    texts = _read_many(src, jsons, warnings)
    for p in jsons:
        if p not in texts:
            continue
        kind, data = classify_json(p, texts[p])
        if kind:
            cands.append({"kind": kind, "path": p, "main": p, "data": data})
    if describe:
        mains = [c["main"] for c in cands if c["kind"] in ("skill", "plugin", "agent", "command")]
        if len(mains) > MAX_DESCRIBE:
            warnings.append(f"{len(mains)} candidatos; descrições lidas só dos primeiros {MAX_DESCRIBE}.")
            mains = mains[:MAX_DESCRIBE]
        texts.update(_read_many(src, mains, warnings))
    out = []
    for c in cands:
        out.append(_describe(src, c, texts.get(c["main"]), fileset))
    out.sort(key=lambda c: (list(KIND_TO_TYPE).index(c["kind"]), c["path"]))
    return out, warnings


def _read_many(src, paths, warnings):
    texts = {}
    if not paths:
        return texts

    def job(p):
        try:
            return p, src.read_text(p)
        except ImportFailure as exc:
            if exc.status == 429:
                raise
            warnings.append(f"não consegui ler {p}: {exc}")
            return p, None

    workers = 1 if isinstance(src, LocalSource) else 8
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for p, t in pool.map(job, paths):
            if t is not None:
                texts[p] = t
    return texts


def _describe(src, c, text, fileset):
    kind, path = c["kind"], c["path"]
    type_id = KIND_TO_TYPE[kind]
    root_name = getattr(src, "name", None) or src.repo or "item"
    name, desc, lic, author = None, "", None, None
    if kind in ("skill", "agent", "command") and text is not None:
        fm, body = hc.parse_frontmatter(text)
        if isinstance(fm.get("name"), str) and kind != "command":
            name = fm["name"]
        desc = str(fm.get("description") or hc.first_paragraph(body) or "")
        lic = fm.get("license") if isinstance(fm.get("license"), str) else None
        meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
        author = fm.get("author") or meta.get("author")
    if kind == "plugin" and text is not None:
        try:
            pj = json.loads(text)
        except ValueError:
            pj = {}
        name = pj.get("name") if isinstance(pj.get("name"), str) else None
        desc = str(pj.get("description") or "")
        lic = pj.get("license") if isinstance(pj.get("license"), str) else None
        a = pj.get("author")
        author = a.get("name") if isinstance(a, dict) else a
    if kind in ("skill", "plugin") and not name:
        name = pbase(path) if path != "." else root_name
    if kind in ("agent", "command") and not name:
        name = pstem(path)
    data = c.get("data")
    if kind in ("mcp", "hook"):
        name = _json_name(src, path, kind, data)
        desc = str(data.get("description") or "")
        if kind == "mcp" and not desc:
            servers = data.get("mcpServers") or {}
            inner = [s.get("description") for s in servers.values() if isinstance(s, dict) and s.get("description")]
            desc = inner[0] if inner else "MCP: " + ", ".join(servers)
        if kind == "hook" and not desc:
            desc = "Hooks: " + ", ".join(sorted((data.get("hooks") or {}).keys()))
    name = hc.slugify(str(name))
    if kind in ("skill", "plugin"):
        nfiles = sum(1 for p in fileset if under(p, path))
    else:
        nfiles = 1 + len(_local_extras(src, path)) if kind in ("mcp", "hook") else 1
    desc = re.sub(r"\s+", " ", desc.replace("\\n", " ")).strip()
    return {
        "kind": kind, "type": type_id, "path": path, "name": name, "description": desc[:500],
        "suggestedCategory": suggest_category(type_id, name, desc),
        "license": lic or src.license, "author": author, "files": nfiles,
        "exists": find_existing(type_id, name),
    }


def _local_extras(src, path):
    """Scripts de apoio de um JSON de hook/MCP na origem: mesmo nome base, pasta <nome>/ ou referenciados."""
    folder, stem = pdir(path), pstem(path)
    out = {}
    for p in src.files:
        if pdir(p) == folder and pstem(p) == stem and p != path and p.endswith(SCRIPT_EXTS):
            out[p] = pbase(p)
        elif under(p, pjoin(folder, stem)) and p != pjoin(folder, stem):
            out[p] = stem + "/" + p[len(pjoin(folder, stem)) + 1:]
    return out


# ---------------------------------------------------------------- aplicar (importar da origem)

def scan(source):
    src = open_source(source)
    cands, warnings = detect(src)
    return {"source": src.info(), "items": cands, "warnings": warnings}


def apply(source, items, overwrite=False, category=None, src=None):
    """Importa os itens escolhidos [{kind, path, name?, category?}] de uma origem."""
    src = src or open_source(source)
    if not items:
        raise ImportFailure("Nenhum item escolhido.")
    imported, errors = [], []
    for it in items:
        try:
            imported.append(_apply_one(src, it, overwrite, category))
        except ImportFailure as exc:
            if exc.status == 429:
                errors.append({"path": it.get("path"), "error": str(exc)})
                break
            errors.append({"path": it.get("path"), "error": str(exc)})
    return {"source": src.info(), "imported": imported, "errors": errors}


def _apply_one(src, it, overwrite, default_category):
    kind = str(it.get("kind") or "").lower()
    kind = TYPE_TO_KIND.get(kind, kind)
    if kind not in KIND_TO_TYPE:
        raise ImportFailure(f"Tipo de item inválido: {it.get('kind')}")
    type_id = KIND_TO_TYPE[kind]
    raw_path = str(it.get("path") or ".").strip("/") or "."
    path = "." if raw_path == "." else safe_rel(raw_path)
    files = src.files
    if kind in ("skill", "plugin"):
        main = pjoin(path, "SKILL.md" if kind == "skill" else ".claude-plugin/plugin.json")
        if main not in files:
            raise NotFound(f"Não achei {main} na origem.")
    elif path not in files:
        raise NotFound(f"Arquivo não encontrado na origem: {path}")
    text = src.read_text(main if kind in ("skill", "plugin") else path)
    cand = None
    if kind in ("mcp", "hook"):
        k, data = classify_json(path, text)
        if k != kind:
            raise ImportFailure(f"{path} não parece um {'MCP (sem mcpServers)' if kind == 'mcp' else 'hook (sem hooks de eventos do Claude Code)'}.")
        cand = _describe(src, {"kind": kind, "path": path, "main": path, "data": data}, text, files)
    else:
        if kind in ("agent", "command") and not path.endswith(".md"):
            raise ImportFailure(f"{path} não é um arquivo .md")
        cand = _describe(src, {"kind": kind, "path": path, "main": main if kind in ("skill", "plugin") else path},
                         text, files)
    name = hc.slugify(it.get("name") or cand["name"])
    category = ensure_category(it.get("category") or default_category or cand["suggestedCategory"])
    is_dir = kind in ("skill", "plugin")
    side = {
        "source": src.source_meta(path, is_dir),
        "license": cand.get("license"),
        "author": cand.get("author") or getattr(src, "owner", None),
        "addedAt": today(),
    }
    if src.kind == "local":
        side["source"]["url"] = None
    if is_dir:
        payload = {}
        sel = [p for p in sorted(files) if under(p, path)]
        big = [p for p in sel if files[p] > MAX_FILE]
        sel = [p for p in sel if files[p] <= MAX_FILE and pbase(p) != hc.SIDE]
        datas = _download_many(src, sel)
        for p in sel:
            relp = p if path == "." else p[len(path) + 1:]
            payload[relp] = datas[p]
        lic_file = next((p for p in sel if pdir(p) == path and pstem(p).upper() in ("LICENSE", "LICENCE")), None)
        if lic_file and not side["license"]:
            side["license"] = guess_license(datas[lic_file].decode("utf-8", "replace"))
        res = write_component(type_id, category, name, files=payload, side=side, overwrite=overwrite)
        if big:
            res["warnings"] = [f"arquivo grande ignorado: {p}" for p in big]
        return res
    if kind in ("agent", "command"):
        return write_component(type_id, category, name, main=src.read(path), side=side, overwrite=overwrite)
    # mcp / hook
    data = classify_json(path, text)[1]
    out = {"description": cand["description"]} if cand["description"] else {}
    if kind == "mcp":
        out.update({k: v for k, v in data.items() if k != "description"})
    else:
        out["hooks"] = data["hooks"]
    stem = pstem(path)
    extras_src = {}
    for p, dest in _local_extras(src, path).items():
        # renomeia para o nome escolhido: x.sh → <nome>.sh, x/arq → <nome>/arq
        if dest.startswith(stem + "/"):
            dest = name + dest[len(stem):]
        elif pstem(dest) == stem and "/" not in dest:
            dest = name + dest[len(stem):]
        extras_src[p] = dest
    for full, ref in re.findall(r"(\.claude/(?:hooks|scripts)/([A-Za-z0-9._/-]+))", text):
        for cand_path in (pjoin(pdir(path), ref), full):
            if cand_path in files and cand_path not in extras_src and cand_path != path:
                extras_src[cand_path] = ref if (pstem(ref) == name and "/" not in ref) else f"{name}/{ref}"
                break
    extras = {}
    datas = _download_many(src, list(extras_src))
    for p, dest in extras_src.items():
        extras[dest] = datas[p]
    body = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
    res = write_component(type_id, category, name, main=body.encode("utf-8"), extras=extras, side=side,
                          overwrite=overwrite)
    res["extras"] = sorted(extras)
    return res


def _download_many(src, paths):
    out = {}
    if not paths:
        return out
    workers = 1 if isinstance(src, LocalSource) else 8
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for p, data in pool.map(lambda p: (p, src.read(p)), paths):
            out[p] = data
    return out


# ---------------------------------------------------------------- repositórios (components/repos)

def add_repo(url, category, name=None, description=None, tags=None, overwrite=False):
    parsed = parse_github_url(url)
    if not parsed and SHORT_RE.match(str(url or "").strip()):
        a, b = url.strip().split("/")
        parsed = {"owner": a, "repo": b, "mode": None, "rest": ""}
    if not parsed:
        raise ImportFailure(f"URL do GitHub inválida: {url}")
    category = ensure_category(category)
    repo = f"{parsed['owner']}/{parsed['repo']}"
    try:
        data = json.loads(gh_api(f"/repos/{repo}"))
    except NotFound:
        raise NotFound(f"Repositório não encontrado (ou privado): {repo}")
    lic = data.get("license") or {}
    spdx = lic.get("spdx_id")
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    topics = data.get("topics") or []
    all_tags = list(dict.fromkeys(list(tags or []) + topics))
    name = hc.slugify(name or data.get("name") or parsed["repo"])
    body = {
        "url": data.get("html_url") or f"https://github.com/{repo}",
        "title": data.get("name") or parsed["repo"],
        "description": description or data.get("description") or "",
        "stars": data.get("stargazers_count"),
        "language": data.get("language"),
        "license": (spdx if spdx and spdx != "NOASSERTION" else lic.get("name")) or None,
        "homepage": data.get("homepage") or None,
        "updatedAt": data.get("pushed_at") or data.get("updated_at"),
        "tags": all_tags,
    }
    text = json.dumps(body, ensure_ascii=False, indent=2) + "\n"
    side = {"source": {"kind": "github", "repo": data.get("full_name") or repo, "path": ".", "commit": None,
                       "url": body["url"]},
            "author": (data.get("owner") or {}).get("login"), "addedAt": today()}
    res = write_component("repos", category, name, main=text.encode("utf-8"), side=side, overwrite=overwrite)
    res["repo"] = body
    return res


# ---------------------------------------------------------------- aitmpl.com

_aitmpl_mem = {"mtime": None, "data": None}


def aitmpl_catalog(refresh=False):
    """Catálogo do aitmpl.com com cache em .cache/aitmpl-catalog.json (1 dia)."""
    path = CACHE / "aitmpl-catalog.json"
    with _lock:
        fresh = path.exists() and time.time() - path.stat().st_mtime < AITMPL_TTL
        if refresh or not fresh:
            try:
                blob = http_get(AITMPL_CATALOG_URL, timeout=90)
                data = json.loads(blob.decode("utf-8"))
                if not isinstance(data.get("components"), list):
                    raise ImportFailure("Catálogo do aitmpl.com em formato inesperado.", 502)
                path.parent.mkdir(parents=True, exist_ok=True)
                tmp = path.with_suffix(".tmp")
                tmp.write_bytes(blob)
                tmp.replace(path)
            except (ImportFailure, ValueError):
                if not path.exists():
                    raise
                print("aviso: não consegui atualizar o catálogo do aitmpl.com; usando o cache antigo.", file=sys.stderr)
        mtime = path.stat().st_mtime
        if _aitmpl_mem["mtime"] != mtime:
            _aitmpl_mem["data"] = json.loads(path.read_text(encoding="utf-8"))
            _aitmpl_mem["mtime"] = mtime
        return _aitmpl_mem["data"]


def _aitmpl_type(type_id):
    if not type_id:
        return None
    t = str(type_id).strip().lower()
    t = {"skill": "skills", "agent": "agents", "command": "commands", "mcp": "mcps", "hook": "hooks",
         "setting": "settings"}.get(t, t)
    if t not in AITMPL_TYPES:
        raise ImportFailure(f"Tipo {t} não é suportado. Use: {', '.join(AITMPL_TYPES)}.")
    return t


def _aitmpl_summary(c):
    scan = c.get("scan") or {}
    return {
        "id": c["id"], "type": c["type"], "category": c.get("category"), "name": c.get("name"),
        "description": re.sub(r"\s+", " ", str(c.get("description") or "").replace("\\n", " "))[:400],
        "license": c.get("license") or (c.get("source") or {}).get("license"),
        "author": c.get("author"), "downloads": c.get("downloads") or 0,
        "scan": {"severity": scan.get("severity"), "score": scan.get("score")} if scan else None,
        "url": (c.get("urls") or {}).get("page"),
        "external": bool((c.get("source") or {}).get("repo")),
        "suggestedCategory": suggest_category(c["type"], c.get("name") or "", c.get("description") or "",
                                              hint=c.get("category")),
        "exists": find_existing(c["type"], hc.slugify(c.get("name") or "")),
    }


def aitmpl_search(query="", type_id=None, limit=50):
    t = _aitmpl_type(type_id)
    cat = aitmpl_catalog()
    terms = [w for w in re.split(r"\s+", (query or "").lower().strip()) if w]
    hits = []
    for c in cat.get("components", []):
        if c.get("type") not in AITMPL_TYPES or (t and c.get("type") != t):
            continue
        name = (c.get("name") or "").lower()
        cid = c.get("id", "").lower()
        desc = (c.get("description") or "").lower()
        kw = " ".join(c.get("keywords") or []).lower()
        score = 0
        ok = True
        for w in terms:
            if w in name:
                score += 10 if name == w else 6
            elif w in cid:
                score += 4
            elif w in kw:
                score += 3
            elif w in desc:
                score += 1
            else:
                ok = False
                break
        if ok:
            hits.append((score, c.get("downloads") or 0, c))
    hits.sort(key=lambda h: (-h[0], -h[1], h[2]["id"]))
    limit = max(1, min(int(limit or 50), 500))
    return {"query": query, "type": t, "total": len(hits), "generatedAt": cat.get("generatedAt"),
            "items": [_aitmpl_summary(h[2]) for h in hits[:limit]]}


def aitmpl_import(ids, category=None, overwrite=False):
    if isinstance(ids, str):
        ids = [ids]
    ids = [str(i).strip().strip("/") for i in (ids or []) if str(i).strip()]
    if not ids:
        raise ImportFailure("Informe ao menos um id do aitmpl.com (ex.: skills/business-marketing/copywriting).")
    if category:
        category = ensure_category(category)
    by_id = {c["id"]: c for c in aitmpl_catalog().get("components", [])}
    imported, errors = [], []
    for cid in ids:
        try:
            entry = by_id.get(cid)
            if not entry:
                typ = cid.split("/")[0]
                if typ not in AITMPL_TYPES and typ in {c.get("type") for c in by_id.values()}:
                    raise ImportFailure(f"Tipo {typ} não é suportado. Use: {', '.join(AITMPL_TYPES)}.")
                raise NotFound(f"Não achei {cid} no catálogo do aitmpl.com.")
            if entry.get("type") not in AITMPL_TYPES:
                raise ImportFailure(f"Tipo {entry.get('type')} não é suportado. Use: {', '.join(AITMPL_TYPES)}.")
            imported.append(_aitmpl_import_one(entry, category, overwrite))
        except ImportFailure as exc:
            errors.append({"id": cid, "error": str(exc)})
            if exc.status == 429:
                break
    return {"imported": imported, "errors": errors}


def _aitmpl_get(repo, commits, path, fallback=None):
    last = None
    for commit in commits:
        try:
            return http_get(raw_url(repo, commit, path), timeout=60), commit
        except NotFound as exc:
            last = exc
    if fallback is not None:
        return (fallback.encode("utf-8") if isinstance(fallback, str) else fallback), None
    raise last or NotFound(f"Não achei {path}")


def _aitmpl_import_one(entry, category, overwrite):
    cid, typ = entry["id"], entry["type"]
    content = http_json(AITMPL_CONTENT_URL.format(id=urllib.parse.quote(cid, safe="/")))
    meta = content.get("meta") or {}
    last_sha = (meta.get("lastCommit") or {}).get("sha")
    ext = entry.get("source") or {}
    if ext.get("repo"):
        repo, commits, base_path = ext["repo"], [ext.get("commit") or "HEAD"], (ext.get("path") or "").strip("/")
    else:
        repo = AITMPL_REPO
        commits = [c for c in (last_sha, "main") if c]
        base_path = f"{AITMPL_BASE}/{typ}/{entry.get('path') or entry['category'] + '/' + entry['name']}"
    name = hc.slugify(entry.get("name") or cid.split("/")[-1])
    category = category or suggest_category(typ, name, entry.get("description") or "", hint=entry.get("category"))
    category = ensure_category(category)
    scan = entry.get("scan") or {}
    lic = entry.get("license") or ext.get("license") or (None if ext.get("repo") else AITMPL_REPO_LICENSE)
    warnings = []
    if str(scan.get("severity") or "").upper() in ("HIGH", "CRITICAL"):
        warnings.append(f"o aitmpl.com marcou este item com risco {scan.get('severity')} (score {scan.get('score')}); revise antes de publicar")
    inline = content.get("files") if isinstance(content.get("files"), dict) else {}
    used_commit = None
    executable = set()
    if typ == "skills":
        paths = [f.get("path") for f in (meta.get("files") or []) if isinstance(f, dict) and f.get("path")]
        if not paths:
            paths = sorted(set(["SKILL.md"] + list(entry.get("files") or []) + list(inline)))
        if "SKILL.md" not in paths:
            paths.insert(0, "SKILL.md")
        payload = {}

        def fetch(p):
            fb = inline.get(p) if p in inline else (content.get("content") if p == "SKILL.md" else None)
            return p, _aitmpl_get(repo, commits, f"{base_path}/{p}", fallback=fb)

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            for p, (data, commit) in pool.map(fetch, paths):
                payload[safe_rel(p)] = data
                used_commit = used_commit or commit
        side = _aitmpl_side(entry, repo, base_path, used_commit or commits[0], lic, scan)
        res = write_component("skills", category, name, files=payload, side=side, overwrite=overwrite)
    else:
        data, used_commit = _aitmpl_get(repo, commits, base_path, fallback=content.get("content"))
        extras = {}
        tags = list(entry.get("keywords") or [])
        if typ in ("mcps", "hooks", "settings"):
            text = data.decode("utf-8", "replace")
            try:
                obj = json.loads(text)
            except ValueError:
                raise ImportFailure(f"JSON inválido em {cid}.")
            if not isinstance(obj, dict):
                raise ImportFailure(f"JSON inesperado em {cid}.")
            changed = False
            if typ == "mcps" and not obj.get("description") and entry.get("description"):
                obj = dict([("description", entry["description"])] + list(obj.items()))
                changed = True
            if typ in ("hooks", "settings"):
                extras, executable = _aitmpl_extras(typ, entry, name, obj, text, repo, used_commit or commits[0])
                if "supportingFiles" in obj or isinstance(obj.get("tags"), list):
                    tags += [t for t in (obj.pop("tags", None) or []) if isinstance(t, str)]
                    obj.pop("supportingFiles", None)
                    changed = True
            if changed:
                data = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        side = _aitmpl_side(entry, repo, base_path, used_commit or commits[0], lic, scan)
        if tags:
            side["tags"] = list(dict.fromkeys(tags))[:12]
        res = write_component(typ, category, name, main=data, extras=extras, side=side, overwrite=overwrite,
                              executable=executable)
        res["extras"] = sorted(extras)
    res["aitmplId"] = cid
    if warnings:
        res["warnings"] = warnings
    return res


def _aitmpl_side(entry, repo, path, commit, lic, scan):
    page = (entry.get("urls") or {}).get("page") or f"https://www.aitmpl.com/component/{entry['id']}"
    return {
        "source": {"kind": "aitmpl", "id": entry["id"], "repo": repo, "path": path, "commit": commit, "url": page},
        "license": lic,
        "author": entry.get("author") or ("claude-code-templates (aitmpl.com)" if repo == AITMPL_REPO else repo.split("/")[0]),
        "scan": {k: scan.get(k) for k in ("severity", "score", "tool", "scannedAt") if scan.get(k) is not None} or None,
        "addedAt": today(),
        "notes": f"Importado do aitmpl.com ({entry['id']}).",
    }


def _aitmpl_extras(typ, entry, name, obj, text, repo, commit):
    """Scripts de apoio de hooks/settings do aitmpl.

    No repositório eles ficam ao lado do JSON, na mesma pasta da categoria e com o mesmo nome base
    (ex.: statusline/context-monitor.json + context-monitor.py). O JSON aponta para eles em
    .claude/hooks/<arquivo> (hooks) ou .claude/scripts/<arquivo> (settings), e alguns hooks listam
    supportingFiles [{source, destination, executable}] (às vezes numa subpasta <nome>/).
    """
    cat_dir = f"{AITMPL_BASE}/{typ}/{entry['category']}"
    wanted, executable = [], set()
    for sf in obj.get("supportingFiles") or []:
        if isinstance(sf, dict) and sf.get("source"):
            wanted.append(sf["source"])
    for ref in re.findall(r"\.claude/(?:hooks|scripts)/([A-Za-z0-9._/-]+)", text):
        wanted.append(ref.rstrip("."))
    probe = not wanted
    if probe:
        wanted = [name + e for e in (".py", ".sh", ".js")]
    extras = {}
    for src in dict.fromkeys(wanted):
        try:
            relp = safe_rel(src)
        except ImportFailure:
            continue
        if "." not in pbase(relp):
            continue
        try:
            data = http_get(raw_url(repo, commit, f"{cat_dir}/{relp}"), timeout=60)
        except NotFound:
            continue
        if "/" not in relp and pstem(relp) == name:
            dest = relp
        elif relp.startswith(name + "/"):
            dest = relp
        else:
            dest = f"{name}/{relp}"
        extras[dest] = data
        if dest.endswith((".sh", ".py", ".bash")):
            executable.add(dest)
    return extras, executable


# ---------------------------------------------------------------- CLI

def _rebuild(args):
    if getattr(args, "no_build", False):
        print("Catálogo não reconstruído (--no-build). Rode: python3 tools/build.py")
        return
    import build  # noqa: WPS433
    res = build.build(quiet=True)
    print(f"Catálogo reconstruído: {len(res['items'])} componentes.")


def _print_result(res):
    for it in res.get("imported", []):
        n_extras = len(it.get("extras") or [])
        extra = f" + {n_extras} script(s) de apoio" if n_extras else ""
        origin = f" ← {it['aitmplId']}" if it.get("aitmplId") else ""
        print(f"ok  {it['id']}{origin} ({len(it.get('files') or []) - n_extras} arquivo(s){extra})")
        for w in it.get("warnings", []):
            print(f"    atenção: {w}")
        if it.get("trash"):
            print(f"    versão antiga movida para {it['trash']}")
    for e in res.get("errors", []):
        print(f"erro  {e.get('path') or e.get('id')}: {e['error']}")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="importers.py", description="Importa componentes para a Central Trip Angle.")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("scan", help="lista candidatos de um repositório GitHub ou pasta")
    p.add_argument("source")
    p.add_argument("--json", action="store_true")
    p = sub.add_parser("apply", help="importa candidatos de uma origem")
    p.add_argument("source")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--all", action="store_true")
    g.add_argument("--pick", help="caminhos separados por vírgula (como aparecem no scan)")
    p.add_argument("--category", help="categoria da Central (padrão: a sugerida para cada item)")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--no-build", action="store_true")
    p = sub.add_parser("aitmpl", help="busca e importa do aitmpl.com")
    asub = p.add_subparsers(dest="acmd")
    s = asub.add_parser("search")
    s.add_argument("terms", nargs="*")
    s.add_argument("--type")
    s.add_argument("--limit", type=int, default=30)
    s.add_argument("--json", action="store_true")
    s.add_argument("--refresh", action="store_true", help="baixa o catálogo de novo, ignorando o cache")
    s = asub.add_parser("import")
    s.add_argument("ids", nargs="+")
    s.add_argument("--category")
    s.add_argument("--overwrite", action="store_true")
    s.add_argument("--no-build", action="store_true")
    p = sub.add_parser("repo", help="cadastra um repositório do GitHub em components/repos")
    p.add_argument("url")
    p.add_argument("--category", required=True)
    p.add_argument("--name")
    p.add_argument("--description")
    p.add_argument("--tags")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--no-build", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "scan":
            res = scan(args.source)
            if args.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
                return 0
            info = res["source"]
            where = info.get("repo") if info["kind"] == "github" else info.get("path")
            print(f"Origem: {info['kind']} {where} @ {(info.get('commit') or '')[:12]} · subpasta {info['scope']} · licença {info.get('license') or '?'}")
            for w in res["warnings"]:
                print("aviso:", w)
            if not res["items"]:
                print("Nenhum componente encontrado.")
                return 1
            for c in res["items"]:
                flag = " (já existe: " + ", ".join(c["exists"]) + ")" if c["exists"] else ""
                print(f"{c['kind']:8} {c['path']}\n         → {c['name']} [{c['suggestedCategory']}]{flag} {c['description'][:90]}")
            print(f"{len(res['items'])} candidato(s).")
            return 0
        if args.cmd == "apply":
            src = open_source(args.source)
            cands, warnings = detect(src, describe=False)
            for w in warnings:
                print("aviso:", w)
            if args.all:
                chosen = cands
            else:
                want = [x.strip().strip("/") or "." for x in args.pick.split(",") if x.strip()]
                by_path = {c["path"]: c for c in cands}
                missing = [w for w in want if w not in by_path]
                if missing:
                    print("erro: não encontrado no scan: " + ", ".join(missing))
                    return 1
                chosen = [by_path[w] for w in want]
            if not chosen:
                print("Nenhum componente encontrado.")
                return 1
            if args.category:
                ensure_category(args.category)
            items = [{"kind": c["kind"], "path": c["path"], "category": args.category} for c in chosen]
            res = apply(args.source, items, overwrite=args.overwrite, src=src)
            _print_result(res)
            if res["imported"]:
                _rebuild(args)
            return 0 if not res["errors"] else 1
        if args.cmd == "aitmpl":
            if args.acmd == "search":
                if args.refresh:
                    aitmpl_catalog(refresh=True)
                res = aitmpl_search(" ".join(args.terms), args.type, args.limit)
                if args.json:
                    print(json.dumps(res, ensure_ascii=False, indent=2))
                    return 0
                for c in res["items"]:
                    sev = (c.get("scan") or {}).get("severity") or "-"
                    print(f"{c['id']}  [{c['suggestedCategory']}] risco {sev} · {c['downloads']} downloads\n    {c['description'][:110]}")
                print(f"{len(res['items'])} de {res['total']} resultado(s).")
                return 0
            if args.acmd == "import":
                res = aitmpl_import(args.ids, args.category, args.overwrite)
                _print_result(res)
                if res["imported"]:
                    _rebuild(args)
                return 0 if not res["errors"] else 1
            ap.parse_args(["aitmpl", "--help"])
            return 2
        if args.cmd == "repo":
            res = add_repo(args.url, args.category, args.name, args.description, args.tags, args.overwrite)
            r = res["repo"]
            print(f"ok  {res['id']} · {r.get('stars')} estrelas · {r.get('language') or '-'} · {r.get('license') or 'sem licença'}")
            _rebuild(args)
            return 0
        ap.print_help()
        return 2
    except ImportFailure as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
