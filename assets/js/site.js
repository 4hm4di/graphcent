/* ==========================================================
   Graphcent: site.js
   No dependencies. Transform-based motion only.
   Every behaviour degrades cleanly without JS and respects
   prefers-reduced-motion.
   ========================================================== */

(function () {
  'use strict';

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const $  = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.prototype.slice.call((r || document).querySelectorAll(s));

  /* ------------------------------------------------------
     1. Seamless marquees
     A track is duplicated once. The CSS animation runs
     0 -> -50%, so frame 0 and frame N are pixel-identical:
     no jump, no gap, no reset flash. Duplicating in JS keeps
     the markup honest for screen readers (aria-hidden copy).
     ------------------------------------------------------ */
  function buildMarquees() {
    $$('[data-marquee] .track').forEach(function (track) {
      if (track.dataset.built) return;
      const originals = Array.prototype.slice.call(track.children);
      if (!originals.length) return;

      function addPass() {
        originals.forEach(function (node) {
          const copy = node.cloneNode(true);
          copy.classList.add('dupe');
          copy.setAttribute('aria-hidden', 'true');
          $$('a, button, input', copy).concat(copy.matches('a, button') ? [copy] : [])
            .forEach(function (f) { f.setAttribute('tabindex', '-1'); });
          track.appendChild(copy);
        });
      }

      /* The CSS translates the track by -50%, so the track must always hold
         an EVEN number of identical sets or the loop visibly jumps. One
         duplicate pass gives two sets. On a wide viewport a short row would
         still show a gap before the reset, so add further passes in PAIRS,
         which keeps the set count even. Capped so a long row cannot run away. */
      addPass();
      var passes = 1;
      var target = window.innerWidth * 2;
      while (track.scrollWidth / 2 < target && passes < 7) {
        addPass(); addPass(); passes += 2;
      }

      track.dataset.built = '1';
    });
  }

  /* Pause a marquee while it is off screen: keeps long pages cheap. */
  function marqueeVisibility() {
    if (!('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        const t = $('.track', e.target);
        if (t) t.style.animationPlayState = e.isIntersecting ? '' : 'paused';
      });
    }, { rootMargin: '120px' });
    $$('[data-marquee]').forEach(function (m) { io.observe(m); });
  }

  /* ------------------------------------------------------
     2. Scroll reveals
     ------------------------------------------------------ */
  function reveals() {
    const els = $$('.rv');
    if (reduce.matches || !('IntersectionObserver' in window)) {
      els.forEach(function (e) { e.classList.add('in'); });
      return;
    }
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    els.forEach(function (e) { io.observe(e); });
  }

  /* ------------------------------------------------------
     3. Header colour: reads what sits just under its edge
     ------------------------------------------------------ */
  function headerTone() {
    const header = $('.nav');
    if (!header) return;
    const themeMeta = $('meta[name="theme-color"]');
    let ticking = false, lastDark = null;
    // progressive-blur strip just under the bar (styled in refine.css §31)
    const fade = document.createElement('div');
    fade.className = 'navfade';
    fade.setAttribute('aria-hidden', 'true');
    fade.innerHTML = '<i></i><i></i><i></i><i></i><i></i><i></i>';
    header.after(fade);
    function run() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        const probe = header.offsetHeight + 8;
        let dark = false;
        $$('.dark, footer').forEach(function (s) {
          const r = s.getBoundingClientRect();
          if (r.top <= probe && r.bottom > probe) dark = true;
        });
        header.classList.toggle('on-dark', dark);
        // frosted only once content is passing beneath it
        const scrolled = window.scrollY > 2;
        header.classList.toggle('is-scrolled', scrolled);
        fade.classList.toggle('on', scrolled);
        document.documentElement.style.setProperty('--navh', header.offsetHeight + 'px');
        // the phone's status bar takes the colour of the header beneath it
        if (themeMeta && dark !== lastDark) {
          themeMeta.setAttribute('content', dark ? '#0A0B35' : '#F3F2EE');
          lastDark = dark;
        }
        ticking = false;
      });
    }
    window.addEventListener('scroll', run, { passive: true });
    window.addEventListener('resize', run);
    run();
  }

  /* ------------------------------------------------------
     4. Mobile menu
     ------------------------------------------------------ */
  function menu() {
    const burger = $('#burger'), overlay = $('#overlay');
    if (!burger || !overlay) return;
    function set(open) {
      document.body.classList.toggle('menu', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      overlay.setAttribute('aria-hidden', String(!open));
      // closed menu: its links must not be reachable with Tab either
      overlay.inert = !open;
      $$('a', overlay).forEach(function (a) { if (open) a.removeAttribute('tabindex'); else a.setAttribute('tabindex', '-1'); });
    }
    set(false);
    burger.addEventListener('click', function () {
      set(!document.body.classList.contains('menu'));
    });
    $$('a', overlay).forEach(function (a) { a.addEventListener('click', function () { set(false); }); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('menu')) set(false);
    });
  }

  /* ------------------------------------------------------
     5. Process: active step follows the scroll position
     ------------------------------------------------------ */
  function processScroll() {
    const host = $('[data-process]');
    if (!host) return;
    const steps = $$('.pstep', host);
    const segs = $$('.pbar .seg', host);
    const visuals = $$('.pvisual > *', host);
    if (!steps.length) return;

    function activate(i) {
      steps.forEach(function (s, k) { s.classList.toggle('on', k === i); });
      segs.forEach(function (s, k) { s.classList.toggle('on', k <= i); });
      visuals.forEach(function (v, k) { v.classList.toggle('on', k === i); });
    }
    activate(0);
    if (reduce.matches) { steps.forEach(function (s) { s.classList.add('on'); });
                          segs.forEach(function (s) { s.classList.add('on'); });
                          visuals.forEach(function (v) { v.classList.add('on'); }); return; }

    let ticking = false;
    function run() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        const line = window.innerHeight * 0.52;
        let active = 0;
        steps.forEach(function (s, k) {
          if (s.getBoundingClientRect().top <= line) active = k;
        });
        activate(active);
        ticking = false;
      });
    }
    window.addEventListener('scroll', run, { passive: true });
    window.addEventListener('resize', run);
    run();
  }

  /* ------------------------------------------------------
     6. Stat counters: verified numbers only
     ------------------------------------------------------ */
  function counters() {
    const nodes = $$('[data-count]');
    if (!nodes.length) return;
    function paint(el, v) {
      el.textContent = (el.dataset.plain === 'true')
        ? String(v)
        : v.toLocaleString('en-US') + (el.dataset.suffix || '');
    }
    if (reduce.matches || !('IntersectionObserver' in window)) {
      nodes.forEach(function (el) { paint(el, +el.dataset.count); });
      return;
    }
    nodes.filter(function (el) { return el.dataset.plain === 'true'; })
         .forEach(function (el) { paint(el, +el.dataset.count); });
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        const el = e.target, target = +el.dataset.count, t0 = performance.now(), dur = 1400;
        (function step(now) {
          const p = Math.min(1, (now - t0) / dur);
          const eased = 1 - Math.pow(1 - p, 3);
          paint(el, Math.round(target * eased));
          if (p < 1) requestAnimationFrame(step);
        })(t0);
        io.unobserve(el);
      });
    }, { threshold: 0.4 });
    nodes.forEach(function (el) {
      if (el.dataset.plain === 'true') return;   // years are stated, not counted
      paint(el, 0);
      io.observe(el);
    });
  }

  /* ------------------------------------------------------
     7. Founder portrait parallax: small, transform only
     ------------------------------------------------------ */
  function parallax() {
    const imgs = $$('[data-parallax]');
    if (!imgs.length || reduce.matches) return;
    let ticking = false;
    function run() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        imgs.forEach(function (img) {
          const host = img.parentElement.getBoundingClientRect();
          if (host.bottom < -200 || host.top > window.innerHeight + 200) return;
          const mid = host.top + host.height / 2 - window.innerHeight / 2;
          const shift = Math.max(-28, Math.min(28, (mid / window.innerHeight) * -34));
          img.style.transform = 'translate3d(0,' + shift.toFixed(2) + 'px,0) scale(1.08)';
        });
        ticking = false;
      });
    }
    window.addEventListener('scroll', run, { passive: true });
    window.addEventListener('resize', run);
    run();
  }

  /* ------------------------------------------------------
     8. Work archive filters
     ------------------------------------------------------ */
  function filters() {
    const bar = $('[data-filters]');
    if (!bar) return;
    const buttons = $$('button', bar);
    const cards = $$('[data-cat]');
    const count = $('[data-count-label]');
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        buttons.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        const f = b.dataset.filter;
        let shown = 0;
        cards.forEach(function (c) {
          const show = f === 'all' || c.dataset.cat === f;
          c.hidden = !show;
          if (show) shown++;
        });
        if (count) count.textContent = shown;
      });
    });
  }

  /* ------------------------------------------------------
     9. Forms
     With GC.BRAND.formEndpoint set (the Google Apps Script web app),
     the enquiry, brief and newsletter forms post straight to it: each
     one lands in the Graphcent forms sheet and arrives by email.
     Without it, the enquiry and brief fall back to a prefilled draft
     in the visitor's mail app.
     ------------------------------------------------------ */
  var FORM_T0 = Date.now();
  function endpoint() { return (window.GC && window.GC.BRAND.formEndpoint) || ''; }
  function mailTo() { return (window.GC && window.GC.BRAND.email) || 'hello@graphcent.com'; }
  function honeypot(form) {
    if (form.querySelector('input[name="website"]')) return;
    var h = document.createElement('div');
    h.setAttribute('aria-hidden', 'true');
    h.style.cssText = 'position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden';
    h.innerHTML = '<label>Leave this empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label>';
    form.appendChild(h);
  }
  var FILE_TYPES = { pdf: 'application/pdf', doc: 'application/msword',
    docx: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' };
  function readFile(file) {
    return new Promise(function (ok, no) {
      var r = new FileReader();
      r.onload = function () { ok(String(r.result).split(',')[1] || ''); };
      r.onerror = function () { no(r.error); };
      r.readAsDataURL(file);
    });
  }
  function postForm(kind, fields, form, file) {
    var body = { form: kind, fields: fields, page: location.href.split('#')[0],
      elapsed: Date.now() - FORM_T0, website: form.elements.website ? form.elements.website.value : '' };
    var go = function () {
      return fetch(endpoint(), { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(body) })
        .then(function (r) { return r.json(); });
    };
    if (!file) return go();
    var ext = (file.name.split('.').pop() || '').toLowerCase();
    return readFile(file).then(function (data) {
      body.file = { name: file.name, type: file.type || FILE_TYPES[ext] || '', data: data };
      return go();
    });
  }
  function busy(btn, on) {
    if (!btn) return;
    if (on) { btn.dataset.html = btn.innerHTML; btn.disabled = true; btn.setAttribute('aria-busy', 'true'); btn.lastChild.textContent = 'SENDING…'; }
    else { btn.disabled = false; btn.removeAttribute('aria-busy'); if (btn.dataset.html) btn.innerHTML = btn.dataset.html; }
  }
  function failText(res) {
    if (res && res.error === 'rate') return 'You have sent a few already. Give it a few minutes, or message us on WhatsApp.';
    return 'That did not send. Check your connection and try again, use Send on WhatsApp, or email ' + mailTo() + '.';
  }
  function sent(form, note, name, email, what) {
    form.reset();
    $$('[data-chips] .chip', form).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
    note.classList.add('ok');
    note.textContent = 'Thanks, ' + (name.split(' ')[0] || name) + '. Your ' + what + ' is with us and we will reply within one working day. A confirmation is on its way to ' + email + '.';
  }
  function submitVia(kind, form, note, fields, file, what, mailFallback) {
    note.classList.remove('ok');
    if (!endpoint()) { mailFallback(); return; }
    var btn = form.querySelector('button[type="submit"]');
    busy(btn, true);
    note.textContent = 'Sending your ' + what + '…';
    postForm(kind, fields, form, file).then(function (res) {
      busy(btn, false);
      if (res && res.ok) sent(form, note, fields.name, fields.email, what);
      else note.textContent = failText(res);
    }).catch(function () { busy(btn, false); note.textContent = failText(); });
  }

  function enquiry() {
    const form = $('#enquiry');
    if (!form) return;
    const note = $('#formnote');
    $$('[data-chips] .chip', form).forEach(function (c) {
      c.addEventListener('click', function () {
        $$('.chip', c.parentElement).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        c.setAttribute('aria-pressed', 'true');
      });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const el = function (n) { return form.elements[n]; };
      const name = (el('name').value || '').trim();
      const email = (el('email').value || '').trim();
      if (!name) { note.textContent = 'Add your name so we know who we are replying to.'; el('name').focus(); return; }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        note.textContent = 'That email address looks incomplete: check it and try again.';
        el('email').focus(); return;
      }
      const chip = form.querySelector('[data-chips] .chip[aria-pressed="true"]');
      const v = function (n) { return el(n) ? (el(n).value || '').trim() : ''; };
      const fields = { name: name, email: email, company: v('company'), service: v('service'),
        budget: chip ? chip.textContent.trim() : '', timeline: v('timeline'), details: v('details') };
      submitVia('enquiry', form, note, fields, null, 'enquiry', function () {
        const lines = ['Name: ' + name, 'Email: ' + email, 'Company: ' + fields.company, 'Service: ' + fields.service,
          'Budget: ' + fields.budget, 'Timeline: ' + fields.timeline, '', fields.details].join('\n');
        note.textContent = 'Opening your mail app with the enquiry filled in. If nothing happens, send it to ' + mailTo() + '.';
        window.location.href = 'mailto:' + mailTo() + '?subject=' + encodeURIComponent('Project enquiry: ' + name)
          + '&body=' + encodeURIComponent(lines);
      });
    });
    honeypot(form);
  }

  /* ------------------------------------------------------
     9b. Footer newsletter: posts the address to the forms backend
     (Newsletter tab of the sheet) when GC.BRAND.formEndpoint is set.
     ------------------------------------------------------ */
  /* ------------------------------------------------------
     9c. Brief Form
     Entirely separate from enquiry() above: its own form id,
     its own note element, its own fields. The Contact form is
     never touched by this. The attached file (PDF/DOC/DOCX, up to 10 MB) is posted with
     the brief. In the mailto fallback a file cannot ride along,
     so the note asks the visitor to attach it themselves.
     ------------------------------------------------------ */
  function briefForm() {
    const form = $('#brief');
    if (!form) return;
    const note = $('#briefnote');
    $$('[data-chips] .chip', form).forEach(function (c) {
      c.addEventListener('click', function () {
        $$('.chip', c.parentElement).forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        c.setAttribute('aria-pressed', 'true');
      });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const el = function (n) { return form.elements[n]; };
      const name = (el('name').value || '').trim();
      const email = (el('email').value || '').trim();
      if (!name) { note.textContent = 'Add your name so we know who we are replying to.'; el('name').focus(); return; }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
        note.textContent = 'That email address looks incomplete: check it and try again.';
        el('email').focus(); return;
      }
      const chip = form.querySelector('[data-chips] .chip[aria-pressed="true"]');
      const file = el('file') && el('file').files && el('file').files[0];
      if (file && endpoint()) {
        const ext = (file.name.split('.').pop() || '').toLowerCase();
        if (['pdf', 'doc', 'docx'].indexOf(ext) < 0) { note.textContent = 'Attach the brief as a PDF, DOC or DOCX file.'; el('file').focus(); return; }
        if (file.size > 10 * 1024 * 1024) { note.textContent = 'That file is over 10 MB. Send a smaller version, or share a link to it in the details.'; el('file').focus(); return; }
      }
      const v = function (n) { return el(n) ? (el(n).value || '').trim() : ''; };
      const fields = { name: name, email: email, company: v('company'), project: v('project'), service: v('service'),
        budget: chip ? chip.textContent.trim() : '', timeline: v('timeline'), source: v('source'), details: v('details') };
      submitVia('brief', form, note, fields, file, 'brief', function () {
        const lines = ['Name: ' + name, 'Email: ' + email, 'Company: ' + fields.company, 'Project: ' + fields.project,
          'Service: ' + fields.service, 'Budget: ' + fields.budget, 'Timeline: ' + fields.timeline,
          'Heard about us via: ' + fields.source, '', fields.details,
          file ? ('\nAttachment to add manually: ' + file.name) : ''].join('\n');
        note.textContent = file
          ? 'Opening your mail app with the brief filled in. Attach ' + file.name + ' before sending, since a mailto link cannot carry it for you.'
          : 'Opening your mail app with the brief filled in. If nothing happens, send it to ' + mailTo() + '.';
        window.location.href = 'mailto:' + mailTo() + '?subject=' + encodeURIComponent('Project brief: ' + name)
          + '&body=' + encodeURIComponent(lines);
      });
    });
    honeypot(form);
  }


  /* ------------------------------------------------------
     9d. WhatsApp
     A floating chat button on every page, and a "Send on WhatsApp"
     option on the Contact and Brief forms that carries the same
     details as the email version. Number: GC.BRAND.whatsapp.
     ------------------------------------------------------ */
  var WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>';
  function waNumber() { return (window.GC && window.GC.BRAND.whatsapp) || '2348122022600'; }
  function waLink(text) { return 'https://wa.me/' + waNumber() + '?text=' + encodeURIComponent(text); }

  function whatsapp() {
    if (document.body.classList.contains('no-wa')) return;
    var a = document.createElement('a');
    a.className = 'wa-fab';
    a.target = '_blank'; a.rel = 'noopener';
    a.setAttribute('aria-label', 'Chat with Graphcent on WhatsApp');
    var page = (document.querySelector('h1') || {}).textContent || document.title;
    page = page.replace(/\s+/g, ' ').trim();
    a.href = waLink('Hello Graphcent, I found you on your website (' + page.slice(0, 60) + ') and would like to talk about a project.');
    a.innerHTML = WA_ICON + '<span class="wa-label">Chat with us</span>';
    var wrap = document.createElement('aside');
    wrap.className = 'wa-wrap'; wrap.setAttribute('aria-label', 'WhatsApp chat');
    wrap.appendChild(a); document.body.appendChild(wrap);
    // full width = icon + label, so the clip and the slide land exactly
    var fit = function () {
      var lab = a.querySelector('.wa-label'); var sz = a.offsetHeight || 56;
      a.style.setProperty('--w', Math.ceil(sz + lab.offsetWidth) + 'px');
    };
    fit();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);

    // the forms: a WhatsApp button beside the email one
    [['#enquiry', '#formnote', 'Project enquiry'], ['#brief', '#briefnote', 'Project brief']].forEach(function (f) {
      var form = $(f[0]); if (!form) return;
      var submit = form.querySelector('button[type="submit"]'); if (!submit) return;
      var note = $(f[1]);
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'btn btn-fill wa-send';
      b.innerHTML = WA_ICON + ' SEND ON WHATSAPP';
      submit.classList.remove('btn-fill'); submit.classList.add('btn-ghost');
      submit.parentNode.insertBefore(b, submit);
      b.addEventListener('click', function () {
        var el = function (n) { return form.elements[n]; };
        var v = function (n) { return el(n) ? (el(n).value || '').trim() : ''; };
        var name = v('name');
        if (!name) { if (note) note.textContent = 'Add your name so we know who we are talking to.'; if (el('name')) el('name').focus(); return; }
        var chip = form.querySelector('[data-chips] .chip[aria-pressed="true"]');
        var lines = [f[2] + ' from graphcent.com', '', 'Name: ' + name];
        [['email', 'Email'], ['company', 'Company'], ['project', 'Project'], ['service', 'Service'],
         ['timeline', 'Timeline'], ['source', 'Heard about us via']].forEach(function (k) { if (v(k[0])) lines.push(k[1] + ': ' + v(k[0])); });
        if (chip) lines.push('Budget: ' + chip.textContent.trim());
        if (v('details')) lines.push('', v('details'));
        var file = el('file') && el('file').files && el('file').files[0];
        if (file) lines.push('', '(I will send the file ' + file.name + ' in this chat.)');
        if (note) note.textContent = 'Opening WhatsApp with your message filled in. Press send there to reach us.';
        window.open(waLink(lines.join('\n')), '_blank', 'noopener');
      });
    });
  }

  /* ------------------------------------------------------
     9e. Google reviews  [data-reviews]
     Loads the studio's Google rating and latest reviews from the
     Places API (New) when the section scrolls near, using
     GC.BRAND.reviews {placeId, apiKey, profile}. Until those are set
     the section stays hidden. New reviews appear automatically
     (Google returns up to five, most relevant first).
     ------------------------------------------------------ */
  function reviews() {
    var box = $('[data-reviews]'); if (!box) return;
    var cfg = (window.GC && window.GC.BRAND.reviews) || {};
    if (!cfg.apiKey || (!cfg.placeId && !cfg.query)) return;
    var esc = function (t) { var d = document.createElement('div'); d.textContent = t || ''; return d.innerHTML; };
    var stars = function (n) { var r = Math.round(n || 0), o = ''; for (var i = 1; i <= 5; i++) o += '<i class="' + (i <= r ? 'on' : '') + '"></i>'; return '<span class="rv-stars" role="img" aria-label="' + (n || 0) + ' out of 5 stars">' + o + '</span>'; };
    function findId() {
      if (cfg.placeId) return Promise.resolve(cfg.placeId);
      return fetch('https://places.googleapis.com/v1/places:searchText', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Goog-Api-Key': cfg.apiKey, 'X-Goog-FieldMask': 'places.id' },
        body: JSON.stringify({ textQuery: cfg.query })
      }).then(function (r) { return r.json(); }).then(function (d) {
        var id = d.places && d.places[0] && d.places[0].id;
        if (!id) throw new Error('place not found');
        cfg.placeId = id; return id;
      });
    }
    function load() {
      findId().then(function () { return fetch('https://places.googleapis.com/v1/places/' + encodeURIComponent(cfg.placeId) + '?languageCode=en', {
        headers: { 'X-Goog-Api-Key': cfg.apiKey, 'X-Goog-FieldMask': 'rating,userRatingCount,reviews,googleMapsUri' }
      }); }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (d) {
        var list = (d.reviews || []).filter(function (x) { return x.text && x.text.text; });
        if (!list.length) return;
        var write = 'https://search.google.com/local/writereview?placeid=' + encodeURIComponent(cfg.placeId);
        var profile = cfg.profile || d.googleMapsUri || write;
        $('.rv-score', box).innerHTML = '<b>' + (d.rating || 0).toFixed(1) + '</b>' + stars(d.rating) +
          '<span>' + (d.userRatingCount || list.length) + ' Google reviews</span>';
        $('.rv-list', box).innerHTML = list.map(function (x) {
          var a = x.authorAttribution || {};
          return '<li class="rv-card"><div class="rv-head">' +
            (a.photoUri ? '<img src="' + esc(a.photoUri) + '" alt="" width="40" height="40" loading="lazy" referrerpolicy="no-referrer">' : '<span class="rv-ini" aria-hidden="true">' + esc((a.displayName || '?').charAt(0)) + '</span>') +
            '<div><b>' + (a.uri ? '<a href="' + esc(a.uri) + '" target="_blank" rel="noopener nofollow">' + esc(a.displayName) + '</a>' : esc(a.displayName)) + '</b>' +
            '<span>' + esc(x.relativePublishTimeDescription) + '</span></div></div>' + stars(x.rating) +
            '<p>' + esc(x.text.text) + '</p></li>';
        }).join('');
        $('.rv-profile', box).href = profile;
        $('.rv-write', box).href = write;
        box.hidden = false;
        if (window.GCSite && GCSite.refreshReveals) GCSite.refreshReveals();
      }).catch(function (e) { if (window.console) console.warn('Google reviews unavailable:', e.message); });
    }
    if ('IntersectionObserver' in window) {
      var anchor = box.previousElementSibling || box.parentNode;
      var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { io.disconnect(); load(); } }, { rootMargin: '600px' });
      io.observe(anchor);
    } else load();
  }

  function newsletter() {
    $$('.newsletter').forEach(function (form) {
      const note = $('.formnote', form);
      const input = form.elements.email;

      function say(text, ok) {
        if (!note) return;
        note.textContent = text;
        note.classList.toggle('ok', !!ok);
      }

      /* typing again after a confirmation clears it */
      input.addEventListener('input', function () {
        if (note && note.classList.contains('ok')) say('', false);
      });

      form.addEventListener('submit', function (e) {
        e.preventDefault();
        const email = (input.value || '').trim();
        if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
          say('That email address looks incomplete: check it and try again.', false);
          input.focus();
          return;
        }
        var done = function () { form.reset(); say('You\u2019re subscribed. Thanks for joining the Graphcent newsletter.', true); };
        if (!endpoint()) { done(); return; }
        var btn = form.querySelector('button[type="submit"]'); if (btn) btn.disabled = true;
        postForm('newsletter', { email: email }, form, null).then(function (res) {
          if (btn) btn.disabled = false;
          if (res && res.ok && res.already) { form.reset(); say('You\u2019re already on the list. Thanks for staying with Graphcent.', true); }
          else if (res && res.ok) { form.reset(); say('You\u2019re subscribed. A welcome email is on its way to ' + email + '.', true); }
          else say(failText(res), false);
        }).catch(function () { if (btn) btn.disabled = false; say(failText(), false); });
      });
      honeypot(form);
    });
  }

  /* ------------------------------------------------------
     09b. Ambient videos: respect reduced motion, pause off screen
     Autoplaying background video stays on its poster frame for visitors
     who ask their device to reduce motion, and pauses whenever it is
     scrolled out of view (saves battery and data on phones).
     ------------------------------------------------------ */
  function ambientVideos() {
    var vids = $$('video[autoplay]');
    if (!vids.length) return;
    var reduceMq = window.matchMedia('(prefers-reduced-motion: reduce)');
    vids.forEach(function (v) {
      if (reduceMq.matches) { v.removeAttribute('autoplay'); v.pause(); return; }
      if (!('IntersectionObserver' in window)) return;
      new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        else v.pause();
      }, { threshold: 0.1 }).observe(v);
    });
  }

  /* ------------------------------------------------------
     10. Page-load sequence
     ------------------------------------------------------ */
  /* ------------------------------------------------------
     12. Cursor: a facet of the Graphcent mark replaces the
     system cursor, blended (difference) with what is under it.
     It trails the pointer closely and turns to point the way
     you move; when you stop it holds its last heading. It
     grows over anything clickable, and grows with a tag
     beside it over projects ("View"), articles ("Read") and
     the interactive mark ("Drag").
     Mouse/trackpad only, never on touch or reduced motion.
     ------------------------------------------------------ */
  function cursor() {
    const fine = window.matchMedia('(hover: hover) and (pointer: fine)');
    if (!fine.matches || reduce.matches) return;

    const dot = document.createElement('div');
    dot.className = 'gc-cur';
    dot.setAttribute('aria-hidden', 'true');
    dot.innerHTML = '<span class="rot"><svg class="tri" viewBox="0 2 24 24" focusable="false">' +
      '<polygon points="12,2 22,20 2,20"/></svg></span>';
    const rot = dot.firstChild;
    const tag = document.createElement('div');
    tag.className = 'gc-tag';
    tag.setAttribute('aria-hidden', 'true');
    tag.innerHTML = '<span class="t"></span>';
    const label = tag.firstChild;
    document.body.append(dot, tag);

    const TAGS = [
      ['.mp-piece polygon', 'Drag'],
      ['.cs-rail', 'Drag'],
      ['.cs-screen', 'Scroll'],
      ['.proj, .reel .card', 'View'],
      ['.article, .featured', 'Read']
    ];
    // anything that does something when clicked
    const LINKS = 'a[href], button, summary, label[for], select, [role="button"], [role="link"], [role="tab"],' +
      ' [onclick], [data-href], input[type="submit"], input[type="button"], input[type="checkbox"],' +
      ' input[type="radio"], input[type="file"], .chip';
    const TEXT = 'input:not([type="submit"]):not([type="button"]):not([type="checkbox"]):not([type="radio"]):not([type="file"]),' +
      ' textarea, [contenteditable]';

    let tx = -100, ty = -100;           // pointer
    let dx = tx, dy = ty, gx = tx, gy = ty; // dot, tag (smoothed)
    let raf = 0, last = 0, seen = false;
    // heading: 0deg points straight up; it starts tilted like a cursor arrow
    let ang = -28, goal = -28, vx = 0, vy = 0, px = 0, py = 0;

    function frame(now) {
      const dt = Math.min(64, now - (last || now)); last = now;
      // frame-rate independent smoothing; the tag rides with the dot
      const kd = 1 - Math.pow(1 - 0.8, dt / 16.67);
      const kg = kd;
      dx += (tx - dx) * kd; dy += (ty - dy) * kd;
      gx += (tx - gx) * kg; gy += (ty - gy) * kg;
      // turn toward the heading along the shortest way round
      const kr = 1 - Math.pow(1 - 0.16, dt / 16.67);
      let diff = ((goal - ang + 540) % 360) - 180;
      ang += diff * kr;
      dot.style.transform = 'translate3d(' + dx + 'px,' + dy + 'px,0)';
      rot.style.transform = 'rotate(' + ang.toFixed(2) + 'deg)';
      tag.style.transform = 'translate3d(' + gx + 'px,' + gy + 'px,0)';
      const settled = Math.abs(tx - dx) + Math.abs(ty - dy) + Math.abs(tx - gx) + Math.abs(ty - gy) < 0.2 &&
        Math.abs(diff) < 0.3;
      raf = settled ? 0 : requestAnimationFrame(frame);
      if (settled) last = 0;
    }
    function kick() { if (!raf) raf = requestAnimationFrame(frame); }

    function state(target) {
      let text = '';
      for (let i = 0; i < TAGS.length && target; i++) {
        if (target.closest(TAGS[i][0])) { text = TAGS[i][1]; break; }
      }
      if (text) label.textContent = text;
      tag.classList.toggle('on', !!text);
      dot.classList.toggle('is-tag', !!text);
      dot.classList.toggle('is-text', !text && !!(target && target.closest(TEXT)));
      dot.classList.toggle('is-link', !text && !!(target && target.closest(LINKS)));
      // navy dot on light sections, paper dot on dark ones
      const dk = !!(target && target.closest('.dark, footer, .overlay, .nav.on-dark'));
      dot.classList.toggle('on-dark', dk);
      tag.classList.toggle('on-dark', dk);
    }

    document.addEventListener('pointermove', function (e) {
      if (e.pointerType !== 'mouse') return;
      tx = e.clientX; ty = e.clientY;
      // smoothed velocity sets the heading; tiny jitters don't turn it
      vx = vx * 0.7 + (tx - px) * 0.3; vy = vy * 0.7 + (ty - py) * 0.3;
      px = tx; py = ty;
      if (vx * vx + vy * vy > 4) goal = Math.atan2(vy, vx) * 180 / Math.PI + 90;
      if (!seen) { // first move: appear where the pointer is, no fly-in from the corner
        seen = true; dx = gx = tx; dy = gy = ty; vx = vy = 0; goal = ang;
        document.documentElement.classList.add('has-cursor');
      }
      kick();
    }, { passive: true });
    document.addEventListener('pointerover', function (e) {
      if (e.pointerType === 'mouse') state(e.target);
    }, { passive: true });
    // scrolling moves the page under a still pointer: re-read what is under it
    let scrollTick = false;
    window.addEventListener('scroll', function () {
      if (!seen || scrollTick) return;
      scrollTick = true;
      requestAnimationFrame(function () {
        scrollTick = false;
        state(document.elementFromPoint(tx, ty));
      });
    }, { passive: true });
    document.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse') dot.classList.add('is-down');
    }, { passive: true });
    document.addEventListener('pointerup', function () { dot.classList.remove('is-down'); }, { passive: true });
    // pointer leaves the window: fade out, come back where it re-enters
    document.documentElement.addEventListener('mouseleave', function () {
      document.documentElement.classList.remove('has-cursor'); seen = false;
    });
    // switching to touch or turning on reduced motion: remove it entirely
    function off() {
      if (fine.matches && !reduce.matches) return;
      cancelAnimationFrame(raf); dot.remove(); tag.remove();
      document.documentElement.classList.remove('has-cursor');
    }
    if (fine.addEventListener) { fine.addEventListener('change', off); reduce.addEventListener('change', off); }
  }

  /* ------------------------------------------------------
     13. Pinned rows and columns.
     Wide screens: details stay put beside the image (Work page,
     "How we work"), or the heading column stays put beside a list
     (Studio capabilities, Investment); a thin line shows how far
     through each one you are, and in a list the item level with
     the pinned heading lights up.
     Phones and tablets: rows become a stacking deck (each card
     pins under the header, the next slides over it, the covered
     one eases back); lists get a slim pinned bar with the section
     name, the item in view, a counter and a progress line.
     ------------------------------------------------------ */
  function pinnedDetails() {
    const decks = $$('.pinrows, .works.stack');
    const rows = $$('.pinrow');
    const cols = $$('[data-pincol]');
    if (!rows.length && !cols.length) return;
    const wide = window.matchMedia('(min-width: 960px)');
    let ticking = false;

    decks.forEach(function (d) { d.classList.add('is-deck'); });

    // phones: a bar per list, pinned under the header
    cols.forEach(function (col) {
      col.classList.add('is-live');
      const items = $$('[data-caprow]', col);
      const label = $('.eyebrow', col);
      const bar = document.createElement('div');
      bar.className = 'pinbar';
      bar.setAttribute('aria-hidden', 'true');
      bar.innerHTML = '<span class="pb-label"></span><span class="pb-now"><b>01</b>/ ' +
        String(items.length).padStart(2, '0') + '</span><span class="pb-item"></span>' +
        '<span class="pb-track"><i></i></span>';
      bar.querySelector('.pb-label').textContent = label ? label.textContent : '';
      const list = items.length ? items[0].parentElement : null;
      if (list) col.insertBefore(bar, list);
      col._bar = bar;
    });

    function progress(box, info) {
      const r = box.getBoundingClientRect();
      const top = parseFloat(getComputedStyle(info).top) || 0;
      const travel = r.height - info.offsetHeight;
      return travel > 0 ? Math.min(1, Math.max(0, (top - r.top) / travel)) : 0;
    }
    function nearest(items, line) {
      let best = 0, dist = Infinity;
      items.forEach(function (it, k) {
        const r = it.getBoundingClientRect();
        const d = Math.abs(r.top + r.height / 2 - line);
        if (d < dist) { dist = d; best = k; }
      });
      return best;
    }
    function titleOf(it) {
      const t = $('b, h3', it);
      return t ? t.textContent : '';
    }

    function wideRun() {
      document.documentElement.classList.remove('pin-stuck');
      decks.forEach(function (d) {
        $$('.pinrow', d).forEach(function (row) { row.style.top = ''; row.style.transform = ''; row.style.removeProperty('--cover'); });
      });
      rows.forEach(function (row) {
        const bar = $('.ptrack i', row), info = $('.pinfo', row);
        if (!bar || !info) return;
        bar.style.transform = row.hidden ? '' : 'scaleX(' + progress(row, info).toFixed(4) + ')';
      });
      cols.forEach(function (col) {
        const bar = $('.ptrack i', col), info = $('.pinfo', col);
        const items = $$('[data-caprow]', col), now = $('[data-capnow]', col);
        if (bar) bar.style.transform = 'scaleX(' + progress(col, info).toFixed(4) + ')';
        const ir = info.getBoundingClientRect();
        const best = nearest(items, ir.top + ir.height / 2);
        items.forEach(function (it, k) { it.classList.toggle('on', k === best); });
        if (now) now.textContent = String(best + 1).padStart(2, '0');
      });
    }

    function phoneRun() {
      const navh = (parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--navh')) || 64);
      const vh = window.innerHeight;
      let stuck = false;
      decks.forEach(function (d) {
        const dr = d.getBoundingClientRect();
        if (dr.top < navh + 20 && dr.bottom > navh + 120) stuck = true;
        const list = $$('.pinrow', d).filter(function (r) { return !r.hidden; });
        list.forEach(function (row, i) {
          // each card pins a little lower than the one before, so the
          // deck shows its edges; a card taller than the screen pins only
          // once its bottom is in view, so none of it is ever hidden
          const want = navh + 10 + Math.min(i, 3) * 8;
          const h = row.offsetHeight;
          row.style.top = (h <= vh - want - 12 ? want : vh - h - 12) + 'px';
          const next = list[i + 1];
          if (!next || reduce.matches) { row.style.transform = ''; row.style.removeProperty('--cover'); return; }
          const r = row.getBoundingClientRect(), n = next.getBoundingClientRect();
          const p = Math.min(1, Math.max(0, (r.bottom - n.top) / r.height));
          // the covered card eases back and is shaded (an overlay, not
          // opacity, so the card behind never shows through it)
          row.style.transform = p ? 'scale(' + (1 - 0.06 * p).toFixed(4) + ')' : '';
          row.style.setProperty('--cover', p.toFixed(3));
        });
      });
      cols.forEach(function (col) {
        const bar = col._bar; if (!bar) return;
        const items = $$('[data-caprow]', col);
        const list = items.length ? items[0].parentElement : null;
        if (!list) return;
        const br = bar.getBoundingClientRect(), lr = list.getBoundingClientRect();
        if (br.top <= navh + 1 && lr.bottom > br.bottom + 40) stuck = true;
        // the row just under the bar is the one in view
        // until the bar reaches the header, the list hasn't started: show item 01
        const best = br.top > navh + 2 ? 0 : nearest(items, br.bottom + Math.min(160, vh * 0.22));
        items.forEach(function (it, k) { it.classList.toggle('on', k === best); });
        bar.querySelector('.pb-now b').textContent = String(best + 1).padStart(2, '0');
        bar.querySelector('.pb-item').textContent = titleOf(items[best]);
        const p = Math.min(1, Math.max(0, (br.bottom - lr.top) / Math.max(1, lr.height - (vh - br.bottom) * 0.5)));
        bar.querySelector('.pb-track i').style.transform = 'scaleX(' + p.toFixed(4) + ')';
      });
      // while something is pinned under the header, it owns that edge:
      // the header's blur strip steps aside so it never blurs pinned content
      document.documentElement.classList.toggle('pin-stuck', stuck);
    }

    function run() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        if (wide.matches) wideRun(); else phoneRun();
      });
    }
    window.addEventListener('scroll', run, { passive: true });
    window.addEventListener('resize', run);
    if (wide.addEventListener) wide.addEventListener('change', run);
    $$('[data-filters] button').forEach(function (b) { b.addEventListener('click', run); });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(run);
    window.addEventListener('load', run);
    run();
  }

  function ready() {
    cursor();
    pinnedDetails();
    buildMarquees();
    marqueeVisibility();
    reveals();
    headerTone();
    menu();
    processScroll();
    counters();
    parallax();
    filters();
    enquiry();
    briefForm();
    newsletter();
    whatsapp();
    reviews();
    ambientVideos();
    requestAnimationFrame(function () {
      setTimeout(function () { document.body.classList.add('ready'); }, 40);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();

  window.GCSite = { init: ready, buildMarquees: buildMarquees };
})();
