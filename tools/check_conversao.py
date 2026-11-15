import sys, importlib.util
from pathlib import Path
root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "tools"))
import hubcore as h
spec = importlib.util.spec_from_file_location("tahub", root / "tools/tahub.py"); t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
txt = '---\ntitle: T\ndescription: D\nvariables:\n  a: "[obrigatório] Campo A"\n  b: "[padrão = 10] Campo B"\n---\nUse {{a}} e {{b}} e {{c}}.\n'
it = {"category": "x", "name": "y", "title": "T"}
bad = 0
for f in list((root / "components/prompts").glob("*/*.md")) + [None]:
    text = txt if f is None else f.read_text(encoding="utf-8")
    item = it if f is None else {"category": f.parent.name, "name": f.stem}
    if h.prompt_to_command(text, item) != t.prompt_to_command(text, item): bad += 1; print("DIFERE", f)
for f in (root / "components/frameworks").glob("*/*.md"):
    item = {"category": f.parent.name, "name": f.stem}
    if h.framework_to_skill(f.read_text(encoding="utf-8"), item) != t.framework_to_skill(f.read_text(encoding="utf-8"), item): bad += 1; print("DIFERE", f)
print("diferenças:", bad)
print(h.prompt_to_command(txt, it))
