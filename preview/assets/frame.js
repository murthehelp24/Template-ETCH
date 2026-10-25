/* Runs inside every preview page (preview/<id>.html). Copied to preview/assets/ by build_preview.py.
   - receives the builder state (colours, root font size) through postMessage — works on file:// too
   - reports its content height so the builder can size the iframe
   - keeps clicks inside the preview (links would navigate away from the static file)
   - edit mode: click a marked text (data-pv-edit) to type over it, click an image slot (data-pv-img) to pick a picture;
     changes go to the builder, which keeps them and writes the text into the copied .etch.txt
   - "ดูทั้งหน้า" (preview/page.html?pb=<page id>): reads the saved page from the builder's storage
   - tiny stand-in for the Oh My Etch menu script (its plugin JS is not available offline) */
(function () {
  var root = document.documentElement;
  var id = document.body.getAttribute('data-template');
  var MAIN = ['main-primary', 'main-accent', 'main-light', 'main-text', 'main-on-primary'];
  var ACSS = ['primary', 'secondary'];
  var expanded = 0; // extra height while a menu / drawer is open

  var HEX = /^#[0-9a-f]{6}$/i; // only plain colours reach the page's CSS

  function apply(state) {
    if (state.root === 10 || state.root === 16) {
      root.style.fontSize = state.root === 16 ? '100%' : '62.5%';
      root.style.setProperty('--etch-root-px', String(state.root));
    }
    var c = state.colors || {};
    MAIN.forEach(function (k) {
      if (HEX.test(c[k])) root.style.setProperty('--' + k, c[k]);
      else root.style.removeProperty('--' + k);
    });
    var a = state.acss || {};
    ACSS.forEach(function (k) {
      if (HEX.test(a[k])) root.style.setProperty('--' + k, a[k]);
      else root.style.removeProperty('--' + k);
    });
    var bt = state.buttons || {};
    [['primaryText', '--pv-btn-primary-text'], ['secondaryText', '--pv-btn-secondary-text']].forEach(function (b) {
      if (HEX.test(bt[b[0]])) root.style.setProperty(b[1], bt[b[0]]);
      else root.style.removeProperty(b[1]);
    });
    report();
  }

  var last = -1;
  function report() {
    var h = Math.ceil(document.body.getBoundingClientRect().height);
    if (expanded) h = Math.max(h, expanded);
    if (h !== last && window.parent !== window) {
      last = h;
      window.parent.postMessage({ type: 'pv-height', id: id, height: h }, '*');
    }
  }

  window.addEventListener('message', function (e) {
    if (e.source !== window.parent || window.parent === window) return; // only the builder that embeds this page
    var d = e.data || {};
    if (d.type === 'pv-state') { apply(d); content(d); }
  });

  // standalone use (preview pages, builder "ดูทั้งหน้า"): ?root=16&c=1e3a5f,,,,ffffff&a=,e8a33d&b=ffffff,
  // c = the five --main-* colours in order, a = ACSS primary, secondary, b = button text (primary, secondary);
  // empty = default
  var q = new URLSearchParams(location.search);
  if (q.has('root') || q.has('c') || q.has('a') || q.has('b')) {
    var list = function (s) { return (s || '').split(',').map(function (v) { return v ? '#' + v : null; }); };
    var cs = list(q.get('c')), as = list(q.get('a')), bs = list(q.get('b'));
    var st = { root: Number(q.get('root')), colors: {}, acss: {}, buttons: { primaryText: bs[0], secondaryText: bs[1] } };
    MAIN.forEach(function (k, i) { st.colors[k] = cs[i]; });
    ACSS.forEach(function (k, i) { st.acss[k] = as[i]; });
    apply(st);
  }

  if ('ResizeObserver' in window) new ResizeObserver(report).observe(document.body);
  window.addEventListener('load', report);

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (a) e.preventDefault();
  }, true);

  // ---------------------------------------------------------------- edited text and pictures
  var editing = false, scopeOf = function () { return [document]; };

  function each(sel, roots, fn) {
    roots.forEach(function (r) {
      if (r.matches && r.matches(sel)) fn(r);
      r.querySelectorAll(sel).forEach(fn);
    });
  }

  // edits: { "t:g.0.1": "new text", "p:g:title": "…" } · images: { "i:g.0.3": "data:image/webp;base64,…" }
  function show(edits, images, roots) {
    edits = edits || {};
    images = images || {};
    each('[data-pv-edit]', roots, function (el) {
      if (el.pvOrig === undefined) el.pvOrig = el.textContent;
      if (el.isContentEditable) return;
      var v = edits[el.getAttribute('data-pv-edit')];
      el.textContent = typeof v === 'string' ? v : el.pvOrig;
    });
    each('[data-pv-img]', roots, function (img) {
      if (img.pvOrig === undefined) img.pvOrig = img.getAttribute('src');
      var v = images[img.getAttribute('data-pv-img')];
      img.setAttribute('src', typeof v === 'string' && /^data:image\//.test(v) ? v : img.pvOrig);
    });
  }

  function content(d) {
    if (!('edits' in d) && !('edit' in d)) return;
    show(d.edits, d.images, scopeOf());
    editing = !!d.edit;
    root.classList.toggle('pv-editing', editing);
    document.querySelectorAll('[data-pv-img]').forEach(function (img) {
      if (editing) img.title = 'คลิกเพื่อใส่รูป'; else img.removeAttribute('title');
    });
    report();
  }

  var css = document.createElement('style');
  css.textContent =
    '.pv-editing [data-pv-edit]{cursor:text}' +
    '.pv-editing [data-pv-edit]:hover{outline:2px dashed rgb(47 91 211/.75);outline-offset:2px}' +
    '[data-pv-edit][contenteditable]{outline:2px solid #2f5bd3!important;outline-offset:2px;background:rgb(47 91 211/.08)}' +
    '.pv-editing [data-pv-img]{cursor:pointer}' +
    '.pv-editing [data-pv-img]:hover,.pv-editing .pv-cover-hover{outline:3px dashed rgb(47 91 211/.85);outline-offset:-3px}' +
    '.pv-cover-pointer,.pv-cover-pointer *{cursor:pointer}';
  document.head.appendChild(css);

  function send(msg) { if (window.parent !== window) window.parent.postMessage(msg, '*'); }

  function startEdit(el, e) {
    var key = el.getAttribute('data-pv-edit');
    var before = el.textContent;
    try { el.contentEditable = 'plaintext-only'; } catch (err) { el.contentEditable = 'true'; }
    el.focus();
    var range = document.caretRangeFromPoint && document.caretRangeFromPoint(e.clientX, e.clientY);
    if (range) { var sel = getSelection(); sel.removeAllRanges(); sel.addRange(range); }
    function done(keep) {
      el.removeEventListener('keydown', onKey);
      el.removeEventListener('blur', onBlur);
      el.removeEventListener('paste', onPaste);
      el.removeAttribute('contenteditable');
      if (!keep) { el.textContent = before; report(); return; }
      var value = el.innerText.replace(/\n$/, '');
      // the same text can appear more than once (a loop, the mobile menu copy): keep them in step
      document.querySelectorAll('[data-pv-edit="' + key + '"]').forEach(function (o) { if (o !== el) o.textContent = value; });
      if (value !== before) send({ type: 'pv-edit', key: key, value: value === el.pvOrig ? null : value });
      report();
    }
    function onKey(k) {
      if (k.key === 'Enter' && !k.shiftKey) { k.preventDefault(); el.blur(); }
      if (k.key === 'Escape') { k.preventDefault(); done(false); el.blur(); }
    }
    function onBlur() { done(true); }
    function onPaste(p) {  // plain text only
      p.preventDefault();
      document.execCommand('insertText', false, (p.clipboardData || window.clipboardData).getData('text/plain'));
    }
    el.addEventListener('keydown', onKey);
    el.addEventListener('blur', onBlur);
    el.addEventListener('paste', onPaste);
  }

  // shrink to at most 1600 px wide and store as WebP (keeps transparency for logos)
  function pickImage(img) {
    var input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.addEventListener('change', function () {
      var file = input.files[0];
      if (!file) return;
      var r = new FileReader();
      r.onload = function () {
        var pic = new Image();
        pic.onload = function () {
          var scale = Math.min(1, 1600 / pic.naturalWidth);
          var cv = document.createElement('canvas');
          cv.width = Math.round(pic.naturalWidth * scale);
          cv.height = Math.round(pic.naturalHeight * scale);
          cv.getContext('2d').drawImage(pic, 0, 0, cv.width, cv.height);
          var url = cv.toDataURL('image/webp', 0.85);
          if (url.indexOf('data:image/webp') !== 0) url = cv.toDataURL('image/png');
          img.setAttribute('src', url);
          send({ type: 'pv-image', key: img.getAttribute('data-pv-img'), dataURL: url,
                 name: file.name.replace(/\.[^.]+$/, '') });
        };
        pic.src = r.result;
      };
      r.readAsDataURL(file);
    });
    input.click();
  }

  // the builder switches its library to this template's kind (header / sections / footer) when it is clicked
  document.addEventListener('pointerdown', function () { send({ type: 'pv-click' }); }, true);

  document.addEventListener('click', function (e) {
    if (!editing) return;
    var el = e.target.closest && e.target.closest('[data-pv-edit]');
    if (el) {
      if (el.isContentEditable) return;
      e.preventDefault();
      e.stopPropagation();
      startEdit(el, e);
      return;
    }
    var img = (e.target.closest && e.target.closest('[data-pv-img]')) || coverImage(e);
    if (img) { e.preventDefault(); e.stopPropagation(); pickImage(img); }
  }, true);

  // a background photo sits under an overlay (hero-image, hero-gradient): find the image slot under the pointer,
  // unless the pointer is on something of its own (a link, a button, a text to edit)
  function coverImage(e) {
    if (!e.target.closest || e.target.closest('a, button, input, select, textarea, [data-pv-edit]')) return null;
    var under = document.elementsFromPoint ? document.elementsFromPoint(e.clientX, e.clientY) : [];
    for (var i = 0; i < under.length; i++) if (under[i].hasAttribute('data-pv-img')) return under[i];
    return null;
  }
  var hovered = null;
  document.addEventListener('pointermove', function (e) {
    var img = editing && !(e.target.closest && e.target.closest('[data-pv-img]')) ? coverImage(e) : null;
    if (img === hovered) return;
    if (hovered) hovered.classList.remove('pv-cover-hover');
    hovered = img;
    if (img) img.classList.add('pv-cover-hover');
    root.classList.toggle('pv-cover-pointer', !!img);
  });

  // "ดูทั้งหน้า": page.html?pb=<id> — the saved page (same browser storage as the builder) gives the edits
  // and pictures for each stamped template, in the order of ?t=
  var pb = q.get('pb');
  if (pb && document.querySelector('[data-pv-inst]')) {
    var saved = null;
    try {
      saved = (JSON.parse(localStorage.getItem('etchPageBuilder.v1')) || { pages: [] }).pages
        .filter(function (p) { return p && p.id === pb; })[0];
    } catch (err) { /* storage blocked: colours from the URL still apply */ }
    if (saved) {
      var keys = [];
      if (saved.header) keys.push('header:' + saved.header);
      (saved.sections || []).forEach(function (s) { keys.push(s.k); });
      if (saved.footer) keys.push('footer:' + saved.footer);
      var rootsOf = function (i) { return Array.prototype.slice.call(document.querySelectorAll('[data-pv-inst="' + i + '"]')); };
      keys.forEach(function (k, i) { show((saved.edits || {})[k], {}, rootsOf(i)); });
      // pictures live in IndexedDB (too big for localStorage)
      try {
        var open = indexedDB.open('etchPageBuilder', 1);
        open.onupgradeneeded = function () { open.result.createObjectStore('images', { keyPath: 'id' }); };
        open.onsuccess = function () {
          var store = open.result.transaction('images').objectStore('images');
          keys.forEach(function (k, i) {
            var refs = (saved.images || {})[k] || {}, got = {}, left = Object.keys(refs).length;
            Object.keys(refs).forEach(function (slot) {
              var req = store.get(refs[slot]);
              req.onsuccess = function () {
                if (req.result) got[slot] = req.result.dataURL;
                if (--left === 0) show((saved.edits || {})[k], got, rootsOf(i));
              };
            });
          });
        };
      } catch (err) { /* no IndexedDB: placeholders stay */ }
    }
  }

  // ---------------------------------------------------------------- Menu Builder header (site-header.etch.txt)
  // Its CSS targets .menu-dropdown / .toggle … classes that are not in the pasted markup (on a live site they come
  // from the menu components already installed there). Add them from the data-menu-element hooks so the bundled
  // CSS + scripts can work in the preview. Runs before the module scripts (those are deferred).
  function addCls(sel, cls, scope) {
    (scope || document).querySelectorAll(sel).forEach(function (el) { el.classList.add.apply(el.classList, cls.split(' ')); });
  }
  if (document.querySelector('[data-menu-element="menu-wrapper"]')) {
    addCls('[data-menu-element="menu-wrapper"]', 'menu-wrapper');
    addCls('[data-menu-element="menu-wrapper"] > div:first-child', 'menu-wrapper__inner');
    addCls('[data-menu-element="dropdown"]', 'menu-dropdown');
    addCls('[data-menu-element="dropdown-trigger"]', 'menu-dropdown__trigger');
    addCls('[data-menu-element="dropdown-label"]', 'menu-dropdown__trigger-label');
    addCls('[data-menu-element="dropdown-trigger"] > [aria-hidden]', 'menu-dropdown__trigger-icon-wrapper');
    addCls('[data-menu-element="dropdown-trigger"] > [aria-hidden] > svg', 'menu-dropdown__trigger-icon');
    addCls('[data-menu-element="dropdown-content"]', 'menu-dropdown__content-wrapper');
    addCls('[data-menu-element="back-button"]', 'menu-dropdown-back-button');
    addCls('[data-menu-element="dropdown-content"] > [tag]', 'menu-dropdown__content');
    addCls('[data-menu-element="nav"] li[data-menu-hide]:not([data-menu-element])', 'menu-link');
    document.querySelectorAll('button[data-target-element]').forEach(function (b) {
      b.classList.add('toggle');
      var svg = b.querySelector('svg');
      if (svg) svg.classList.add('toggle__icon', 'toggle-animated-hamburger-' + (svg.querySelectorAll('line').length === 2 ? 1 : 2));
      var label = b.querySelector('[aria-hidden] > span');
      if (label) label.parentNode.classList.add('toggle__label');
    });
  }

  // ---------------------------------------------------------------- Oh My Etch menu stand-in
  var omeRoot = document.querySelector('[data-ome-nav-menu-root]');
  if (!omeRoot) {
    if (window.parent !== window) window.parent.postMessage({ type: 'pv-ready', id: id }, '*');
    return;
  }

  function setExpanded(px) {
    expanded = px;
    last = -1;
    report();
  }

  // desktop dropdowns: open on hover / click
  omeRoot.querySelectorAll('[data-ome-nav-menu-item]').forEach(function (item) {
    var trigger = item.querySelector('[data-ome-nav-menu-trigger]');
    var content = item.querySelector('[data-ome-nav-menu-content]');
    if (!trigger || !content) return;
    function open(on) {
      [item, trigger, content].forEach(function (el) { el.setAttribute('data-ome-state', on ? 'open' : 'closed'); });
      trigger.setAttribute('aria-expanded', on ? 'true' : 'false');
      if (on) content.removeAttribute('hidden'); else content.setAttribute('hidden', '');
      setExpanded(on ? Math.ceil(content.getBoundingClientRect().bottom) + 16 : 0);
    }
    item.addEventListener('mouseenter', function () { open(true); });
    item.addEventListener('mouseleave', function () { open(false); });
    trigger.addEventListener('click', function () { open(trigger.getAttribute('data-ome-state') !== 'open'); });
  });

  // mobile drawer: build the list from the desktop menu (the plugin does this at runtime)
  document.querySelectorAll('[data-ome-mobile-nav-root]').forEach(function (mobile) {
    var drawer = mobile.querySelector('[data-ome-drawer-root]');
    var list = mobile.querySelector('[data-ome-mobile-nav-static-preview] [data-ome-mobile-nav-list]') ||
      mobile.querySelector('[data-ome-mobile-nav-panels] > [data-ome-mobile-nav-panel] [data-ome-mobile-nav-list]');
    var tpl = mobile.querySelector('[data-ome-mobile-nav-template]');
    var panels = mobile.querySelector('[data-ome-mobile-nav-panels]');
    if (!drawer || !panels) return;
    if (!list && tpl) {
      var panel = tpl.querySelector('[data-ome-mobile-nav-panel]').cloneNode(true);
      list = panel.querySelector('[data-ome-mobile-nav-list]');
      list.innerHTML = '';
      var after = panels.querySelector('[data-ome-mobile-nav-slot-after]');
      if (after) { after.removeAttribute('hidden'); panel.appendChild(after); }
      panels.insertBefore(panel, panels.firstChild);
    }
    if (list && tpl && !list.children.length) {
      var itemCls = (tpl.querySelector('[data-ome-mobile-nav-item]') || {}).className || '';
      var linkCls = (tpl.querySelector('[data-ome-mobile-nav-link]') || {}).className || '';
      omeRoot.querySelectorAll('[data-ome-nav-menu-list] > [data-ome-nav-menu-item]').forEach(function (it) {
        var link = it.querySelector(':scope > a');
        var trig = it.querySelector('[data-ome-nav-menu-trigger]');
        var li = document.createElement('li');
        li.className = itemCls;
        li.setAttribute('data-ome-mobile-nav-item', '');
        var a = document.createElement(link ? 'a' : 'button');
        a.className = linkCls;
        a.textContent = (link || trig || it).textContent.trim();
        if (link) a.href = link.getAttribute('href');
        li.appendChild(a);
        list.appendChild(li);
      });
    }
    // the plugin moves the drawer into a fixed host (overlay + sliding panel) at the end of <body>
    var host = document.createElement('div');
    host.setAttribute('data-ome-drawer-host', '');
    host.setAttribute('data-ome-state', 'closed');
    host.setAttribute('data-ome-direction', drawer.getAttribute('data-ome-direction') || 'right');
    host.innerHTML = '<div data-ome-drawer-host-overlay></div><div data-ome-drawer-host-content></div>';
    document.body.appendChild(host);
    host.lastChild.appendChild(drawer);
    drawer.removeAttribute('hidden');
    host.firstChild.addEventListener('click', function () { open(false); });

    function open(on) {
      drawer.setAttribute('data-ome-state', on ? 'open' : 'closed');
      host.setAttribute('data-ome-state', on ? 'open' : 'closed');
      mobile.querySelectorAll('[data-ome-drawer-trigger]').forEach(function (b) {
        b.setAttribute('aria-expanded', on ? 'true' : 'false');
      });
      setExpanded(on ? 640 : 0);
    }
    mobile.querySelectorAll('[data-ome-drawer-trigger]').forEach(function (b) {
      b.addEventListener('click', function () { open(drawer.getAttribute('data-ome-state') !== 'open'); });
    });
    mobile.querySelectorAll('[data-ome-drawer-close]').forEach(function (b) {
      b.addEventListener('click', function () { open(false); });
    });
  });

  if (window.parent !== window) window.parent.postMessage({ type: 'pv-ready', id: id }, '*');
})();
