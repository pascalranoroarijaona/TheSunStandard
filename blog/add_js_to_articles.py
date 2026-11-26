import glob, os

TARGET_FILES = [
    "l-univers-participatif.html",
    "le-monde-est-complexe.html",
    "nautile-nakamoto.html",
    "matrice-inversee.html",
    "nakamoto-riemann.html",
    "ornoir_ornum.html",
    "weboflife.html",
    "wood-wide-web.html",
    "horloge-cosmo-btc-cadran-mu.html",
    "horizon-zero-2044.html",
]

SCRIPT_TAG = '<script defer src="corpus-atlas.js"></script>\n</body>'

for fname in TARGET_FILES:
    if not os.path.exists(fname):
        print(f"Skipped (not found): {fname}")
        continue
    with open(fname, "r", encoding="utf-8") as f:
        html = f.read()

    updated = False
    if "corpus-atlas.js" not in html and "</body>" in html:
        html = html.replace("</body>", SCRIPT_TAG, 1)
        updated = True

    if f'href="https://www.thesunstandard.net/blog/{fname}"' not in html and "</title>" in html:
        canonical = f'</title>\n    <link rel="canonical" href="https://www.thesunstandard.net/blog/{fname}" />'
        html = html.replace("</title>", canonical, 1)
        updated = True

    if updated:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated: {fname}")
    else:
        print(f"Already up to date: {fname}")