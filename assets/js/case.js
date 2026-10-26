/* ==========================================================
   Graphcent: case.js
   Interactive pieces for the case study pages.
   1. Segmented sets   [data-sets]   switch between groups (Customer / Rider app,
                                     Distributor / Admin console)
   2. Phone rail       .cs-rail      drag with a mouse, snap, prev/next, progress
   3. Console viewer   [data-viewer] a list of screens switching one stage
   4. Device preview   [data-devices] the landing page at desktop / tablet /
                                     mobile, scrollable inside, optional slow
                                     auto-scroll that stops when you touch it
   5. Live site        [data-live]   the client's real website in a device
                                     frame at its true width, scaled to fit
   6. Backend demo     [data-flow]   form -> Apps Script -> Sheet + email,
                                     simulated in the page (nothing is sent)
   Everything works without this script too: rails scroll natively, the first
   screen and the desktop page are shown, and all images are in the page.
   ========================================================== */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* 1. segmented sets: buttons [data-set="x"] show the matching [data-set-panel="x"] */
  function sets() {
    $$('[data-sets]').forEach(function (host) {
      var btns = $$('[data-set]', host);
      var panels = $$('[data-set-panel]', host);
      function show(name) {
        btns.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.set === name)); });
        panels.forEach(function (p) {
          var on = p.dataset.setPanel === name;
          p.hidden = !on;
          if (on) p.dispatchEvent(new CustomEvent('cs:show', { bubbles: true }));
        });
      }
      btns.forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.set); }); });
    });
  }

  /* 2. phone rails */
  function rails() {
    $$('.cs-railwrap').forEach(function (wrap) {
      var prev = $('[data-prev]', wrap), next = $('[data-next]', wrap);
      function active() { return $$('.cs-rail', wrap).filter(function (r) { return !r.closest('[hidden]'); })[0]; }
      function update() {
        var rail = active(); if (!rail) return;
        var max = rail.scrollWidth - rail.clientWidth;
        var p = max > 0 ? rail.scrollLeft / max : 1;
        var bar = $('.cs-railbar i', wrap);
        if (bar) bar.style.transform = 'scaleX(' + Math.max(0.04, p).toFixed(3) + ')';
        if (prev) prev.disabled = rail.scrollLeft < 4;
        if (next) next.disabled = rail.scrollLeft > max - 4;
      }
      function step(dir) {
        var rail = active(); if (!rail) return;
        var card = $('.cs-phone', rail);
        var w = card ? card.getBoundingClientRect().width + parseFloat(getComputedStyle(rail).columnGap || 20) : rail.clientWidth * 0.8;
        rail.scrollBy({ left: dir * w * 2, behavior: reduce.matches ? 'auto' : 'smooth' });
      }
      if (prev) prev.addEventListener('click', function () { step(-1); });
      if (next) next.addEventListener('click', function () { step(1); });
      wrap.addEventListener('cs:show', function () { requestAnimationFrame(update); });

      $$('.cs-rail', wrap).forEach(function (rail) {
        rail.addEventListener('scroll', function () { requestAnimationFrame(update); }, { passive: true });
        // drag to scroll with a mouse (touch already scrolls natively)
        var down = null;
        rail.addEventListener('pointerdown', function (e) {
          if (e.pointerType !== 'mouse' || e.button !== 0) return;
          down = { x: e.clientX, left: rail.scrollLeft, moved: false, id: e.pointerId };
        });
        rail.addEventListener('pointermove', function (e) {
          if (!down || e.pointerId !== down.id) return;
          var dx = e.clientX - down.x;
          if (!down.moved && Math.abs(dx) > 4) {
            down.moved = true; rail.classList.add('is-dragging');
            try { rail.setPointerCapture(e.pointerId); } catch (err) {}
          }
          if (down.moved) rail.scrollLeft = down.left - dx;
        });
        function end() {
          if (!down) return;
          var was = down.moved; down = null;
          if (was) {
            // release: let snapping take over again from where it was let go
            rail.classList.remove('is-dragging');
          }
        }
        rail.addEventListener('pointerup', end);
        rail.addEventListener('pointercancel', end);
        rail.addEventListener('keydown', function (e) {
          if (e.key === 'ArrowRight') { e.preventDefault(); step(0.5); }
          if (e.key === 'ArrowLeft') { e.preventDefault(); step(-0.5); }
        });
      });
      window.addEventListener('resize', update);
      update();
    });
  }

  /* 3. console viewer: a list of screens switching one stage */
  function viewers() {
    $$('[data-viewer]').forEach(function (v) {
      var btns = $$('.cs-list button', v), imgs = $$('.cs-stage img', v);
      var url = $('.cs-bar span', v);
      function show(i) {
        btns.forEach(function (b, k) { b.setAttribute('aria-pressed', String(k === i)); });
        imgs.forEach(function (im, k) {
          if (k === i) { im.loading = 'eager'; im.classList.add('on'); } else im.classList.remove('on');
        });
        if (url && btns[i] && btns[i].dataset.url) url.textContent = btns[i].dataset.url;
        var stage = $('.cs-stage', v); if (stage) stage.scrollTop = 0;
        var cap = $('.cs-caption', v); if (cap && btns[i]) cap.textContent = btns[i].dataset.desc || '';
      }
      btns.forEach(function (b, i) {
        b.addEventListener('click', function () { show(i); });
        b.addEventListener('keydown', function (e) {
          var k = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 }[e.key];
          if (!k) return;
          e.preventDefault();
          var n = (i + k + btns.length) % btns.length;
          btns[n].focus(); show(n);
        });
      });
      // warm the next screens once the viewer is near, so switching is instant
      if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (es) {
          if (!es[0].isIntersecting) return;
          imgs.forEach(function (im) { im.loading = 'eager'; });
          io.disconnect();
        }, { rootMargin: '400px' });
        io.observe(v);
      }
    });
  }

  /* 4. device preview: desktop / tablet / mobile, scrollable inside */
  function devices() {
    $$('[data-devices]').forEach(function (d) {
      var btns = $$('[data-device-btn]', d), pages = $$('.cs-pages', d);
      var screen = $('.cs-screen', d), url = $('.cs-bar span', d);
      var play = $('[data-autoplay]', d), raf = 0, playing = false;
      function stop() {
        playing = false; cancelAnimationFrame(raf);
        if (play) { play.setAttribute('aria-pressed', 'false'); play.textContent = 'Auto-scroll'; }
      }
      function show(name) {
        stop();
        d.dataset.device = name;
        btns.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.deviceBtn === name)); });
        pages.forEach(function (p) { p.hidden = p.dataset.page !== name; });
        screen.scrollTop = 0;
      }
      btns.forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.deviceBtn); }); });
      if (play && !reduce.matches) {
        play.addEventListener('click', function () {
          if (playing) return stop();
          playing = true; play.setAttribute('aria-pressed', 'true'); play.textContent = 'Stop';
          var last = 0;
          (function tick(now) {
            if (!playing) return;
            var dt = last ? Math.min(48, now - last) : 16; last = now;
            screen.scrollTop += dt * 0.12 * (screen.clientHeight / 600);
            if (screen.scrollTop >= screen.scrollHeight - screen.clientHeight - 1) return stop();
            raf = requestAnimationFrame(tick);
          })(performance.now());
        });
        // any manual scroll or touch takes over from auto-scroll
        ['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach(function (ev) {
          screen.addEventListener(ev, function () { if (playing) stop(); }, { passive: true });
        });
      }
      show(d.dataset.device || 'desktop');
    });
  }


  /* 5. live site: the client's real website in a device frame, rendered at
     its true width (1440 / 768 / 390) and scaled to fit the frame */
  function live() {
    $$('[data-live]').forEach(function (L) {
      var vp = $('.cs-viewport', L), frame = $('iframe', vp), url = $('.cs-bar span', L);
      var open = $('.cs-bar a', L);
      var devBtns = $$('[data-device-btn]', L), pageBtns = $$('[data-live-page]', L);
      var widths = { desktop: 1440, tablet: 768, mobile: 390 };
      function fit() {
        var w = widths[L.dataset.device] || 1440;
        var s = vp.clientWidth / w;
        frame.style.width = w + 'px';
        frame.style.height = Math.ceil(vp.clientHeight / s) + 'px';
        frame.style.transform = 'scale(' + s.toFixed(4) + ')';
      }
      devBtns.forEach(function (b) {
        b.addEventListener('click', function () {
          L.dataset.device = b.dataset.deviceBtn;
          devBtns.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
          // let the frame finish resizing, then re-fit
          setTimeout(fit, 30); setTimeout(fit, 480);
        });
      });
      pageBtns.forEach(function (b) {
        b.addEventListener('click', function () {
          pageBtns.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
          frame.src = b.dataset.livePage;
          var label = b.dataset.livePage.replace(/^https?:\/\//, '').replace(/\/$/, '');
          if (url) url.textContent = label;
          if (open) open.href = b.dataset.livePage;
        });
      });
      frame.addEventListener('load', function () { vp.classList.add('is-live'); });
      // the custom cursor can't follow the pointer into the embedded site
      frame.addEventListener('mouseenter', function () { document.documentElement.classList.add('cursor-away'); });
      frame.addEventListener('mouseleave', function () { document.documentElement.classList.remove('cursor-away'); });
      window.addEventListener('resize', fit);
      fit();
      // on a phone-sized screen, open in the phone layout: a desktop site
      // scaled down to a quarter of its size isn't readable
      if (window.innerWidth < 700) {
        var m = devBtns.filter(function (b) { return b.dataset.deviceBtn === 'mobile'; })[0];
        if (m) m.click();
      }
    });
  }

  /* 6. backend flow demo: form -> Apps Script -> Google Sheet + email.
     Runs entirely in this page. Nothing is sent anywhere. */
  function flow() {
    $$('[data-flow]').forEach(function (F) {
      var form = $('form', F), nodes = $$('.cs-node', F), err = $('.err', F), btn = $('button[type=submit]', F);
      var sheet = $('.cs-sheet tbody', F), mail = $('.cs-mail', F), live = $('[aria-live]', F);
      var busy = false;
      function stat(n, t) { var s = $('.stat', nodes[n]); if (s) s.textContent = t; }
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (busy) return;
        var name = form.elements.name.value.trim(), type = form.elements.type.value;
        var hp = form.elements.hp_extra && form.elements.hp_extra.value;
        if (!name || !type) { err.textContent = !name ? 'Add a name to send the demo enquiry.' : 'Choose an enquiry type.'; (name ? form.elements.type : form.elements.name).focus(); return; }
        err.textContent = '';
        busy = true; btn.textContent = 'Sending\u2026'; btn.disabled = true;
        nodes.forEach(function (n, k) { n.classList.remove('on'); stat(k, 'Waiting'); });
        var gap = reduce.matches ? 0 : 420;
        var now = new Date(), time = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
        var steps = [
          function () { nodes[0].classList.add('on'); stat(0, hp ? 'Blocked' : 'Checked'); },
          function () { nodes[1].classList.add('on'); stat(1, 'Received'); },
          function () {
            nodes[2].classList.add('on'); stat(2, 'Row added');
            var empty = $('.empty', sheet); if (empty) empty.remove();
            var tr = document.createElement('tr'); tr.className = 'cs-new';
            [time, name, type, 'contact.html'].forEach(function (v) { var td = document.createElement('td'); td.textContent = v; tr.appendChild(td); });
            sheet.insertBefore(tr, sheet.firstChild);
            while (sheet.children.length > 4) sheet.removeChild(sheet.lastChild);
          },
          function () {
            nodes[3].classList.add('on'); stat(3, 'Delivered');
            var empty = $('.empty', mail); if (empty) empty.remove();
            var li = document.createElement('li'); li.className = 'cs-new';
            var b = document.createElement('b'); b.textContent = 'AMEA website enquiry: ' + type;
            var s = document.createElement('span'); s.textContent = 'From ' + name + ' \u00b7 to info@amea.ng \u00b7 ' + time;
            li.appendChild(b); li.appendChild(s);
            mail.insertBefore(li, mail.firstChild);
            while (mail.children.length > 3) mail.removeChild(mail.lastChild);
            if (live) live.textContent = 'Demo: the enquiry from ' + name + ' was added to the sheet and emailed to info@amea.ng. Nothing was actually sent.';
            btn.textContent = 'Send another'; btn.disabled = false; busy = false;
          }
        ];
        steps.forEach(function (fn, k) { setTimeout(fn, gap * (k + 1)); });
      });
    });
  }

  /* 7. Before / after   [data-compare]  drag (or arrow keys) to compare two logos */
  function compare() {
    $$('[data-compare]').forEach(function (box) {
      var r = $('input[type=range]', box);
      if (!r) return;
      function set() { box.style.setProperty('--pos', r.value + '%'); }
      r.addEventListener('input', set); set();
    });
  }

  /* 8. Logo explorer    [data-logolab]  pick a version, then light or dark */
  function logolab() {
    $$('[data-logolab]').forEach(function (lab) {
      var vers = $$('[data-ver]', lab), bgs = $$('[data-bg]', lab), ims = $$('[data-key]', lab);
      var cap = $('.cs-caption', lab), v = vers[0].dataset.ver, bg = 'light';
      function show() {
        var has = function (b) { return ims.some(function (im) { return im.dataset.key === v + '-' + b; }); };
        if (!has(bg)) bg = 'light';
        bgs.forEach(function (b) {
          var ok = has(b.dataset.bg);
          b.disabled = !ok; b.setAttribute('aria-pressed', String(b.dataset.bg === bg));
        });
        vers.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.ver === v)); });
        ims.forEach(function (im) {
          var on = im.dataset.key === v + '-' + bg;
          im.classList.toggle('on', on);
          if (on) im.loading = 'eager';
        });
        lab.dataset.tone = bg;
        var cur = vers.filter(function (b) { return b.dataset.ver === v; })[0];
        if (cap && cur) cap.textContent = cur.dataset.desc + (has('dark') ? '' : ' Light only.');
      }
      vers.forEach(function (b) { b.addEventListener('click', function () { v = b.dataset.ver; show(); }); });
      bgs.forEach(function (b) { b.addEventListener('click', function () { if (!b.disabled) { bg = b.dataset.bg; show(); } }); });
      show();
    });
  }

  /* 9. Size test        [data-scale]    one slider sizes the old and new mark together */
  function scale() {
    $$('[data-scale]').forEach(function (box) {
      var r = $('input[type=range]', box), out = $('output', box);
      var marks = [[24, 'Favicon'], [48, 'App icon, social avatar'], [96, 'Business card'], [180, 'Letterhead, packaging'], [400, 'Signage, vehicle']];
      function set() {
        var n = +r.value; box.style.setProperty('--s', n + 'px');
        var use = marks.filter(function (m) { return n <= m[0]; })[0] || marks[marks.length - 1];
        if (out) out.textContent = n + 'px · ' + use[1];
      }
      r.addEventListener('input', set); set();
    });
  }

  /* 10. Swatches        [data-swatch]   click to copy the hex value */
  function swatches() {
    var live = $('[data-swatch-live]');
    $$('[data-swatch]').forEach(function (b) {
      b.addEventListener('click', function () {
        var hex = b.dataset.swatch;
        var done = function () {
          var cp = $('.cp', b); b.classList.add('copied'); if (cp) cp.textContent = 'Copied';
          setTimeout(function () { b.classList.remove('copied'); if (cp) cp.textContent = 'Copy'; }, 1400);
          if (live) live.textContent = hex + ' copied';
        };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(hex).then(done, done);
        else done();
      });
    });
  }

  /* 11. Paint the mark  [data-paint]    ribbons pour in one by one; chips highlight one */
  function paint() {
    var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    $$('[data-paint]').forEach(function (box) {
      var order = (box.dataset.paint || '').split(',');
      var ribs = $$('[data-rib]', box.querySelector('svg') || box);
      ribs.forEach(function (r) { r.style.setProperty('--i', Math.max(0, order.indexOf(r.dataset.rib))); });
      function run() {
        if (still) { box.classList.add('painted'); return; }
        box.classList.remove('painted'); void box.offsetWidth; box.classList.add('painted');
      }
      if (!still) box.classList.add('armed');
      if ('IntersectionObserver' in window && !still) {
        var io = new IntersectionObserver(function (es) {
          if (es[0].isIntersecting) { run(); io.disconnect(); }
        }, { threshold: 0.4 });
        io.observe(box);
      } else run();
      var play = $('[data-paint-play]', box);
      if (play) play.addEventListener('click', run);
      $$('[data-rib-chip]', box).forEach(function (c) {
        function on() {
          box.classList.add('focus');
          ribs.forEach(function (r) { r.classList.toggle('on', r.dataset.rib === c.dataset.ribChip); });
        }
        function off() { box.classList.remove('focus'); ribs.forEach(function (r) { r.classList.remove('on'); }); }
        c.addEventListener('mouseenter', on); c.addEventListener('focus', on);
        c.addEventListener('mouseleave', off); c.addEventListener('blur', off);
      });
    });
  }

  /* 12. Type tester     [data-typetest] type once, see it in each brand typeface */
  function typetest() {
    $$('[data-typetest]').forEach(function (box) {
      var input = $('input', box), outs = $$('[data-type-out]', box);
      function set() {
        var v = input.value.trim() || input.placeholder;
        outs.forEach(function (o) { o.textContent = v; });
      }
      input.addEventListener('input', set); set();
    });
  }

  function init() { sets(); rails(); viewers(); devices(); live(); flow(); compare(); logolab(); scale(); swatches(); paint(); typetest(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
