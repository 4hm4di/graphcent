#!/usr/bin/env python3
"""
Graphcent: inline-icons.py

Inlines the supplied SVGs from assets/icons/ui/ into every icon placeholder
in the HTML, so the artwork ships as real inline SVG that inherits
currentColor. No build tooling, no runtime fetch, no sprite.

Markup contract, written once by hand and refreshed by this script:

    <span class="ico" data-icon="services/brand-identity"></span>

The span keeps its data-icon attribute, so running this again after you
edit or replace an SVG re-syncs every page. Safe to run any number of times.

Source templates under partials/ are skipped: those still hold the
placeholder span so tools/build-partials.py can keep inlining fresh icons
into the pages it writes. Only the pages themselves get the SVG inlined.

    python3 tools/inline-icons.py
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, 'assets', 'icons', 'ui')

PLACEHOLDER = re.compile(
    r'(<span class="ico[^"]*" data-icon="([^"]+)"[^>]*>)(.*?)(</span>)',
    re.S
)


def load(name):
    path = os.path.join(ICONS, name + '.svg')
    if not os.path.exists(path):
        return None
    return open(path, encoding='utf-8').read().strip()


def main():
    cache, filled, missing = {}, 0, set()

    for page in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
        if os.path.relpath(page, ROOT).startswith('partials'):
            continue

        src = open(page, encoding='utf-8').read()

        def swap(m):
            nonlocal filled
            name = m.group(2)
            if name not in cache:
                cache[name] = load(name)
            svg = cache[name]
            if svg is None:
                missing.add(name)
                return m.group(0)
            filled += 1
            return m.group(1) + svg + m.group(4)

        out = PLACEHOLDER.sub(swap, src)
        if out != src:
            open(page, 'w', encoding='utf-8').write(out)

    print('icons inlined: %d across the site' % filled)
    if missing:
        print('MISSING from assets/icons/ui/: ' + ', '.join(sorted(missing)))


if __name__ == '__main__':
    main()
