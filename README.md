# Graphcent

The website of Graphcent, a creative and marketing studio in Kano, Nigeria: **[graphcent.com](https://graphcent.com)**.

A plain static site: HTML, CSS and a little JavaScript. No framework, no build step needed to publish.

## Publishing

GitHub Pages, from the `main` branch, root folder. The `CNAME` file holds the custom domain `graphcent.com`.
`.nojekyll` tells Pages to publish the files exactly as they are.

## Structure

- `index.html`, `work/`, `studio/`, `insights/`, `contact/`, `brief/`, legal pages, `404.html`
- `assets/css/` tokens.css, site.css, refine.css
- `assets/js/` data.js (content), site.js (site behaviour), studio.js (homepage and 404 pieces), case.js (case studies), post.js (articles)
- `assets/projects/<slug>/` project images; `assets/guides/` downloadable guides (portfolio editions)
- `tools/` small Python scripts that build pages and listings

## Updating

- Project order, cards and service previews: edit `tools/site_projects.py`, then `python3 tools/build-listings.py .`
- Identity case studies: edit `tools/identity_projects.py`, then `python3 tools/build-identity.py .`
- Articles: `python3 tools/build-article-*.py`, then `python3 tools/add-share.py .`
- Shared footer and icons: `npm run build`
- Search and social previews, last: `python3 tools/make-og.py .` (when images or titles change), then `python3 tools/seo.py .`
  It sets titles, descriptions, Open Graph / X tags, 1200x630 JPG previews (`assets/og/`), icons, structured data and the sitemap.

## Guides and client work

Downloadable guides are portfolio editions: pages flattened to images, contact details removed, and a credit
line on every page. All client logos, names and artwork belong to their owners and are shown as examples of
Graphcent's work. They are not licensed for reuse.

© Graphcent. All rights reserved.
