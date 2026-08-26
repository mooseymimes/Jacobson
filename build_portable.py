#!/usr/bin/env python3
"""Build portable.html — a single self-contained file for opening directly
from phone storage (content:// / file:// URIs), where browsers can't load a
page's sibling CSS/JS/image files.

Reads the modular site (the source of truth), inlines the stylesheet and
images as data URIs, converts each page into a <section class="route">, and
rewrites internal links to hash routes handled by a small inline router.

Usage: python3 build_portable.py   (writes portable.html in the repo root)
"""

import base64
import mimetypes
import posixpath
import re
from pathlib import Path

ROOT = Path(__file__).parent

# (source file, hash route). Order = order of sections in the file.
PAGES = [
    ("index.html", "home"),
    ("about.html", "about"),
    ("teaching.html", "teaching"),
    ("econ101-syllabus.html", "econ101"),
    ("contact.html", "contact"),
    ("dissertation/index.html", "dissertation"),
    ("dissertation/growth.html", "growth"),
    ("dissertation/education.html", "education"),
    ("dissertation/society.html", "society"),
    ("dissertation/sectors.html", "sectors"),
    ("dissertation/convergence.html", "convergence"),
    ("dissertation/bibliography.html", "bibliography"),
    ("articles/index.html", "articles"),
    ("articles/adryn-smith-response.html", "adryn"),
    ("articles/adryn-smith-hw2.html", "adryn2"),
    ("articles/supply-and-demand.html", "supplydemand"),
    ("articles/dragon-champion-review.html", "dragonchampion"),
]

# filename -> route, used when rewriting hrefs
ROUTE_OF = {src: route for src, route in PAGES}


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def rewrite_href(href: str, page_dir: str) -> str:
    """Map an internal link to its hash route, resolving it relative to the
    directory of the page it appears on."""
    if href.startswith(("http", "#", "mailto:")):
        return href
    clean = posixpath.normpath(posixpath.join(page_dir, href.split("#")[0]))
    route = ROUTE_OF.get(clean)
    return f"#{route}" if route else href


def extract_content(html: str, page_dir: str) -> str:
    """Grab everything between the shared header and footer (hero + main),
    plus any page-local <style class="article-style"> block from the head."""
    m = re.search(r"</header>(.*)<footer class=\"site-footer\">", html, re.S)
    body = m.group(1)
    body = re.sub(
        r'(href=")([^"]+)(")',
        lambda mm: mm.group(1) + rewrite_href(mm.group(2), page_dir) + mm.group(3),
        body,
    )
    # inline images
    def img_sub(mm):
        rel = mm.group(2).replace("../", "")
        return mm.group(1) + data_uri(ROOT / rel) + mm.group(3)

    body = re.sub(r'(src=")((?:\.\./)?assets/img/[^"]+)(")', img_sub, body)

    # carry over the page's unique design, if it declares one
    style = re.search(r'<style class="article-style">(.*?)</style>', html, re.S)
    if style:
        body = f"<style>{style.group(1)}</style>\n" + body

    # keep page-local scripts (e.g. the archive filter) that live inside <main>
    return body.strip()


def extract_page_script(html: str) -> str:
    """Return any inline <script> other than the shared main.js include."""
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    return "\n".join(scripts)


def main():
    css = (ROOT / "assets/css/main.css").read_text()

    sections = []
    page_scripts = []
    for src, route in PAGES:
        html = (ROOT / src).read_text()
        content = extract_content(html, posixpath.dirname(src))
        sections.append(f'<section class="route" id="route-{route}">\n{content}\n</section>')
        script = extract_page_script(html)
        if script:
            page_scripts.append(script)

    nav_items = "\n".join(
        f'          <li><a data-page="{p}" href="#{r}">{label}</a></li>'
        for p, r, label in [
            ("home", "home", "Home"),
            ("about", "about", "About"),
            ("dissertation", "dissertation", "The Dissertation"),
            ("articles", "articles", "Scholarly Articles"),
            ("teaching", "teaching", "Teaching"),
            ("contact", "contact", "Contact"),
        ]
    )

    # which nav item to highlight for each route
    nav_page = {r: r for _, r in PAGES}
    for r in ("growth", "education", "society", "sectors", "convergence", "bibliography"):
        nav_page[r] = "dissertation"
    nav_page["adryn"] = "articles"
    nav_page["adryn2"] = "articles"
    nav_page["supplydemand"] = "articles"
    nav_page["dragonchampion"] = "articles"
    nav_page["econ101"] = "teaching"

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dr. Paul Jacobson — Colossus of Economic Thought</title>
  <meta name="description" content="The official website of Dr. Paul Jacobson — single-file portable edition.">
  <style>
{css}
  .route {{ display: none; }}
  .route.active {{ display: block; }}
  </style>
</head>
<body data-page="home">

  <header class="site-header">
    <div class="nav-bar">
      <a class="brand" href="#home">Dr. Paul Jacobson<small>Department of Economics</small></a>
      <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">&#9776;</button>
      <nav class="site-nav">
        <ul>
{nav_items}
        </ul>
      </nav>
    </div>
  </header>

{chr(10).join(sections)}

  <footer class="site-footer">
    <div class="inner">
      <span>&copy; Dr. Paul Jacobson. All insights reserved.</span>
      <span><a href="#dissertation">The Dissertation</a> &middot; <a href="#contact">Contact</a></span>
    </div>
  </footer>

  <script>
  (function () {{
    var NAV_PAGE = {nav_page!r};

    var toggle = document.querySelector(".nav-toggle");
    var nav = document.querySelector(".site-nav");
    toggle.addEventListener("click", function () {{
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }});

    function show() {{
      var route = (location.hash || "#home").slice(1);
      if (!document.getElementById("route-" + route)) route = "home";
      document.querySelectorAll(".route").forEach(function (s) {{
        s.classList.toggle("active", s.id === "route-" + route);
      }});
      var page = NAV_PAGE[route] || "home";
      document.querySelectorAll(".site-nav a[data-page]").forEach(function (a) {{
        a.classList.toggle("active", a.getAttribute("data-page") === page);
      }});
      nav.classList.remove("open");
      window.scrollTo(0, 0);
    }}

    window.addEventListener("hashchange", show);
    show();
  }})();
  </script>
  <script>
{chr(10).join(page_scripts)}
  </script>
</body>
</html>
"""
    out = ROOT / "portable.html"
    out.write_text(page)
    print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
