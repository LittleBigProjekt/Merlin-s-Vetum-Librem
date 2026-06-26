#!/usr/bin/env python3
"""Genera el sitio estático HTML desde content/."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SITE = ROOT / "site"
PAGES = SITE / "pages"

SECTIONS = [
    {
        "id": "arquitectura",
        "title": "Arquitectura",
        "subtitle": "Mapa del codex",
        "items": [
            ("arch-tectonics", "Arch & Tectonics", "00-arquitectura/arch-tectonics.md"),
        ],
    },
    {
        "id": "prolog",
        "title": "Prólogo",
        "subtitle": "Das Licht — Kapitel 0",
        "items": [
            ("prolog", "Prolog — Das Licht", "01-prolog/prolog-kapitel-0.md"),
        ],
    },
    {
        "id": "fundamentos",
        "title": "Fundamentos",
        "subtitle": "Liber I — De Fundamentis",
        "items": [
            ("fundamentis", "Liber I — De Fundamentis", "02-fundamentos/liber-i-fundamentis.md"),
        ],
    },
    {
        "id": "nucleo",
        "title": "Núcleo",
        "subtitle": "There will be light — Kapitel I–V",
        "items": [
            ("kapitel-01", "Kapitel I — Die Grenze", "03-nucleo/kapitel-01-grenze.md"),
            ("kapitel-02", "Kapitel II — Die Dualität", "03-nucleo/kapitel-02-dualitaet.md"),
            ("kapitel-03", "Kapitel III — Das Werkzeug", "03-nucleo/kapitel-03-werkzeug.md"),
            ("kapitel-04", "Kapitel IV — Die Zeit", "03-nucleo/kapitel-04-zeit.md"),
            ("kapitel-05", "Kapitel V — Das Fraktal", "03-nucleo/kapitel-05-fraktal.md"),
        ],
    },
    {
        "id": "capitulos",
        "title": "Capítulos latinos",
        "subtitle": "Profundización temática",
        "items": [
            ("caput-x", "Caput X — De Duobus Radiis", "04-capitulos/caput-x-duobus-radiis.md"),
            ("caput-xii", "Caput XII — De Trinitate Radii", "04-capitulos/caput-xii-trinitas-radii.md"),
            ("caput-xiii-xv", "Caput XIII–XV — Homine · Oculi · Aether", "04-capitulos/caput-xiii-xv-homine-aether.md"),
            ("caput-xvi", "Caput XVI — De Forma Mundi", "04-capitulos/caput-xvi-forma-mundi.md"),
            ("caput-xx", "Caput XX — Trinitas Ignis", "04-capitulos/caput-xx-trinitas-ignis.md"),
            ("caput-xxi", "Caput XXI — Sköll & Hati", "04-capitulos/caput-xxi-skoell-hati.md"),
            ("caput-xxii", "Caput XXII — Jörmungandr", "04-capitulos/caput-xxii-jormungandr.md"),
        ],
    },
    {
        "id": "intermezzo",
        "title": "Intermezzo",
        "subtitle": "Puente hacia Loki",
        "items": [
            ("intermezzo-apfel", "Der Apfel, der keiner war", "05-intermezzo/apfel-loki.md"),
        ],
    },
    {
        "id": "extras",
        "title": "Extras",
        "subtitle": "Runas y bocetos",
        "items": [
            ("runa", "Runa — Mantra", "assets/runa.md"),
            ("bocetos", "Depidgeons — Bocetos", "99-bocetos/depidgeons.md"),
        ],
    },
]


def md_to_html(text: str) -> str:
    lines = text.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    in_ul = False
    in_table = False
    table_rows: list[list[str]] = []

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def flush_table():
        nonlocal in_table, table_rows
        if not in_table:
            return
        if table_rows:
            out.append('<div class="table-wrap"><table>')
            for i, row in enumerate(table_rows):
                tag = "th" if i == 0 else "td"
                cells = "".join(f"<{tag}>{html.escape(c.strip())}</{tag}>" for c in row)
                out.append(f"<tr>{cells}</tr>")
            out.append("</table></div>")
        in_table = False
        table_rows = []

    for raw in lines:
        line = raw.rstrip()

        if line.strip().startswith("|") and "|" in line.strip()[1:]:
            close_ul()
            cells = [c for c in line.strip().strip("|").split("|")]
            if all(re.match(r"^[-: ]+$", c) for c in cells):
                continue
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            continue

        flush_table()

        if re.match(r"^---+$", line.strip()):
            close_ul()
            out.append("<hr>")
            continue

        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            close_ul()
            level = len(m.group(1))
            title = inline(m.group(2))
            out.append(f"<h{level}>{title}</h{level}>")
            continue

        if re.match(r"^[-*]\s+", line):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            item = inline(re.sub(r"^[-*]\s+", "", line))
            out.append(f"<li>{item}</li>")
            continue

        if re.match(r"^\d+\.\s+", line):
            close_ul()
            item = inline(re.sub(r"^\d+\.\s+", "", line))
            out.append(f"<p class=\"numbered\">{item}</p>")
            continue

        if line.strip().startswith(">"):
            close_ul()
            quote = inline(line.strip().lstrip(">").strip())
            out.append(f"<blockquote>{quote}</blockquote>")
            continue

        if not line.strip():
            close_ul()
            out.append("")
            continue

        close_ul()
        out.append(f"<p>{inline(line)}</p>")

    close_ul()
    flush_table()
    return "\n".join(out)


def inline(text: str) -> str:
    t = html.escape(text)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def nav_html(current_slug: str | None, ordered: list[tuple[str, str, str]]) -> str:
    parts = ['<nav class="page-nav">', '<a class="nav-home" href="../index.html">← Índice</a>']
    idx = next((i for i, (slug, _, _) in enumerate(ordered) if slug == current_slug), None)
    if idx is not None:
        if idx > 0:
            prev_slug, prev_title, _ = ordered[idx - 1]
            parts.append(f'<a class="nav-prev" href="{prev_slug}.html">← {html.escape(prev_title)}</a>')
        if idx < len(ordered) - 1:
            next_slug, next_title, _ = ordered[idx + 1]
            parts.append(f'<a class="nav-next" href="{next_slug}.html">{html.escape(next_title)} →</a>')
    parts.append("</nav>")
    return "\n".join(parts)


def page_shell(title: str, body: str, nav: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} — Merlin's Vetum Librem</title>
  <link rel="stylesheet" href="../css/style.css">
</head>
<body>
  <header class="site-header">
    <a href="../index.html" class="brand">Merlin's Vetum Librem</a>
    <span class="tagline">Vetus Librem · Liber I</span>
  </header>
  <main class="content">
    {nav}
    <article class="prose">
      {body}
    </article>
    {nav}
  </main>
  <footer class="site-footer">
    <p>Collage of an answer to some old questions…</p>
  </footer>
</body>
</html>
"""


def index_shell(sections_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Merlin's Vetum Librem</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body class="index-page">
  <header class="hero">
    <p class="hero-eyebrow">Vetus Librem · Liber I</p>
    <h1>Merlin's Vetum Librem</h1>
    <p class="hero-lead">Collage of an answer to some old questions…</p>
    <p class="hero-desc">Un codex cosmológico fractal: Nullpunkt, Licht, Liebe, Grenze, Zeit, Fraktal.</p>
  </header>
  <main class="index-main">
    {sections_html}
  </main>
  <footer class="site-footer">
    <p>Abre cualquier capítulo para leer. Orden recomendado: Prólogo → Fundamentos → Núcleo → Capítulos.</p>
  </footer>
</body>
</html>
"""


def build() -> None:
    PAGES.mkdir(parents=True, exist_ok=True)
    (SITE / "css").mkdir(parents=True, exist_ok=True)

    ordered: list[tuple[str, str, str]] = []
    for section in SECTIONS:
        for slug, title, rel_path in section["items"]:
            ordered.append((slug, title, rel_path))

    for slug, title, rel_path in ordered:
        src = CONTENT / rel_path
        if not src.exists():
            raise FileNotFoundError(f"Missing source: {src}")
        body = md_to_html(src.read_text(encoding="utf-8"))
        nav = nav_html(slug, ordered)
        page = page_shell(title, body, nav)
        (PAGES / f"{slug}.html").write_text(page, encoding="utf-8")

    sections_parts: list[str] = []
    for section in SECTIONS:
        cards = []
        for slug, title, _ in section["items"]:
            cards.append(
                f'<li><a href="pages/{slug}.html"><span class="card-title">{html.escape(title)}</span></a></li>'
            )
        sections_parts.append(
            f"""<section class="index-section" id="{section['id']}">
  <header class="section-head">
    <h2>{html.escape(section['title'])}</h2>
    <p>{html.escape(section['subtitle'])}</p>
  </header>
  <ul class="card-list">{''.join(cards)}</ul>
</section>"""
        )

    (SITE / "index.html").write_text(index_shell("\n".join(sections_parts)), encoding="utf-8")
    print(f"Built {len(ordered)} pages + index.html")


if __name__ == "__main__":
    build()
