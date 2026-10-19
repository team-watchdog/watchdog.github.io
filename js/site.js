/* Watchdog site script: theme, reading-language preference, listing filters,
   article table of contents and figure captions. No dependencies. */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var LANG_NAMES = { en: 'English', si: 'සිංහල', ta: 'தமிழ்' };

  /* ---------- theme ---------- */
  var themeBtn = $('#theme-toggle');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    store.set('wd-theme', next);
  });

  /* ---------- query string helpers ---------- */
  var params = new URLSearchParams(location.search);
  function syncUrl() {
    var p = new URLSearchParams();
    if (state.lang !== 'auto' && $('[data-filterable]')) p.set('lang', state.lang);
    if (state.cat) p.set('cat', state.cat);
    if (state.q) p.set('q', state.q);
    var qs = p.toString();
    history.replaceState(null, '', location.pathname + (qs ? '?' + qs : '') + location.hash);
  }

  /* ---------- state ---------- */
  var stored = store.get('wd-lang');
  var state = {
    lang: /^(auto|en|si|ta)$/.test(params.get('lang') || '') ? params.get('lang') : (/^(auto|en|si|ta)$/.test(stored || '') ? stored : 'auto'),
    cat: params.get('cat') || '',
    q: params.get('q') || ''
  };
  var pageLang = (window.WD && window.WD.lang) || 'en';

  /* ---------- cards ---------- */
  var cards = $$('.card[data-variants]');
  cards.forEach(function (c) {
    try { c._v = JSON.parse(c.getAttribute('data-variants')); } catch (e) { c._v = {}; }
    c._canon = c.getAttribute('data-lang');
  });

  function showVariant(card, lang) {
    var v = card._v[lang];
    if (!v) return false;
    var a = $('.card-title a', card);
    if (a) { a.textContent = v.t; a.setAttribute('href', v.u); }
    var title = $('.card-title', card); if (title) title.setAttribute('lang', lang);
    var dek = $('.card-dek', card);
    if (dek) { dek.textContent = v.d; dek.setAttribute('lang', lang); }
    var media = $('.card-media', card); if (media) media.setAttribute('href', v.u);
    $$('.lang-tag', card).forEach(function (t) {
      t.classList.toggle('is-current', t.getAttribute('data-tag-lang') === lang);
    });
    card.setAttribute('data-lang', lang);
    return true;
  }

  function applyCards() {
    var strictGrids = $$('[data-filterable]');
    var visible = 0, total = 0;
    cards.forEach(function (card) {
      var strict = !!card.closest('[data-filterable]');
      var want = state.lang;
      var hidden = false;
      if (want === 'auto') showVariant(card, card._canon);
      else if (card._v[want]) showVariant(card, want);
      else { showVariant(card, card._canon); if (strict) hidden = true; }
      if (strict) {
        total++;
        var cats = (card.getAttribute('data-cat') || '').split(' ');
        if (state.cat && cats.indexOf(state.cat) === -1) hidden = true;
        if (state.q) {
          var hay = card.getAttribute('data-search') || '';
          if (state.q.toLowerCase().split(/\s+/).some(function (w) { return w && hay.indexOf(w) === -1; })) hidden = true;
        }
        card.hidden = hidden;
        if (!hidden) visible++;
      }
    });
    var note = $('#empty-note'); if (note) note.hidden = !strictGrids.length || visible > 0;
    var count = $('#result-count');
    if (count && strictGrids.length) count.textContent = visible + ' of ' + total + ' stories';
  }

  function applyButtons() {
    $$('[data-pref]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-pref') === state.lang)); });
    $$('[data-cat-filter]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-cat-filter') === state.cat)); });
  }

  function setLang(l, persist) {
    state.lang = l;
    if (persist !== false) store.set('wd-lang', l);
    applyButtons(); applyCards(); syncUrl(); articleBanner();
  }
  $$('[data-pref]').forEach(function (b) {
    b.addEventListener('click', function () { setLang(b.getAttribute('data-pref')); });
  });
  $$('[data-cat-filter]').forEach(function (b) {
    b.addEventListener('click', function () { state.cat = b.getAttribute('data-cat-filter'); applyButtons(); applyCards(); syncUrl(); });
  });
  var search = $('#q');
  if (search) {
    search.value = state.q;
    search.addEventListener('input', function () { state.q = search.value.trim(); applyCards(); syncUrl(); });
    if (params.get('focus') === 'search') search.focus();
  }

  /* ---------- article: language banner and preference ---------- */
  var article = $('.article[data-sib-en], .article[data-sib-si], .article[data-sib-ta]') || $('.article');
  function articleBanner() {
    var banner = $('#lang-banner');
    if (!banner || !article) return;
    var pref = state.lang;
    if (pref === 'auto' || pref === pageLang) { banner.hidden = true; return; }
    var url = article.getAttribute('data-sib-' + pref);
    if (!url) { banner.hidden = true; return; }
    banner.innerHTML = '';
    banner.appendChild(doc.createTextNode('This story is also available in '));
    var a = doc.createElement('a');
    a.href = url; a.lang = pref; a.textContent = LANG_NAMES[pref];
    banner.appendChild(a);
    banner.appendChild(doc.createTextNode(', your reading language.'));
    banner.hidden = false;
  }
  $$('[data-set-pref]').forEach(function (a) {
    a.addEventListener('click', function () { store.set('wd-lang', a.getAttribute('data-set-pref')); });
  });

  applyButtons(); applyCards(); articleBanner();

  /* ---------- article: figures with captions ---------- */
  var body = $('#article-body');
  if (body) {
    $$('p > img:only-child', body).forEach(function (img) {
      var alt = (img.getAttribute('alt') || '').trim();
      var p = img.parentNode;
      if (p.textContent.trim() !== '') return;
      var fig = doc.createElement('figure');
      p.parentNode.replaceChild(fig, p);
      fig.appendChild(img);
      if (alt.length > 3 && !/^(image|screenshot)$/i.test(alt)) {
        var cap = doc.createElement('figcaption'); cap.textContent = alt; fig.appendChild(cap);
      }
    });
    $$('table', body).forEach(function (t) {
      if (t.parentNode.classList.contains('table-wrap')) return;
      var w = doc.createElement('div'); w.className = 'table-wrap';
      t.parentNode.insertBefore(w, t); w.appendChild(t);
    });

    /* table of contents */
    var heads = $$('h2, h3', body);
    var toc = $('#toc'), list = $('#toc-list');
    if (toc && list && heads.length >= 4) {
      heads.forEach(function (h, i) {
        if (!h.id) h.id = 'sec-' + (i + 1);
        var li = doc.createElement('li'); li.className = 'toc-' + h.tagName.toLowerCase();
        var a = doc.createElement('a'); a.href = '#' + h.id; a.textContent = h.textContent.replace(/\s+/g, ' ').trim();
        li.appendChild(a); list.appendChild(li);
      });
      toc.hidden = false;
      var det = $('#toc-details');
      var mq = window.matchMedia('(min-width: 1080px)');
      det.open = mq.matches;
      if ('IntersectionObserver' in window) {
        var links = {};
        $$('a', list).forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (e.isIntersecting) {
              $$('a[aria-current]', list).forEach(function (a) { a.removeAttribute('aria-current'); });
              var l = links[e.target.id]; if (l) l.setAttribute('aria-current', 'true');
            }
          });
        }, { rootMargin: '-80px 0px -70% 0px' });
        heads.forEach(function (h) { io.observe(h); });
      }
    }
  }

  /* ---------- copy link ---------- */
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var url = b.getAttribute('data-copy'), old = b.textContent;
      (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () {
        b.textContent = 'Copied'; setTimeout(function () { b.textContent = old; }, 1800);
      }, function () { window.prompt('Copy this link', url); });
    });
  });
})();
