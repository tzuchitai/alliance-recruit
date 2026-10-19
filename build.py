"""Build the site from src.html.

index.html    — full HTML document for GitHub Pages
artifact.html — body-only fragment for the claude.ai Artifact (it adds its own <html>/<head>)
"""
import base64
import pathlib

root = pathlib.Path(__file__).parent
src = (root / "src.html").read_text(encoding="utf-8")


def b64(name):
    return "data:image/png;base64," + base64.b64encode((root / "assets" / name).read_bytes()).decode()


body = src.replace("__ALLIANCE__", b64("alliance-logo.png")).replace("__EDU__", b64("edu-mark.png"))

# src.html starts with charset/viewport metas; keep them only in the full document.
fragment = "\n".join(l for l in body.split("\n") if not l.startswith(('<meta charset', '<meta name="viewport"')))
(root / "artifact.html").write_text(fragment, encoding="utf-8")

head_end = fragment.index("</style>") + len("</style>")
page = (
    '<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="description" content="聯盟動物醫院 2026 獸醫師招募：各分院定位、院長專長、職涯階梯、培育制度與薪資福利。">\n'
    + fragment[:head_end] + "\n</head>\n<body>\n" + fragment[head_end:] + "\n</body>\n</html>\n"
)
(root / "index.html").write_text(page, encoding="utf-8")
print("built index.html and artifact.html")
