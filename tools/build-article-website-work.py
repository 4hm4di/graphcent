"""Build insights/what-makes-a-website-work/index.html, the featured article.

The story of how Graphcent rebuilt amea.ng, told around one question: what makes a
website actually work for a business. Shell (head, header, CTA, footer) comes from
work/amea/index.html, which sits at the same folder depth.
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'what-makes-a-website-work'
URL = f'https://graphcent.com/insights/{SLUG}/'
TITLE = 'What makes a website actually work for a business?'
DESC = ('AMEA’s website was down. Here is how Graphcent rebuilt amea.ng end to end, from the first '
        'line of code to forms that land, search, launch and handing over every login.')
DATE_ISO, DATE = '2026-10-23', 'October 2026'

shell = open(os.path.join(ROOT, 'work/amea/index.html'), encoding='utf-8').read()
head, rest = shell.split('<main id="main">', 1)
tail = rest[rest.index('<section class="sect cta dark"'):]

# --- head: title, description, canonical, social, article schema ----------------------------
old_title = re.search(r'<title>(.*?)</title>', head).group(1)
old_desc = re.search(r'<meta name="description" content="(.*?)">', head).group(1)
page_title = f'{TITLE} Insights: Graphcent'
head = head.replace(old_title, html.escape(page_title, quote=False))
head = head.replace(old_desc, html.escape(DESC))
head = head.replace('https://graphcent.com/work/amea/', URL)
head = head.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
head = head.replace('https://graphcent.com/assets/images/og-graphcent.png',
                    'https://graphcent.com/assets/projects/amea/hero.webp')
head = re.sub(r'<meta property="og:image:width" content="\d+">', '<meta property="og:image:width" content="2160">', head)
head = re.sub(r'<meta property="og:image:height" content="\d+">', '<meta property="og:image:height" content="1350">', head)
head = re.sub(r'<meta property="og:image:alt" content="[^"]*">',
              '<meta property="og:image:alt" content="The new amea.ng homepage, designed and built by Graphcent">', head)
schema = {
    '@context': 'https://schema.org', '@type': 'Article', 'headline': TITLE, 'description': DESC,
    'datePublished': DATE_ISO, 'dateModified': DATE_ISO, 'mainEntityOfPage': URL,
    'image': 'https://graphcent.com/assets/projects/amea/hero.webp',
    'author': {'@type': 'Organization', 'name': 'Graphcent', 'url': 'https://graphcent.com/'},
    'publisher': {'@type': 'Organization', 'name': 'Graphcent', 'url': 'https://graphcent.com/'},
    'about': {'@type': 'Organization', 'name': 'AMEA Agro and Mining Export Alliance Limited', 'url': 'https://amea.ng/'}
}
head = head.replace('</head>', '<script type="application/ld+json">' + json.dumps(schema) + '</script>\n</head>')
# nav: this page belongs to Insights
head = head.replace(' aria-current="page">Work', '>Work')
head = head.replace('href="../../insights/index.html">Insights', 'href="../../insights/index.html" aria-current="page">Insights', 1)

# --- body ------------------------------------------------------------------------------------
A = '../../assets/projects/amea'


def fig(src, alt, cap, w=1800, h=1125, cls='wide'):
    return (f'<figure class="pfig {cls} rv"><div class="pframe"><img src="{src}" alt="{alt}" loading="lazy" '
            f'decoding="async" width="{w}" height="{h}"></div><figcaption>{cap}</figcaption></figure>')


phones = ''.join(
    f'<div class="pframe"><img src="{A}/phone/{f}.webp" alt="{a}" loading="lazy" decoding="async" width="600" height="1298"></div>'
    for f, a in (('01-home', 'amea.ng home on a phone'), ('04-map', 'The licence map on a phone'),
                 ('08-contact', 'The enquiry form on a phone')))

body = f'''
<div class="readbar" aria-hidden="true"><i></i></div>
<article class="postpage">
<section class="sect post-top"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="../../insights/index.html">Insights</a><span aria-hidden="true">/</span><span>Web</span></nav>
<p class="eyebrow post-flag"><span class="feat">Featured</span> Web &middot; Case story</p>
<h1 class="post-title rv">What makes a website actually work for a business?</h1>
<p class="lede post-lede rv">Traffic is not the goal. Clarity, trust and a next step are. This is the story of how we brought AMEA back online, and what rebuilding their website taught us about the difference between a site that exists and a site that works.</p>
<div class="post-meta"><span>By Graphcent Studio</span><span>{DATE}</span><span data-readtime>7 min read</span></div>
</div></section>

<div class="wrap"><figure class="post-hero rv"><div class="pframe"><img src="{A}/hero.webp" alt="The new amea.ng homepage on desktop" width="2160" height="1350" decoding="async" fetchpriority="high"></div><figcaption>The new <a href="https://amea.ng/" target="_blank" rel="noopener">amea.ng</a>, designed and built by Graphcent.</figcaption></figure></div>

<section class="sect post-wrap"><div class="wrap post-grid">
<aside class="post-aside" aria-label="Project at a glance">
<dl class="glance">
<div><dt>Client</dt><dd>AMEA Agro and Mining Export Alliance Limited, Kano</dd></div>
<div><dt>Problem</dt><dd>Old website down, brand needed a revamp</dd></div>
<div><dt>We delivered</dt><dd>Design, frontend, forms backend, email, SEO, launch, handover</dd></div>
<div><dt>Live</dt><dd><a href="https://amea.ng/" target="_blank" rel="noopener">amea.ng &#8599;</a></dd></div>
</dl>
<a class="tlink" href="../../work/amea/index.html">See the case study <span class="ar" aria-hidden="true">&rarr;</span></a>
</aside>

<div class="post">
<h2 id="down">The website was down</h2>
<p>AMEA is an indigenous Nigerian company headquartered in Kano. It explores and mines solid minerals, develops integrated agriculture and builds export partnerships, with mining leases and exploration licences for gold, lithium and iron ore in Niger and Kebbi States.</p>
<p>When AMEA came to us, their website was down. For most businesses that is an inconvenience. For a company whose investors, buyers and partners check them online before the first call, it is a problem that speaks before you do. A dead link quietly asks the question nobody says out loud: <em>are they still operating?</em></p>
<p>They did not only need the site back. They needed it rebuilt so it would represent the company they are today, and keep working long after we handed it over.</p>

<blockquote class="pull rv"><p>A website that is down is not neutral. It is the first thing a serious partner learns about you.</p></blockquote>

<h2 id="job">Start with the job the site has to do</h2>
<p>Before we chose a colour or a font, we wrote down who visits AMEA and what each of them must leave with. Investors want proof: licences, locations and a company they can verify. Buyers want to know what AMEA trades and how to start a conversation. Communities, job seekers and the press each have their own question.</p>
<p>That list became the structure of the site: 21 pages, each with one clear purpose, and enquiry forms shaped around the different reasons people get in touch. A website works when every visitor can find their answer, and their next step, without having to think about where to look.</p>

<h2 id="build">Straight to code, with real content</h2>
<p>We skipped the static mockup stage and designed directly in the browser, with AMEA&rsquo;s real content on real phones and laptops. It meant every decision was tested where it would actually live, not on an artboard.</p>
<p>The result leads with a film of the work itself, a header that turns to glass as you scroll, and the feature we are proudest of: an interactive map of AMEA&rsquo;s licence areas, filterable by mineral, so an investor can see in seconds what the company holds and where.</p>
</div>
</div>
{fig(f'{A}/features/03-licence-map.webp', 'Interactive map of AMEA licence areas on amea.ng', 'Six licence areas, mapped and filterable by mineral. Proof an investor can see, not just read.')}
<div class="wrap post-grid"><div class="post-aside-pad" aria-hidden="true"></div><div class="post">
<p>We also wrote six plain-language explainers on the questions AMEA gets asked most: what a mining lease actually is, what lithium spodumene is, how a mineral goes from exploration to market. Good content does two jobs at once. It answers a real visitor, and it gives search engines a reason to send the next one.</p>

<h2 id="forms">The part nobody sees: forms that actually arrive</h2>
<p>This is where many business websites quietly fail. The contact form looks fine, a visitor fills it in, and the message goes nowhere. The visitor thinks they have been ignored. The business never knew they existed.</p>
<p>We built the backend so that cannot happen on amea.ng. Every enquiry takes the same path:</p>
<ol class="flowline" aria-label="How an enquiry travels">
<li><b>Checked</b><span>Required fields are validated, and a hidden trap filters out spam bots.</span></li>
<li><b>Received</b><span>A Google Apps Script web app owned by AMEA receives the enquiry.</span></li>
<li><b>Recorded</b><span>It is written as a new row in a Google Sheet, a permanent record nothing can lose.</span></li>
<li><b>Delivered</b><span>An email lands at info@amea.ng, so the right person can reply the same day.</span></li>
</ol>
<p>One rule mattered more than any other: the form never pretends. If anything in that chain is not connected, the visitor sees a clear message with AMEA&rsquo;s email address instead of a fake &ldquo;thank you&rdquo;. Before launch we sent test enquiries until we saw the row appear and the email arrive.</p>
</div></div>
{fig(f'{A}/features/07-enquiry-form.webp', 'The amea.ng enquiry form', 'One form, routed by the reason someone is getting in touch.')}
<div class="wrap post-grid"><div class="post-aside-pad" aria-hidden="true"></div><div class="post">

<h2 id="found">Built to be found, and to respect visitors</h2>
<p>A website nobody finds does not work either, so search was built in from the first page, not added at the end:</p>
<ul class="ticks">
<li>Every page has its own title, description and social preview.</li>
<li>Structured data describes AMEA as an organisation on every page, with breadcrumbs, articles and an FAQ, so search engines understand what they are reading.</li>
<li>A sitemap and an open robots file welcome search engines and AI assistants, with a plain summary of the company so assistants describe AMEA accurately.</li>
<li>Pages are light and fast on mobile data, which is how most of AMEA&rsquo;s Nigerian visitors arrive.</li>
</ul>
<p>Trust is also about how you treat people. The site asks before it measures anything: analytics only runs for visitors who allow it in the cookie banner, and the privacy, cookie and terms pages say plainly what happens with their information.</p>
</div></div>
<div class="wrap"><figure class="pfig phones rv"><div class="ptrio">{phones}</div><figcaption>Designed for the phone first: home, the licence map and the enquiry form.</figcaption></figure></div>
<div class="wrap post-grid"><div class="post-aside-pad" aria-hidden="true"></div><div class="post">

<h2 id="launch">Launch day, on their own domain</h2>
<p>AMEA reviewed the site on a private preview link while we refined it. When they signed off, we pointed amea.ng at the new site, switched on HTTPS, and left the domain&rsquo;s email records untouched, so not a single message to an @amea.ng address was lost during the move. The site came back online as if it had never been away, only better.</p>

<h2 id="handover">The handover: every key, in their hands</h2>
<p>This is the step we care about most, and the one most often skipped. It is common for a business to lose its website simply because the only person with the logins has moved on. We did not want AMEA to ever be in that position again.</p>
<p>So the handover was not an email that said &ldquo;it&rsquo;s live&rdquo;. AMEA received:</p>
<ul class="handover">
<li><b>Domain and DNS</b><span>Access to the registrar account that controls amea.ng.</span></li>
<li><b>Hosting and code</b><span>The repository that holds every file of the website.</span></li>
<li><b>Forms and records</b><span>The Google account that owns the enquiry Sheet and the script behind it.</span></li>
<li><b>Analytics</b><span>The analytics property, ready to read whenever they need it.</span></li>
<li><b>A written guide</b><span>Plain-language steps for publishing changes, the forms and what to check if something stops.</span></li>
</ul>
<p>We walked the team through each login and made sure the credentials sat with them, not with us. We are still here when they need us. But a business should never <em>need</em> its agency to keep its own website alive.</p>

<h2 id="answer">So, what makes a website work?</h2>
<p>Looking back at AMEA, the answer has very little to do with traffic. A website works for a business when:</p>
<ol class="answers">
<li><b>It is up, and the business owns it.</b> Domain, hosting and logins in the client&rsquo;s hands.</li>
<li><b>It answers the visitor&rsquo;s question fast.</b> Clear structure, one purpose per page.</li>
<li><b>It earns trust with proof.</b> Real licences, real locations, real people.</li>
<li><b>It gives a next step that actually arrives.</b> Forms that record and deliver, every time.</li>
<li><b>It can be found.</b> Search built in from the first page.</li>
</ol>
<p>Everything else, the film, the glass header, the map, is how we make those five things feel good to use.</p>

<div class="post-card rv">
<div><p class="eyebrow">The full project</p><p class="post-card-t">See how we built amea.ng, with the live site, the enquiry pipeline and every screen.</p></div>
<div class="cta-row"><a class="btn btn-fill" href="../../work/amea/index.html">VIEW THE CASE STUDY <span class="ar" aria-hidden="true">&rarr;</span></a><a class="btn btn-ghost" href="https://amea.ng/" target="_blank" rel="noopener">VISIT AMEA.NG <span class="ar" aria-hidden="true">&#8599;</span></a></div>
</div>
</div></div>
</section>
</article>
'''

# the CTA in the shell reads well here too; scripts: no case.js on an article
tail = tail.replace('<script src="../../assets/js/case.js" defer></script>', '<script src="../../assets/js/post.js" defer></script>')

# reading time from the words actually on the page
words = len(re.sub(r'<[^>]+>', ' ', body).split())
mins = max(1, round(words / 230))
body = body.replace('<span data-readtime>7 min read</span>', f'<span data-readtime>{mins} min read</span>')

page = head + '<main id="main">' + body + tail
os.makedirs(os.path.join(ROOT, 'insights', SLUG), exist_ok=True)
open(os.path.join(ROOT, 'insights', SLUG, 'index.html'), 'w', encoding='utf-8').write(page)
print(f'built insights/{SLUG}/index.html, {words} words, {mins} min read')
