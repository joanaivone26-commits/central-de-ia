#!/usr/bin/env python3
"""Importa a central de repositórios (catálogos JSON pesquisados) para a Central de IA Trip Angle.

Uso:
  python3 tools/importar_catalogo_repos.py <pasta-dados> [--atualizar]

A pasta precisa ter um ou mais destes arquivos (formato dos catálogos da aula de edição de vídeo com IA):
  catalogo-video.json · catalogo-audio.json · catalogo-lipsync.json · catalogo-mcp.json · alternativas-comerciais.json

Cada repositório vira components/repos/<categoria>/<nome>.json com a ficha técnica completa (função, melhor uso,
Mac, hardware, licenças, uso comercial, status...). As ferramentas comerciais viram components/sites/.
Sem --atualizar, itens que já existem (mesma URL) são mantidos como estão.
"""
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hubcore as hc  # noqa: E402

CATALOGOS = {
    "catalogo-video.json": "video-ia",
    "catalogo-audio.json": "audio-voz",
    "catalogo-lipsync.json": "lipsync-avatar",
    "catalogo-mcp.json": "video-ia",
}
AREAS = {"Lip sync e avatar": "lipsync-avatar", "Vídeo e edição": "video-ia", "Voz e áudio": "audio-voz"}
SUBCATS = {
    "geracao-video": "Geração de vídeo", "edicao-programatica": "Edição por código", "base-edicao": "Base de edição",
    "upscale": "Upscale", "comfyui": "ComfyUI", "visao-rostos": "Visão e rostos", "automacao-cortes": "Cortes automáticos",
    "apple-silicon": "Apple Silicon", "gui-editor": "Editor visual", "shorts-automaticos": "Shorts automáticos",
    "matting-fundo": "Recorte de fundo", "interpolacao": "Interpolação", "remocao-objetos": "Remoção de objetos",
    "transcricao": "Transcrição", "clonagem-voz": "Clonagem de voz", "tts": "Texto para fala", "diarizacao": "Diarização",
    "legendas": "Legendas", "audio-generativo": "Áudio generativo", "separacao": "Separação de faixas",
    "dublagem-pipeline": "Dublagem", "alinhamento": "Alinhamento", "realce-audio": "Realce de áudio",
    "conversao-voz": "Conversão de voz", "talking-head-foto": "Foto falante", "lip-sync-video": "Lip sync em vídeo",
    "comfyui-no": "Nó de ComfyUI", "visemas-2d": "Visemas 2D", "restauracao-facial": "Restauração facial",
    "retrato-animado": "Retrato animado", "medicao-sincronia": "Medição de sincronia", "mcp": "MCP e skills",
}
CAMPOS = [  # (campo do catálogo, rótulo na ficha)
    ("melhor_uso", "Melhor uso"), ("entrada_saida", "Entrada → saída"), ("mac_apple_silicon", "Roda no Mac"),
    ("nota_mac", "Nota sobre o Mac"), ("hardware", "Hardware"), ("licenca_codigo", "Licença do código"),
    ("licenca_pesos", "Licença dos pesos"), ("licenca", "Licença"), ("uso_comercial", "Uso comercial"),
    ("status", "Status"), ("ultima_atividade", "Última atividade"), ("versao_recente", "Versão recente"),
    ("nivel", "Nível"), ("portugues_br", "Português (BR)"), ("qualidade", "Qualidade"), ("no_comfyui", "No ComfyUI"),
    ("funciona_no_claude", "Funciona no Claude"), ("funciona_no_codex", "Funciona no Codex"),
    ("ferramentas_expostas", "Ferramentas expostas"), ("requisitos", "Requisitos"), ("pip", "Instalação"),
    ("observacoes", "Observações"),
]


def estrelas(v):
    s = str(v or "").strip().lower().replace(",", ".")
    m = re.match(r"^([\d.]+)\s*k$", s)
    try:
        return int(float(m.group(1)) * 1000) if m else int(float(s))
    except ValueError:
        return None


REPO_RE = re.compile(r"^https://(github\.com|huggingface\.co|gitlab\.com)/[\w.-]+/[\w.-]+/?$")


def url_repo(v):
    """URL limpa do repositório, ou "" quando o campo é uma anotação (ex.: serviço hospedado sem repo público)."""
    s = str(v or "").strip()
    if not s.startswith("http") and re.match(r"^[\w.-]+/[\w.-]+$", s):
        s = f"https://github.com/{s}"
    s = s.rstrip("/")
    return s if REPO_RE.match(s) else ""


def texto(v):
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    if isinstance(v, bool):
        return "sim" if v else "não"
    return str(v).strip()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    pasta = Path(sys.argv[1]).expanduser()
    atualizar = "--atualizar" in sys.argv
    hoje = datetime.date.today().isoformat()
    existentes = {}
    for f in (hc.COMPONENTS / "repos").glob("*/*.json"):
        if f.name.endswith(hc.SIDE):
            continue
        u = (hc.load_json(f, {}) or {}).get("url", "").rstrip("/").lower()
        if u:
            existentes[u] = f
    novos = atualizados = pulados = 0
    for nome_arq, cat in CATALOGOS.items():
        arq = pasta / nome_arq
        if not arq.exists():
            continue
        for r in json.loads(arq.read_text(encoding="utf-8")):
            url = url_repo(r.get("repo"))
            if not url:
                pulados += 1
                continue
            alvo = existentes.get(url.lower())
            if alvo and not atualizar:
                pulados += 1
                continue
            dono, _, nome_repo = url.replace("https://github.com/", "").partition("/")
            slug = hc.slugify(nome_repo or r.get("nome", "repo"))
            destino = alvo or hc.COMPONENTS / "repos" / cat / f"{slug}.json"
            if not alvo and destino.exists():
                destino = destino.with_name(f"{hc.slugify(dono)}-{slug}.json")
            sub = r.get("categoria") or ""
            detalhes = {rot: texto(r[c]) for c, rot in CAMPOS if r.get(c) not in (None, "", [])}
            dados = {
                "url": url,
                "title": r.get("nome") or nome_repo,
                "description": texto(r.get("funcao") or ""),
                "tags": [t for t in [SUBCATS.get(sub, sub), "mcp" if nome_arq == "catalogo-mcp.json" else ""] if t],
                "stars": estrelas(r.get("estrelas_aprox")),
                "license": texto(r.get("licenca_codigo") or r.get("licenca") or "") or None,
                "subcategoria": SUBCATS.get(sub, sub),
                "detalhes": detalhes,
                "fontes": r.get("fontes") or [],
            }
            destino.parent.mkdir(parents=True, exist_ok=True)
            hc.write_json(destino, dados)
            hc.write_json(destino.with_name(destino.stem + hc.SIDE), {
                "addedAt": hoje,
                "source": {"kind": "catalogo", "note": "Central de repositórios de IA para vídeo e áudio (pesquisa Trip Angle)"},
            })
            existentes[url.lower()] = destino
            if alvo:
                atualizados += 1
            else:
                novos += 1
    alt = pasta / "alternativas-comerciais.json"
    sites = 0
    if alt.exists():
        for a in json.loads(alt.read_text(encoding="utf-8")):
            cat = AREAS.get(a.get("area"), "video-ia")
            slug = hc.slugify(re.sub(r"\(.*?\)", "", a.get("nome", "")).strip() or "ferramenta")
            destino = hc.COMPONENTS / "sites" / cat / f"{slug}.json"
            if destino.exists() and not atualizar:
                continue
            hc.write_json(destino, {"url": a.get("link"), "title": a.get("nome"), "description": a.get("funcao"),
                                    "tags": ["ferramenta comercial", a.get("area", "")], "pricing": "pago ou freemium"})
            hc.write_json(destino.with_name(destino.stem + hc.SIDE), {"addedAt": hoje, "source": {
                "kind": "catalogo", "note": "Alternativas comerciais da central de repositórios (pesquisa Trip Angle)"}})
            sites += 1
    print(f"Repositórios: {novos} novos, {atualizados} atualizados, {pulados} mantidos. Ferramentas: {sites}.")
    print("Rode: python3 tools/build.py")


if __name__ == "__main__":
    main()
