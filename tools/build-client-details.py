"""Build the client onboarding page (client-details/index.html).

Run from the site root:  python3 tools/build-client-details.py .   then tools/seo.py .
The page is sent to clients on WhatsApp after onboarding. It embeds the Graphcent
"Client & Project Details" Google Form and is kept out of search (noindex) and the menu.
The form has file-upload questions, so Google asks respondents to sign in; signing in
inside an embedded frame can be blocked (Safari/iOS), hence the "open the form" button.
"""
import sys, os, re

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
FORM = 'https://forms.gle/SdMWB7S6cp31DicD9'
EMBED = 'https://docs.google.com/forms/d/e/1FAIpQLSfnLN7crJgFA0OUWOtBs2QOkiMMpQI2lRdZjMC1BYGSg0E4QA/viewform?embedded=true'
WA = 'https://wa.me/2348122022600?text=' + 'Hello%20Graphcent%2C%20I%20need%20help%20with%20the%20client%20details%20form.'

MAIN = f'''<main id="main">
<section class="sect dark" style="padding-bottom:clamp(40px,5vw,70px)"><div class="wrap">
<p class="eyebrow">Client onboarding</p>
<h1 class="dl rv" style="margin-top:clamp(20px,3vw,40px)">YOUR BRAND,<br>IN DETAIL.</h1>
<p class="lede rv" style="margin-top:clamp(24px,3vw,44px)">Welcome to Graphcent. This form collects your business, brand and project details, so we can prepare your project documents and invoice and start the work properly. The more you share, the better the first round will be.</p>
<div class="cd-actions rv"><a class="btn btn-fill" href="{FORM}" target="_blank" rel="noopener">OPEN THE FORM <span class="ar" aria-hidden="true">&#8599;</span></a><a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">ASK US ON WHATSAPP</a></div>
<ol class="cd-steps rv">
<li><i>01</i><b>Get your files ready</b><span>Logo files, brand colours, photos and any references you like. You can upload them in the form.</span></li>
<li><i>02</i><b>Sign in with Google</b><span>Google asks you to sign in before you can upload files. Your answers come straight to the Graphcent team.</span></li>
<li><i>03</i><b>We take it from here</b><span>We review everything and confirm the next steps with you on WhatsApp.</span></li>
</ol>
</div></section>
<section class="sect" id="form"><div class="wrap" style="max-width:860px">
<div class="cd-embed"><iframe src="{EMBED}" title="Graphcent client and project details form" loading="lazy" data-embed>Loading the form&hellip;</iframe></div>
<p class="cd-note">Form not loading, or stuck on Google sign-in? <a href="{FORM}" target="_blank" rel="noopener">Open it in a new tab <span aria-hidden="true">&#8599;</span></a> and fill it in there.</p>
</div></section>
</main>'''

src = open(os.path.join(ROOT, 'brief/index.html'), encoding='utf-8').read()
a = src.index('<main id="main">'); b = src.index('</main>') + len('</main>')
page = src[:a] + MAIN + src[b:]
title = 'Client & Project Details: Graphcent'
desc = 'Graphcent client onboarding: share your business, brand and project details, and upload your files, so we can start your project.'
page = re.sub(r'<title>.*?</title>', f'<title>{title.replace("&", "&amp;")}</title>', page, count=1)
page = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, page, count=1)
page = page.replace('https://graphcent.com/brief/', 'https://graphcent.com/client-details/')
if '<meta name="robots"' not in page:
    page = page.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, nofollow">', 1)
os.makedirs(os.path.join(ROOT, 'client-details'), exist_ok=True)
open(os.path.join(ROOT, 'client-details/index.html'), 'w', encoding='utf-8').write(page)
print('built client-details/')
