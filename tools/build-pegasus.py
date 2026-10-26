"""Build the Pegasus Interiors case study (work/pegasus-interiors/index.html).

Run from the site root:  python3 tools/build-pegasus.py .
Shell (head, header, CTA, footer) comes from work/amea/index.html. Images live in
assets/projects/pegasus-interiors (converted from the client's Pegasus_Branding_Assets).
"""
import sys, os, re, html
from PIL import Image

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
SLUG = 'pegasus-interiors'
REL = f'../../assets/projects/{SLUG}'
esc = lambda t: html.escape(t, quote=True)
SYMBOL = open(os.path.join(ROOT, f'assets/projects/{SLUG}/symbol-inline.svg'), encoding='utf-8').read()


def size(rel):
    with Image.open(os.path.join(ROOT, rel.replace('../../', ''))) as im:
        return im.size


def img(src, alt, cls='', eager=False, extra=''):
    w, h = size(src)
    c = f' class="{cls}"' if cls else ''
    lazy = '' if eager else ' loading="lazy"'
    return f'<img{c} src="{src}" alt="{esc(alt)}"{lazy} decoding="async" width="{w}" height="{h}"{extra}>'


# logo explorer: version -> (label, description, {light: board, dark: board})
VERSIONS = [
    ('stacked', 'Stacked', 'The primary logo: the Pegasus symbol over the wordmark. For square spaces, signage and social.', {'light': '01', 'dark': '03'}),
    ('horizontal', 'Horizontal', 'The same logo in one line, for headers, letterheads, envelopes and anywhere wide.', {'light': '02', 'dark': '04'}),
    ('tagline', 'With tagline', 'The stacked logo with the brand line, Crafting Timeless Spaces, for moments that introduce the company.', {'light': '05'}),
    ('emblem1', 'Emblem I', 'The circular emblem, a seal for stamps, packaging, watermarks and uniforms.', {'light': '07', 'dark': '09'}),
    ('emblem2', 'Emblem II', 'The second emblem, with the colours reversed between ring and symbol.', {'light': '08', 'dark': '10'}),
]
ver_btns = ''.join(f'<button type="button" data-ver="{v}" data-desc="{esc(d)}" aria-pressed="{str(k == 0).lower()}">{esc(l)}</button>'
                   for k, (v, l, d, _) in enumerate(VERSIONS))
ver_imgs = ''.join(img(f'{REL}/logo/{n}.webp', f'Pegasus Interiors {l.lower()} logo on {bg}', extra=f' data-key="{v}-{bg}"', eager=(v == 'stacked' and bg == 'light'))
                   for v, l, d, boards in VERSIONS for bg, n in boards.items())

COLOURS = [('Pegasus Gold', '#B9934D', 'The symbol, rules and accents.', 'dark'),
           ('Charcoal', '#1A1A1A', 'The wordmark and dark surfaces.', 'light'),
           ('Cream', '#F7F2EC', 'Paper, backgrounds and light surfaces.', 'dark'),
           ('Stone', '#4D4D4D', 'Secondary text: INTERIORS and details.', 'light')]
swatches = ''.join(f'<button type="button" class="pg-swatch" data-swatch="{h}" style="--c:{h}" data-ink="{ink}"><span class="chip" aria-hidden="true"></span>'
                   f'<b>{esc(n)}</b><code>{h}</code><span class="use">{esc(u)}</span><span class="cp" aria-hidden="true">Copy</span></button>'
                   for n, h, u, ink in COLOURS)

DELIVERED = [  # everything in this light identity package
    ('Logo', ['Brand symbol, full colour and mono', 'Stacked logo', 'Horizontal logo', 'Tagline version', 'Two circular emblems', 'Light and dark versions']),
    ('Stationery', ['Business card', 'Letterhead', 'Invoice', 'Envelope', 'Emblem watermark']),
    ('Brand in use', ['Shop signage', 'Door hanger', 'Staff ID card', 'Emblem sticker']),
]
groups = [f'<div class="pg-group"><h3>{g}</h3><ul>' + ''.join(f'<li class="done">{esc(i)}</li>' for i in items) + '</ul></div>'
          for g, items in DELIVERED]

MAIN = f'''<main id="main"><section class="sect dark phero"><div class="wrap"><a class="small" href="../../work/index.html" style="display:inline-block;margin-bottom:clamp(24px,3vw,42px)">&larr; &nbsp;All work</a><div class="split" style="align-items:end"><h1 class="dl rv">PEGASUS<br>INTERIORS</h1><p class="lede rv">Pegasus Interiors came to Graphcent with a logo the whole team liked, and one request: something better. We gave them more than a better logo. We built a brand identity: a logo system, an emblem, a palette and stationery, ready to grow into everything the business touches.</p></div><div class="facts phero-facts rv" data-n="4"><div class="fact"><div class="k">Client</div><div class="v">Pegasus Interiors, Kano</div></div><div class="fact"><div class="k">Category</div><div class="v">Brand identity</div></div><div class="fact"><div class="k">Scope</div><div class="v">Logo system, emblem, colour, stationery</div></div><div class="fact"><div class="k">Services</div><div class="v">Brand Identity, Logo Design, Stationery Design</div></div></div><a class="tlink rv" href="../../insights/why-a-logo-is-not-a-brand/index.html" style="margin-top:clamp(22px,3vw,36px)">Read the story: Why a logo is not a brand <span class="ar" aria-hidden="true">&rarr;</span></a></div></section>

<section class="cs-hero"><div class="wrap"><div class="proj"><div class="frame rv" style="aspect-ratio:auto">{img(f"{REL}/mockups/signage.webp", "The Pegasus Interiors logo as brushed-steel letters on a charcoal shopfront sign", eager=True, extra=' fetchpriority="high"')}</div></div></div></section>

<section class="sect"><div class="wrap"><div class="split">
<div class="rv" style="display:grid;gap:clamp(28px,3.6vw,52px)">
<div><h2 class="ds" style="margin-bottom:14px">The brief</h2><p class="lede" style="max-width:62ch">Pegasus Interiors, an interior design company in Kano, reached out on WhatsApp with their existing logo: a winged horse in front of building outlines. &ldquo;We all like it,&rdquo; they said. &ldquo;It&rsquo;s just that we want something better.&rdquo;</p></div>
<div><h2 class="ds" style="margin-bottom:14px">The approach</h2><p class="lede" style="max-width:62ch">Keep what they loved, the Pegasus and the gold, and rebuild it so it works everywhere. The buildings moved inside the horse: one solid, single-colour symbol that holds up on a favicon, a business card and a billboard. Around it we built the system a brand actually runs on.</p></div>
</div>
<div class="rv"><h3 class="small" style="margin-bottom:16px">Scope</h3><ol class="cs-scope">
<li><i>01</i><b>Brand symbol</b><span>The Pegasus redrawn as one solid shape, with the architecture carried inside the body. Full colour and mono.</span></li>
<li><i>02</i><b>Logo system</b><span>Stacked and horizontal lockups, with and without the tagline, on light and dark.</span></li>
<li><i>03</i><b>Emblem</b><span>Two circular seals for stamps, packaging, watermarks and uniforms, on light and dark.</span></li>
<li><i>04</i><b>Colour</b><span>Pegasus Gold, Charcoal, Cream and Stone: warm, calm and premium, like the spaces they design.</span></li>
<li><i>05</i><b>Stationery</b><span>Business card, letterhead, invoice and envelope, with the emblem as a watermark.</span></li>
</ol></div>
</div>
<div class="cs-nums rv" style="margin-top:clamp(40px,6vw,88px)">
<div><div class="n"><span data-count="3" data-suffix="" data-plain="false">3</span></div><div class="k">Logo forms</div></div>
<div><div class="n"><span data-count="10" data-suffix="" data-plain="false">10</span></div><div class="k">Logo versions</div></div>
<div><div class="n"><span data-count="4" data-suffix="" data-plain="false">4</span></div><div class="k">Brand colours</div></div>
<div><div class="n"><span data-count="4" data-suffix="" data-plain="false">4</span></div><div class="k">Stationery pieces</div></div>
</div>
</div></section>

<section class="sect dark"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">01 &nbsp;Before and after</p><h2 class="dm rv">SAME SPIRIT.<br>STRONGER MARK.</h2></div>
<p class="lede rv">Drag across to compare the logo Pegasus Interiors had with the one we designed.</p></div>
<div class="pg-compare rv" data-compare>
<figure class="pg-before">{img(f"{REL}/before.webp", "The previous Pegasus Interiors logo: an illustrated winged horse in front of thin gold building outlines")}<figcaption>Before</figcaption></figure>
<figure class="pg-after">{img(f"{REL}/logo/05.webp", "The new Pegasus Interiors logo: a solid gold Pegasus symbol over a serif wordmark, with the tagline Crafting Timeless Spaces")}<figcaption>After</figcaption></figure>
<span class="pg-handle" aria-hidden="true"></span>
<input type="range" min="0" max="100" value="50" aria-label="Compare the previous logo, on the left, with the new logo, on the right">
</div>
</div></section>

<section class="sect"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">02 &nbsp;Logo system</p><h2 class="dm rv">ONE MARK,<br>MANY JOBS.</h2></div>
<p class="lede rv">Choose a version, then see it on light and dark.</p></div>
<div class="pg-lab" data-logolab data-tone="light">
<div class="pg-labtools"><div class="filters" role="group" aria-label="Logo version">{ver_btns}</div>
<div class="filters" role="group" aria-label="Background"><button type="button" data-bg="light" aria-pressed="true">On light</button><button type="button" data-bg="dark" aria-pressed="false">On dark</button></div></div>
<div class="pg-stage">{ver_imgs}</div>
<p class="cs-caption" aria-live="polite"></p>
</div>
</div></section>

<section class="sect dark"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">03 &nbsp;Size test</p><h2 class="dm rv">BUILT TO WORK<br>AT ANY SIZE.</h2></div>
<p class="lede rv">A logo lives on a browser tab as much as on a billboard. Shrink both marks and watch which one holds.</p></div>
<div class="pg-scale" data-scale>
<div class="pg-scaleboard">
<figure><div class="pg-box">{img(f"{REL}/before.webp", "The previous logo at the chosen size")}</div><figcaption>Before</figcaption></figure>
<figure><div class="pg-box pg-sym" role="img" aria-label="The new Pegasus symbol at the chosen size">{SYMBOL}</div><figcaption>After</figcaption></figure>
</div>
<label class="pg-range"><span>Size</span><input type="range" min="16" max="320" value="120" step="1"><output>120px</output></label>
</div>
</div></section>

<section class="sect"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">04 &nbsp;Colour</p><h2 class="dm rv">GOLD, CHARCOAL<br>AND CREAM.</h2></div>
<p class="lede rv">Four colours, picked from the materials of a well-finished room: brass, dark timber, warm plaster and stone. Tap a colour to copy it.</p></div>
<div class="pg-swatches">{swatches}</div><p class="vh" data-swatch-live aria-live="polite"></p>
</div></section>

<section class="sect dark"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">05 &nbsp;Stationery</p><h2 class="dm rv">THE BRAND,<br>ON PAPER.</h2></div>
<p class="lede rv">The first things a client holds: a card, a letter, an invoice. Gold rules and a faint emblem watermark tie them together.</p></div>
<div class="pg-paper">
<figure class="c1 rv">{img(f"{REL}/stationery/card-front.webp", "Business card front: the horizontal logo in gold and white on charcoal, with gold rules")}<figcaption>Business card, front</figcaption></figure>
<figure class="c2 rv">{img(f"{REL}/stationery/card-back.webp", "Business card back: name, title and contact details on cream with gold rules and a QR code")}<figcaption>Business card, back</figcaption></figure>
<figure class="env rv">{img(f"{REL}/stationery/envelope.webp", "Envelope: the horizontal logo with the contact panel framed in a gold rule")}<figcaption>Envelope</figcaption></figure>
<figure class="a4 rv">{img(f"{REL}/stationery/letterhead.webp", "Letterhead with the horizontal logo, gold rules and the emblem as a watermark")}<figcaption>Letterhead</figcaption></figure>
<figure class="a4 rv">{img(f"{REL}/stationery/invoice.webp", "Invoice template with itemised table, payment details and totals in gold")}<figcaption>Invoice</figcaption></figure>
</div>
<div class="cs-head pg-gap"><div><p class="eyebrow">06 &nbsp;In the world</p><h2 class="dm rv">FROM THE SIGN<br>TO THE DOOR.</h2></div>
<p class="lede rv">The identity where clients and staff actually meet it: above the shopfront, in a stack of cards, on a door, around a neck.</p></div>
<div class="pg-world">
<figure class="wide rv">{img(f"{REL}/mockups/stationery-set.webp", "The full stationery set: letterhead, business cards, envelope, an emblem sticker and the gold palette cards marked Luxury, Timeless, Memorable and Premium")}<figcaption>Stationery set, with the emblem sticker and palette</figcaption></figure>
<figure class="rv">{img(f"{REL}/mockups/cards-stack.webp", "Stacks of charcoal and cream Pegasus Interiors business cards on a gold background")}<figcaption>Business cards</figcaption></figure>
<figure class="rv">{img(f"{REL}/mockups/door-hanger.webp", "A cream door hanger with the circular emblem on a charcoal door with a copper handle")}<figcaption>Door hanger</figcaption></figure>
<figure class="rv">{img(f"{REL}/mockups/id-badge.webp", "A staff ID card in a gold holder on a gold lanyard, with the horizontal logo")}<figcaption>Staff ID card</figcaption></figure>
</div>
</div></section>

<section class="sect"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">07 &nbsp;Deliverables</p><h2 class="dm rv">WHAT WE<br>DELIVERED.</h2></div>
<p class="lede rv">A light identity package: the essentials a growing business needs to show up the same way on a card, a letter, a door and a shopfront.</p></div>
<div class="pg-groups pg-delivered rv">{"".join(groups)}</div>
</div></section>

<section class="sect dark"><div class="wrap"><div class="nextproj"><span class="small">Credits &nbsp;&nbsp; Brand identity by Graphcent</span><a class="tlink" href="../../work/colorwaves/index.html">Next project: ColorWaves<span class="ar" aria-hidden="true">&rarr;</span></a></div></div></section>'''

src = open(os.path.join(ROOT, 'work/amea/index.html'), encoding='utf-8').read()
a = src.index('<main id="main">')
cta_a = src.index('<section class="sect cta dark" id="start">')
cta_b = src.index('</main>') + len('</main>')
page = src[:a] + MAIN + '\n' + src[cta_a:cta_b] + src[cta_b:]

title = 'Pegasus Interiors: Brand Identity: Graphcent'
desc = ('Pegasus Interiors: a brand identity by Graphcent. A stronger Pegasus symbol, a logo system and emblem, '
        'a gold, charcoal and cream palette, and stationery for an interior design company in Kano.')
page = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', page, count=1)
for prop in ('og:title', 'twitter:title'):
    page = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', rf'\g<1>{esc(title)}', page)
for prop in ('description', 'og:description', 'twitter:description'):
    page = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', rf'\g<1>{esc(desc)}', page)
page = page.replace('https://graphcent.com/work/amea/', f'https://graphcent.com/work/{SLUG}/')
os.makedirs(os.path.join(ROOT, f'work/{SLUG}'), exist_ok=True)
open(os.path.join(ROOT, f'work/{SLUG}/index.html'), 'w', encoding='utf-8').write(page)
print(f'built work/{SLUG}/index.html')
