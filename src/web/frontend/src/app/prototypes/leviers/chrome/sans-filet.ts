import type { LevierOption, Valeurs } from '../options'

const TRANSPARENT = 'transparent'

// No rule across the frame: the sidebar and the top bar of a phone take a grey background, space separates the header
// from the content, and the only rule of the main column runs under the tabs, from one gutter to the other; when
// content scrolls under the top of an area, the area shows the shadow of the DSFR header, with a rule between the
// gutters where no tabs run
const CADRE: Valeurs = {
  '--csp-chrome-border-color': TRANSPARENT,
  '--csp-nav-divider-color': TRANSPARENT,
  '--csp-app-shell-topbar-background': 'var(--csp-nav-background)',
  '--csp-table-toolbar-divider-color': TRANSPARENT,
  '--csp-page-header-subtitle-height-empty': '0px',
  '--csp-scroll-edge-rule-color': 'var(--border-default-grey)',
  '--csp-scroll-edge-shadow': 'var(--raised-shadow)',
}

// Labels without inline padding: the first label, the start of the rule and the content share the gutter, and the
// underline of the current tab has the width of its label; from the md breakpoint the rule spans the content column,
// below it the whole row, where the triggers scroll
const ONGLETS: Valeurs = {
  '--csp-tabs-trigger-padding-inline': '0px',
  '--csp-tabs-gap': 'var(--csp-space-8)',
  '--csp-page-tabs-divider-box': 'content-box',
  '--csp-tabs-focus-offset': '2px',
  '--csp-tabs-trigger-background-hover': TRANSPARENT,
  '--csp-tabs-trigger-background-active': TRANSPARENT,
  '--csp-tabs-trigger-background-current-hover': TRANSPARENT,
  '--csp-tabs-trigger-border-color-hover': 'var(--border-contrast-grey)',
}

// A kanban column is a lane on the alternative grey, without outline, and the board scrolls to the edge of the window
const KANBAN: Valeurs = {
  '--csp-region-border-color': TRANSPARENT,
  '--csp-kanban-gap': 'var(--csp-space-4)',
  '--csp-kanban-scroll-to-edge': '1',
}

// The panel and the drawers stand out by their shadow; space separates their header and footer from their body, and
// the scroll edge marks the footer while content remains under it
const COUCHES: Valeurs = {
  '--csp-lifted-border-color': TRANSPARENT,
  '--csp-drawer-divider-color': TRANSPARENT,
  '--csp-aside-border-color': TRANSPARENT,
}

export const SANS_FILET: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  { id: 'sans-filet', nom: 'Séparation par l’espace', valeurs: { ...CADRE, ...ONGLETS, ...KANBAN, ...COUCHES } },
]
