"""The public project list, in display order. Drives the Work page, the homepage
(selected work, reel, featured case study), data.js PROJECTS, the sitemap and the
next-project chain. Unlaunched projects stay out of this list (and out of the repo).
"""

ORDER = ['aiff-26', 'amea', 'onemajlis', 'pegasus-interiors', 'colorwaves', 'ajyad', 'i-mac-academy', 'onims',
         'reclaim-and-renew', 'dreams-pharmacy', 'gurasar']

CARDS = {
    'aiff-26': dict(name='AIFF \u201926', rt='Event Branding', year='2026', filter='event-branding',
                    chips=['Creative Direction', 'Event Branding', 'Print Consultation'],
                    desc='Arewa Islamic Finance Forum 2026: the full visual presence of a five-day forum, from the social campaign to the stage, the venue and every printed piece.',
                    alt='The AIFF \u201926 welcome banner: Arewa Islamic Finance Forum, From Awareness to Adoption and Advocacy'),
    'amea': dict(name='AMEA', rt='Website Design &amp; Development', year='', filter='web-design',
                 chips=['Web Design', 'Frontend Development', 'Forms &amp; Email'],
                 desc='The old site was down. We rebuilt amea.ng end to end, from frontend development to the forms and email behind it.',
                 alt='The new amea.ng: the homepage over the mining film, the licence map and the licence records on a phone'),
    'onemajlis': dict(name='OneMajlis', rt='UI/UX Design &amp; Rebranding', year='2025', filter='ui-ux',
                      chips=['UI/UX Design', 'Rebranding', 'Web Design'],
                      desc='A halal community platform, rebranded and designed end to end: a dome and three figures, and the product at onemajlis.com.',
                      alt='OneMajlis button pins in navy and white with the dome-and-figures mark'),
    'pegasus-interiors': dict(name='Pegasus Interiors', rt='Brand Identity', year='2026', filter='brand-identity',
                              chips=['Brand Identity', 'Logo Design', 'Stationery'],
                              desc='They liked their logo but wanted something better. We built them a brand: a symbol that works at any size, an emblem, colour and stationery.',
                              alt='Pegasus Interiors: the new logo in brushed-steel letters on a charcoal shopfront sign'),
    'colorwaves': dict(name='ColorWaves', rt='Naming &amp; Brand Identity', year='2024', filter='brand-identity',
                       chips=['Brand Naming', 'Brand Identity', 'Guidelines'],
                       desc='A new paint, interiors and design company with no name. We named it, then built the identity from the name.',
                       alt='ColorWaves stationery on deep plum: letterhead, envelope, business cards and a mug with the rainbow W'),
    'ajyad': dict(name='Ajyad Investments', rt='Brand Identity', year='2025', filter='brand-identity',
                  chips=['Brand Identity', 'Logo Design', 'Guidelines'],
                  desc='One drop, three colours: an identity for an investment company in oil and gas, real estate and agriculture.',
                  alt='Ajyad ID cards on green with the three-colour drop'),
    'i-mac-academy': dict(name='I-MAC Academy', rt='Brand Identity', year='2025', filter='brand-identity',
                          chips=['Brand Identity', 'Logo Design', 'Guidelines'],
                          desc='A media academy wordmark where the i is a microphone and the m is an open book.',
                          alt='A microphone with an I-MAC mic flag on teal'),
    'onims': dict(name='Onims Agro Solutions', rt='Rebranding', year='2025', filter='brand-identity',
                  chips=['Rebranding', 'Logo Design', 'Guidelines'],
                  desc='An agricultural rebrand built on one letter: a circular N with two leaves in its negative space.',
                  alt='Stacks of Onims business cards on lime green'),
    'reclaim-and-renew': dict(name='Reclaim &amp; Renew', rt='Brand Identity', year='2024', filter='brand-identity',
                              chips=['Brand Identity', 'Logo Design', 'Campaign'],
                              desc='Three Rs turned into a triangle of renewal, for a cleaning company and its Cleaner Streets campaign.',
                              alt='Green, black and aqua Reclaim and Renew bins'),
    'dreams-pharmacy': dict(name='Dreams Pharmacy', rt='Rebranding', year='', filter='brand-identity',
                            chips=['Rebranding', 'Logo Design'],
                            desc='A pharmacy rebrand: a bold D with a capsule hidden in its negative space.',
                            alt='Dreams Pharmacy envelope, letterhead and cards on deep teal'),
    'gurasar': dict(name='Gurasar Banɗashe', rt='Packaging Design', year='', filter='graphic-design',
                    chips=['Packaging Design', 'Graphic Design'],
                    desc='A pizza box and takeaway bag in one bold red, with a hand-drawn food pattern and a round badge.',
                    alt='Red Gurasar takeaway bags, front and back'),
}


def next_of(slug):
    i = ORDER.index(slug)
    n = ORDER[(i + 1) % len(ORDER)]
    return n, CARDS[n]['name']


# The homepage "Featured case study" block
FEATURE = dict(
    slug='aiff-26', title='AIFF \u201926', img='hero.webp', w=2400, h=1280,
    alt='The AIFF \u201926 welcome banner at the venue entrance: Arewa Islamic Finance Forum',
    lede='Arewa Islamic Finance Forum 2026, convened by IFING Media. We took the event to full visibility: '
         'creative direction, design execution and print consultation for five days in Kano.',
    cols=[('Discipline', 'Creative direction and event branding, from the first countdown post to the last certificate.'),
          ('Approach', 'One pattern and palette carried through every touchpoint: social, stage, venue, wayfinding and print.'),
          ('Delivered', '18 to 22 July 2026 at Amani Event Center, Kano: campaign, stage, nine venue banners and the print kit.')],
)
