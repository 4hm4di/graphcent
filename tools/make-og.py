"""Make 1200x630 social preview images (assets/og/<name>.jpg) in the Graphcent style.

python3 tools/make-og.py .     (needs Playwright + Chromium; fonts from Google Fonts or local)
Each card: the page's own image on the right, a navy panel with the wordmark, a label, the title
and graphcent.com. JPG, because WhatsApp, LinkedIn and X do not all accept WebP previews.
"""
import sys, os, html
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
FONT_DIR = os.environ.get('GC_FONTS', '/tmp/fonts/node_modules/@fontsource')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from site_projects import ORDER, CARDS

CARDS_OG = []   # (name, label, title, image path(s) relative to ROOT)
for s in ORDER:
    c = CARDS[s]
    img = {'colorwaves': 'assets/projects/colorwaves/world/billboard.webp', 'pegasus-interiors': 'assets/projects/pegasus-interiors/mockups/signage.webp',
           'amea': 'assets/projects/amea/thumbnail.webp'}.get(s, f'assets/projects/{s}/hero.webp')
    CARDS_OG.append((f'work-{s}', html.unescape(c['rt']), html.unescape(c['name']), [img]))
CARDS_OG += [
    ('work', 'Selected work', 'Identities, digital products and packaging.', [f'assets/projects/{s}/thumbnail.webp' for s in ORDER[:4]]),
    ('studio', 'The studio', 'One team for brand, digital and production.', ['assets/images/studio-desk.jpg']),
    ('insights', 'Insights', 'Ideas, lessons and stories from the work.', ['assets/images/insights/02-what-makes-a-website-work.webp', 'assets/images/insights/01-why-a-logo-is-not-a-brand.webp',
                                                                           'assets/images/insights/03-designing-for-nigerian-businesses.webp', 'assets/images/insights/05-from-brand-identity-to-digital-experience.webp']),
    ('article-what-makes-a-website-work', 'Insights · Web', 'What makes a website actually work for a business?', ['assets/projects/amea/thumbnail.webp']),
    ('article-why-a-logo-is-not-a-brand', 'Insights · Branding', 'Why a logo is not a brand', ['assets/projects/pegasus-interiors/mockups/signage.webp']),
    ('contact', 'Contact', 'Tell us what you’re building.', []),
    ('brief', 'Start a project', 'Send us a brief.', []),
]


def font_face(fam, d):
    out = ''
    for w in (500, 600, 700, 800):
        f = f'{FONT_DIR}/{d}/files/{d}-latin-{w}-normal.woff2'
        if os.path.exists(f):
            out += f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{f}') format('woff2')}}"
    return out


CSS = font_face('Archivo', 'archivo') + font_face('Inter Tight', 'inter-tight') + '''
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#0A0B35;color:#F3F2EE;font-family:'Inter Tight',sans-serif;overflow:hidden;position:relative}
.panel{position:absolute;left:0;top:0;bottom:0;width:520px;padding:56px 56px 48px;display:flex;flex-direction:column;justify-content:space-between;z-index:2;background:#0A0B35}
.full .panel{width:1200px}
.logo{height:34px;width:auto;display:block}
.label{font-size:17px;letter-spacing:.16em;text-transform:uppercase;color:rgba(243,242,238,.62);display:flex;align-items:center;gap:12px;font-weight:500}
.label:before{content:"";width:26px;height:1px;background:currentColor}
h1{font-family:'Archivo',sans-serif;font-weight:800;text-transform:uppercase;letter-spacing:-.02em;line-height:.96;font-size:58px;margin-top:18px}
.full h1{font-size:92px;max-width:900px}
.foot{display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(243,242,238,.16);padding-top:20px;font-size:17px;letter-spacing:.12em;text-transform:uppercase;color:rgba(243,242,238,.62)}
.foot b{color:#00CCFF;font-weight:500;letter-spacing:.04em;text-transform:none;font-size:20px}
.media{position:absolute;left:520px;top:0;right:0;bottom:0;background:#E5E3DC;overflow:hidden}
.media img{width:100%;height:100%;object-fit:cover;display:block}
.media.grid{display:grid;grid-template-columns:1fr 1fr;gap:4px;background:#0A0B35}
.mark{position:absolute;right:56px;top:150px;width:300px;opacity:.95}
'''


def page(label, title, imgs):
    logo = open(os.path.join(ROOT, 'assets/logos/graphcent-wordmark-light.svg'), encoding='utf-8').read()
    logo = logo.replace('<svg', '<svg class="logo"', 1)
    if imgs:
        cls = 'grid' if len(imgs) > 1 else ''
        media = f'<div class="media {cls}">' + ''.join(f'<img src="file://{os.path.join(ROOT, i)}">' for i in imgs) + '</div>'
        body = ''
    else:
        media = ''
        body = ' class="full"'
    t = html.escape(title)
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body{body}>'
            f'<div class="panel">{logo}<div><p class="label">{html.escape(label)}</p><h1>{t}</h1></div>'
            f'<div class="foot"><span>Graphcent</span><b>graphcent.com</b></div></div>{media}</body></html>')


os.makedirs(os.path.join(ROOT, 'assets/og'), exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('GC_CHROMIUM') or None)
    pg = b.new_page(viewport={'width': 1200, 'height': 630})
    for name, label, title, imgs in CARDS_OG:
        tmp = os.path.join(ROOT, 'assets/og', f'_{name}.html')
        open(tmp, 'w', encoding='utf-8').write(page(label, title, imgs))
        pg.goto('file://' + tmp); pg.wait_for_timeout(250)
        # long titles: shrink until the panel fits
        pg.evaluate('''() => { const h = document.querySelector('h1'), p = document.querySelector('.panel');
            let s = parseFloat(getComputedStyle(h).fontSize);
            while (p.scrollHeight > p.clientHeight + 1 && s > 30) { s -= 2; h.style.fontSize = s + 'px'; } }''')
        pg.screenshot(path=os.path.join(ROOT, 'assets/og', f'{name}.jpg'), type='jpeg', quality=86)
        os.remove(tmp)
        print('og', name)
    b.close()
