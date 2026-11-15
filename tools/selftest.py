#!/usr/bin/env python3
"""Teste de ponta a ponta da Central Trip Angle (não altera o projeto).

Copia o repositório para uma pasta temporária, gera o site, sobe o admin e um servidor
estático, instala um componente de cada tipo num projeto vazio pelo HTTP (como um usuário
faria) e confere os arquivos gravados. Uso:  python3 tools/selftest.py
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OK, FAIL = [], []


def check(nome, cond, detalhe=""):
    (OK if cond else FAIL).append(nome)
    print(("  ✓ " if cond else "  ✗ ") + nome + ("" if cond or not detalhe else f"  → {detalhe}"))


def porta_livre():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def esperar(url, seg=20):
    fim = time.time() + seg
    while time.time() < fim:
        try:
            urllib.request.urlopen(url, timeout=2).read()
            return True
        except Exception:  # noqa: BLE001
            time.sleep(0.3)
    return False


def post(url, corpo):
    req = urllib.request.Request(url, data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read() or b"{}")
        except Exception:  # noqa: BLE001
            return {"ok": False, "error": f"HTTP {e.code}"}


def get_json(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read())


def main():
    tmp = Path(tempfile.mkdtemp(prefix="tahub-selftest-"))
    copia = tmp / "hub"
    shutil.copytree(REPO, copia, ignore=shutil.ignore_patterns("dist", ".trash", ".cache", "__pycache__", ".git"))
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=copia, check=False)
    procs = []
    try:
        print("1. Build")
        r = subprocess.run([sys.executable, "tools/build.py"], cwd=copia, capture_output=True, text=True)
        check("build roda sem erro", r.returncode == 0, r.stderr[-400:])
        cat = json.loads((copia / "dist/api/catalog.json").read_text())
        check("catálogo tem itens", cat["counts"]["total"] > 0)
        check("marketplace gerado", (copia / ".claude-plugin/marketplace.json").exists())
        check("instalador publicado em dist/tahub.py", (copia / "dist/tahub.py").exists())

        print("2. Painel admin")
        pa = porta_livre()
        procs.append(subprocess.Popen([sys.executable, "tools/admin.py", "--port", str(pa), "--no-open"], cwd=copia,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        base = f"http://127.0.0.1:{pa}"
        check("admin responde", esperar(base + "/admin-api/ping"))
        j = get_json(base + "/admin-api/ping")
        check("ping ok", j.get("ok") is True, j)
        skill = "---\nname: teste-selftest\ndescription: Skill de teste do selftest.\n---\n\n# Teste\n"
        j = post(base + "/admin-api/component", {"type": "skills", "category": "copy", "name": "teste-selftest",
                                                  "content": skill, "meta": {"tags": ["teste"]}})
        check("criar skill pelo admin", j.get("ok") is True, j)
        cat = get_json(base + "/api/catalog.json")
        ids = {i["id"] for i in cat["items"]}
        check("skill nova aparece no catálogo", "skills/copy/teste-selftest" in ids)
        j = post(base + "/admin-api/component", {"type": "mcps", "category": "automacao", "name": "mcp-invalido", "content": "{nao json"})
        check("MCP com JSON inválido é recusado", j.get("ok") is False)
        j = post(base + "/admin-api/component/delete", {"id": "skills/copy/teste-selftest"})
        check("excluir vai para .trash", j.get("ok") is True and (copia / ".trash").exists(), j)
        req = urllib.request.Request(base + "/admin-api/ping", headers={"Host": "evil.example"})
        try:
            urllib.request.urlopen(req, timeout=5)
            check("Host estranho recusado", False)
        except urllib.error.HTTPError:
            check("Host estranho recusado", True)
        tah = urllib.request.urlopen(base + "/tahub.py", timeout=10).read().decode()
        check("admin injeta a origem no tahub.py", f"127.0.0.1:{pa}" in tah or f"localhost:{pa}" in tah)

        print("3. Instalação como usuário (HTTP)")
        subprocess.run([sys.executable, "tools/build.py"], cwd=copia, capture_output=True)
        ps = porta_livre()
        procs.append(subprocess.Popen([sys.executable, "-m", "http.server", str(ps), "--bind", "127.0.0.1",
                                       "--directory", str(copia / "dist")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        origem = f"http://127.0.0.1:{ps}"
        check("servidor estático responde", esperar(origem + "/api/catalog.json"))
        cat = get_json(origem + "/api/catalog.json")
        proj = tmp / "projeto"
        proj.mkdir()
        home = tmp / "home"
        (home / ".claude").mkdir(parents=True)
        env = dict(os.environ, HOME=str(home), CLAUDE_CONFIG_DIR=str(home / ".claude"), TAHUB_SOURCE=origem, PATH="/usr/bin:/bin")
        cli = str(copia / "dist/tahub.py")

        def roda(*args):
            return subprocess.run([sys.executable, cli, *args, "--yes", "-d", str(proj)], env=env, capture_output=True, text=True, timeout=180)

        pegar = {}
        for it in cat["items"]:
            if not it.get("partOf") and it["type"] not in pegar:
                pegar[it["type"]] = it
        for tipo, it in sorted(pegar.items()):
            flag = next(t["flag"] for t in cat["types"] if t["id"] == tipo)
            if tipo in ("repos", "plugins", "sites"):
                continue
            r = roda(flag, f"{it['category']}/{it['name']}")
            check(f"instala {tipo} ({it['name']})", r.returncode == 0, (r.stdout + r.stderr)[-500:])
        if "skills" in pegar:
            check("skill gravada em .claude/skills", (proj / ".claude/skills" / pegar["skills"]["name"] / "SKILL.md").exists())
        if "agents" in pegar:
            check("agente gravado em .claude/agents", (proj / ".claude/agents" / (pegar["agents"]["name"] + ".md")).exists())
        if "commands" in pegar:
            check("comando gravado em .claude/commands", (proj / ".claude/commands" / (pegar["commands"]["name"] + ".md")).exists())
        if "mcps" in pegar:
            mcp = json.loads((proj / ".mcp.json").read_text()) if (proj / ".mcp.json").exists() else {}
            check(".mcp.json com mcpServers", bool(mcp.get("mcpServers")))
        if "hooks" in pegar or "settings" in pegar:
            sl = proj / ".claude/settings.local.json"
            check("settings.local.json válido", sl.exists() and isinstance(json.loads(sl.read_text()), dict))
        if "hooks" in pegar:
            antes = (proj / ".claude/settings.local.json").read_text()
            roda("--hook", f"{pegar['hooks']['category']}/{pegar['hooks']['name']}")
            depois = (proj / ".claude/settings.local.json").read_text()
            check("reinstalar hook não duplica", json.loads(antes) == json.loads(depois))
        r = subprocess.run([sys.executable, cli, "--search", "copy"], env=env, capture_output=True, text=True, timeout=60)
        check("busca pelo terminal", r.returncode == 0 and "copy" in r.stdout.lower())
        r = subprocess.run([sys.executable, cli, "--health-check"], env=env, capture_output=True, text=True, timeout=60, cwd=proj)
        check("health-check roda", r.returncode in (0, 1) and r.stdout.strip() != "")
        if cat.get("bundles"):
            b = cat["bundles"][0]["name"]
            r = subprocess.run([sys.executable, cli, "--plugin", b, "--scope", "user", "--yes", "-d", str(proj)],
                               env=dict(env, TAHUB_SOURCE=str(copia / "dist")), capture_output=True, text=True, timeout=60)
            us = home / ".claude/settings.json"
            dados = json.loads(us.read_text()) if us.exists() else {}
            check(f"kit {b} habilitado no escopo user", r.returncode == 0 and any(k.startswith(b + "@") for k in dados.get("enabledPlugins", {})),
                  (r.stdout + r.stderr)[-400:])
    finally:
        for p in procs:
            p.terminate()
        for p in procs:
            try:
                p.wait(timeout=5)
            except Exception:  # noqa: BLE001
                p.kill()
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"\n{len(OK)} ok, {len(FAIL)} falhas")
    if FAIL:
        print("Falhas: " + "; ".join(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
