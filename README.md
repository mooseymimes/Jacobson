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
further pages without touching the rest of the site. No build step, no
dependencies — open `index.html` in any browser (works on mobile) or serve
with any static host (e.g. GitHub Pages).

## Local preview

```
python3 -m http.server 8000
# then open http://localhost:8000
```
