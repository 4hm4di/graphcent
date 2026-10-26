"""Build the ColorWaves case study (work/colorwaves/index.html).

Run from the site root:  python3 tools/build-colorwaves.py .
Naming and brand identity. Shell from work/amea/index.html; assets in
assets/projects/colorwaves (converted from the client's Colorwaves_Branding.zip:
mockups, logo files and the 46-page ColorWaves Identity guide).
"""
import sys, os, re, html
from PIL import Image

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
SLUG = 'colorwaves'
REL = f'../../assets/projects/{SLUG}'
esc = lambda t: html.escape(t, quote=True)
MARK = open(os.path.join(ROOT, f'assets/projects/{SLUG}/mark-inline.svg'), encoding='utf-8').read()


def size(rel):
    with Image.open(os.path.join(ROOT, rel.replace('../../', ''))) as im:
        return im.size


def img(src, alt, cls='', eager=False, extra=''):
    w, h = size(src)
    c = f' class="{cls}"' if cls else ''
    lazy = '' if eager else ' loading="lazy"'
    return f'<img{c} src="{src}" alt="{esc(alt)}"{lazy} decoding="async" width="{w}" height="{h}"{extra}>'


# --- 02 the mark ---------------------------------------------------------------------------------
RIBBONS = [('Red', '#E81416'), ('Yellow', '#F9EA36'), ('Green', '#79C214'), ('Coral', '#FF6F61'), ('Blue', '#487DE7'), ('Violet', '#70369D')]
rib_chips = ''.join(f'<button type="button" class="cw-chip" data-rib-chip="{n}" style="--c:{h}"><span aria-hidden="true"></span>{n}</button>' for n, h in RIBBONS)

# --- 03 logo system ------------------------------------------------------------------------------
VERSIONS = [
    ('horizontal', 'Horizontal', 'The primary logo in one line: website headers, business cards, email signatures, social profiles.'),
    ('vertical', 'Vertical', 'Stacked for packaging, signage, promotional pieces and mobile, where width is limited.'),
    ('mark', 'Logomark', 'The W on its own: app icons, favicons, merchandise and anywhere the name is already known.'),
]
ver_btns = ''.join(f'<button type="button" data-ver="{v}" data-desc="{esc(d)}" aria-pressed="{str(k == 0).lower()}">{esc(l)}</button>'
                   for k, (v, l, d) in enumerate(VERSIONS))
ver_imgs = ''.join(img(f'{REL}/logo/{v}-{bg}.webp', f'ColorWaves {l.lower()} logo on {"Cloud White" if bg == "light" else "Midnight Plum"}',
                       extra=f' data-key="{v}-{bg}"', eager=(v == 'horizontal' and bg == 'light'))
                   for v, l, d in VERSIONS for bg in ('light', 'dark'))

# --- 04 colour -----------------------------------------------------------------------------------
PALETTE = [
    ('Primary', 'The rainbow: the core of the brand, one colour per ribbon family.', [
        ('Red', '#E81416', 'light'), ('Orange', '#FFA500', 'dark'), ('Yellow', '#F9EA36', 'dark'), ('Green', '#79C214', 'dark'),
        ('Blue', '#487DE7', 'light'), ('Indigo', '#4B369D', 'light'), ('Violet', '#70369D', 'light')]),
    ('Secondary', 'Warmth and play around the primaries.', [
        ('Coral', '#FF6F61', 'dark'), ('Gold', '#FFD700', 'dark'), ('Lime Green', '#A2D63A', 'dark'), ('Sky Blue', '#2E86C1', 'light')]),
    ('Neutral', 'A calm base that lets the colour do the talking.', [
        ('Cloud White', '#F7F7F7', 'dark'), ('Ash Gray', '#B0B0B0', 'dark'), ('Slate Gray', '#707070', 'light'), ('Midnight Plum', '#1A001A', 'light')]),
]
pal = ''
for name, note, cols in PALETTE:
    sw = ''.join(f'<button type="button" class="pg-swatch cw-swatch" data-swatch="{h}" style="--c:{h}" data-ink="{ink}"><span class="chip" aria-hidden="true"></span>'
                 f'<b>{esc(n)}</b><code>{h}</code><span class="cp" aria-hidden="true">Copy</span></button>' for n, h, ink in cols)
    pal += f'<div class="cw-palrow"><div class="cw-palk"><h3>{name}</h3><p>{esc(note)}</p></div><div class="cw-swatches n{len(cols)}">{sw}</div></div>'

# --- 07 in the world -----------------------------------------------------------------------------
WORLD = [
    ('stationery', 'Stationery', [
        ('stationery-1', 'Letterhead, envelope, business cards and a mug on deep plum, with red and green shapes', 'Letterhead, envelope and cards'),
        ('stationery-2', 'Letterhead, ID card on a green lanyard, mug and clips on plum', 'ID card, letterhead and mug'),
        ('stationery-3', 'A notebook cover with the rainbow pattern, a branded mug and clips in a tray', 'Notebook and mug'),
        ('card-1', 'A white ColorWaves business card on red, green and blue shapes', 'Business card, front'),
        ('card-2', 'A dark ColorWaves business card on red, green and blue shapes', 'Business card, back'),
        ('flash-drive', 'A lime green ColorWaves flash drive', 'Flash drive')]),
    ('products', 'Products & merch', [
        ('paint-buckets', 'ColorWaves paint buckets: Stucco Wave, Artisan Trowel and Perfect Matte, on lime green', 'Product labels'),
        ('cap-pins', 'A grey cap with the W and a spread of branded pin badges', 'Cap and pins'),
        ('tshirts', 'Green, black and white T-shirts with the W and flowing ribbons', 'T-shirts'),
        ('tote-tape', 'A tote bag with the rainbow pattern and a roll of branded tape', 'Tote bag and tape'),
        ('paper-bags', 'Purple paper bags with green handles and rainbow waves', 'Paper bags')]),
    ('campaigns', 'Campaigns', [
        ('billboard', 'A billboard reading Bring your walls to life, with a model and paint buckets', 'Billboard'),
        ('bus-stop', 'A lit bus stop screen announcing the first products', 'Bus stop screen'),
        ('poster-wall', 'Four lit posters in a concrete gallery', 'LED posters'),
        ('train-screen', 'A screen advert at the foot of a station escalator', 'Station screen'),
        ('conference-screen', 'A product launch on a conference hall screen', 'Conference screen'),
        ('eid-poster', 'An Eid al-Adha greeting with a rainbow-coloured ram', 'Eid al-Adha post'),
        ('ramadan-poster', 'A Ramadan Mubarak greeting with a glowing crescent', 'Ramadan post')]),
    ('signage', 'Signage & vehicles', [
        ('wall-3d', 'The ColorWaves logo in 3D letters on a timber reception wall', 'Reception wall'),
        ('signage-3d', 'An outdoor 3D sign naming Coatings, Revitalization and Interiors', 'Outdoor sign'),
        ('street-flags', 'Two ColorWaves banners on a street lamp post', 'Street banners'),
        ('rollup-flags', 'A roll-up banner and lamp post banners', 'Roll-up and banners'),
        ('barrier-banners', 'Two road barrier banners announcing products and interiors', 'Barrier banners'),
        ('vehicles', 'A tricycle, a van and a truck in ColorWaves livery', 'Vehicles')]),
]
set_btns = ''.join(f'<button type="button" data-set="{k}" aria-pressed="{str(i == 0).lower()}">{esc(l)}</button>' for i, (k, l, _) in enumerate(WORLD))
panels = ''.join(
    f'<div class="cw-grid" data-set-panel="{k}"{"" if i == 0 else " hidden"}>' +
    ''.join(f'<figure>{img(f"{REL}/world/{f}.webp", a)}<figcaption>{esc(c)}</figcaption></figure>' for f, a, c in items) + '</div>'
    for i, (k, l, items) in enumerate(WORLD))

DELIVERED = [
    ('Name & voice', ['Brand name', 'Tagline', 'Tone of voice and key messages', 'Brand architecture: three sub-brands']),
    ('Identity', ['Logomark', 'Horizontal and vertical logos', 'Black and white versions', 'Clear space rules', '15-colour palette', 'Maven Pro and Inter']),
    ('Brand in use', ['46-page identity guide', 'Stationery and business cards', 'Merchandise and product labels', 'Campaigns and social posts', 'Signage and vehicle livery']),
]
groups = ''.join(f'<div class="pg-group"><h3>{g}</h3><ul>' + ''.join(f'<li class="done">{esc(i)}</li>' for i in items) + '</ul></div>'
                 for g, items in DELIVERED)

MAIN = f'''<main id="main"><section class="sect dark phero"><div class="wrap"><a class="small" href="../../work/index.html" style="display:inline-block;margin-bottom:clamp(24px,3vw,42px)">&larr; &nbsp;All work</a><div class="split" style="align-items:end"><h1 class="dl rv">COLORWAVES</h1><p class="lede rv">The founder came to Graphcent with a business that would span interiors, paint and architectural design, and no name yet. We started with the name. Then we gave it an identity that means something: one wave of paint that becomes a W, in every colour of the rainbow.</p></div><div class="facts phero-facts rv" data-n="4"><div class="fact"><div class="k">Client</div><div class="v">ColorWaves</div></div><div class="fact"><div class="k">Category</div><div class="v">Naming &amp; brand identity</div></div><div class="fact"><div class="k">Scope</div><div class="v">Name, logo system, colour, type, voice, sub-brands, applications</div></div><div class="fact"><div class="k">Services</div><div class="v">Brand Naming, Brand Identity, Brand Guidelines</div></div></div><div class="pj-links"><a class="tlink rv" href="#guide">Brand guidelines <span class="ar" aria-hidden="true">&darr;</span></a></div></div></section>

<section class="cs-hero"><div class="wrap"><div class="proj"><div class="frame rv" style="aspect-ratio:auto">{img(f"{REL}/world/billboard.webp", "A ColorWaves billboard against the sky: Bring your walls to life, with a model and the paint range", eager=True, extra=' fetchpriority="high"')}</div></div></div></section>

<section class="sect"><div class="wrap"><div class="split">
<div class="rv" style="display:grid;gap:clamp(28px,3.6vw,52px)">
<div><h2 class="ds" style="margin-bottom:14px">The brief</h2><p class="lede" style="max-width:62ch">A founder starting a company that does three things most businesses keep apart: interiors, paint and architectural design. Before anything visual, she needed a name that could hold all three, be easy to say and remember, and leave room to grow.</p></div>
<div><h2 class="ds" style="margin-bottom:14px">The approach</h2><p class="lede" style="max-width:62ch">We explored names around what the business really sells: colour, and the change it brings to a space. ColorWaves stuck: colour in motion. Everything else grew out of the name. The wave became a W, the W became a rainbow of paint, and the rainbow became a palette, a voice and a family of three sub-brands.</p></div>
</div>
<div class="rv"><h3 class="small" style="margin-bottom:16px">Scope</h3><ol class="cs-scope">
<li><i>01</i><b>Naming</b><span>Name exploration for a business spanning interiors, paint and architectural design, ending at ColorWaves.</span></li>
<li><i>02</i><b>Logomark</b><span>A single wave that forms the letter W, painted in six ribbons of colour.</span></li>
<li><i>03</i><b>Logo system</b><span>Horizontal and vertical logos and the mark on its own, in black and white versions, with clear space rules.</span></li>
<li><i>04</i><b>Colour &amp; type</b><span>Fifteen colours in three groups, Maven Pro for the logotype and Inter for everything else.</span></li>
<li><i>05</i><b>Voice &amp; architecture</b><span>A tagline, tone of voice, key messages and three sub-brands under one roof.</span></li>
<li><i>06</i><b>Guide &amp; applications</b><span>A 46-page identity guide, and the brand on stationery, merchandise, product labels, campaigns, signage and vehicles.</span></li>
</ol></div>
</div>
<div class="cs-nums rv" style="margin-top:clamp(40px,6vw,88px)">
<div><div class="n"><span data-count="1" data-suffix="" data-plain="false">1</span></div><div class="k">Name</div></div>
<div><div class="n"><span data-count="6" data-suffix="" data-plain="false">6</span></div><div class="k">Ribbons in the mark</div></div>
<div><div class="n"><span data-count="15" data-suffix="" data-plain="false">15</span></div><div class="k">Brand colours</div></div>
<div><div class="n"><span data-count="3" data-suffix="" data-plain="false">3</span></div><div class="k">Sub-brands</div></div>
</div>
</div></section>

<section class="sect dark"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">01 &nbsp;The name</p><h2 class="dm rv">FIRST, A NAME<br>WORTH BUILDING ON.</h2></div>
<p class="lede rv">The business had no name when the founder reached out, so that is where we started. The name had to cover paint, interiors and design, and still sound like one company.</p></div>
<div class="cw-name">
<p class="cw-stack rv" aria-hidden="true"><span>Col</span><span>or</span><span>Wa</span><span>ves</span></p>
<div class="cw-eq">
<div class="cw-term rv"><b>Color</b><p>What the business sells: paint, and the colour every space starts from.</p></div>
<span class="cw-op" aria-hidden="true">+</span>
<div class="cw-term rv"><b>Waves</b><p>Movement: paint flowing across a wall, and a change that spreads through a room.</p></div>
<span class="cw-op" aria-hidden="true">=</span>
<div class="cw-term cw-result rv"><b>ColorWaves</b><p>Colour in motion. One name that holds interiors, paint and design, with a tagline to match: <em>Transforming Spaces, Inspiring Lives.</em></p></div>
</div>
</div>
</div></section>

<section class="sect"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">02 &nbsp;The mark</p><h2 class="dm rv">ONE WAVE<br>BECOMES A W.</h2></div>
<p class="lede rv">The name drew the mark: a single wave that forms the letter W, the flow of paint and the brand&rsquo;s initial in one shape. Each ribbon is a different colour, for creativity, diversity and the range ColorWaves offers.</p></div>
<div class="cw-paint" data-paint="Red,Yellow,Green,Coral,Blue,Violet">
<div class="cw-paintboard">{MARK}</div>
<div class="cw-painttools"><div class="cw-chips" role="group" aria-label="Highlight a ribbon">{rib_chips}</div>
<button type="button" class="btn btn-ghost btn-sm" data-paint-play>Paint it again</button></div>
</div>
</div></section>

<section class="sect dark"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">03 &nbsp;Logo system</p><h2 class="dm rv">THREE WAYS<br>TO SIGN.</h2></div>
<p class="lede rv">Choose a version, then see it on Cloud White and on Midnight Plum.</p></div>
<div class="pg-lab cw-lab" data-logolab data-tone="light">
<div class="pg-labtools"><div class="filters" role="group" aria-label="Logo version">{ver_btns}</div>
<div class="filters" role="group" aria-label="Background"><button type="button" data-bg="light" aria-pressed="true">On light</button><button type="button" data-bg="dark" aria-pressed="false">On dark</button></div></div>
<div class="pg-stage">{ver_imgs}</div>
<p class="cs-caption" aria-live="polite"></p>
</div>
</div></section>

<section class="sect"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">04 &nbsp;Colour</p><h2 class="dm rv">FIFTEEN COLOURS,<br>ONE RAINBOW.</h2></div>
<p class="lede rv">The rainbow leads, warm secondaries play around it, and calm neutrals keep it professional. Tap a colour to copy it.</p></div>
<div class="cw-palette">{pal}</div><p class="vh" data-swatch-live aria-live="polite"></p>
</div></section>

<section class="sect dark"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">05 &nbsp;Typography</p><h2 class="dm rv">TWO TYPEFACES,<br>CLEAR JOBS.</h2></div>
<p class="lede rv">Maven Pro, with its smooth curves, sets the name and echoes the wave. Inter carries everything else: headlines, body copy and the small print. Type something to try them.</p></div>
<div class="cw-type" data-typetest>
<label class="cw-typein"><span>Your words</span><input type="text" maxlength="60" placeholder="Bring your walls to life" autocomplete="off"></label>
<div class="cw-specimens">
<div class="cw-spec"><p class="k">Maven Pro &middot; Logotype</p><p class="cw-out mav" data-type-out></p></div>
<div class="cw-spec"><p class="k">Inter &middot; Everything else</p><p class="cw-out int" data-type-out></p></div>
</div>
</div>
</div></section>

<section class="sect"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">06 &nbsp;Voice &amp; family</p><h2 class="dm rv">ONE BRAND,<br>THREE SPECIALISTS.</h2></div>
<p class="lede rv">Friendly, engaging and inspiring, with vivid language that brings colour to life. Under the ColorWaves name sit three sub-brands, one for each thing the business does.</p></div>
<p class="cw-tag rv">&ldquo;Transforming Spaces, Inspiring Lives.&rdquo;</p>
<div class="cw-family">
<div class="cw-sub rv"><img src="{REL}/logo/mark.webp" alt="" width="400" height="240" loading="lazy" decoding="async"><h3>ColorWaves <span>Coating</span></h3><p>Premium paints and coatings, durable and eco-friendly, for homes and commercial spaces.</p></div>
<div class="cw-sub rv"><img src="{REL}/logo/mark.webp" alt="" width="400" height="240" loading="lazy" decoding="async"><h3>ColorWaves <span>Revitalization</span></h3><p>Refurbishing and reviving older spaces with new techniques, restoring their beauty and colour.</p></div>
<div class="cw-sub rv"><img src="{REL}/logo/mark.webp" alt="" width="400" height="240" loading="lazy" decoding="async"><h3>WaveFront <span>Design</span></h3><p>Interior design and colour consultation, for personal, harmonious spaces.</p></div>
</div>
</div></section>

<section class="sect dark" data-sets><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">07 &nbsp;In the world</p><h2 class="dm rv">COLOUR,<br>EVERYWHERE.</h2></div>
<div class="cs-tools"><div class="filters" role="group" aria-label="Choose a group">{set_btns}</div></div></div>
{panels}
</div></section>

<section class="sect"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">08 &nbsp;Deliverables</p><h2 class="dm rv">WHAT WE<br>DELIVERED.</h2></div>
<p class="lede rv">From a name to a brand ready for its first shop sign: everything ColorWaves needs to launch and look like one company.</p></div>
<div class="pg-groups pg-delivered rv">{groups}</div>
<div class="dl-card rv" id="guide"><div><p class="eyebrow">Download</p><h3>ColorWaves brand guidelines</h3><p class="dl-meta">PDF &middot; 45 pages &middot; 3.7 MB &middot; portfolio edition</p><p class="dl-note">For viewing only: contact details removed, not for reuse. &copy; 2024 ColorWaves. Design by Graphcent.</p></div><a class="btn btn-fill" href="../../assets/guides/colorwaves-brand-guidelines.pdf" download="colorwaves-brand-guidelines.pdf">DOWNLOAD PDF <span class="ar" aria-hidden="true">&darr;</span></a></div>
</div></section>

<section class="sect dark"><div class="wrap"><div class="nextproj"><span class="small">Credits &nbsp;&nbsp; Naming and brand identity by Graphcent</span><a class="tlink" href="../../work/ajyad/index.html">Next project: Ajyad Investments<span class="ar" aria-hidden="true">&rarr;</span></a></div></div></section>'''

src = open(os.path.join(ROOT, 'work/amea/index.html'), encoding='utf-8').read()
a = src.index('<main id="main">')
cta_a = src.index('<section class="sect cta dark" id="start">')
cta_b = src.index('</main>') + len('</main>')
page = src[:a] + MAIN + '\n' + src[cta_a:cta_b] + src[cta_b:]

title = 'ColorWaves: Naming and Brand Identity: Graphcent'
desc = ('ColorWaves: naming and brand identity by Graphcent for a new interiors, paint and architectural design company. '
        'A wave that becomes a W, a 15-colour palette, a voice and three sub-brands.')
page = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', page, count=1)
for prop in ('og:title', 'twitter:title'):
    page = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', rf'\g<1>{esc(title)}', page)
for prop in ('description', 'og:description', 'twitter:description'):
    page = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', rf'\g<1>{esc(desc)}', page)
page = page.replace('https://graphcent.com/work/amea/', f'https://graphcent.com/work/{SLUG}/')
# the brand's own typefaces, for the type tester and the name section
page = page.replace('</head>', '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&amp;family=Maven+Pro:wght@500;700&amp;display=swap">\n</head>', 1)
os.makedirs(os.path.join(ROOT, f'work/{SLUG}'), exist_ok=True)
open(os.path.join(ROOT, f'work/{SLUG}/index.html'), 'w', encoding='utf-8').write(page)
print(f'built work/{SLUG}/index.html')
