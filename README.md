# Yifan Hao's personal website

Live site: https://haoyifan99.github.io/

The website is static HTML, CSS, and a small progressive enhancement script. GitHub Pages serves the repository root.

## Update content

- Edit `publications.json` for publication metadata. Homepage selections and the complete research page are generated from the same source.
- Edit `build_site.py` for the biography, experience, teaching, awards, and other page copy.
- Replace `cv.pdf` with the current public CV.
- Run `python3 build_site.py` and commit the generated HTML alongside the source changes.

## Preview

Run `python3 -m http.server 8765 --bind 127.0.0.1`, then open http://127.0.0.1:8765/.

The existing `Bio.html`, `research.html`, and `Miscellaneous.html` URLs remain supported. All publication entries are present in HTML without JavaScript; the optional topic filter is enabled only when JavaScript runs.
