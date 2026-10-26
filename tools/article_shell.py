"""Shared page shell for article pages (insights/<slug>/index.html).

The head, header, CTA and footer come from work/amea/index.html (same folder depth);
this swaps in the article's title, description, canonical, social image and
Article schema, marks Insights as the current section and loads post.js.
"""
import os, re, json, html


def make_page(root, slug, title, desc, date_iso, image, image_w, image_h, image_alt, about, body):
    url = f'https://graphcent.com/insights/{slug}/'
    shell = open(os.path.join(root, 'work/amea/index.html'), encoding='utf-8').read()
    head, rest = shell.split('<main id="main">', 1)
    tail = rest[rest.index('<section class="sect cta dark"'):]
    old_title = re.search(r'<title>(.*?)</title>', head).group(1)
    old_desc = re.search(r'<meta name="description" content="(.*?)">', head).group(1)
    head = head.replace(old_title, html.escape(f'{title} Insights: Graphcent', quote=False))
    head = head.replace(old_desc, html.escape(desc))
    head = head.replace('https://graphcent.com/work/amea/', url)
    head = head.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
    head = head.replace('https://graphcent.com/assets/images/og-graphcent.png', f'https://graphcent.com/{image}')
    head = re.sub(r'<meta property="og:image:width" content="\d+">', f'<meta property="og:image:width" content="{image_w}">', head)
    head = re.sub(r'<meta property="og:image:height" content="\d+">', f'<meta property="og:image:height" content="{image_h}">', head)
    head = re.sub(r'<meta property="og:image:alt" content="[^"]*">', f'<meta property="og:image:alt" content="{html.escape(image_alt)}">', head)
    schema = {
        '@context': 'https://schema.org', '@type': 'Article', 'headline': title, 'description': desc,
        'datePublished': date_iso, 'dateModified': date_iso, 'mainEntityOfPage': url,
        'image': f'https://graphcent.com/{image}',
        'author': {'@type': 'Organization', 'name': 'Graphcent', 'url': 'https://graphcent.com/'},
        'publisher': {'@type': 'Organization', 'name': 'Graphcent', 'url': 'https://graphcent.com/'},
        'about': about,
    }
    head = head.replace('</head>', '<script type="application/ld+json">' + json.dumps(schema) + '</script>\n</head>')
    head = head.replace(' aria-current="page">Work', '>Work')
    head = head.replace('href="../../insights/index.html">Insights', 'href="../../insights/index.html" aria-current="page">Insights', 1)
    tail = tail.replace('<script src="../../assets/js/case.js" defer></script>', '<script src="../../assets/js/post.js" defer></script>')
    words = len(re.sub(r'<[^>]+>', ' ', body).split())
    mins = max(1, round(words / 230))
    body = re.sub(r'<span data-readtime>[^<]*</span>', f'<span data-readtime>{mins} min read</span>', body)
    page = head + '<main id="main">' + body + tail
    os.makedirs(os.path.join(root, 'insights', slug), exist_ok=True)
    open(os.path.join(root, 'insights', slug, 'index.html'), 'w', encoding='utf-8').write(page)
    return words, mins
