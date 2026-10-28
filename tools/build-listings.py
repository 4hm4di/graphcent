"""Rebuild every project listing from tools/site_projects.py.

Run from the site root:  python3 tools/build-listings.py .
Updates: Work page grid + count, homepage selected work, project reel, featured case study,
service hover previews, data.js PROJECTS / SERVICES peeks, sitemap.
"""
import sys, os, re, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_projects import ORDER, CARDS, FEATURE

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
N = len(ORDER)
WORDS = {8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen'}
FEATURED = FEATURE['slug']
SERVICE_PEEK = {  # service title -> image path (from assets/projects)
    'Brand Identity': 'onims/world/branding.webp',
    'UI/UX Design': 'onemajlis/product/site-hero.webp',
    'Web Design &amp; Development': 'amea/hero.webp',
    'Creative Direction': 'aiff-26/hero.webp',
    'Graphic Design': 'gurasar/world/pizza-boxes.webp',
    'Printing &amp; 3D Signage Fabrication': 'pegasus-interiors/mockups/signage.webp',
    'Social Media Management': 'aiff-26/social/05-tickets-open.webp',
    'Marketing': 'reclaim-and-renew/world/billboard.webp',
}
PEEK_ALT = {
    'Brand Identity': 'Onims stationery set, brand identity by Graphcent',
    'UI/UX Design': 'The onemajlis.com homepage, UI/UX design by Graphcent',
    'Web Design &amp; Development': 'The amea.ng homepage, designed and built by Graphcent',
    'Creative Direction': 'The AIFF \u201926 welcome banner, creative direction by Graphcent',
    'Graphic Design': 'Gurasar pizza boxes, packaging design by Graphcent',
    'Printing &amp; 3D Signage Fabrication': 'Pegasus Interiors 3D steel shopfront letters',
    'Social Media Management': 'An AIFF \u201926 tickets announcement post',
    'Marketing': 'A Reclaim and Renew campaign billboard: Cleaner Streets, Brighter Future',
}


def read(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def write(p, s): open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)


def block(s, start):
    """Return (start, end) of the element opening at index start (balanced <div>)."""
    depth, i = 0, start
    tag = re.compile(r'<(/?)div\b[^>]*>')
    for m in tag.finditer(s, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start, m.end()
    raise ValueError('unbalanced')


def meta(slug, i, pre):
    c = CARDS[slug]
    yr = f'<span>{c["year"]}</span>' if c['year'] else ''
    chips = ''.join(f'<span class="schip">{x}</span>' for x in c['chips'])
    return (f'<div class="projmeta"><h3>{c["name"]} <span class="ar" aria-hidden="true">&rarr;</span></h3>'
            f'<div class="rt"><span class="idx">{i:02d} / {N:02d}</span><span>{c["rt"]}</span>{yr}</div></div>'
            f'<div class="chips">{chips}</div><p class="desc">{c["desc"]}</p>')


def frame(slug, pre):
    c = CARDS[slug]
    return (f'<div class="frame"><img src="{pre}assets/projects/{slug}/thumbnail.webp" alt="{html.escape(html.unescape(c["alt"]))}" '
            f'loading="lazy" decoding="async" width="1600" height="1200"></div>')


# ---- Work page ------------------------------------------------------------------------------
w = read('work/index.html')
a = w.index('<div class="works stack" id="workgrid">')
a, b = block(w, a)
WK = ['w8', 'w8', 'w4 off', 'w5', 'w6', 'w6 off', 'w7', 'w7 off', 'w5', 'w5 off', 'w8', 'w4 off']
cards = ''.join(f'<a class="proj pinrow {WK[i % len(WK)]} rv" data-cat="{CARDS[s]["filter"]}" href="../work/{s}/index.html">{frame(s, "../")}'
                f'<div class="pinfo"><span class="ptrack" aria-hidden="true"><i></i></span>{meta(s, i + 1, "../")}</div></a>'
                for i, s in enumerate(ORDER))
w = w[:a] + '<div class="works stack" id="workgrid"><h2 class="vh">All projects</h2>' + cards + '</div>' + w[b:]
LABELS = {'event-branding': 'Event Branding', 'brand-identity': 'Brand Identity', 'ui-ux': 'UI/UX', 'web-design': 'Web Design', 'graphic-design': 'Packaging &amp; Graphic Design'}
used = [k for k in LABELS if any(CARDS[x]['filter'] == k for x in ORDER)]
fb = '<button data-filter="all" aria-pressed="true">All</button>' + ''.join(f'<button data-filter="{k}" aria-pressed="false">{LABELS[k]}</button>' for k in used)
w = re.sub(r'(<div class="filters" data-filters[^>]*>).*?(</div>)', lambda m: m.group(1) + fb + m.group(2), w, count=1, flags=re.S)
w = re.sub(r'<span data-count-label>\d+</span>', f'<span data-count-label>{N}</span>', w)
w = w.replace('Every project below is published in full on Behance.', 'Every project below has its own case study.')
write('work/index.html', w)

# ---- Homepage -------------------------------------------------------------------------------
s = read('index.html')
i = s.index('<div class="works"', s.index('Selected work'))
a, b = block(s, i)
HK = ['w8', 'w4 off', 'w5', 'w7 off', 'w6', 'w6 off']
sel = ''.join(f'<a class="proj {HK[k]} rv" data-cat="{CARDS[x]["filter"]}" href="work/{x}/index.html">{frame(x, "")}{meta(x, ORDER.index(x) + 1, "")}</a>'
              for k, x in enumerate(ORDER[:6]))
open_tag = re.match(r'<div class="works"[^>]*>', s[a:]).group(0)
s = s[:a] + open_tag + sel + '</div>' + s[b:]
s = re.sub(r'<p class="lede rv">\w+ projects across identity, digital product, web and production\.[^<]*</p>',
           f'<p class="lede rv">{WORDS.get(N, N)} projects across identity, digital product, web and packaging, each with its own case study.</p>', s)
# reel
i = s.index('<div class="marquee reel rtl" data-marquee aria-label="Project reel"><div class="track">')
t0 = s.index('<div class="track">', i)
a, b = block(s, t0)
reel = ''.join(f'<a class="card" href="work/{x}/index.html">{frame(x, "")}<div class="cap"><b>{CARDS[x]["name"]} <span class="ar" aria-hidden="true">&rarr;</span></b><span>{CARDS[x]["rt"]}</span></div></a>'
               for x in ORDER)
s = s[:a] + '<div class="track">' + reel + '</div>' + s[b:]
# featured case study
i = s.index('<p class="eyebrow">Featured case study</p>')
sa = s.rindex('<section', 0, i); sb = s.index('</section>', i) + len('</section>')
c = CARDS[FEATURED]
F = FEATURE
feat = ('<section class="sect dark"><div class="wrap">\n<p class="eyebrow">Featured case study</p>\n'
        f'<a class="proj rv" href="work/{FEATURED}/index.html" style="display:block;margin-top:clamp(22px,3vw,40px)"><div class="frame">'
        f'<img src="assets/projects/{FEATURED}/{F["img"]}" alt="{html.escape(F["alt"])}" loading="lazy" decoding="async" width="{F["w"]}" height="{F["h"]}"></div>'
        '<div class="chips">' + ''.join(f'<span class="schip">{x}</span>' for x in c['chips']) + '</div></a>\n'
        f'<div class="split" style="margin-top:clamp(30px,4vw,54px);align-items:end"><h2 class="dl rv">{F["title"]}</h2>'
        f'<p class="lede rv">{F["lede"]}</p></div>\n'
        '<div class="cols3 rv" style="margin-top:clamp(36px,5vw,72px)">' + ''.join(f'<div><h2>{k}</h2><p class="lede sm">{v}</p></div>' for k, v in F['cols']) + '</div>\n'
        f'<div style="margin-top:clamp(32px,4vw,58px)"><a class="tlink" href="work/{FEATURED}/index.html">VIEW CASE STUDY <span class="ar" aria-hidden="true">&rarr;</span></a></div>\n</div></section>')
s = s[:sa] + feat + s[sb:]
# service previews
for title, path in SERVICE_PEEK.items():
    m = re.search(r'(<a class="srow[^>]*>(?:(?!</a>).)*?<h3>' + re.escape(title) + r'</h3>(?:(?!</a>).)*?)<img[^>]*>', s, re.S)
    if not m:
        print('service row not found:', title); continue
    old = s[m.end(1):m.end()]
    from PIL import Image
    with Image.open(os.path.join(ROOT, 'assets/projects', path)) as im:
        wd, ht = im.size
    cls = re.search(r'class="([^"]*)"', old)
    new = (f'<img{" class=" + chr(34) + cls.group(1) + chr(34) if cls else ""} src="assets/projects/{path}" alt="{html.escape(html.unescape(PEEK_ALT[title]))}" '
           f'loading="lazy" decoding="async" width="{wd}" height="{ht}">')
    s = s[:m.end(1)] + new + s[m.end():]
write('index.html', s)

# ---- data.js ---------------------------------------------------------------------------------
d = read('assets/js/data.js')
d = re.sub(r'(  /\* Public projects, in display order[^\n]*\*/\n)+', '', d)
a = d.index('  const PROJECTS = [')
b = d.index('  ];', a) + len('  ];')
entries = []
for x in ORDER:
    c = CARDS[x]
    entries.append("    { slug: '%s', name: %r, category: %r, filter: '%s', year: '%s',\n      summary: %r }" % (
        x, html.unescape(c['name']), html.unescape(c['rt']), c['filter'], c['year'], html.unescape(c['desc'])))
d = d[:a] + '  /* Public projects, in display order (tools/site_projects.py). */\n  const PROJECTS = [\n' + ',\n'.join(entries) + '\n  ];' + d[b:]
peeks = {'Brand Identity': 'onims/world/branding.webp', 'UI/UX Design': 'onemajlis/product/site-hero.webp',
         'Web Design & Development': 'amea/hero.webp', 'Creative Direction': 'aiff-26/hero.webp',
         'Graphic Design': 'gurasar/world/pizza-boxes.webp', 'Printing & 3D Signage Fabrication': 'pegasus-interiors/mockups/signage.webp',
         'Social Media Management': 'aiff-26/social/05-tickets-open.webp', 'Marketing': 'reclaim-and-renew/world/billboard.webp'}
for t, pth in peeks.items():
    d = re.sub(r"(t: '" + re.escape(t) + r"',[^\n]*?peek: ')[^']*'", lambda m: m.group(1) + pth + "'", d)
write('assets/js/data.js', d)

# ---- sitemap -----------------------------------------------------------------------------------
sm = read('sitemap.xml')
sm = re.sub(r'\s*<url><loc>https://graphcent\.com/work/[^<]+/</loc>[^\n]*</url>', '', sm)
add = ''.join(f'\n  <url><loc>https://graphcent.com/work/{x}/</loc><changefreq>yearly</changefreq></url>' for x in ORDER)
sm = sm.replace('<url><loc>https://graphcent.com/work/</loc>', '<url><loc>https://graphcent.com/work/</loc>', 1)
i = sm.index('</url>', sm.index('<loc>https://graphcent.com/work/</loc>')) + len('</url>')
sm = sm[:i] + add + sm[i:]
write('sitemap.xml', sm)
print('listings rebuilt:', N, 'projects')
