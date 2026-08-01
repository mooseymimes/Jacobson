# Dr. Paul Jacobson — Official Website

A mobile-first, modular static website for Dr. Paul Jacobson, colossus of economic
thought (by any objective measure, particularly his own), featuring his dissertation
*The Miracle on the Han River* as a dedicated section with per-chapter pages.

## Structure

```
index.html                    Home — hero + subcategory cards
about.html                    About the Author (persona from the source document)
teaching.html                 Courses
contact.html                  Contact & office hours
articles/
  index.html                  Scholarly Articles archive (searchable; scales
                              beyond what a nav menu could hold)
  adryn-smith-response.html   No. 001 — referee report on Adryn Smith's
                              homework ("graded paper" design)
dissertation/
  index.html                  Dissertation hub: abstract + table of contents
  growth.html                 Ch. I  — GDP trajectory
  education.html              Ch. II — Human capital & growth accounting
  society.html                Ch. III — Demographic headwinds
  sectors.html                Ch. IV — Sectoral transformation
  convergence.html            Ch. V  — Development accounting vs. the US
  bibliography.html           Ch. VI — Sources
assets/
  css/main.css                Shared stylesheet (mobile-first)
  js/main.js                  Shared nav toggle + active-link marking
  img/                        Figures and photos extracted from the source PDF
```

Every section is its own page, so any card/subcategory can be expanded into
further pages without touching the rest of the site.

Articles are deliberately free-form: each page may declare its own design in a
`<style class="article-style">` block in its `<head>` (prefix its classes,
e.g. `.aj1-`, to keep them page-local). The portable build carries these
per-article styles along automatically. New articles only need an entry in the
archive list (`articles/index.html`) and, for the portable build, one line in
`build_portable.py`'s `PAGES` list. No build step, no
dependencies — serve with any static host (e.g. GitHub Pages) or open
`index.html` in a desktop browser.

## Opening on a phone (portable.html)

Android opens files from storage as `content://` URIs and only grants the
browser access to that single file — sibling CSS/JS/images and links to other
pages won't load. For that case use **`portable.html`**: a single
self-contained build (inlined styles, embedded images, hash-based section
navigation). Download just that one file to your phone and open it.

Regenerate it after editing the site:

```
python3 build_portable.py
```

The modular pages remain the source of truth; `portable.html` is generated.

## Local preview

```
python3 -m http.server 8000
# then open http://localhost:8000
```

## Hosting note

For the full multi-page experience on mobile, host the repo (e.g. enable
GitHub Pages in the repository settings) and visit the URL — no workaround
needed then.
