/* Article pages: reading progress under the header, and the share buttons. */
(function () {
  var bar = document.querySelector('.readbar i');
  var post = document.querySelector('.postpage');
  if (bar && post) {
    var ticking = false;
    var update = function () {
      ticking = false;
      var r = post.getBoundingClientRect();
      var total = r.height - window.innerHeight;
      var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 1;
      bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
    };
    var req = function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', req, { passive: true });
    window.addEventListener('resize', req);
    update();
  }

  /* Share: links carry the canonical address; when the page is served from
     somewhere else (a preview, staging), share the address people are on. */
  var here = /^https?:$/.test(location.protocol) ? location.origin + location.pathname.replace(/index\.html$/, '') : '';
  Array.prototype.forEach.call(document.querySelectorAll('[data-share]'), function (box) {
    var canon = box.dataset.url, title = box.dataset.title;
    var url = here || canon;
    var live = box.querySelector('[data-share-live]');
    if (url !== canon) {
      Array.prototype.forEach.call(box.querySelectorAll('a.share-btn'), function (a) {
        a.href = a.href.split(encodeURIComponent(canon)).join(encodeURIComponent(url));
      });
    }
    var nat = box.querySelector('[data-share-native]');
    if (nat && navigator.share) {
      nat.hidden = false;
      nat.addEventListener('click', function () {
        navigator.share({ title: title, text: title, url: url }).catch(function () {});
      });
    }
    var copy = box.querySelector('[data-share-copy]');
    if (copy) {
      var label = copy.querySelector('span');
      copy.addEventListener('click', function () {
        var done = function () {
          copy.classList.add('done'); if (label) label.textContent = 'Link copied';
          if (live) live.textContent = 'Link copied';
          setTimeout(function () { copy.classList.remove('done'); if (label) label.textContent = 'Copy link'; }, 1600);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, function () { window.prompt('Copy this link', url); });
        else window.prompt('Copy this link', url);
      });
    }
  });
})();
