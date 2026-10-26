"""Add share buttons to every article page (insights/<slug>/index.html).

Run from the site root after building articles:  python3 tools/add-share.py .
Idempotent: earlier share blocks (between <!--share--> markers) are replaced.
Links work without JavaScript (they use the canonical URL); post.js swaps in the
page's real address, adds Copy link and the phone's own share sheet.
"""
import sys, os, re, json, glob, html
from urllib.parse import quote

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
ICONS = json.load(open(os.path.join(ROOT, 'tools/share-icons.json')))
home = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
LINKEDIN = re.search(r'data-icon="socials/linked">(<svg.*?</svg>)', home, re.S).group(1)


def si(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="{ICONS[name]}"/></svg>'


MAIL = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.6">'
        '<rect x="2.5" y="5" width="19" height="14"/><path d="M3 6l9 7 9-7"/></svg>')
LINK = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.6">'
        '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l3.2-3.2a4.5 4.5 0 0 0-6.4-6.4L11.6 6"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3.2 3.2a4.5 4.5 0 0 0 6.4 6.4l1.6-1.6"/></svg>')
SHARE = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.6">'
         '<path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M5 12v9h14v-9"/></svg>')


def bar(url, title, label, where):
    t, u = quote(title, safe=''), quote(url, safe='')
    links = [
        ('whatsapp', 'WhatsApp', f'https://wa.me/?text={t}%20{u}', si('whatsapp')),
        ('x', 'X', f'https://x.com/intent/post?text={t}&url={u}', si('x')),
        ('linkedin', 'LinkedIn', f'https://www.linkedin.com/sharing/share-offsite/?url={u}', LINKEDIN),
        ('facebook', 'Facebook', f'https://www.facebook.com/sharer/sharer.php?u={u}', si('facebook')),
        ('telegram', 'Telegram', f'https://t.me/share/url?url={u}&text={t}', si('telegram')),
        ('email', 'Email', f'mailto:?subject={t}&body={t}%0A%0A{u}', MAIL),
    ]
    a = ''.join(f'<a class="share-btn" data-net="{n}" href="{html.escape(h)}"'
                f'{"" if n == "email" else " target=\"_blank\" rel=\"noopener\""} aria-label="Share on {l}" title="{l}">{svg}</a>'
                for n, l, h, svg in links)
    return (f'<!--share--><div class="share share-{where}" data-share data-url="{html.escape(url)}" data-title="{html.escape(title)}">'
            f'<span class="share-k">{label}</span><div class="share-row">'
            f'<button type="button" class="share-btn share-native" data-share-native hidden aria-label="Share with another app">{SHARE}<span>Share</span></button>'
            f'{a}<button type="button" class="share-btn share-copy" data-share-copy aria-label="Copy link">{LINK}<span>Copy link</span></button>'
            f'</div><p class="vh" aria-live="polite" data-share-live></p></div><!--/share-->')


n = 0
for p in sorted(glob.glob(os.path.join(ROOT, 'insights/*/index.html'))):
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'<!--share-->.*?<!--/share-->', '', s, flags=re.S)
    url = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1)
    title = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1))).strip()
    # top: under the byline
    m = re.search(r'(<div class="post-meta">.*?</div>)', s, re.S)
    s = s[:m.end()] + bar(url, title, 'Share', 'top') + s[m.end():]
    # bottom: before the closing card
    k = s.index('<div class="post-card')
    s = s[:k] + bar(url, title, 'Share this story', 'end') + s[k:]
    open(p, 'w', encoding='utf-8').write(s)
    n += 1
    print('share buttons:', os.path.relpath(p, ROOT))
print(n, 'articles')
