"""Build the identity case studies in tools/identity_projects.py (work/<slug>/index.html).

Run from the site root:  python3 tools/build-identity.py .   (or add slugs to build some)
Shell (head, header, CTA, footer) from work/amea/index.html. Assets prepared into
assets/projects/<slug>/ (hero, thumbnail, world/, guide/) and assets/guides/<slug>-brand-guidelines.pdf.
"""
import sys, os, re, html
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from identity_projects import PROJECTS
from site_projects import next_of

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
ONLY = set(sys.argv[2:])
esc = lambda t: html.escape(t, quote=True)
GOOGLE = {'Inter': 'Inter:wght@400;600', 'DM Sans': 'DM+Sans:wght@400;600', 'Outfit': 'Outfit:wght@400;600',
          'Cabin': 'Cabin:wght@400;600', 'Grand Hotel': 'Grand+Hotel'}


def size(rel):
    with Image.open(os.path.join(ROOT, rel.replace('../../', ''))) as im:
        return im.size


def img(src, alt, cls='', eager=False, extra=''):
    w, h = size(src)
    c = f' class="{cls}"' if cls else ''
    lazy = '' if eager else ' loading="lazy"'
    return f'<img{c} src="{src}" alt="{esc(alt)}"{lazy} decoding="async" width="{w}" height="{h}"{extra}>'


def pdf_info(path):
    try:
        import pymupdf
        with pymupdf.open(path) as d:
            n = len(d)
    except Exception:
        n = 0
    return n, os.path.getsize(path)


def build(P):
    slug = P['slug']; REL = f'../../assets/projects/{slug}'
    name, client = P['name'], P['client']
    guide_pdf = os.path.join(ROOT, f'assets/guides/{slug}-brand-guidelines.pdf')
    has_pdf = os.path.exists(guide_pdf)
    pages, nbytes = pdf_info(guide_pdf) if has_pdf else (0, 0)
    label = P.get('guide_label', 'Brand guidelines')
    n_img = len(P['gallery']) + len(P.get('gallery_pages', []))
    nxt, nxt_name = next_of(slug)
    sec = 0

    def num():
        nonlocal sec; sec += 1; return f'{sec:02d}'

    links = ''
    if P.get('live'):
        host = P['live'].split('//')[1]
        links += f'<a class="tlink rv" href="{esc(P["live"])}" target="_blank" rel="noopener">Visit {esc(host.replace("www.", ""))} <span class="ar" aria-hidden="true">&#8599;</span></a>'
    if has_pdf:
        links += f'<a class="tlink rv" href="#guide">{label} <span class="ar" aria-hidden="true">&darr;</span></a>'
    scope_short = ', '.join(t for t, _ in P['scope'][:4]).replace('&', '&amp;')
    hero = (f'<section class="sect dark phero"><div class="wrap"><a class="small" href="../../work/index.html" style="display:inline-block;margin-bottom:clamp(24px,3vw,42px)">&larr; &nbsp;All work</a>'
            f'<div class="split" style="align-items:end"><h1 class="dl rv">{esc(name).upper()}</h1><p class="lede rv">{P["lede"]}</p></div>'
            f'<div class="facts phero-facts rv" data-n="4"><div class="fact"><div class="k">Client</div><div class="v">{esc(client)}</div></div>'
            f'<div class="fact"><div class="k">Category</div><div class="v">{esc(P["category"])}{(" &middot; " + P["year"]) if P["year"] else ""}</div></div>'
            f'<div class="fact"><div class="k">Scope</div><div class="v">{scope_short}</div></div>'
            f'<div class="fact"><div class="k">Services</div><div class="v">{esc(", ".join(P["services"]))}</div></div></div>'
            + (f'<div class="pj-links">{links}</div>' if links else '') + '</div></section>')
    hero_img = (f'<section class="cs-hero"><div class="wrap"><div class="proj"><div class="frame rv" style="aspect-ratio:auto">'
                f'{img(f"{REL}/hero.webp", f"{name}: {P["category"].lower()} by Graphcent", eager=True, extra=chr(32) + "fetchpriority=" + chr(34) + "high" + chr(34))}</div></div></div></section>')
    scope = ''.join(f'<li><i>{k:02d}</i><b>{esc(t)}</b><span>{esc(d)}</span></li>' for k, (t, d) in enumerate(P['scope'], 1))
    faces = [f for f in dict.fromkeys(P['type'][:1] + P['type'][1:2]) if f]
    nums = [(len(P['palette']), 'Brand colours'), (len(faces), 'Typefaces' if len(faces) > 1 else 'Typeface'), (n_img, 'Applications shown')]
    if has_pdf:
        nums.insert(0, (pages, 'Guide pages'))
    numhtml = ''.join(f'<div><div class="n"><span data-count="{n}" data-suffix="" data-plain="false">{n}</span></div><div class="k">{esc(k)}</div></div>' for n, k in nums)
    intro = (f'<section class="sect"><div class="wrap"><div class="split"><div class="rv" style="display:grid;gap:clamp(28px,3.6vw,52px)">'
             f'<div><h2 class="ds" style="margin-bottom:14px">The brief</h2><p class="lede" style="max-width:62ch">{P["brief"]}</p></div>'
             f'<div><h2 class="ds" style="margin-bottom:14px">The approach</h2><p class="lede" style="max-width:62ch">{P["approach"]}</p></div></div>'
             f'<div class="rv"><h3 class="small" style="margin-bottom:16px">Scope</h3><ol class="cs-scope">{scope}</ol></div></div>'
             f'<div class="cs-nums rv" style="margin-top:clamp(40px,6vw,88px)">{numhtml}</div></div></section>')
    parts = [hero, hero_img, intro]
    tone = ['dark', '']  # alternate section tones after the light intro

    def section(inner, i):
        return f'<section class="sect {tone[i % 2]}"><div class="wrap">{inner}</div></section>'
    k = 0
    # the product (OneMajlis)
    if P.get('product'):
        shots = ''.join(f'<figure class="pj-shot rv"><div class="cs-browser"><div class="cs-bar" aria-hidden="true"><b></b><b></b><b></b><span>{esc(P["live"].split("//")[1])}</span></div>'
                        f'{img(f"{REL}/product/{f}.webp", alt)}</div></figure>' for f, alt in P['product'])
        parts.append(section(f'<div class="cs-head"><div><p class="eyebrow">{num()} &nbsp;The product</p><h2 class="dm rv">LIVE AT<br>{esc(P["live"].split("//")[1].replace("www.", "").upper())}.</h2></div>'
                             f'<p class="lede rv">The product carries the brand: halal interests, companies and individuals, rewards and investment, laid out so each category is one tap away.</p></div>'
                             f'<div class="pj-shots">{shots}</div><a class="btn btn-fill rv" style="margin-top:clamp(22px,3vw,36px)" href="{esc(P["live"])}" target="_blank" rel="noopener">VISIT THE SITE <span class="ar" aria-hidden="true">&#8599;</span></a>', k)); k += 1
    # inside the guide (viewer) + download
    btns, ims = [], []
    for i, (n, lab, desc) in enumerate(P['guide']):
        on = i == 0
        btns.append(f'<button type="button" aria-pressed="{str(on).lower()}" data-desc="{esc(desc)}"><i>{i + 1:02d}</i>{esc(lab)}</button>')
        ims.append(img(f'{REL}/guide/p{n:02d}.webp', f'{name} guide, page {n}: {lab}', cls='on' if on else '', eager=False))
    first = P['guide'][0][2]
    viewer = (f'<div class="cs-console pj-viewer" data-viewer><div class="cs-list" role="group" aria-label="Pages from the {esc(name)} guide">{"".join(btns)}</div>'
              f'<div><div class="cs-stage pj-stage">{"".join(ims)}</div><p class="cs-caption" aria-live="polite">{esc(first)}</p></div></div>')
    dl = ''
    if has_pdf:
        yr = f'{P["year"]} ' if P['year'] else ''
        dl = (f'<div class="dl-card rv" id="guide"><div><p class="eyebrow">Download</p><h3>{esc(name)} {label.lower()}</h3>'
              f'<p class="dl-meta">PDF &middot; {pages} pages &middot; {nbytes / 1e6:.1f} MB &middot; portfolio edition</p>'
              f'<p class="dl-note">For viewing only: contact details removed, not for reuse. &copy; {esc(yr)}{esc(client)}. Design by Graphcent.</p></div>'
              f'<a class="btn btn-fill" href="../../assets/guides/{slug}-brand-guidelines.pdf" download="{slug}-brand-guidelines.pdf">DOWNLOAD PDF <span class="ar" aria-hidden="true">&darr;</span></a></div>')
    parts.append(section(f'<div class="cs-head"><div><p class="eyebrow">{num()} &nbsp;Inside the guide</p><h2 class="dm rv">THE THINKING,<br>PAGE BY PAGE.</h2></div>'
                         f'<p class="lede rv">Pick a page from the {label.lower()}: how the mark is built, what it means, and the rules that keep it consistent.</p></div>{viewer}{dl}', k)); k += 1
    # colour + type
    sw = ''.join(f'<button type="button" class="pg-swatch cw-swatch" data-swatch="{h}" style="--c:{h}" data-ink="{ink}"><span class="chip" aria-hidden="true"></span>'
                 f'<b>{esc(n)}</b><code>{h}</code><span class="cp" aria-hidden="true">Copy</span></button>' for n, h, ink in P['palette'])
    head, body, tester = P['type']
    if tester:
        tbox = (f'<div class="cw-type pj-type" data-typetest><label class="cw-typein"><span>Try {esc(tester)}</span>'
                f'<input type="text" maxlength="60" placeholder="{esc(name)}" autocomplete="off"></label>'
                f'<div class="cw-specimens"><div class="cw-spec"><p class="k">{esc(tester)}</p><p class="cw-out" data-type-out style="font-family:\'{esc(tester)}\',sans-serif"></p></div></div></div>')
    else:
        tbox = f'<p class="pj-typenote">Headings are set in <b>{esc(head)}</b>. See the typography page in the guide above.</p>'
    tnames = ' and '.join(f'<b>{esc(f)}</b>' for f in faces)
    parts.append(section(f'<div class="cs-head"><div><p class="eyebrow">{num()} &nbsp;Colour &amp; type</p><h2 class="dm rv">THE PALETTE.</h2></div>'
                         f'<p class="lede rv">Tap a colour to copy it. Type: {tnames}.</p></div>'
                         f'<div class="cw-swatches n{len(P["palette"])} pj-swatches">{sw}</div><p class="vh" data-swatch-live aria-live="polite"></p>{tbox}', k)); k += 1
    # in the world
    figs = [(name_, alt, cap) for _, name_, alt, cap in P['gallery']] + [(name_, alt, cap) for _, name_, alt, cap in P.get('gallery_pages', [])]
    gal = ''.join(f'<figure>{img(f"{REL}/world/{f}.webp", a)}<figcaption>{esc(c)}</figcaption></figure>' for f, a, c in figs)
    parts.append(section(f'<div class="cs-head"><div><p class="eyebrow">{num()} &nbsp;In the world</p><h2 class="dm rv">THE BRAND<br>IN USE.</h2></div>'
                         f'<p class="lede rv">Where people meet it: {esc(", ".join(c.lower() for _, _, c in figs[:4]))} and more.</p></div><div class="cw-grid">{gal}</div>', k)); k += 1
    # deliverables
    groups = ''.join(f'<div class="pg-group"><h3>{esc(g)}</h3><ul>' + ''.join(f'<li class="done">{esc(i)}</li>' for i in items) + '</ul></div>' for g, items in P['deliverables'])
    parts.append(section(f'<div class="cs-head"><div><p class="eyebrow">{num()} &nbsp;Deliverables</p><h2 class="dm rv">WHAT WE<br>DELIVERED.</h2></div></div>'
                         f'<div class="pg-groups pg-delivered rv">{groups}</div>', k)); k += 1
    credits = (f'<section class="sect dark"><div class="wrap"><div class="nextproj"><span class="small">Credits &nbsp;&nbsp; {esc(P["category"])} by Graphcent</span>'
               f'<a class="tlink" href="../../work/{nxt}/index.html">Next project: {nxt_name} <span class="ar" aria-hidden="true">&rarr;</span></a></div></div></section>')
    if tone[(k - 1) % 2] == 'dark':   # keep the credits band from sitting on another dark section
        credits = credits.replace('class="sect dark"', 'class="sect"', 1)
    parts.append(credits)
    MAIN = '<main id="main">' + '\n'.join(parts)

    src = open(os.path.join(ROOT, 'work/amea/index.html'), encoding='utf-8').read()
    a = src.index('<main id="main">')
    cta_a = src.index('<section class="sect cta dark" id="start">')
    cta_b = src.index('</main>') + len('</main>')
    page = src[:a] + MAIN + '\n' + src[cta_a:cta_b] + src[cta_b:]
    title = f'{name}: {P["category"]}: Graphcent'
    desc = re.sub(r'<[^>]+>|&[a-z]+;', '', P['lede'])[:300]
    page = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', page, count=1)
    for prop in ('og:title', 'twitter:title'):
        page = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', lambda m: m.group(1) + esc(title), page)
    for prop in ('description', 'og:description', 'twitter:description'):
        page = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', lambda m: m.group(1) + esc(desc), page)
    page = page.replace('https://graphcent.com/work/amea/', f'https://graphcent.com/work/{slug}/')
    fams = [GOOGLE[f] for f in dict.fromkeys([P['type'][2]]) if f in GOOGLE]
    if fams:
        page = page.replace('</head>', '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?' + '&amp;'.join('family=' + f for f in fams) + '&amp;display=swap">\n</head>', 1)
    os.makedirs(os.path.join(ROOT, f'work/{slug}'), exist_ok=True)
    open(os.path.join(ROOT, f'work/{slug}/index.html'), 'w', encoding='utf-8').write(page)
    print(f'built work/{slug}/ ({sec} sections, guide {"yes" if has_pdf else "no"})')


for P in PROJECTS:
    if not ONLY or P['slug'] in ONLY:
        build(P)
