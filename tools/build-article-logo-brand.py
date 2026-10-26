"""Build insights/why-a-logo-is-not-a-brand/index.html.

The Pegasus Interiors story: a client who asked for a better logo, and ended up
asking for a brand. Run from the site root: python3 tools/build-article-logo-brand.py
then python3 tools/add-share.py . to add the share buttons.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_shell import make_page

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'why-a-logo-is-not-a-brand'
TITLE = 'Why a logo is not a brand'
DESC = ('Pegasus Interiors asked Graphcent for a better logo. What they needed, and what they ended up asking '
        'for, was a brand. The story of one WhatsApp brief and the difference between the two.')
A = '../../assets/projects/pegasus-interiors'


def fig(inner, cap, cls='wide'):
    return f'<figure class="pfig {cls} rv">{inner}<figcaption>{cap}</figcaption></figure>'


def im(src, alt, w, h, lazy=True):
    return (f'<div class="pframe"><img src="{src}" alt="{alt}"{" loading=\"lazy\"" if lazy else ""} '
            f'decoding="async" width="{w}" height="{h}"></div>')


ASKED_NEXT = ['Favicon', 'Compliment card', 'Email signature', 'Quotation template', 'Delivery slip', 'Flyer template',
              'Billboard, horizontal', 'Billboard, vertical', 'WhatsApp Business banner', 'Instagram post template',
              'Instagram story template', 'Product price tag', 'Packaging sticker', 'Vehicle branding',
              'Staff uniform', 'Presentation template']
ASKED_DONE = ['Circular emblem', 'Watermark', 'Business card', 'Letterhead', 'Invoice', 'Envelope']
chips = (''.join(f'<li class="done">{t}</li>' for t in ASKED_DONE) +
         ''.join(f'<li>{t}</li>' for t in ASKED_NEXT))

body = f'''
<div class="readbar" aria-hidden="true"><i></i></div>
<article class="postpage">
<section class="sect post-top"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="../../insights/index.html">Insights</a><span aria-hidden="true">/</span><span>Branding</span></nav>
<p class="eyebrow post-flag">Branding &middot; Case story</p>
<h1 class="post-title rv">Why a logo is not a brand</h1>
<p class="lede post-lede rv">A logo is the signature. The brand is everything the signature is attached to. When Pegasus Interiors asked us for a better logo, the most useful thing we could give them was the difference between the two.</p>
<div class="post-meta"><span>By Graphcent Studio</span><span>6 June 2026</span><span data-readtime>6 min read</span></div>
</div></section>

<div class="wrap"><figure class="post-hero rv"><div class="pframe"><img src="{A}/mockups/signage.webp" alt="The Pegasus Interiors logo as brushed-steel letters on a charcoal shopfront sign" width="2000" height="1333" decoding="async" fetchpriority="high"></div><figcaption>The new Pegasus Interiors mark above the shopfront. See the <a href="../../work/pegasus-interiors/index.html">full case study</a>.</figcaption></figure></div>

<section class="sect post-wrap"><div class="wrap post-grid">
<aside class="post-aside" aria-label="Project at a glance">
<dl class="glance">
<div><dt>Client</dt><dd>Pegasus Interiors, an interior design company in Kano</dd></div>
<div><dt>They asked for</dt><dd>&ldquo;Something better&rdquo; than their logo</dd></div>
<div><dt>We delivered</dt><dd>Symbol, logo system, emblem, colour, stationery</dd></div>
<div><dt>Where it started</dt><dd>A WhatsApp message</dd></div>
</dl>
<a class="tlink" href="../../work/pegasus-interiors/index.html">See the case study <span class="ar" aria-hidden="true">&rarr;</span></a>
</aside>

<div class="post">
<h2 id="message">It started with a WhatsApp message</h2>
<p>Most of our projects begin somewhere less formal than a brief, and this one began in a chat. Pegasus Interiors, an interior design company in Kano, sent us their logo: a winged horse rearing in front of thin gold building outlines, the name set in a light, spaced-out serif, and the line &ldquo;Crafting Timeless Spaces&rdquo; underneath.</p>
<p>Then came the sentence that every designer has heard in some form:</p>
<div class="chat rv" aria-label="The client's first messages, names removed">
<div class="msg in img"><img src="{A}/before.webp" alt="The previous Pegasus Interiors logo" width="480" height="480" loading="lazy" decoding="async"></div>
<div class="msg in">This was the previous design</div>
<div class="msg in">We all like it. It&rsquo;s just that we want something better</div>
</div>
<p>It is a more honest brief than it sounds. Nobody disliked the logo. What they could not put into words was that it was not doing enough for them. That gap, between a mark people like and a mark that works, is the difference between a logo and a brand.</p>

<h2 id="better">What &ldquo;better&rdquo; actually meant</h2>
<p>Before drawing anything, we listed every place this logo would have to live. A business card. An invoice sent to a client. The sign above the studio. The side of a van. Embroidery on a staff shirt. An Instagram avatar the size of a fingernail. A browser tab smaller than that.</p>
<p>The old logo was drawn for one of those places: large, on white, in full colour. Its gradient wings and hairline buildings were lovely at that size and lost almost everywhere else. Shrink it and the buildings vanish. Print it in one colour and the wings turn to a blur. Stitch it onto a uniform and the detail has nowhere to go.</p>
</div></div>
{fig(f'<div class="pcompare">{im(f"{A}/before.webp", "The previous logo", 480, 480)}{im(f"{A}/logo/05.webp", "The new logo", 1400, 1400)}</div>', 'Before and after. The Pegasus and the gold stayed; how they are drawn changed. Drag between them in the <a href="../../work/pegasus-interiors/index.html">case study</a>.', 'duo')}
<div class="wrap post-grid"><div class="post-aside-pad" aria-hidden="true"></div><div class="post">

<blockquote class="pull rv"><p>A logo is judged at its smallest size, not its biggest.</p></blockquote>

<h2 id="kept">Keep what they loved</h2>
<p>&ldquo;We all like it&rdquo; mattered, so we did not start over. The Pegasus was already theirs, and so was the gold. We kept both and changed how they were drawn.</p>
<p>The horse became one solid silhouette that reads at any size and in any single colour. The buildings did not disappear: they moved inside the horse, as the vertical lines that run through its body, so the architecture is carried in the mark itself instead of standing behind it. The name moved to a confident serif, with INTERIORS in a clean sans beneath it. The tagline stays, for the moments when the company introduces itself.</p>

<h2 id="system">Then we built the rest</h2>
<p>A better mark was only the start. A brand is what happens when that mark meets everything else, so we designed the pieces it would meet first:</p>
<ul class="ticks">
<li><b>A logo system.</b> Stacked and horizontal lockups, with and without the tagline, each on light and on dark.</li>
<li><b>Two circular emblems.</b> Seals for stamps, packaging and uniforms, and a faint watermark on the letterhead.</li>
<li><b>Four colours.</b> Pegasus Gold, Charcoal, Cream and Stone, taken from the materials of a well-finished room: brass, dark timber, warm plaster, stone.</li>
<li><b>Stationery.</b> A business card, letterhead, invoice and envelope, tied together with thin gold rules.</li>
</ul>
</div></div>
{fig(f'<div class="pquad">{im(f"{A}/logo/01.webp", "Stacked logo on cream", 1400, 1400)}{im(f"{A}/logo/04.webp", "Horizontal logo on charcoal", 1400, 1400)}{im(f"{A}/logo/07.webp", "Emblem on cream", 1400, 1400)}{im(f"{A}/logo/10.webp", "Emblem on charcoal", 1400, 1400)}</div>', 'One mark, many jobs: stacked, horizontal and the emblem, on light and on dark.')}
{fig(im(f"{A}/mockups/stationery-set.webp", "The full Pegasus Interiors stationery set: letterhead, business cards, envelope, emblem sticker and gold palette cards", 2000, 1333), 'The first pieces of the system: letterhead, cards, envelope and an emblem sticker, on the gold palette.')}
<div class="wrap post-grid"><div class="post-aside-pad" aria-hidden="true"></div><div class="post">

<h2 id="turn">The moment the brief changed</h2>
<p>When the client&rsquo;s leadership saw the identity, the reply that came back did not ask for changes to the logo. It said the list was good but incomplete, and asked for something much bigger: <em>&ldquo;We need to have everything in one place.&rdquo;</em></p>
<p>What followed was a list of everywhere the business shows up. A favicon. A compliment card and an email signature. Quotation templates and delivery slips. Flyers, and billboards in both orientations. A WhatsApp Business banner, Instagram templates, price tags, packaging stickers, the company vehicle, the staff uniform, a presentation template. Each one, they asked, labelled with its size and its use. And a note that this could be the start of a long relationship.</p>
<p>Read that list again and notice what is not on it: another version of the logo. They had stopped asking for a mark and started asking for a brand: one consistent way of showing up on a van, a price tag, an invoice and a phone screen. That shift is the whole point of this article.</p>

<h2 id="answer">So, why is a logo not a brand?</h2>
<p>Because a logo is one decision, and a brand is every decision that follows from it. Pegasus Interiors taught us to put it simply:</p>
<ol class="answers">
<li><b>A logo identifies you. A brand makes you recognisable</b> everywhere you show up, even when the logo is not there.</li>
<li><b>A logo is one file. A brand is a system:</b> versions, colours and rules that tell everyone how to use them.</li>
<li><b>A logo is judged on a screen. A brand is judged on an invoice,</b> a van, a uniform and a WhatsApp chat.</li>
<li><b>&ldquo;Something better&rdquo; rarely means a new logo.</b> It usually means something that works everywhere.</li>
</ol>
<p>Pegasus Interiors came to us for a better logo. They left with a light identity built to last: a mark that holds at any size, and the essentials to show up the same way on a card, a letter, a door and a shopfront. Whatever comes next can be built from it.</p>

<div class="post-card rv">
<div><p class="eyebrow">The full project</p><p class="post-card-t">Compare the before and after, try the logo at any size and explore every version of the Pegasus Interiors identity.</p></div>
<div class="cta-row"><a class="btn btn-fill" href="../../work/pegasus-interiors/index.html">VIEW THE CASE STUDY <span class="ar" aria-hidden="true">&rarr;</span></a><a class="btn btn-ghost" href="../../contact/index.html">START A BRAND <span class="ar" aria-hidden="true">&rarr;</span></a></div>
</div>
</div></div>
</section>
</article>
'''

words, mins = make_page(ROOT, SLUG, TITLE, DESC, '2026-06-06',
                        'assets/projects/pegasus-interiors/mockups/signage.webp', 2000, 1333,
                        'The Pegasus Interiors shopfront sign designed by Graphcent',
                        {'@type': 'Organization', 'name': 'Pegasus Interiors'}, body)
print(f'built insights/{SLUG}/index.html, {words} words, {mins} min read')
