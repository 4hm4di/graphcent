"""Build the AIFF '26 event branding case study (work/aiff-26/index.html).

Run from the site root:  python3 tools/build-aiff.py .   then tools/seo.py .
Arewa Islamic Finance Forum 2026, convened by IFING Media Ltd. Graphcent: creative direction,
event branding, design execution and print consultation. Assets in assets/projects/aiff-26.
The creative director's report is Ahmad Abdallah's LinkedIn post, embedded with LinkedIn's own player.
"""
import sys, os, re, html
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_projects import next_of

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
SLUG = 'aiff-26'
REL = f'../../assets/projects/{SLUG}'
EVENT = 'https://mtechnoble.zohobackstage.com/AREWAISLAMICFINANCEFORUM'
POST = 'https://www.linkedin.com/posts/ahmard_aiff-creativedirection-eventbranding-ugcPost-7486028600404725760-Q3OA/'
EMBED = 'https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7486028600404725760'
esc = lambda t: html.escape(t, quote=True)


def size(rel):
    with Image.open(os.path.join(ROOT, rel.replace('../../', ''))) as im:
        return im.size


def img(src, alt, cls='', eager=False, extra=''):
    w, h = size(src)
    c = f' class="{cls}"' if cls else ''
    return f'<img{c} src="{src}" alt="{esc(alt)}"{"" if eager else " loading=\"lazy\""} decoding="async" width="{w}" height="{h}"{extra}>'


SOCIAL = [('01-countdown-2', 'Countdown: 2 days to go'), ('02-countdown-1', 'Countdown: 1 day to go'),
          ('03-speaker-farrukh', 'Speaker: Dr Farrukh Habib'), ('04-speaker-oseni', 'Speaker: Dr Umar Oseni'),
          ('05-tickets-open', 'Tickets now open'), ('06-tickets-live', 'Tickets are live'),
          ('07-venue', 'Venue reveal'), ('08-exhibitors', 'Call for exhibitors'), ('09-sponsor', 'Sponsor announcement')]
VENUE = {
    'hall': ('Marquee hall', [('hall-02', 'Key focus areas, with the forum&rsquo;s speakers'), ('hall-01', 'Partners wall with the welcome panel'),
                              ('hall-03', 'Welcome banner with the key focus areas'), ('hall-04', 'AIFF impact areas with the welcome panel')]),
    'outdoor': ('Outdoor flow', [('outdoor-03', 'Welcome banner at the entrance'), ('outdoor-01', 'Registration point with the event QR code'),
                                 ('outdoor-02', 'Partners and sponsors wall'), ('outdoor-04', 'AIFF &rsquo;26 banner with the key focus areas and a speaker'),
                                 ('outdoor-05', 'Square AIFF &rsquo;26 pattern banner')]),
    'stage': ('Stage', [('stage', 'The stage design: backdrop, side panels and branded stage front')]),
}
PRINT = [('badge', 'Conference badge on a branded lanyard'), ('agenda-cover', 'Agenda booklet cover'),
         ('agenda-spread', 'Agenda booklet, open'), ('agenda-inside', 'Speaker pages in the agenda'),
         ('programme', 'Programme booklet'), ('certificate', 'Certificate of participation'),
         ('notebook', 'Branded notebook'), ('notebooks', 'Notebooks, stacked'), ('gift-bag', 'Delegate gift bag')]
PALETTE = [('Forest', '#09342D', 'light'), ('Navy', '#012B5D', 'light'), ('Forum Green', '#008C4A', 'light'), ('Sage', '#8ABD6B', 'dark'),
           ('Terracotta', '#C56E3A', 'light'), ('Sand', '#E0B07A', 'dark'), ('Cream', '#F4F0E8', 'dark')]

phones = ''.join(f'<figure class="cs-phone aiff-post"><div class="scr">{img(f"{REL}/social/{f}.webp", f"AIFF 2026 social post: {c}")}</div>'
                 f'<figcaption><i>{k:02d}</i>{esc(c)}</figcaption></figure>' for k, (f, c) in enumerate(SOCIAL, 1))
vbtns = ''.join(f'<button type="button" data-set="{k}" aria-pressed="{str(i == 0).lower()}">{v[0]}</button>' for i, (k, v) in enumerate(VENUE.items()))
vpanels = ''.join(f'<div class="aiff-venue" data-set-panel="{k}"{"" if i == 0 else " hidden"}>' +
                  ''.join(f'<figure>{img(f"{REL}/venue/{f}.webp", html.unescape(c))}<figcaption>{c}</figcaption></figure>' for f, c in v[1]) + '</div>'
                  for i, (k, v) in enumerate(VENUE.items()))
prints = ''.join(f'<figure>{img(f"{REL}/print/{f}.webp", c)}<figcaption>{esc(c)}</figcaption></figure>' for f, c in PRINT)
swatches = ''.join(f'<button type="button" class="pg-swatch cw-swatch" data-swatch="{h}" style="--c:{h}" data-ink="{ink}"><span class="chip" aria-hidden="true"></span>'
                   f'<b>{esc(n)}</b><code>{h}</code><span class="cp" aria-hidden="true">Copy</span></button>' for n, h, ink in PALETTE)
DELIVERED = [('Campaign', ['Countdown posts', 'Speaker announcements', 'Ticket launch', 'Venue reveal', 'Exhibitor and sponsor posts']),
             ('Venue', ['Stage design', 'Marquee hall banners', 'Outdoor wayfinding banners', 'Registration point', 'Partners wall']),
             ('Print', ['Badges and lanyards', 'Agenda and programme booklets', 'Certificates', 'Notebooks', 'Gift bags', 'Print consultation'])]
groups = ''.join(f'<div class="pg-group"><h3>{g}</h3><ul>' + ''.join(f'<li class="done">{esc(i)}</li>' for i in items) + '</ul></div>' for g, items in DELIVERED)
REELS = [('DC7qg5BoCPp', '2024', 'Arewa Islamic Finance Summit (AIFs)',
          'Event branding designed by Ahmad, printed by FB Print. Posted 28 November 2024.'),
         ('Da_mQVuozmN', '2026', 'Arewa Islamic Finance Forum (AIFF &rsquo;26)',
          'Creative direction, design execution and print consultation by Graphcent. Posted 20 July 2026.')]
reels = ''.join(f'<figure class="aiff-reel rv"><figcaption><b>{y}</b><span>{n}</span><small>{c}</small></figcaption>'
                f'<div class="aiff-ig"><iframe src="https://www.instagram.com/reel/{code}/embed/" title="{esc(html.unescape(n))} on Instagram, {y}" '
                f'loading="lazy" scrolling="no" allowfullscreen data-embed data-ig></iframe></div>'
                f'<a class="tlink" href="https://www.instagram.com/reel/{code}/" target="_blank" rel="noopener">Watch on Instagram <span class="ar" aria-hidden="true">&#8599;</span></a></figure>'
                for code, y, n, c in REELS)
nxt, nxt_name = next_of(SLUG)

MAIN = f'''<main id="main"><section class="sect dark phero"><div class="wrap"><a class="small" href="../../work/index.html" style="display:inline-block;margin-bottom:clamp(24px,3vw,42px)">&larr; &nbsp;All work</a><div class="split" style="align-items:end"><h1 class="dl rv">AIFF &rsquo;26</h1><p class="lede rv">The Arewa Islamic Finance Forum 2026, convened by IFING Media, brought bankers, regulators, scholars and entrepreneurs together in Kano for five days. Graphcent gave the forum its full visual presence: creative direction, design execution and print consultation, from the first countdown post to the last certificate.</p></div><div class="facts phero-facts rv" data-n="4"><div class="fact"><div class="k">Client</div><div class="v">IFING Media Ltd (convener)</div></div><div class="fact"><div class="k">Event</div><div class="v">18&ndash;22 July 2026, Amani Event Center, Kano</div></div><div class="fact"><div class="k">Category</div><div class="v">Event branding &middot; 2026</div></div><div class="fact"><div class="k">Services</div><div class="v">Creative Direction, Event Branding, Design Execution, Print Consultation</div></div></div><div class="pj-links"><a class="tlink rv" href="#report">The creative director&rsquo;s report <span class="ar" aria-hidden="true">&darr;</span></a><a class="tlink rv" href="{EVENT}" target="_blank" rel="noopener">Event page <span class="ar" aria-hidden="true">&#8599;</span></a></div></div></section>

<section class="cs-hero"><div class="wrap"><div class="proj"><div class="frame rv" style="aspect-ratio:auto">{img(f"{REL}/hero.webp", "The AIFF 2026 welcome banner: Arewa Islamic Finance Forum, Islamic Finance: From Awareness to Adoption and Advocacy", eager=True, extra=' fetchpriority="high"')}</div></div><div class="aiff-band" aria-hidden="true"></div></div></section>

<section class="sect"><div class="wrap"><div class="split">
<div class="rv" style="display:grid;gap:clamp(28px,3.6vw,52px)">
<div><h2 class="ds" style="margin-bottom:14px">The brief</h2><p class="lede" style="max-width:62ch">A forum on the journey of Islamic finance from awareness to adoption and advocacy, with banking, capital markets, pensions, takaful and estate planning on the agenda. It needed to look credible to institutions, welcoming to the public, and consistent everywhere attendees met it: online before the event, at the gate, in the hall and in their hands.</p></div>
<div><h2 class="ds" style="margin-bottom:14px">The approach</h2><p class="lede" style="max-width:62ch">One system, carried everywhere. A geometric pattern drawn from arches and Arewa motifs, a palette of forest, navy, green, terracotta and sand, and one bold headline style. We set the rules, designed every piece, and worked with the printers so the colours on the banners matched the screens.</p></div>
</div>
<div class="rv"><h3 class="small" style="margin-bottom:16px">Scope</h3><ol class="cs-scope">
<li><i>01</i><b>Creative direction</b><span>The visual system for the forum: pattern, palette, type and how they flex.</span></li>
<li><i>02</i><b>Social campaign</b><span>Countdowns, speaker cards, ticket launch, venue reveal, exhibitors and sponsors.</span></li>
<li><i>03</i><b>Stage &amp; venue</b><span>Stage design, marquee hall banners and the outdoor wayfinding flow.</span></li>
<li><i>04</i><b>Print kit</b><span>Badges, agenda and programme, certificates, notebooks and gift bags.</span></li>
<li><i>05</i><b>Print consultation</b><span>Materials, sizes and colour checks with the printers, so everything arrived right.</span></li>
</ol></div>
</div>
<div class="cs-nums rv" style="margin-top:clamp(40px,6vw,88px)">
<div><div class="n"><span data-count="5" data-suffix="" data-plain="false">5</span></div><div class="k">Event days</div></div>
<div><div class="n"><span data-count="9" data-suffix="" data-plain="false">9</span></div><div class="k">Campaign posts</div></div>
<div><div class="n"><span data-count="9" data-suffix="" data-plain="false">9</span></div><div class="k">Venue banners</div></div>
<div><div class="n"><span data-count="9" data-suffix="" data-plain="false">9</span></div><div class="k">Print pieces</div></div>
</div>
</div></section>

<section class="sect dark"><div class="wrap"><div class="cs-railwrap">
<div class="cs-head"><div><p class="eyebrow">01 &nbsp;Campaign</p><h2 class="dm rv">BEFORE THE DOORS<br>OPENED.</h2></div>
<div class="cs-tools"><button type="button" class="cs-btn" data-prev aria-label="Previous posts">&larr;</button><button type="button" class="cs-btn" data-next aria-label="Next posts">&rarr;</button></div></div>
<p class="lede rv" style="max-width:60ch">The forum started online: countdowns, speaker cards, ticket launches, the venue reveal and calls for exhibitors and sponsors, all in one recognisable look.</p>
<div class="cs-rail" tabindex="0" role="region" aria-label="AIFF 2026 social posts, scroll sideways" style="margin-top:clamp(24px,3vw,40px)">{phones}</div>
<div class="cs-railbar" aria-hidden="true"><i></i></div>
</div></div></section>

<section class="sect" data-sets><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">02 &nbsp;Stage &amp; venue</p><h2 class="dm rv">FULL VISIBILITY,<br>GATE TO STAGE.</h2></div>
<div class="cs-tools"><div class="filters" role="group" aria-label="Choose an area of the venue">{vbtns}</div></div></div>
{vpanels}
</div></section>

<section class="sect dark"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">03 &nbsp;Print</p><h2 class="dm rv">IN EVERY<br>ATTENDEE&rsquo;S HANDS.</h2></div>
<p class="lede rv">Badges, booklets, certificates, notebooks and gift bags, with print consultation so each piece came back from the printer the way it was designed.</p></div>
<div class="cw-grid">{prints}</div>
</div></section>

<section class="sect"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">04 &nbsp;Colour</p><h2 class="dm rv">THE FORUM&rsquo;S<br>PALETTE.</h2></div>
<p class="lede rv">Forest and navy for authority, green for growth and the faith, terracotta and sand for warmth and the region. Tap a colour to copy it.</p></div>
<div class="cw-swatches n7 pj-swatches">{swatches}</div><p class="vh" data-swatch-live aria-live="polite"></p>
</div></section>

<section class="sect dark" id="report"><div class="wrap aiff-report">
<div class="rv"><p class="eyebrow">05 &nbsp;The report</p><h2 class="dm" style="margin-top:clamp(16px,2vw,24px)">FROM A BLANK<br>CANVAS TO A<br>FULL EVENT.</h2>
<p class="lede" style="margin-top:clamp(18px,2.4vw,28px)">Ahmad Abdallah, Graphcent&rsquo;s creative director, on seeing months of work come to life at AIFF &rsquo;26: the visual identity, social creatives, stage design, venue branding, digital assets and print production.</p>
<blockquote class="pull"><p>Good design isn&rsquo;t just about making things look beautiful. It&rsquo;s about creating experiences.</p></blockquote>
<a class="btn btn-ghost" href="{POST}" target="_blank" rel="noopener">READ IT ON LINKEDIN <span class="ar" aria-hidden="true">&#8599;</span></a></div>
<div class="aiff-embed rv"><iframe src="{EMBED}" title="Ahmad Abdallah on LinkedIn: the AIFF 2026 creative direction report" loading="lazy" allowfullscreen data-embed></iframe></div>
</div>
<div class="wrap aiff-then" id="reels">
<div class="cs-head"><div><p class="eyebrow">Then &amp; now</p><h2 class="dm rv">TWO YEARS,<br>ONE FORUM.</h2></div>
<p class="lede rv">In November 2024 the event was the Arewa Islamic Finance Summit (AIFs), and Ahmad designed its branding. In 2026 it came back as a forum, and Graphcent delivered its whole visual presence. The two reels, side by side.</p></div>
<div class="aiff-reels">{reels}</div>
</div></section>

<section class="sect"><div class="wrap">
<div class="cs-head"><div><p class="eyebrow">06 &nbsp;Deliverables</p><h2 class="dm rv">WHAT WE<br>DELIVERED.</h2></div></div>
<div class="pg-groups pg-delivered rv">{groups}</div>
</div></section>

<section class="sect dark"><div class="wrap"><div class="nextproj"><span class="small">Credits &nbsp;&nbsp; Creative direction, design and print consultation by Graphcent. Convened by IFING Media Ltd.</span><a class="tlink" href="../../work/{nxt}/index.html">Next project: {nxt_name} <span class="ar" aria-hidden="true">&rarr;</span></a></div></div></section>'''

src = open(os.path.join(ROOT, 'work/amea/index.html'), encoding='utf-8').read()
a = src.index('<main id="main">')
cta_a = src.index('<section class="sect cta dark" id="start">')
cta_b = src.index('</main>') + len('</main>')
page = src[:a] + MAIN + '\n' + src[cta_a:cta_b] + src[cta_b:]
title = 'AIFF ’26: Event Branding: Graphcent'
desc = ('Arewa Islamic Finance Forum 2026: creative direction, event branding and print consultation by Graphcent, '
        'from the social campaign to the stage, venue and print kit.')
page = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', page, count=1)
page = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(desc), page, count=1)
page = page.replace('https://graphcent.com/work/amea/', f'https://graphcent.com/work/{SLUG}/')
os.makedirs(os.path.join(ROOT, f'work/{SLUG}'), exist_ok=True)
open(os.path.join(ROOT, f'work/{SLUG}/index.html'), 'w', encoding='utf-8').write(page)
print(f'built work/{SLUG}/')
