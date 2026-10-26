"""Build the AMEA case study page (work/amea/index.html).

Run from the site root:  python3 tools/build-amea.py .
Takes the page shell (head, header, footer) from the existing work/amea/index.html,
swaps in AMEA's title and metadata, and writes the case study body from the
images in assets/projects/amea. Re-run after changing images or copy below.
"""
import sys, os, re, html
from PIL import Image

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
P = os.path.join(ROOT, 'assets/projects/amea')
REL = '../../assets/projects/amea'
SITE = 'https://amea.ng'
esc = lambda t: html.escape(t, quote=True)

FEATURES = [
    ('01-hero-film', 'Hero film', '', 'The homepage film follows your scroll: move down the page and the scene moves with you.'),
    ('02-glass-header', 'Glass header', '', 'The header starts transparent over the film and turns into a glass pill once you scroll.'),
    ('03-licence-map', '3D licence map', 'assets.html', 'AMEA’s licence areas on a 3D map of Nigeria. Select a marker to see the site and its licence details.'),
    ('04-licence-filters', 'Licence filters', 'assets.html', 'The licence records filter by type, Mining Lease or Exploration Licence, and by mineral.'),
    ('05-site-reel', 'Site reel', 'mining.html', 'Unedited footage from the mining site plays silently while it is on screen, and stops when it is not.'),
    ('06-cookie-consent', 'Cookie consent', '', 'A cookie banner with real choices. Analytics and Google Maps load only after the visitor allows them.'),
    ('07-enquiry-form', 'Enquiry form', 'contact.html', 'Seven enquiry types, each naming the email it sends. The map waits for consent before it loads.'),
    ('08-insights', 'Insights', 'insights.html', 'Plain-language explainers on licences, minerals, agriculture and the standards AMEA follows.'),
]
PAGES = [
    ('09-mining', 'Mining & minerals', 'mining.html', 'Gold, lithium, spodumene, iron ore and the rest of the portfolio, with a mining enquiry form.'),
    ('10-agriculture', 'Agriculture', 'agriculture.html', 'Commercial farming, agro-processing, livestock and aquaculture, prepared for export.'),
    ('11-careers', 'Careers', 'careers.html', 'Roles across geology, mining engineering, finance, ICT, administration and sustainability.'),
    ('12-about', 'About', 'about.html', 'AMEA’s background, vision, mission, values and leadership.'),
]
PHONES = [('01-home', 'Home'), ('02-menu', 'Menu'), ('03-mining', 'Mining'), ('04-map', 'Licence map'),
          ('05-licences', 'Licence records'), ('06-agriculture', 'Agriculture'), ('07-insights', 'Insights'),
          ('08-contact', 'Enquiry form'), ('09-careers', 'Careers')]
LIVE_PAGES = [('Home', ''), ('Mining', 'mining.html'), ('Assets & licences', 'assets.html'),
              ('Agriculture', 'agriculture.html'), ('Careers', 'careers.html'), ('Contact', 'contact.html')]
TYPES = ['General enquiry', 'Investment and partnership', 'Mineral, trade and export', 'Agriculture',
         'Community and sustainability', 'Careers', 'Media']


def size(rel):
    with Image.open(os.path.join(ROOT, rel.replace('../../', ''))) as im:
        return im.size


def img(src, alt, cls='', eager=False, extra=''):
    w, h = size(src)
    c = f' class="{cls}"' if cls else ''
    lazy = '' if eager else ' loading="lazy"'
    return f'<img{c} src="{src}" alt="{esc(alt)}"{lazy} decoding="async" width="{w}" height="{h}"{extra}>'


def viewer(items, title):
    btns, ims = [], []
    for i, (slug, label, page, desc) in enumerate(items):
        on = i == 0
        url = 'amea.ng/' + page if page else 'amea.ng'
        btns.append(f'<button type="button" aria-pressed="{str(on).lower()}" data-url="{esc(url)}" data-desc="{esc(desc)}"><i>{i+1:02d}</i>{esc(label)}</button>')
        ims.append(img(f'{REL}/features/{slug}.webp', f'AMEA website: {label}', cls='on' if on else '', eager=on))
    first = items[0]
    return (f'<div class="cs-console" data-viewer><div class="cs-list" role="group" aria-label="{esc(title)}">{"".join(btns)}</div>'
            f'<div><div class="cs-browser"><div class="cs-bar" aria-hidden="true"><b></b><b></b><b></b><span>{esc("amea.ng/" + first[2] if first[2] else "amea.ng")}</span></div>'
            f'<div class="cs-stage" style="aspect-ratio:16/10">{"".join(ims)}</div></div>'
            f'<p class="cs-caption" aria-live="polite">{esc(first[3])}</p></div></div>')


phones = ''.join(f'<figure class="cs-phone"><div class="scr">{img(f"{REL}/phone/{s}.webp", f"AMEA website on a phone: {l}")}</div>'
                 f'<figcaption><i>{k:02d}</i>{esc(l)}</figcaption></figure>' for k, (s, l) in enumerate(PHONES, 1))
pick = ''.join(f'<button type="button" data-live-page="{SITE}/{p}" aria-pressed="{str(k == 0).lower()}">{esc(l)}</button>'
               for k, (l, p) in enumerate(LIVE_PAGES))
opts = ''.join(f'<option>{esc(t)}</option>' for t in TYPES)

MAIN = f'''<main id="main"><section class="sect dark phero"><div class="wrap"><a class="small" href="../../work/index.html" style="display:inline-block;margin-bottom:clamp(24px,3vw,42px)">&larr; &nbsp;All work</a><div class="split" style="align-items:end"><h1 class="dl rv">AMEA</h1><p class="lede rv">AMEA&rsquo;s old website was down and needed a revamp. Graphcent built the new amea.ng end to end: design, frontend development and the services behind it, from the enquiry forms to email.</p></div><div class="facts phero-facts rv" data-n="4"><div class="fact"><div class="k">Client</div><div class="v">AMEA Agro and Mining Export Alliance Limited</div></div><div class="fact"><div class="k">Category</div><div class="v">Website design &amp; development</div></div><div class="fact"><div class="k">Scope</div><div class="v">21-page website, enquiry forms, email, analytics</div></div><div class="fact"><div class="k">Services</div><div class="v">Web Design, Frontend Development, Forms &amp; Email Backend, Hosting &amp; SEO</div></div></div><a class="tlink rv" href="{SITE}/" target="_blank" rel="noopener" style="margin-top:clamp(22px,3vw,36px)">Visit amea.ng <span class="ar" aria-hidden="true">&#8599;</span></a></div></section>

<section class="cs-hero"><div class="wrap"><div class="proj"><div class="frame rv" style="aspect-ratio:auto">{img(f"{REL}/hero.webp", "The new amea.ng homepage: From Nigerian ground to global markets, over the mining film", eager=True, extra=' fetchpriority="high"')}</div></div></div></section>

<section class="sect"><div class="wrap"><div class="split">
<div class="rv" style="display:grid;gap:clamp(28px,3.6vw,52px)">
<div><h2 class="ds" style="margin-bottom:14px">The brief</h2><p class="lede" style="max-width:62ch">AMEA, an indigenous Nigerian mining and agro-export company based in Kano, came to Graphcent with their old website down and in need of a revamp. They needed a site that presents the company with confidence and turns interest from partners, buyers and job seekers into real enquiries.</p></div>
<div><h2 class="ds" style="margin-bottom:14px">The approach</h2><p class="lede" style="max-width:62ch">We took it all the way, designed straight in code: every page, every interaction, and the services that keep it running. Enquiries land in a Google Sheet and in the AMEA inbox, analytics only runs with the visitor&rsquo;s consent, and the site is served on AMEA&rsquo;s own domain.</p></div>
</div>
<div class="rv"><h3 class="small" style="margin-bottom:16px">Scope</h3><ol class="cs-scope">
<li><i>01</i><b>Design &amp; frontend</b><span>21 pages: home, what we do, mining, agriculture, global markets, assets and licences, sustainability, careers, contact, six explainers and the legal pages.</span></li>
<li><i>02</i><b>Enquiry forms &amp; email</b><span>Five enquiry forms post to a Google Apps Script web app: each enquiry becomes a row in a Google Sheet and an email to info@amea.ng. A hidden spam trap stops bots, and a failed send says so; it never fakes success.</span></li>
<li><i>03</i><b>Interactive licence map</b><span>A 3D map of Nigeria with AMEA&rsquo;s licence areas, and licence records you can filter by type and mineral.</span></li>
<li><i>04</i><b>Privacy &amp; consent</b><span>A cookie banner with real choices: analytics and Google Maps load only after the visitor allows them.</span></li>
<li><i>05</i><b>Launch &amp; search</b><span>Live on amea.ng with HTTPS, plus a sitemap, structured data and social sharing cards.</span></li>
</ol></div>
</div>
<div class="cs-nums rv" style="margin-top:clamp(40px,6vw,88px)">
<div><div class="n"><span data-count="21" data-suffix="" data-plain="false">21</span></div><div class="k">Pages</div></div>
<div><div class="n"><span data-count="5" data-suffix="" data-plain="false">5</span></div><div class="k">Enquiry forms</div></div>
<div><div class="n"><span data-count="6" data-suffix="" data-plain="false">6</span></div><div class="k">Explainer articles</div></div>
<div><div class="n"><span data-count="6" data-suffix="" data-plain="false">6</span></div><div class="k">Licence areas mapped</div></div>
</div>
</div></section>

<section class="sect dark"><div class="wrap"><div class="cs-live cs-devices" data-live data-device="desktop">
<div class="cs-head"><div><p class="eyebrow">01 &nbsp;Live site</p><h2 class="dm rv">THE REAL SITE.<br>TRY IT HERE.</h2></div>
<div class="cs-tools"><div class="filters" role="group" aria-label="Choose a screen size"><button type="button" data-device-btn="desktop" aria-pressed="true">Desktop</button><button type="button" data-device-btn="tablet" aria-pressed="false">Tablet</button><button type="button" data-device-btn="mobile" aria-pressed="false">Mobile</button></div></div></div>
<div class="cs-frame"><div class="cs-browser"><div class="cs-bar"><b aria-hidden="true"></b><b aria-hidden="true"></b><b aria-hidden="true"></b><span>amea.ng</span><a href="{SITE}/" target="_blank" rel="noopener">Open <span aria-hidden="true">&#8599;</span></a></div>
<div class="cs-viewport">{img(f"{REL}/poster-desktop.webp", "", cls="cs-poster")}<iframe src="{SITE}/" title="The AMEA website, live at amea.ng" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe></div></div></div>
<div class="cs-pages-pick" role="group" aria-label="Choose a page">{pick}</div>
<p class="cs-hint"><span>This is amea.ng, live. Click around.</span></p>
</div></div></section>

<section class="sect"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">02 &nbsp;Forms &amp; email</p><h2 class="dm rv">EVERY ENQUIRY<br>LANDS TWICE.</h2></div>
<p class="lede rv">Try the enquiry pipeline behind AMEA&rsquo;s forms. The demo runs the same steps, but nothing leaves this page.</p></div>
<div class="cs-flow" data-flow>
<form class="cs-demo" novalidate>
<label>Full name<input name="name" type="text" autocomplete="off" placeholder="Your name"></label>
<label>Enquiry type<select name="type"><option value="">Choose one</option>{opts}</select></label>
<label>Message<textarea name="message" rows="3" placeholder="What would you like to ask AMEA?"></textarea></label>
<label class="vh" aria-hidden="true">Leave this empty<input name="hp_extra" type="text" tabindex="-1" autocomplete="off"></label>
<p class="err" role="alert"></p>
<div style="display:flex;flex-wrap:wrap;gap:14px;align-items:center"><button type="submit" class="btn btn-fill btn-sm">Send demo enquiry</button><span class="note">Demo only. Nothing is sent.</span></div>
</form>
<div class="cs-pipe">
<div class="cs-node"><h3>Enquiry form</h3><p>Checks the required fields and the hidden spam trap.</p><span class="stat">Waiting</span></div>
<div class="cs-node"><h3>Google Apps Script</h3><p>AMEA&rsquo;s web app receives the enquiry.</p><span class="stat">Waiting</span></div>
<div class="cs-node"><h3>Google Sheet</h3><p>Every enquiry becomes a row.</p><span class="stat">Waiting</span>
<table class="cs-sheet"><thead><tr><th scope="col">Time</th><th scope="col">Name</th><th scope="col">Enquiry type</th><th scope="col">Page</th></tr></thead><tbody><tr class="empty"><td colspan="4">New enquiries appear here</td></tr></tbody></table></div>
<div class="cs-node"><h3>Email to info@amea.ng</h3><p>The AMEA team gets it in their inbox.</p><span class="stat">Waiting</span>
<ul class="cs-mail"><li class="empty">The email appears here</li></ul></div>
<p class="vh" aria-live="polite"></p>
</div>
</div>
</div></section>

<section class="sect dark" data-sets><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">03 &nbsp;Details</p><h2 class="dm rv">BUILT TO BE<br>USED.</h2></div>
<div class="cs-tools"><div class="filters" role="group" aria-label="Choose features or pages"><button type="button" data-set="features" aria-pressed="true">Features</button><button type="button" data-set="pages" aria-pressed="false">Pages</button></div></div></div>
<div class="cs-set" data-set-panel="features">{viewer(FEATURES, "AMEA website features")}</div>
<div class="cs-set" data-set-panel="pages" hidden>{viewer(PAGES, "AMEA website pages")}</div>
</div></section>

<section class="sect"><div class="wrap"><div class="cs-railwrap">
<div class="cs-head"><div><p class="eyebrow">04 &nbsp;Mobile</p><h2 class="dm rv">SAME SITE,<br>IN YOUR HAND.</h2></div>
<div class="cs-tools"><button type="button" class="cs-btn" data-prev aria-label="Previous screens">&larr;</button><button type="button" class="cs-btn" data-next aria-label="Next screens">&rarr;</button></div></div>
<div class="cs-rail" tabindex="0" role="region" aria-label="The AMEA website on a phone, scroll sideways">{phones}</div>
<div class="cs-railbar" aria-hidden="true"><i></i></div>
</div></div></section>

<section class="sect dark"><div class="wrap"><div class="nextproj"><span class="small">Credits &nbsp;&nbsp; Design, development and services by Graphcent</span><a class="tlink" href="../../work/onemajlis/index.html">Next project: OneMajlis<span class="ar" aria-hidden="true">&rarr;</span></a></div></div></section>'''

src = open(os.path.join(ROOT, 'work/amea/index.html'), encoding='utf-8').read()
# keep the shell; take the CTA section from the page as it is
a = src.index('<main id="main">')
cta_a = src.index('<section class="sect cta dark" id="start">')
cta_b = src.index('</main>') + len('</main>')
page = src[:a] + MAIN + '\n' + src[cta_a:cta_b] + src[cta_b:]

title = 'AMEA: Website Design and Development: Graphcent'
desc = ('AMEA: the new amea.ng, designed and built end to end by Graphcent, from frontend '
        'development to the enquiry forms, Google Sheets and email behind it.')
page = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', page, count=1)
for prop in ('og:title', 'twitter:title'):
    page = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', rf'\g<1>{esc(title)}', page)
for prop in ('description', 'og:description', 'twitter:description'):
    page = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*', rf'\g<1>{esc(desc)}', page)
os.makedirs(os.path.join(ROOT, 'work/amea'), exist_ok=True)
open(os.path.join(ROOT, 'work/amea/index.html'), 'w', encoding='utf-8').write(page)
print('built work/amea/index.html')
