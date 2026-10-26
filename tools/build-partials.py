#!/usr/bin/env python3
"""
Graphcent: build-partials.py

There is one footer on this site: partials/footer.html. This script writes it
into every page, replacing whatever <footer>...</footer> is currently there.
That is what makes the footer genuinely shared on a static site with no build
framework: edit the partial, run this, and all pages move together.

{{base}} in the partial is replaced with the relative path back to the site
root for each page ('' at root, '../' one level down, and so on).

    python3 tools/build-partials.py
    python3 tools/inline-icons.py     # run this after, to fill the icons
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTIAL = os.path.join(ROOT, 'partials', 'footer.html')
FOOTER = re.compile(r'<footer>.*?</footer>', re.S)


def main():
    src = open(PARTIAL, encoding='utf-8').read().strip()
    written, skipped = 0, []

    for page in sorted(glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)):
        if os.path.relpath(page, ROOT).startswith('partials'):
            continue
        html = open(page, encoding='utf-8').read()
        if not FOOTER.search(html):
            skipped.append(os.path.relpath(page, ROOT))
            continue
        depth = os.path.relpath(page, ROOT).count(os.sep)
        base = '../' * depth
        # 404.html is served for any missing URL at any depth, so its links
        # must start from the site root or they break on nested paths
        if os.path.relpath(page, ROOT) == '404.html':
            base = '/'
        html = FOOTER.sub(lambda _: src.replace('{{base}}', base), html, count=1)
        open(page, 'w', encoding='utf-8').write(html)
        written += 1

    print('footer synced into %d pages' % written)
    if skipped:
        print('no <footer> found in: ' + ', '.join(skipped))


if __name__ == '__main__':
    main()
