/** CSS of the Menu Builder header (build_header_menubuilder.py), copied from the top-level string constants of _build/build_header_menubuilder.py
 * (each value as Python evaluates it). Kept exactly as written: these builders do not call portable(). */

export const ROOT_CSS = `/* Colours come from the main colours (:where(:root)) — change them there */
  --header-bg: var(--main-primary);
  --header-text: var(--main-on-primary);
  --header-accent: var(--main-accent);
  --header-border: var(--main-line-on-primary);
  --header-panel-bg: var(--main-primary);
  --header-logo-height: 40px;
  --ease-swift: cubic-bezier(0.55, 0, 0.1, 1);

  pointer-events: none;
  z-index: 50;
  padding: 0;

  > * {
    pointer-events: auto;
  }

  @media (width <= 768px) {
    --header-logo-height: 32px;
  }

  /* ===== POSITION (data attributes on this element) ===== */
  &[data-overlay-header='true'],
  &[data-sticky-header='true'] {
    inset-block-start: var(--wp-admin--admin-bar--height, 0px);
  }

  &[data-overlay-header='true'] {
    position: absolute;
  }

  &[data-sticky-header='true'] {
    position: sticky;
  }

  &[data-sticky-header='true'][data-overlay-header='true'] {
    position: fixed;
  }

  &[data-overlay-header='true'][data-overlay-header-offset='true'] + main > :first-child > :first-child {
    margin-block-start: var(--header-height);
  }

  &[data-hide-on-scroll='true'] .site-header__bar {
    transition: transform 0.4s var(--ease-swift);
  }

  &.hide .site-header__bar {
    transform: translateY(-100%);
  }

  /* ===== HAMBURGER: only while the menu is in mobile mode ===== */
  #mobile-menu-toggle {
    display: none;
  }

  &:has(.menu-wrapper.mobile) :is(#mobile-menu-toggle, .toggle) {
    display: flex;
  }

  /* tablet: keep the buttons next to the hamburger */
  &:has(.menu-wrapper.mobile) .site-header__actions {
    margin-inline-start: auto;
  }

  .toggle {
    --toggle-icon-color: var(--header-text);
    color: var(--header-text);
  }

  /* ===== SKIP LINK (added by script) ===== */
  .skip-link {
    position: absolute;
    top: -1500px;
    left: 32px;
    z-index: 999;
    overflow: hidden;
    background: var(--main-light);
    color: var(--main-text);

    &:focus-visible {
      top: 32px;
    }
  }

  /* ===== MENU VARIABLES ===== */
  --link-color: var(--header-text);
  --link-color-hover: var(--header-text);
  --link-color-active: var(--header-accent);
  --link-bg-color: transparent;
  --link-bg-color-hover: transparent;
  --link-bg-color-active: transparent;
  --link-font-weight: var(--btn-font-weight);
  --link-transition: all 0.2s ease-out;
  --link-padding-inline: var(--btn-padding-inline, 1em);
  --link-padding-block: var(--btn-padding-block, 0.75em);
  --link-border-radius: var(--btn-border-radius);

  --dropdown-padding: calc(to-rem(5px) + 3px) 0 to-rem(5px);
  --dropdown-border-radius: 0;
  --dropdown-border-width: 0px;
  --dropdown-border-color: transparent;
  --dropdown-bg: linear-gradient(var(--header-accent), var(--header-accent)) top / 100% 3px no-repeat, var(--header-panel-bg);
  --dropdown-box-shadow: 0 16px 36px var(--main-shadow);
  --dropdown-closed-top: 30px;
  --dropdown-open-top: 22px;

  --mobile-menu-padding-inline: var(--gutter);
  --mobile-menu-padding-block: var(--space-m);
  --mobile-menu-bg-color: var(--header-panel-bg);
  --mobile-menu-width: 768px;
  --mobile-dropdown-stacked-timing: cubic-bezier(0.86, 0.01, 0.09, 1.01);

  /* ===== DROPDOWN ANIMATION ===== */
  .menu-dropdown .menu-dropdown__content-wrapper {
    filter: blur(4px);
  }

  .menu-dropdown.is-open > .menu-dropdown__content-wrapper {
    filter: blur(0);
  }

  .menu-wrapper.desktop .menu-dropdown .menu-dropdown__content-wrapper,
  .menu-wrapper.desktop .morph-container {
    scale: 0.95;
  }

  .menu-wrapper.desktop .menu-dropdown.is-open > .menu-dropdown__content-wrapper,
  .menu-wrapper.desktop .morph-container.is-active {
    scale: 1;
  }

  .menu-dropdown-back-button {
    font-weight: var(--link-font-weight);
    padding-block: 1em;
    padding-inline: var(--mobile-menu-padding-inline);
    color: var(--link-color);
    background-color: var(--mobile-menu-bg-color);
    border-block-end: 1px solid var(--header-border);
  }

  /* show desktop menu before the menu script initialises */
  .menu-wrapper.desktop:not([data-menu-initialized]) {
    @media (width >= 1200px) {
      opacity: 1;
    }
  }

  /* ===== DESKTOP MENU (centred between logo and buttons) ===== */
  .menu-wrapper.desktop {
    flex: 1 1 auto;

    .site-header__nav-list {
      justify-content: center;
    }

    .site-header__nav-list > li {
      inline-size: fit-content;
      white-space: nowrap;
    }

    .site-header__nav-list > li > *:is(a, button) {
      position: relative;
      padding-inline: var(--link-padding-inline);
      padding-block: var(--link-padding-block);
      border-radius: var(--link-border-radius);
      font-size: var(--text-s);
      line-height: 100%;
      color: var(--link-color);
      text-decoration: none;
      transition: var(--link-transition);

      /* animated underline */
      &::after {
        content: '';
        position: absolute;
        left: var(--link-padding-inline, 1em);
        right: var(--link-padding-inline, 1em);
        bottom: 0.35em;
        height: 2px;
        background-color: var(--header-accent);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.25s ease;
      }

      &:hover::after,
      &[aria-expanded='true']::after {
        transform: scaleX(1);
      }

      &.active-link {
        color: var(--link-color-active);
      }
    }

    .menu-dropdown__content {
      min-inline-size: 220px;
      gap: 0;
    }

    .menu-dropdown__content > li:not(:last-child) > a {
      box-shadow: inset 0 -1px 0 var(--header-border);
    }

    .menu-dropdown__content > li > a {
      display: block;
      padding: 0.6em 1.25em;
      font-size: var(--text-s);
      font-weight: 400;
      line-height: 1.3;
      color: var(--header-text);
      text-decoration: none;
      white-space: nowrap;
      transition: background-color 0.15s ease;

      &:hover,
      &:focus-visible {
        background-color: var(--header-accent);
        color: var(--header-text);
      }

      &:focus-visible {
        outline: 2px solid var(--header-text);
        outline-offset: -2px;
      }

      &[href='#'] {
        cursor: default;
      }
    }
  }

  /* ===== MOBILE MENU ===== */
  .menu-wrapper.mobile {
    .menu-wrapper__inner {
      display: flex;
      flex-direction: column;
      border-block-start: 3px solid var(--header-accent);
      color: var(--header-text);
    }

    .site-header__nav {
      flex: 1;
      position: relative;
      padding-inline: var(--mobile-menu-padding-inline);
      overflow-y: auto;
      overflow-x: clip;
    }

    .site-header__nav-list {
      flex-direction: column;
      justify-content: flex-start;
      flex-grow: 1;
      block-size: 100%;

      > li {
        inline-size: 100%;
        max-inline-size: 100%;
        border-block-end: 1px solid var(--header-border);

        > a,
        .menu-dropdown,
        .menu-dropdown__trigger {
          inline-size: 100%;
        }
      }
    }

    .site-header__nav-list > li > *:is(a, button),
    .menu-dropdown__content > li > *:is(a, button) {
      padding-block: var(--btn-padding-block);
      padding-inline: 0;
      line-height: 100%;
      color: var(--header-text);
      text-decoration: none;
      background-color: transparent;
      transition: var(--link-transition);

      &:hover,
      &[aria-expanded='true'] {
        color: var(--header-accent);
      }
    }

    .menu-dropdown__trigger {
      inline-size: 100%;
      justify-content: space-between;
    }

    .menu-dropdown__content-wrapper {
      background-color: transparent;
    }

    .menu-dropdown__content a {
      opacity: 0.8;
    }

    :where(& .menu-dropdown__content-wrapper.stacked-mode .menu-dropdown__content) {
      padding-block: var(--mobile-menu-padding-block);
      padding-inline: var(--mobile-menu-padding-inline);
    }

    :where(& .menu-dropdown.accordion-mode .menu-dropdown__content) {
      padding-inline: var(--space-xs);
    }

    :where(& .menu-dropdown.accordion-mode[data-mega-menu='true'] .menu-dropdown__content) {
      padding-block: var(--space-xs);
    }
  }`;

export const BAR_CSS = `inline-size: 100%;
  padding: var(--space-xs) var(--gutter);
  background-color: var(--header-bg);
  border-block-end: 1px solid var(--header-border);`;

export const CONTAINER_CSS = `flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-m);`;

export const LOGO_CSS = `display: flex;
  flex-shrink: 0;`;

export const LOGO_IMG_CSS = `block-size: var(--header-logo-height);
  inline-size: auto;
  max-inline-size: 100%;
  object-fit: contain;`;

export const ACTIONS_CSS = `display: flex;
  align-items: center;
  gap: var(--space-xs);
  flex-shrink: 0;

  @media (width <= 768px) {
    display: none;
  }`;

export const NAV_LIST_CSS = `display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--space-xs);
  margin: 0;
  padding: 0;
  list-style: none;

  li {
    max-inline-size: 100%;
  }`;
