/* Runs inside every preview page (preview/<id>.html). Copied to preview/assets/ by build_preview.py.
   - receives the builder state (colours, root font size) through postMessage — works on file:// too
   - reports its content height so the builder can size the iframe
   - keeps clicks inside the preview (links would navigate away from the static file)
   - tiny stand-in for the Oh My Etch menu script (its plugin JS is not available offline) */
(function () {
  var root = document.documentElement;
  var id = document.body.getAttribute('data-template');
  var MAIN = ['main-primary', 'main-accent', 'main-light', 'main-text', 'main-on-primary'];
  var ACSS = ['primary', 'secondary'];
  var expanded = 0; // extra height while a menu / drawer is open

  function apply(state) {
    if (state.root) {
      root.style.fontSize = state.root === 16 ? '100%' : '62.5%';
      root.style.setProperty('--etch-root-px', String(state.root));
    }
    var c = state.colors || {};
    MAIN.forEach(function (k) {
      if (c[k]) root.style.setProperty('--' + k, c[k]);
      else root.style.removeProperty('--' + k);
    });
    var a = state.acss || {};
    ACSS.forEach(function (k) {
      if (a[k]) root.style.setProperty('--' + k, a[k]);
      else root.style.removeProperty('--' + k);
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
    var d = e.data || {};
    if (d.type === 'pv-state') apply(d);
  });

  // standalone use: ?root=16 in the URL
  var m = /[?&]root=(10|16)/.exec(location.search);
  if (m) apply({ root: Number(m[1]) });

  if ('ResizeObserver' in window) new ResizeObserver(report).observe(document.body);
  window.addEventListener('load', report);

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (a) e.preventDefault();
  }, true);

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
