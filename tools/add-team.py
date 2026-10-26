"""Insert the team section into studio/index.html (between <!--team--> markers; idempotent).

Run from the site root: python3 tools/add-team.py .
Portraits in assets/team/<slug>.webp (mono) and <slug>-colour.webp, made uniform from the
team's own photos: background removed, aligned by face, one backdrop, graded as a set.
Roles checked against each person's own LinkedIn / Instagram (October 2026).
"""
import sys, os, re, html
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
esc = lambda t: html.escape(t, quote=True)
TEAM = [  # slug, name, role, links
    ('muhd-hussain-kamsusi', 'Muhd Hussain Kamsusi', 'Project Manager',
     [('LinkedIn', 'https://www.linkedin.com/in/lambu-hussain-b5a4b3187'), ('Instagram', 'https://www.instagram.com/lambu_hussain')]),
    ('ibrahim-abubakar-aliyu', 'Ibrahim Abubakar Aliyu', 'UI/UX Designer',
     [('Instagram', 'https://www.instagram.com/raiss_design')]),
    ('al-amin-abdullahi-daho', 'Al-amin Abdullahi Daho', 'Developer & Data Analyst',
     [('LinkedIn', 'https://www.linkedin.com/in/alamindaho'), ('Instagram', 'https://www.instagram.com/alamindaho')]),
    ('muhammad-ameen', 'Muhammad Ameen', 'Cinematographer & Editor',
     [('LinkedIn', 'https://www.linkedin.com/in/muh%E2%80%99d-mas-888475238'), ('Instagram', 'https://www.instagram.com/muhd.mas')]),
    ('habiba-aliyu-galadima', 'Habiba Aliyu Galadima', 'Content Creator & Strategist',
     [('Instagram', 'https://www.instagram.com/thecinebloom')]),
]
p = os.path.join(ROOT, 'studio/index.html')
s = open(p, encoding='utf-8').read()
s = re.sub(r'<!--team-->.*?<!--/team-->', '', s, flags=re.S)
ICON = {
    'Instagram': re.search(r'data-icon="socials/instagram">(<svg.*?</svg>)', s, re.S).group(1),
    'LinkedIn': re.search(r'data-icon="socials/linked">(<svg.*?</svg>)', s, re.S).group(1),
}
cards = ''
for slug, name, role, links in TEAM:
    first = name.split()[0]
    soc = ''.join(f'<a class="tm-link" href="{esc(u)}" target="_blank" rel="noopener" aria-label="{esc(first)} on {n}">'
                  f'<span class="ico ico-sm">{ICON[n]}</span></a>' for n, u in links)
    cards += (f'<li class="tm rv"><div class="tm-photo">'
              f'<img src="../assets/team/{slug}.webp" alt="{esc(name)}, {esc(role)} at Graphcent" loading="lazy" decoding="async" width="800" height="1000">'
              f'<img class="tm-colour" src="../assets/team/{slug}-colour.webp" alt="" aria-hidden="true" loading="lazy" decoding="async" width="800" height="1000">'
              f'</div><div class="tm-meta"><div><h3>{esc(name)}</h3><p>{esc(role)}</p></div><div class="tm-links">{soc}</div></div></li>')
block = ('<!--team--><section class="sect" style="padding-top:0"><div class="wrap">'
         '<div class="split" style="align-items:end"><div><p class="eyebrow">The team</p>'
         '<h2 class="dm rv" style="margin-top:clamp(16px,2vw,24px)">THE PEOPLE<br>BEHIND THE WORK.</h2></div>'
         '<p class="lede rv">Design, development, film and content, from one team. Each project brings in the people it needs, '
         'led from first call to final file.</p></div>'
         f'<ul class="team">{cards}</ul></div></section><!--/team-->')
i = s.index('<p class="eyebrow">Founder</p>')
end = s.index('</section>', i) + len('</section>')
s = s[:end] + block + s[end:]
open(p, 'w', encoding='utf-8').write(s)
print('team section:', len(TEAM), 'people')
