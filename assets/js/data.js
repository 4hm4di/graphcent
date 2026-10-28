/* ==========================================================
   Graphcent: data.js
   Single source of truth for site content.

   SOURCING RULE
   Every string in this file is either (a) taken from
   graphcent.framer.media, (b) taken from the Behance project
   titles supplied in the brief, or (c) studio-authored copy
   written for this site. Nothing here is invented fact:
   no fabricated results, statistics, testimonials or clients.

   Fields marked  // VERIFY  are blank on purpose because the
   source was not publicly readable. Fill them in rather than
   guessing: see README.md.
   ========================================================== */

window.GC = (function () {
  const BRAND = {
    name: 'Graphcent',
    descriptor: 'Creative & Marketing Studio',
    founded: 2019,
    founder: 'Ahmad Abdallah',
    founderRole: 'Founder & Creative Director',
    founderInstagram: 'https://instagram.com/fl.ahmard',
    founderGithub: 'https://github.com/4hm4di',
    founderLinkedin: 'https://www.linkedin.com/in/ahmard/',
    email: 'hello@graphcent.com',
    /* Google Apps Script web app (/exec URL) that receives the forms. Empty = mail-app fallback. */
    formEndpoint: 'https://script.google.com/macros/s/AKfycbzEiDNPzvzbr8_ifr6dQoWND7H7EXXEL-yptC7r6caGpHOUIDBPLoowqd9HHY7ad9p8hg/exec',
    phone: '+234 812 202 2600',
    phoneHref: 'tel:+2348122022600',
    whatsapp: '2348122022600',          // wa.me number: country code, no + or spaces
    /* Google reviews (homepage). Add apiKey to switch the section on:
       apiKey   a browser key restricted to graphcent.com/* and to "Places API (New)"
       placeId  optional; when blank the site finds it from `query` (one lookup per visit)
       profile  the Google Business Profile link (Graphcent Ventures, Kano) */
    reviews: { apiKey: '', placeId: '', query: 'Graphcent Ventures, Tukuntawa Quarters, Kano',
               profile: 'https://share.google/HXJt5c3vsTtt2XMGD' },
    location: 'Kano, Nigeria',
    hours: 'Monday to Saturday, 9:00 to 18:00 GMT+1',
    socials: [
      ['Behance', 'https://www.behance.net/graphcent'],
      ['Instagram', 'https://instagram.com/graphcent'],
      ['LinkedIn', 'https://www.linkedin.com/in/graphcent'],
      ['TikTok', 'https://www.tiktok.com/@graphcentprints']
    ]
  };

  /* ---- the six projects supplied in the brief ----
     year / description present only where documented.      */
  /* Public projects, in display order (tools/site_projects.py). */
  const PROJECTS = [
    { slug: 'aiff-26', name: 'AIFF ’26', category: 'Event Branding', filter: 'event-branding', year: '2026',
      summary: 'Arewa Islamic Finance Forum 2026: the full visual presence of a five-day forum, from the social campaign to the stage, the venue and every printed piece.' },
    { slug: 'amea', name: 'AMEA', category: 'Website Design & Development', filter: 'web-design', year: '',
      summary: 'The old site was down. We rebuilt amea.ng end to end, from frontend development to the forms and email behind it.' },
    { slug: 'onemajlis', name: 'OneMajlis', category: 'UI/UX Design & Rebranding', filter: 'ui-ux', year: '2025',
      summary: 'A halal community platform, rebranded and designed end to end: a dome and three figures, and the product at onemajlis.com.' },
    { slug: 'pegasus-interiors', name: 'Pegasus Interiors', category: 'Brand Identity', filter: 'brand-identity', year: '2026',
      summary: 'They liked their logo but wanted something better. We built them a brand: a symbol that works at any size, an emblem, colour and stationery.' },
    { slug: 'colorwaves', name: 'ColorWaves', category: 'Naming & Brand Identity', filter: 'brand-identity', year: '2024',
      summary: 'A new paint, interiors and design company with no name. We named it, then built the identity from the name.' },
    { slug: 'ajyad', name: 'Ajyad Investments', category: 'Brand Identity', filter: 'brand-identity', year: '2025',
      summary: 'One drop, three colours: an identity for an investment company in oil and gas, real estate and agriculture.' },
    { slug: 'i-mac-academy', name: 'I-MAC Academy', category: 'Brand Identity', filter: 'brand-identity', year: '2025',
      summary: 'A media academy wordmark where the i is a microphone and the m is an open book.' },
    { slug: 'onims', name: 'Onims Agro Solutions', category: 'Rebranding', filter: 'brand-identity', year: '2025',
      summary: 'An agricultural rebrand built on one letter: a circular N with two leaves in its negative space.' },
    { slug: 'reclaim-and-renew', name: 'Reclaim & Renew', category: 'Brand Identity', filter: 'brand-identity', year: '2024',
      summary: 'Three Rs turned into a triangle of renewal, for a cleaning company and its Cleaner Streets campaign.' },
    { slug: 'dreams-pharmacy', name: 'Dreams Pharmacy', category: 'Rebranding', filter: 'brand-identity', year: '',
      summary: 'A pharmacy rebrand: a bold D with a capsule hidden in its negative space.' },
    { slug: 'gurasar', name: 'Gurasar Banɗashe', category: 'Packaging Design', filter: 'graphic-design', year: '',
      summary: 'A pizza box and takeaway bag in one bold red, with a hand-drawn food pattern and a round badge.' }
  ];

  /* Filters render only when at least one project matches,
     so the archive never shows an empty category.           */
  const FILTERS = [
    ['all', 'All'],
    ['brand-identity', 'Brand Identity'],
    ['graphic-design', 'Graphic Design'],
    ['ui-ux', 'UI/UX'],
    ['web-design', 'Web Design'],
    ['creative-direction', 'Creative Direction']
  ];

  const WORDS = ['Brand Identity', 'UI/UX', 'Web Design', 'Marketing',
                 'Creative Direction', 'Graphic Design', 'Print', 'Social Media'];

  const SERVICES = [
    { n: '01', t: 'Brand Identity', icon: 'brand-identity', peek: 'onims/world/branding.webp',
      d: 'Brand strategy, naming direction, visual identity, logo systems and brand guidelines.' },
    { n: '02', t: 'UI/UX Design', icon: 'ui-ux-design', peek: 'onemajlis/product/site-hero.webp',
      d: 'Mobile apps, web applications, dashboards, design systems and digital product experiences.' },
    { n: '03', t: 'Web Design & Development', icon: 'web-design-development', peek: 'amea/hero.webp',
      d: 'Websites, landing pages, WordPress websites, frontend development and digital experiences.' },
    { n: '04', t: 'Creative Direction', icon: 'creative-direction', peek: 'aiff-26/hero.webp',
      d: 'Visual direction across brands, campaigns, launches and digital experiences.' },
    { n: '05', t: 'Graphic Design', icon: 'graphic-design', peek: 'gurasar/world/pizza-boxes.webp',
      d: 'Campaigns, marketing materials, editorial design, social assets and visual communication.' },
    { n: '06', t: 'Printing & 3D Signage Fabrication', icon: 'printing-signage', peek: 'pegasus-interiors/mockups/signage.webp',
      d: 'Physical brand applications, signage, print production, large-format graphics and 3D fabricated brand installations.' },
    { n: '07', t: 'Social Media Management', icon: 'social-media-management', peek: 'aiff-26/social/05-tickets-open.webp',
      d: 'Content planning, creative production, platform management and brand consistency.' },
    { n: '08', t: 'Marketing', icon: 'marketing', peek: 'reclaim-and-renew/world/billboard.webp',
      d: 'Campaign development, digital marketing, promotional creative and strategic brand communication.' }
  ];

  const DEFINES = [
    { icon: 'creative-thinking', t: 'Creative Thinking',
      d: 'We look beyond the obvious to find ideas that give brands character and direction.' },
    { icon: 'clear-communication', t: 'Clear Communication',
      d: 'Good design should make an idea easier to understand, not harder.' },
    { icon: 'real-business', t: 'Built for Real Business',
      d: 'We create work that looks good, works properly and makes sense for the business behind it.' },
    { icon: 'flexible-team', t: 'Flexible by Design',
      d: 'Our team structure allows us to bring the right people into each project.' },
    { icon: 'idea-to-execution', t: 'From Idea to Execution',
      d: 'We can take a project from strategy and identity through digital, marketing and physical production.' }
  ];

  const ARTICLES = [
    { slug: 'why-a-logo-is-not-a-brand', cat: 'Branding', title: 'Why a logo is not a brand',
      excerpt: 'Pegasus Interiors asked for a better logo. What they needed was a brand. A story about the difference.',
      date: '6 June 2026', read: '4 min read', url: 'insights/why-a-logo-is-not-a-brand/', thumb: 'assets/images/insights/01-why-a-logo-is-not-a-brand.webp' },
    { slug: 'what-makes-a-website-work', cat: 'Web', title: 'What makes a website actually work for a business?',
      excerpt: 'How we brought AMEA\u2019s website back online, from the first line of code to handing over every login.',
      date: 'October 2026', read: '5 min read', featured: true, url: 'insights/what-makes-a-website-work/', thumb: 'assets/images/insights/02-what-makes-a-website-work.webp' },
    { slug: 'designing-for-nigerian-businesses', cat: 'Creative Business', title: 'Designing for Nigerian businesses without losing good design',
      excerpt: 'Local context and high design standards are not opposites. They need each other.',
      date: 'September 2025', read: '3 min read', thumb: 'assets/images/insights/03-designing-for-nigerian-businesses.webp' }
  ];

  const ARTICLE_CATEGORIES = ['Branding', 'Design', 'Marketing', 'UI/UX', 'Web', 'Creative Business', 'Studio Notes'];

  /* Process copy condensed from graphcent.framer.media */
  const PROCESS = [
    { n: '01', t: 'Research',
      d: 'We start by understanding your market, audience and business goals. Competitor analysis, brand audits and interviews show where the brand stands today and what has to change for it to grow.' },
    { n: '02', t: 'Strategy',
      d: 'We define the core of the brand: positioning, messaging and tone of voice. That foundation decides how the brand communicates and behaves on every platform, visually and verbally.' },
    { n: '03', t: 'Design',
      d: 'Strategy becomes a visual identity: logo, colour, typography and imagery: applied consistently across website, print and social so the brand is recognisable wherever it appears.' }
  ,
    { n: '04', t: 'Execution',
      d: 'We build and produce the work. Websites, apps, campaigns, social content, print and signage, delivered as finished pieces the business can actually use.' }
  ];

  /* Verified on the studio's own About page. */
  /* Team: roles checked against each person's own LinkedIn / Instagram, October 2026.
     Portraits in assets/team (mono + colour), section built by tools/add-team.py. */
  const TEAM = [
    { slug: 'muhd-hussain-kamsusi', name: 'Muhd Hussain Kamsusi', role: 'Project Manager',
      linkedin: 'https://www.linkedin.com/in/lambu-hussain-b5a4b3187', instagram: 'https://www.instagram.com/lambu_hussain' },
    { slug: 'ibrahim-abubakar-aliyu', name: 'Ibrahim Abubakar Aliyu', role: 'UI/UX Designer',
      instagram: 'https://www.instagram.com/raiss_design' },
    { slug: 'al-amin-abdullahi-daho', name: 'Al-amin Abdullahi Daho', role: 'Developer & Data Analyst',
      linkedin: 'https://www.linkedin.com/in/alamindaho', instagram: 'https://www.instagram.com/alamindaho' },
    { slug: 'muhammad-ameen', name: 'Muhammad Ameen', role: 'Cinematographer & Editor',
      linkedin: 'https://www.linkedin.com/in/muh%E2%80%99d-mas-888475238', instagram: 'https://www.instagram.com/muhd.mas' },
    { slug: 'habiba-aliyu-galadima', name: 'Habiba Aliyu Galadima', role: 'Content Creator & Strategist',
      instagram: 'https://www.instagram.com/thecinebloom' }
  ];

  const STATS = [
    { n: 232, suffix: '+', k: 'Projects Delivered',
      p: 'Small and large projects across branding, digital, marketing and creative production.' },
    { n: 7, suffix: '+', k: 'Years Experience',
      p: 'Seven years working across creative design, branding, digital experiences and visual communication.' },
    { n: 8, suffix: '', k: 'Creatives',
      p: 'The people behind creative direction, design, development and production.' },
    { n: 97, suffix: '%', k: 'Client Satisfaction',
      p: 'How clients rate their experience working with Graphcent.' }
  ];

  /* Verified on the studio's own About page. */
  const AWARDS = [
    { org: 'African International Conference on Islamic Finance', award: 'Outstanding Media Deliverance', year: '2025' },
    { org: 'Northern GenZ Awards', award: 'Best Branding Agency', year: '2024' },
    { org: 'Arewa Islamic Finance Summit', award: 'Event Branding', year: '2024' },
    { org: 'GSDC NWU Chapter', award: 'Best Designer of the Chapter', year: '2023' },
    { org: 'Stemlab Tech Hub', award: 'Iconic Designer of the Hub', year: '2021' }
  ];

  /* Only names with a documented Graphcent relationship:
     the six project clients, plus the organisations named in
     the studio's own awards list. Add or correct in one place. */
  const CLIENTS = [
    { name: 'Feiyaz Consults', note: 'Rebranding' },
    { name: 'Sinch-X', note: 'Brand guide' },
    { name: 'Zakta', note: 'Brand identity' },
    { name: 'Elastic', note: 'Brand identity' },
    { name: 'N-Medix', note: 'Visual identity' },
    { name: 'JLCF', note: 'Identity' },
    { name: 'African Intl. Conference on Islamic Finance', note: 'Media' },
    { name: 'Arewa Islamic Finance Summit', note: 'Event branding' },
    { name: 'Northern GenZ Awards', note: 'Branding' },
    { name: 'GSDC NWU Chapter', note: 'Design' },
    { name: 'Stemlab Tech Hub', note: 'Design' },
    { name: 'OneMajlis', note: 'Landing page' },
    { name: 'Ray Detergents', note: 'Website and inventory' },
    { name: 'ColorWaves', note: 'Partner' },
    { name: 'IFING Media', note: 'Partner' },
    { name: 'MTECH Noble Hub', note: 'Partner' }
  ];

  const PRICING = [
    { n: '01', t: 'Starter', price: '\u20A670K+', items: [
      'Focused design requests', 'Social media assets',
      'Single creative deliverables', 'Smaller design needs' ] },
    { n: '02', t: 'Brand & Digital', price: '\u20A6250K \u2014 1.5M+', items: [
      'Brand identity', 'UI/UX design', 'Websites',
      'Visual systems', 'Larger design engagements' ] },
    { n: '03', t: 'Full Creative Engagement', price: '\u20A61.5M \u2014 5M+', items: [
      'Comprehensive brand identity', 'Large digital products',
      'Multiple brand touchpoints', 'Creative direction', 'Complex design systems' ] }
  ];

  const BUDGETS = ['\u20A670K \u2013 \u20A6250K', '\u20A6250K \u2013 \u20A61M',
                   '\u20A61M \u2013 \u20A62.5M', '\u20A62.5M \u2013 \u20A65M+', 'Not sure yet'];

  const TIMELINES = ['As soon as possible', '2 \u2013 4 weeks', '4 \u2013 8 weeks',
                     'Later this year', 'Still exploring'];

  /* FAQ copy from graphcent.framer.media */
  const FAQ = [
    { q: 'Who do you typically work with?',
      a: 'Ambitious brands, agencies and creatives who want to push boundaries: whether you are launching a product, refreshing an identity or building a full digital experience.' },
    { q: 'What is your creative process like?',
      a: 'We start by listening closely to understand your goals and challenges. From there we research, develop concepts, storyboard, design and refine until everything is polished. Communication stays open at every stage.' },
    { q: 'How long does a typical project take?',
      a: 'Timelines vary with scope and complexity, but most projects take between two and eight weeks. We set clear expectations upfront and give regular updates throughout.' },
    { q: 'Who actually does the work?',
      a: 'Our core team handles creative direction, design, UI/UX, development and media production. For specialised needs we bring in trusted partners such as VFX artists, photographers and sound designers.' }
  ];

  return { BRAND, TEAM, PROJECTS, FILTERS, WORDS, SERVICES, DEFINES, ARTICLES,
           ARTICLE_CATEGORIES, PROCESS, STATS, AWARDS, CLIENTS, PRICING,
           BUDGETS, TIMELINES, FAQ };
})();
