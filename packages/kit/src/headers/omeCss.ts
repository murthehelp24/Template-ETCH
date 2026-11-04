/** CSS of the Oh My Etch header (build_header_ome.py), copied from the top-level string constants of _build/build_header_ome.py
 * (each value as Python evaluates it). Kept exactly as written: these builders do not call portable(). */

export const MENU_ID = `main-menu`;

export const THEME_CSS = `/* Colours come from the main colours (:where(:root)) — change them there.
     Declared on :root because the mobile drawer is moved to <body> when it opens. */
  --main-header-logo-height: 40px;

  @media (width <= 768px) {
    --main-header-logo-height: 32px;
  }`;

export const ROOT_CSS = `pointer-events: none;
  z-index: 50;
  padding: 0;

  > * {
    pointer-events: auto;
  }

  /* position (data attributes on this element) */
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

  &[data-hide-on-scroll='true'] .main-header__bar {
    transition: transform 0.4s cubic-bezier(0.55, 0, 0.1, 1);
  }

  &.hide .main-header__bar {
    transform: translateY(-100%);
  }

  /* ACSS gives every <button> outside a <nav> button typography — keep menu buttons like links */
  button.main-header__link {
    font-weight: inherit;
    font-family: inherit;
    line-height: inherit;
    letter-spacing: inherit;
    text-transform: none;
  }

  .skip-link {
    position: absolute;
    top: -1500px;
    left: 32px;
    z-index: 999;
    background: var(--main-light);
    color: var(--main-text);

    &:focus-visible {
      top: 32px;
    }
  }`;

export const BAR_CSS = `inline-size: 100%;
  padding: var(--space-xs) var(--gutter);
  background-color: var(--main-primary);
  color: var(--main-on-primary);
  border-block-end: 1px solid var(--main-line-on-primary);`;

export const CONTAINER_CSS = `flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-m);

  /* desktop nav (Oh My Etch root) fills the middle so the links sit centred.
     Styled from here: Etch drops class-prop ids on paste for the Nav's styling group. */
  > [data-ome-nav-menu-root] {
    flex: 1 1 auto;

    @media (width <= 1199px) {
      display: none;
    }
  }

  @media (width >= 1200px) {
    > [data-ome-mobile-nav-root] {
      display: none;
    }
  }`;

export const LOGO_CSS = `display: flex;
  flex-shrink: 0;`;

export const LOGO_IMG_CSS = `block-size: var(--main-header-logo-height);
  inline-size: auto;
  max-inline-size: 100%;
  object-fit: contain;`;

export const NAV_LIST_CSS = `justify-content: center;
  align-items: center;
  gap: var(--space-xs);`;

export const LINK_CSS = `position: relative;
  display: inline-flex;
  align-items: center;
  gap: 0.25em;
  padding: var(--btn-padding-block, 0.75em) var(--btn-padding-inline, 1em);
  background: none;
  border: 0;
  font: inherit;
  font-size: var(--text-s);
  line-height: 1;
  white-space: nowrap;
  color: var(--main-on-primary);
  text-decoration: none;
  cursor: pointer;

  /* animated underline */
  &::after {
    content: '';
    position: absolute;
    inset-inline: var(--btn-padding-inline, 1em);
    inset-block-end: 0.35em;
    block-size: 2px;
    background-color: var(--main-accent);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.25s ease;
  }

  &:hover::after,
  &[aria-current='page']::after,
  &[aria-expanded='true']::after {
    transform: scaleX(1);
  }

  [data-ome-nav-menu-trigger-chevron] {
    transition: rotate 0.2s ease;
  }

  &[aria-expanded='true'] [data-ome-nav-menu-trigger-chevron] {
    rotate: 180deg;
  }`;

export const DROPDOWN_CSS = `display: flex;
  flex-direction: column;
  min-inline-size: 220px;
  padding-block: var(--space-xs);
  background-color: var(--main-primary);
  border-block-start: 3px solid var(--main-accent);
  box-shadow: 0 16px 36px var(--main-shadow);
  transition: opacity 0.15s ease, translate 0.15s ease;

  &[data-ome-state='closed'] {
    opacity: 0;
    translate: 0 8px;
  }`;

export const DROPDOWN_LINK_CSS = `display: block;
  padding: 0.6em 1.25em;
  font-size: var(--text-s);
  line-height: 1.3;
  white-space: nowrap;
  color: var(--main-on-primary);
  text-decoration: none;
  transition: background-color 0.15s ease;

  &:not(:last-child) {
    box-shadow: inset 0 -1px 0 var(--main-line-on-primary);
  }

  &:hover,
  &:focus-visible {
    background-color: var(--main-accent);
  }

  &:focus-visible {
    outline: 2px solid var(--main-on-primary);
    outline-offset: -2px;
  }`;

export const ACTIONS_CSS = `display: flex;
  align-items: center;
  gap: var(--space-xs);
  flex-shrink: 0;

  /* tablet: keep the buttons next to the hamburger */
  @media (width <= 1199px) {
    margin-inline-start: auto;
  }

  @media (width <= 768px) {
    display: none;
  }`;

export const BURGER_CSS = `display: inline-flex;
  align-items: center;
  justify-content: center;
  min-inline-size: 44px;
  min-block-size: 44px;
  padding: 0;
  background: none;
  border: 0;
  color: var(--main-on-primary);
  cursor: pointer;

  svg {
    inline-size: 28px;
    block-size: 28px;
  }`;

export const DRAWER_CSS = `--ome-drawer-overlay-color: color-mix(in srgb, var(--main-text) 60%, transparent);
  --ome-drawer-animation-duration: 250ms;
  inline-size: min(360px, 85vw);
  padding-block-start: var(--wp-admin--admin-bar--height, 0px);
  background-color: var(--main-primary);
  color: var(--main-on-primary);
  border-block-start: 3px solid var(--main-accent);

  /* ACSS gives every <button> outside a <nav> button typography — keep menu buttons like links */
  .main-header__mobile-link,
  .main-header__drawer-button {
    font-weight: inherit;
    font-family: inherit;
    line-height: inherit;
    letter-spacing: inherit;
    text-transform: none;
  }`;

export const DRAWER_CONTENT_CSS = `--_min-width: 100%;
  --_min-height: 100dvh;
  --_background: var(--main-primary);
  --_color: var(--main-on-primary);
  --_panel-background: var(--main-primary);`;

export const DRAWER_HEAD_CSS = `display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-xs);
  padding: var(--space-xs) var(--gutter);
  border-block-end: 1px solid var(--main-line-on-primary);`;

export const DRAWER_BUTTON_CSS = `display: inline-flex;
  align-items: center;
  gap: 0.375em;
  min-inline-size: 44px;
  min-block-size: 44px;
  margin-inline-start: auto;
  padding: 0;
  background: none;
  border: 0;
  font: inherit;
  color: inherit;
  cursor: pointer;

  &[data-ome-mobile-nav-back] {
    margin-inline-start: 0;
  }`;

export const MLIST_CSS = `display: grid;
  padding-inline: var(--gutter);`;

export const MITEM_CSS = `display: flex;
  align-items: stretch;
  border-block-end: 1px solid var(--main-line-on-primary);`;

export const MLINK_CSS = `display: flex;
  align-items: center;
  justify-content: space-between;
  inline-size: 100%;
  min-block-size: 48px;
  padding-block: var(--space-xs);
  padding-inline: 0;
  background: none;
  border: 0;
  font: inherit;
  text-align: start;
  color: var(--main-on-primary);
  text-decoration: none;
  cursor: pointer;

  &:hover,
  &:focus-visible {
    color: var(--main-accent);
  }`;

export const NEXT_ICON_CSS = `display: inline-flex;
  inline-size: 1em;
  block-size: 1em;
  flex-shrink: 0;`;

export const MSLOT_CSS = `display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  padding: var(--space-m) var(--gutter);`;
