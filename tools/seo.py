"""Search and social metadata for every page. Run LAST, after any page builder:

    python3 tools/make-og.py .   (only when images or titles change)
    python3 tools/seo.py .

Per page: title, description (<=160), canonical, Open Graph and X/Twitter tags kept identical to the
title/description, a 1200x630 JPG preview (assets/og/), icon links + web manifest, structured data
(page type + breadcrumbs), and the sitemap with lastmod dates. Idempotent.
"""
import sys, os, re, json, html, datetime, hashlib, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_projects import ORDER, CARDS

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
BASE = 'https://graphcent.com'
TODAY = datetime.date.today().isoformat()
esc = lambda t: html.escape(t, quote=True)

OG = {  # page -> (og image under assets/, alt)
    'index.html': ('images/og-graphcent.png', 'Graphcent: creative and marketing studio, Kano, Nigeria'),
    'work/index.html': ('og/work.jpg', 'Graphcent selected work: identities, digital products and packaging'),
    'studio/index.html': ('og/studio.jpg', 'The Graphcent studio'),
    'insights/index.html': ('og/insights.jpg', 'Graphcent insights'),
    'insights/what-makes-a-website-work/index.html': ('og/article-what-makes-a-website-work.jpg', 'What makes a website actually work for a business? The AMEA story'),
    'insights/why-a-logo-is-not-a-brand/index.html': ('og/article-why-a-logo-is-not-a-brand.jpg', 'Why a logo is not a brand: the Pegasus Interiors story'),
    'contact/index.html': ('og/contact.jpg', 'Contact Graphcent'),
    'brief/index.html': ('og/brief.jpg', 'Send Graphcent a project brief'),
}
for s in ORDER:
    OG[f'work/{s}/index.html'] = (f'og/work-{s}.jpg', f'{html.unescape(CARDS[s]["name"])}: {html.unescape(CARDS[s]["rt"]).lower()} by Graphcent')

TITLES = {
    'insights/what-makes-a-website-work/index.html': 'What makes a website actually work for a business? · Graphcent',
    'insights/why-a-logo-is-not-a-brand/index.html': 'Why a logo is not a brand · Graphcent Insights',
    'insights/index.html': 'Insights: Graphcent',
}
DESCS = {
    'work/ajyad/index.html': 'Brand identity for Ajyad Investments: one liquid drop in three colours for oil and gas, real estate and agriculture. By Graphcent, Kano.',
    'work/colorwaves/index.html': 'Naming and brand identity for ColorWaves, a paint, interiors and design company: a wave that becomes a W, in every colour. By Graphcent.',
    'work/onemajlis/index.html': 'UI/UX design and rebranding for OneMajlis, a halal community platform: a dome and three figures, and the product at onemajlis.com.',
    'work/pegasus-interiors/index.html': 'Brand identity for Pegasus Interiors, Kano: a stronger Pegasus symbol, logo system, emblem, colour and stationery. By Graphcent.',
    'insights/why-a-logo-is-not-a-brand/index.html': 'Pegasus Interiors asked Graphcent for a better logo. What they needed was a brand. The story of one WhatsApp brief and the difference.',
    'insights/what-makes-a-website-work/index.html': 'AMEA’s website was down. How Graphcent rebuilt amea.ng end to end: code, forms that arrive, search, launch and handing over every login.',
    'insights/index.html': 'Ideas, lessons and stories from the work Graphcent does across branding, design, web and marketing. Studio notes from Kano, Nigeria.',
    'index.html': 'Graphcent is a creative and marketing studio in Kano, Nigeria: brand identity, UI/UX, web design and development, marketing, printing and 3D signage.',
    'work/i-mac-academy/index.html': 'Brand identity for I-MAC, a media academy: a wordmark where the i is a microphone and the m is an open book. By Graphcent, Kano.',
    'work/onims/index.html': 'Rebranding Onims Agro Solutions: a circular N with two leaves in its negative space, a green palette and a full brand system. By Graphcent.',
    'work/aiff-26/index.html': 'Arewa Islamic Finance Forum 2026: creative direction, event branding and print consultation by Graphcent, from social campaign to stage and venue.',
    '404.html': 'This page could not be found. Head back to the Graphcent homepage or see our work.',
}
CRUMB = {'work': 'Work', 'studio': 'Studio', 'insights': 'Insights', 'contact': 'Contact', 'brief': 'Brief',
         'privacy-policy': 'Privacy Policy', 'terms-of-service': 'Terms of Service', 'cookie-policy': 'Cookie Policy'}
PAGE_TYPE = {'studio/index.html': 'AboutPage', 'contact/index.html': 'ContactPage', 'work/index.html': 'CollectionPage',
             'insights/index.html': 'CollectionPage'}
ORG = {'@type': 'Organization', '@id': BASE + '/#organization', 'name': 'Graphcent', 'url': BASE + '/',
       'logo': BASE + '/assets/icons/icon-512.png'}


def get(s, pat):
    m = re.search(pat, s, re.S)
    return html.unescape(m.group(1)) if m else ''


def set_meta(s, attr, key, val, after):
    tag = f'<meta {attr}="{key}" content="{esc(val)}">'
    pat = re.compile(rf'<meta {attr}="{re.escape(key)}" content="[^"]*">')
    if pat.search(s):
        return pat.sub(lambda m: tag, s, count=1)
    i = s.index(after) + len(after)
    return s[:i] + '\n' + tag + s[i:]


def rel(p, target):
    depth = p.count('/')
    return '../' * depth + target


pages = []
for dp, dn, fn in os.walk(ROOT):
    if any(x in dp for x in ('node_modules', 'partials', 'tools', '/assets')):
        continue
    for f in fn:
        if f.endswith('.html'):
            pages.append(os.path.relpath(os.path.join(dp, f), ROOT))
pages.sort()
sitemap = []
for p in pages:
    fp = os.path.join(ROOT, p)
    s = open(fp, encoding='utf-8').read()
    # title + description
    if p in TITLES:
        s = re.sub(r'<title>.*?</title>', f'<title>{esc(TITLES[p])}</title>', s, count=1)
    if p in DESCS:
        s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(DESCS[p])}">', s, count=1)
    title = get(s, r'<title>(.*?)</title>')
    desc = get(s, r'<meta name="description" content="([^"]*)"')
    canon = get(s, r'<link rel="canonical" href="([^"]*)"')
    if p == '404.html':
        canon = canon or BASE + '/404.html'
    # social: identical to title/description
    img, alt = OG.get(p, ('images/og-graphcent.png', 'Graphcent: creative and marketing studio, Kano, Nigeria'))
    # versioned by content, so WhatsApp, LinkedIn, X and Facebook fetch a new preview whenever the image changes
    with open(os.path.join(ROOT, 'assets', img), 'rb') as fh:
        ver = hashlib.sha1(fh.read()).hexdigest()[:8]
    url = f'{BASE}/assets/{img}?v={ver}'
    a = '<link rel="canonical" href="' + get(s, r'<link rel="canonical" href="([^"]*)"') + '">' if '<link rel="canonical"' in s else '<meta name="description"'
    anchor = re.search(r'<meta name="description" content="[^"]*">', s).group(0)
    for key, val in (('og:title', title), ('og:description', desc), ('og:url', canon), ('og:image', url),
                     ('og:image:secure_url', url), ('og:image:type', 'image/png' if img.endswith('.png') else 'image/jpeg'),
                     ('og:image:width', '1200'), ('og:image:height', '630'), ('og:image:alt', alt),
                     ('og:locale', 'en_NG'), ('og:site_name', 'Graphcent')):
        s = set_meta(s, 'property', key, val, anchor)
    for key, val in (('twitter:card', 'summary_large_image'), ('twitter:title', title), ('twitter:description', desc),
                     ('twitter:image', url), ('twitter:image:alt', alt)):
        s = set_meta(s, 'name', key, val, anchor)
    s = set_meta(s, 'name', 'referrer', 'strict-origin-when-cross-origin', anchor)
    # icons + manifest
    s = re.sub(r'\n?<link rel="(?:icon|apple-touch-icon|manifest|shortcut icon)"[^>]*>', '', s)
    icons = (f'\n<link rel="icon" href="{rel(p, "favicon.ico")}" sizes="48x48">'
             f'\n<link rel="icon" href="{rel(p, "assets/icons/favicon.svg")}" type="image/svg+xml">'
             f'\n<link rel="icon" href="{rel(p, "assets/icons/favicon-32.png")}" type="image/png" sizes="32x32">'
             f'\n<link rel="apple-touch-icon" href="{rel(p, "assets/icons/apple-touch-icon.png")}">'
             f'\n<link rel="manifest" href="{rel(p, "site.webmanifest")}">')
    tc = re.search(r'<meta name="theme-color"[^>]*>', s)
    i = tc.end() if tc else s.index('</title>') + len('</title>')
    s = s[:i] + icons + s[i:]
    # version the site's own CSS/JS by content, so a returning visitor never runs a stale cached copy
    def _ver(m):
        path = os.path.normpath(os.path.join(ROOT, os.path.dirname(p), m.group(2)))
        if not os.path.isfile(path):
            return m.group(0)
        h = hashlib.md5(open(path, 'rb').read()).hexdigest()[:8]
        return f'{m.group(1)}{m.group(2)}?v={h}{m.group(3)}'
    s = re.sub(r'((?:src|href)=")((?:\.\./)*assets/(?:css|js)/[\w.-]+\.(?:css|js))(?:\?v=\w+)?(")', _ver, s)
    # structured data for the page (the homepage keeps its own business data)
    s = re.sub(r'\n?<script type="application/ld\+json" id="ld-page">.*?</script>', '', s, flags=re.S)
    if p != 'index.html' and p != '404.html':
        parts = p.split('/')[:-1]
        crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'}]
        for k, part in enumerate(parts):
            name = CRUMB.get(part) or re.sub(r'\s*[:·|].*$', '', title)
            crumbs.append({'@type': 'ListItem', 'position': k + 2, 'name': name, 'item': f'{BASE}/{"/".join(parts[:k + 1])}/'})
        graph = [{'@type': 'BreadcrumbList', 'itemListElement': crumbs}]
        if p.startswith('work/') and p != 'work/index.html':
            slug = parts[1]
            c = CARDS.get(slug, {})
            cw = {'@type': 'CreativeWork', 'name': html.unescape(c.get('name', title)), 'headline': title, 'description': desc,
                  'url': canon, 'image': url, 'creator': ORG, 'genre': html.unescape(c.get('rt', ''))}
            if c.get('year'):
                cw['dateCreated'] = c['year']
            graph.append(cw)
        elif p.startswith('insights/') and p != 'insights/index.html':
            pass  # articles carry their own Article schema
        else:
            graph.append({'@type': PAGE_TYPE.get(p, 'WebPage'), 'name': title, 'description': desc, 'url': canon,
                          'isPartOf': {'@type': 'WebSite', 'name': 'Graphcent', 'url': BASE + '/'}, 'publisher': ORG})
        ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
        s = s.replace('</head>', f'<script type="application/ld+json" id="ld-page">{ld}</script>\n</head>', 1)
    # articles: point their Article schema at the JPG preview
    s = re.sub(r'("image": ")https://graphcent\.com/assets/[^"]+(")', lambda m: m.group(1) + url + m.group(2), s) if p.startswith('insights/') and p != 'insights/index.html' else s
    open(fp, 'w', encoding='utf-8').write(s)
    if p != '404.html' and 'noindex' not in s:
        sitemap.append(canon)
    print(f'{p:46s} {len(title):3d}ch title  {len(desc):3d}ch desc  og:{img}')

# sitemap
pri = lambda u: '1.0' if u == BASE + '/' else '0.8' if u.count('/') <= 4 else '0.6'
xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
order = [BASE + '/'] + sorted(u for u in sitemap if u != BASE + '/')
for u in order:
    xml.append(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{pri(u)}</priority></url>')
xml.append('</urlset>')
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('\n'.join(xml) + '\n')
open(os.path.join(ROOT, 'robots.txt'), 'w').write(
    'User-agent: *\nAllow: /\nDisallow: /tools/\nDisallow: /partials/\n\nSitemap: https://graphcent.com/sitemap.xml\n')
print('sitemap:', len(order), 'URLs')
