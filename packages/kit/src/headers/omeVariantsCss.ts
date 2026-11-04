/** CSS of the header variants (build_header_variants.py), copied from the top-level string constants of _build/build_header_variants.py
 * (each value as Python evaluates it). They go through style(), so portable() turns their rem into to-rem(). */

export const LIGHT_CSS = `/* light bar: dark text on the light colour, primary button */
  .main-header__bar {
    background-color: var(--main-light);
    color: var(--main-text);
    border-block-end-color: var(--main-line);
    box-shadow: 0 2px 12px var(--main-shadow);
  }

  .main-header__link,
  .main-header__burger {
    color: var(--main-text);
  }

  .main-header__link::after {
    background-color: var(--main-primary);
  }

  .main-header__dropdown {
    background-color: var(--main-light);
    border-block-start-color: var(--main-primary);
  }

  .main-header__dropdown-link {
    color: var(--main-text);

    &:not(:last-child) {
      box-shadow: inset 0 -1px 0 var(--main-line);
    }

    &:hover,
    &:focus-visible {
      background-color: var(--main-light-alt);
      color: var(--main-primary);
    }

    &:focus-visible {
      outline-color: var(--main-primary);
    }
  }`;

export const CENTER_CSS = `/* desktop: logo centred on the first row, buttons on its right, menu centred on the row below */
  @media (width >= 1200px) {
    --main-header-logo-height: 52px;

    .main-header__container {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      row-gap: var(--space-xs);
    }

    .main-header__logo {
      grid-column: 2;
      grid-row: 1;
      justify-self: center;
    }

    .main-header__actions {
      grid-column: 3;
      grid-row: 1;
      justify-self: end;
    }

    .main-header__container > [data-ome-nav-menu-root] {
      grid-column: 1 / -1;
      grid-row: 2;
      padding-block-start: var(--space-xs);
      border-block-start: 1px solid var(--main-line-on-primary);
    }
  }`;

export const TOPBAR_CSS = `/* a thin info strip above the bar (inside it, so hide-on-scroll moves both) */
  .main-header__topbar {
    margin-block: calc(var(--space-xs) * -1) var(--space-xs);
    margin-inline: calc(var(--gutter) * -1);
    padding: 0.5em var(--gutter);
    background-color: var(--main-light-alt);
    color: var(--main-text);
    font-size: var(--text-xs, var(--text-s));
    line-height: 1.4;
  }

  .main-header__topbar-inner {
    display: flex;
    inline-size: 100%;
    max-inline-size: var(--content-width, 1366px);
    margin-inline: auto;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.25em var(--space-m);
  }

  .main-header__topbar-group {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.25em var(--space-m);
  }

  .main-header__topbar-item {
    display: inline-flex;
    align-items: center;
    gap: 0.5em;
    color: inherit;
    text-decoration: none;

    svg {
      inline-size: 1.1em;
      block-size: 1.1em;
      flex: 0 0 auto;
      color: var(--main-primary);
    }
  }

  a.main-header__topbar-item:hover {
    color: var(--main-primary);
    text-decoration: underline;
  }

  /* phones: the hours and phone only */
  @media (width <= 768px) {
    .main-header__topbar-inner {
      justify-content: center;
    }

    .main-header__topbar-group--extra,
    .main-header__topbar-item--address {
      display: none;
    }
  }`;

export const FLOATING_CSS = `/* the bar floats: a rounded, shadowed band with space around it; round buttons to match */
  .main-header__bar {
    background-color: transparent;
    border-block-end: 0;
    padding-block: var(--space-s);
  }

  .main-header__container {
    padding: var(--space-xs) var(--space-xs) var(--space-xs) var(--space-l);
    background-color: var(--main-primary);
    border-radius: 999px;
    box-shadow: 0 10px 30px var(--main-shadow);

    @media (width <= 768px) {
      padding-inline: var(--space-m) var(--space-xs);
    }
  }

  .main-header__actions > a {
    border-radius: 999px;
  }`;

export const RIGHT_CSS = `/* menu on the right, next to the button */
  .main-header__bar {
    padding-block: var(--space-s);
  }

  .main-header__nav-list {
    justify-content: flex-end;
  }`;
