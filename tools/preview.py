"""Gera preview.html: o README renderizado pelo GitHub, com o tema escuro do GitHub.

Corre:  python tools/preview.py   (precisa do gh com login feito)
"""
import base64
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

md = (ROOT / "README.md").read_text(encoding="utf-8")
body = subprocess.run(
    ["gh", "api", "markdown", "--input", "-"],
    input=json.dumps({"text": md, "mode": "markdown", "context": "m1ke26/m1ke26"}),
    capture_output=True, text=True, encoding="utf-8", check=True,
).stdout


def inline(m):
    path = ROOT / m.group(1)
    if not path.is_file():
        return m.group(0)
    data = base64.b64encode(path.read_bytes()).decode()
    return f'src="data:image/svg+xml;base64,{data}"'


body = re.sub(r'src="((?!https?:|data:)[^"]+\.svg)"', inline, body)

page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Preview perfil</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown-dark.min.css">
<style>body{{background:#0d1117;margin:0;padding:32px 16px}}.markdown-body{{max-width:840px;margin:auto;border:1px solid #30363d;border-radius:6px;padding:32px}}</style>
</head><body><article class="markdown-body">{body}</article></body></html>"""
(ROOT / "preview.html").write_text(page, encoding="utf-8")
print(ROOT / "preview.html")
