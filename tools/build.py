#!/usr/bin/env python3
"""Gera o catálogo, os pacotes do marketplace e a pasta dist/ publicável.

Uso:
  python3 tools/build.py            # gera tudo
  python3 tools/build.py --check    # só valida e mostra avisos
Variáveis opcionais: TAHUB_SITE_URL, TAHUB_GITHUB_REPO (sobrepõem hub.config.json).
"""
import datetime
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hubcore as hc  # noqa: E402

SOURCE_PLACEHOLDER = "__TAHUB_DEFAULT_SOURCE__"
BUNDLE_TYPES = ("skills", "agents", "commands", "prompts", "frameworks")


def build(check_only=False, quiet=False):
    log = (lambda *a: None) if quiet else print
    warnings = []
    cfg = hc.load_config()
    cats = hc.load_categories()
    items = hc.scan_components(warn=warnings.append)
    cat_ids = {c["id"] for c in cats}
    ids = {it["id"] for it in items}
    collections = []
    for col in hc.load_json(hc.ROOT / "collections.json", []) or []:
        faltando = [i for i in col.get("items", []) if i not in ids]
        for i in faltando:
            warnings.append(f"kit curado {col.get('id')}: item não existe {i}")
        col = dict(col, items=[i for i in col.get("items", []) if i in ids])
        if col["items"]:
            collections.append(col)
    journeys = []
    for j in hc.load_json(hc.ROOT / "journeys.json", []) or []:
        for n, passo in enumerate(j.get("passos", []), 1):
            for ref in [passo.get("principal")] + list(passo.get("apoio", [])):
                if ref and ref not in ids:
                    warnings.append(f"jornada {j.get('id')} passo {n}: item não existe {ref}")
            passo["apoio"] = [r for r in passo.get("apoio", []) if r in ids]
            if passo.get("principal") not in ids:
                passo["principal"] = None
        journeys.append(j)
    for it in items:
        if it["type"] == "prompts" and it.get("level") == "mestre":
            faltam = [n for n in range(1, 9) if n not in it.get("secoes", [])]
            if faltam:
                warnings.append(f"prompt mestre {it['id']}: faltam as seções {faltam}")
            if it.get("lines", 0) < 180:
                warnings.append(f"prompt mestre {it['id']}: só {it.get('lines')} linhas (mínimo 180)")
            if not it.get("etapas") or not it.get("stage"):
                warnings.append(f"prompt mestre {it['id']}: declare etapas e stage no frontmatter")
            sem = [v["name"] for v in it.get("variables", []) if v.get("required") is None]
            if sem:
                warnings.append(f"prompt mestre {it['id']}: variáveis sem [obrigatório]/[opcional]/[padrão = …]: {', '.join(sem)}")
        if it.get("status") and it["status"] not in hc.STATUS:
            warnings.append(f"status inválido em {it['id']}: {it['status']} (use {', '.join(hc.STATUS)})")
        if it["category"] not in cat_ids:
            cats.append({"id": it["category"], "label": hc.humanize(it["category"]), "icon": "•",
                         "description": "", "order": 999})
            cat_ids.add(it["category"])
        if not it["description"]:
            warnings.append(f"sem descrição: {it['id']}")
    if check_only:
        for w in warnings:
            log("aviso:", w)
        log(f"{len(items)} componentes lidos, {len(warnings)} avisos.")
        return {"items": items, "warnings": warnings}

    agora = datetime.datetime.now()
    # um número novo a cada publicação (até várias no mesmo dia), para o Claude Code oferecer a atualização
    version = "1.%s.%d" % (agora.strftime("%Y%m%d"), agora.hour * 100 + agora.minute)
    bundles = write_bundles(cfg, cats, items, version, warnings)
    redistribuidos = [i for i in items if i["type"] not in ("repos", "sites")]
    aviso = avisos_de_terceiros(redistribuidos, "Avisos de terceiros · Central de IA Trip Angle")
    if aviso and not check_only:
        (hc.ROOT / "THIRD_PARTY_NOTICES.md").write_text(aviso + "\n", encoding="utf-8")
    write_marketplace(cfg, cats, items, bundles, version)
    catalog = write_dist(cfg, cats, items, bundles, collections, journeys)
    for w in warnings:
        log("aviso:", w)
    counts = ", ".join(f"{t['label']} {catalog['counts'].get(t['id'], 0)}" for t in hc.TYPES)
    log(f"Catálogo: {len(items)} componentes ({counts}).")
    log(f"Pacotes do marketplace: {len(bundles)}. Site gerado em dist/.")
    return {"items": items, "warnings": warnings, "catalog": catalog}


# ---------------------------------------------------------------- bundles

MIT_TEXTO = """Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

# Avisos de copyright das origens MIT de onde a Central redistribui componentes.
MIT_COPYRIGHT = {
    "davila7/claude-code-templates": "Copyright (c) 2025 Daniel (San) Ávila",
    "coreyhaines31/marketingskills": "Copyright (c) 2025 Corey Haines",
    "obra/superpowers": "Copyright (c) 2025 Jesse Vincent",
}


def _terceiro(it):
    s = it.get("source") or {}
    return s.get("kind") in ("aitmpl", "github") and s.get("repo")


def avisos_de_terceiros(itens, titulo):
    """Markdown com a lista de componentes de terceiros e os textos de licença que precisam ir junto."""
    terc = sorted((it for it in itens if _terceiro(it)), key=lambda i: i["id"])
    if not terc:
        return None
    linhas = [f"# {titulo}", "",
              "Esta pasta inclui componentes de terceiros, redistribuídos conforme as licenças deles. "
              "O restante é conteúdo original da Trip Angle.", "",
              "| Componente | Autor | Licença | Origem |", "|---|---|---|---|"]
    origens = set()
    for it in terc:
        s = it["source"]
        origens.add(s["repo"])
        if "superpowers" in str(it.get("author") or ""):
            origens.add("obra/superpowers")
        url = s.get("url") or f"https://github.com/{s['repo']}"
        autor = str(it.get("author") or s["repo"]).replace("|", "/")
        linhas.append(f"| {it['type']}/{it['name']} | {autor} | {it.get('license') or 'ver origem'} | {url} |")
    linhas += ["", "## Textos das licenças", ""]
    for repo in sorted(origens):
        if repo in MIT_COPYRIGHT:
            linhas += [f"### {repo} (MIT)", "", "```", "MIT License", "", MIT_COPYRIGHT[repo], "", MIT_TEXTO, "```", ""]
    if any(str(it.get("license")) == "Apache-2.0" for it in terc):
        linhas += ["### Apache License 2.0", "",
                   "Os componentes marcados Apache-2.0 trazem o texto completo da licença no arquivo LICENSE.txt "
                   "dentro da própria pasta.", ""]
    return "\n".join(linhas)


def write_bundles(cfg, cats, items, version, warnings):
    """Um plugin por categoria com as skills, agentes e comandos soltos dela."""
    if hc.BUNDLES.exists():
        shutil.rmtree(hc.BUNDLES)
    by_cat = {}
    for it in items:
        if it["type"] in BUNDLE_TYPES and not it["partOf"]:
            by_cat.setdefault(it["category"], []).append(it)
    labels = {c["id"]: c for c in cats}
    bundles = []
    for cat, members in sorted(by_cat.items()):
        name = f"ta-{cat}"
        root = hc.BUNDLES / cat
        used = {"skills": set(), "agents": set(), "commands": set()}
        for it in members:
            # prompts viram comandos e frameworks viram skills dentro do plugin
            destino = {"prompts": "commands", "frameworks": "skills"}.get(it["type"], it["type"])
            nome = hc.framework_skill_name(it["name"]) if it["type"] == "frameworks" else it["name"]
            if nome in used[destino]:
                warnings.append(f"pacote {name}: nome repetido {destino}/{nome} ({it['id']}) ignorado")
                continue
            used[destino].add(nome)
            src = hc.ROOT / it["base"]
            if it["type"] == "skills":
                shutil.copytree(src, root / "skills" / it["name"], ignore=shutil.ignore_patterns(hc.SIDE, ".DS_Store"))
            elif it["type"] == "prompts":
                (root / "commands").mkdir(parents=True, exist_ok=True)
                (root / "commands" / f"{nome}.md").write_text(
                    hc.prompt_to_command(src.read_text(encoding="utf-8"), it), encoding="utf-8")
            elif it["type"] == "frameworks":
                (root / "skills" / nome).mkdir(parents=True, exist_ok=True)
                (root / "skills" / nome / "SKILL.md").write_text(
                    hc.framework_to_skill(src.read_text(encoding="utf-8"), it), encoding="utf-8")
            else:
                (root / it["type"]).mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, root / it["type"] / src.name)
            it["bundle"] = name
        label = labels.get(cat, {}).get("label", hc.humanize(cat))
        n_prompts = sum(1 for m in members if m["type"] == "prompts" and m.get("bundle") == name)
        n_fw = sum(1 for m in members if m["type"] == "frameworks" and m.get("bundle") == name)
        partes = [f"{len(used['skills']) - n_fw} skills", f"{len(used['agents'])} agentes",
                  f"{len(used['commands']) - n_prompts} comandos"]
        if n_prompts:
            partes.append(f"{n_prompts} prompts")
        if n_fw:
            partes.append(f"{n_fw} frameworks")
        desc = f"{label}: {', '.join(partes)} da {cfg.get('name', 'Central de IA Trip Angle')}."
        aviso = avisos_de_terceiros([m for m in members if m.get("bundle") == name], f"Avisos de terceiros · {name}")
        if aviso:
            (root / "THIRD_PARTY_NOTICES.md").write_text(aviso + "\n", encoding="utf-8")
        hc.write_json(root / ".claude-plugin" / "plugin.json", {
            "name": name,
            "version": version,
            "description": desc,
            "author": {"name": cfg.get("owner", {}).get("name", "Trip Angle")},
            "keywords": ["trip-angle", cat, "marketing-digital"],
        })
        bundles.append({"name": name, "category": cat, "label": label, "description": desc,
                        "source": f"./bundles/{cat}", "skills": len(used["skills"]) - n_fw,
                        "agents": len(used["agents"]), "commands": len(used["commands"]) - n_prompts,
                        "prompts": n_prompts, "frameworks": n_fw,
                        "members": [m["id"] for m in members if m.get("bundle") == name]})
    return bundles


def write_marketplace(cfg, cats, items, bundles, version):
    plugins = []
    for it in items:
        if it["type"] == "plugins":
            plugins.append({
                "name": it.get("pluginName") or it["name"],
                "source": "./" + it["base"],
                "description": it["description"][:500],
                "version": it.get("version") or "1.0.0",
                "category": it["category"],
                "keywords": (it.get("tags") or [])[:10],
            })
            it["marketplaceName"] = it.get("pluginName") or it["name"]
    for b in bundles:
        plugins.append({"name": b["name"], "source": b["source"], "description": b["description"],
                        "version": version, "category": b["category"],
                        "keywords": ["trip-angle", b["category"]]})
    hc.write_json(hc.ROOT / ".claude-plugin" / "marketplace.json", {
        "name": cfg.get("marketplaceName", "trip-angle"),
        "owner": {"name": cfg.get("owner", {}).get("name", "Trip Angle")},
        "metadata": {"description": cfg.get("description", ""), "version": version},
        "plugins": plugins,
    })


# ---------------------------------------------------------------- dist

def write_dist(cfg, cats, items, bundles, collections=(), journeys=()):
    dist = hc.DIST
    if dist.exists():
        shutil.rmtree(dist)
    shutil.copytree(hc.SITE, dist, ignore=shutil.ignore_patterns("admin.html", "admin.js", ".DS_Store"))
    idx = dist / "index.html"
    base_url = (cfg.get("siteUrl") or "").rstrip("/")
    html = idx.read_text(encoding="utf-8")
    if base_url:
        html = html.replace("%%SITE_URL%%", base_url)
    else:  # sem endereço público, as tags de pré-visualização não teriam URL válida
        html = "\n".join(l for l in html.split("\n") if "%%SITE_URL%%" not in l)
    idx.write_text(html, encoding="utf-8")
    shutil.copytree(hc.COMPONENTS, dist / "components", ignore=shutil.ignore_patterns(".DS_Store", "__pycache__"))
    counts = {t["id"]: 0 for t in hc.TYPES}
    cat_counts = {}
    for it in items:
        counts[it["type"]] += 1
        cat_counts[it["category"]] = cat_counts.get(it["category"], 0) + 1
    cats_out = sorted([dict(c, count=cat_counts.get(c["id"], 0)) for c in cats], key=lambda c: c["order"])
    public_cfg = {k: cfg.get(k) for k in ("name", "shortName", "tagline", "description", "siteUrl", "githubRepo",
                                           "branch", "marketplaceName", "owner", "socials", "cta")}
    catalog = {
        "schemaVersion": 1,
        "generatedAt": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
        "hub": public_cfg,
        "types": [dict(t, count=counts[t["id"]]) for t in hc.TYPES],
        "categories": cats_out,
        "counts": dict(counts, total=len(items)),
        "bundles": bundles,
        "collections": list(collections),
        "journeys": list(journeys),
        "items": sorted(items, key=lambda x: (x["type"], x["category"], x["name"])),
    }
    api = dist / "api"
    blob = json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
    (api).mkdir(parents=True, exist_ok=True)
    (api / "catalog.json").write_text(blob, encoding="utf-8")
    for t in hc.TYPES:
        sub = [i for i in catalog["items"] if i["type"] == t["id"]]
        hc.write_json(api / f"{t['id']}.json", {"type": t["id"], "count": len(sub), "items": sub})
    hc.write_json(api / "version.json", {
        "generatedAt": catalog["generatedAt"], "counts": catalog["counts"],
        "sha256": hashlib.sha256(blob.encode("utf-8")).hexdigest(),
    })
    # CLI com a origem padrão embutida
    cli = (hc.ROOT / "tools" / "tahub.py")
    if cli.exists():
        text = cli.read_text(encoding="utf-8").replace(SOURCE_PLACEHOLDER, cfg.get("siteUrl") or "")
        (dist / "tahub.py").write_text(text, encoding="utf-8")
    mp = hc.ROOT / ".claude-plugin" / "marketplace.json"
    if mp.exists():
        shutil.copy2(mp, dist / "marketplace.json")
    (dist / ".nojekyll").write_text("", encoding="utf-8")
    write_llms(cfg, catalog, dist)
    write_feed(cfg, catalog, dist)
    return catalog


def write_llms(cfg, catalog, dist):
    base = (cfg.get("siteUrl") or "").rstrip("/")
    lines = [f"# {cfg.get('name', 'Central de IA Trip Angle')}", "", f"> {cfg.get('description', '')}", "",
             f"Catálogo em JSON: {base}/api/catalog.json. Instalador: {base}/tahub.py (Python 3.9+, sem dependências).", ""]
    for t in catalog["types"]:
        sub = [i for i in catalog["items"] if i["type"] == t["id"]]
        if not sub:
            continue
        lines.append(f"## {t['label']} ({len(sub)})")
        for i in sub:
            lines.append(f"- {i['category']}/{i['name']}: {i['description'][:160]}")
        lines.append("")
    (dist / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


def write_feed(cfg, catalog, dist):
    """RSS 2.0 com os 50 componentes mais recentes (para newsletter, WhatsApp ou leitor de RSS)."""
    import xml.etree.ElementTree as ET
    from email.utils import format_datetime
    base = cfg.get("siteUrl") or ""
    rss = ET.Element("rss", version="2.0")
    ch = ET.SubElement(rss, "channel")
    ET.SubElement(ch, "title").text = cfg.get("name", "Central de IA Trip Angle")
    ET.SubElement(ch, "link").text = base + "/" if base else "./"
    ET.SubElement(ch, "description").text = cfg.get("description", "")
    ET.SubElement(ch, "language").text = "pt-BR"
    tipos = {t["id"]: t["singular"] for t in hc.TYPES}
    recentes = sorted((i for i in catalog["items"] if not i.get("partOf")),
                      key=lambda i: (str(i.get("addedAt") or ""), i["id"]), reverse=True)[:50]
    for i in recentes:
        el = ET.SubElement(ch, "item")
        ET.SubElement(el, "title").text = f"[{tipos.get(i['type'], i['type'])}] {i['title']}"
        link = f"{base}/#/item/{i['id']}" if base else f"#/item/{i['id']}"
        ET.SubElement(el, "link").text = link
        ET.SubElement(el, "guid", isPermaLink="false").text = i["id"]
        ET.SubElement(el, "description").text = i.get("description") or ""
        try:
            d = datetime.datetime.strptime(str(i.get("addedAt")), "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
            ET.SubElement(el, "pubDate").text = format_datetime(d)
        except ValueError:
            pass
    ET.ElementTree(rss).write(dist / "feed.xml", encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    res = build(check_only="--check" in sys.argv)
    sys.exit(0)
