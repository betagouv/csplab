import type { LevierOption, Valeurs } from '../options'

const FILET = 'var(--border-default-grey)'
const ACCENT = 'var(--border-action-high-blue-france)'
const SURFACE = 'var(--csp-surface-background)'
const MARGE_PAGE = 'var(--csp-page-container-padding-inline)'

// Shared by both options: the navigation lies on the canvas without rules, a kanban column and a fixed step of a
// sortable list take the background of the canvas inside the surface, and the surface role gives the background and
// the border of every surface
const CANEVAS: Valeurs = {
  '--csp-canvas-background': 'var(--background-alt-grey)',
  '--csp-nav-background': 'var(--csp-canvas-background)',
  '--csp-chrome-border-width': '0px',
  '--csp-nav-divider-width': '0px',
  '--csp-surface-background': 'var(--background-raised-grey)',
  '--csp-surface-border-color': FILET,
  '--csp-region-background': 'var(--csp-canvas-background)',
  '--csp-region-border-color': 'transparent',
  '--csp-region-border-color-drop': ACCENT,
  '--csp-sortable-list-item-alt-background': 'var(--csp-canvas-background)',
  // Forced colors: only the active tab keeps its bottom border
  '--csp-tabs-trigger-border-bottom-color-forced': 'Canvas',
}

// In the dark theme a lighter surface is a higher one: the canvas takes the darkest grey of the DSFR, the cards and
// the head of a table the grey above the surface
const CANEVAS_SOMBRE: Valeurs = {
  '--csp-canvas-background': 'var(--background-default-grey)',
  '--csp-raised-background': 'var(--background-overlap-grey)',
  '--csp-raised-background-hover': 'var(--background-overlap-grey-hover)',
  '--csp-table-head-background': 'var(--background-contrast-grey)',
  '--csp-table-footer-background': 'var(--background-contrast-grey)',
}

// Top, sides and background of the selected tab of the DSFR, drawn over its whole height so that they meet the
// border of the surface
const ONGLET_OUVERT = [
  `linear-gradient(${ACCENT} 0 0) top / 100% 2px no-repeat border-box`,
  'linear-gradient(var(--csp-surface-border-color) 0 0) left / 1px 100% no-repeat border-box',
  'linear-gradient(var(--csp-surface-border-color) 0 0) right / 1px 100% no-repeat border-box',
  SURFACE,
].join(', ')

// The surface keeps 32px of padding, the padding of a DSFR tab panel from 48em, and the canvas takes the rest of the
// page margin, rounded down to the 8px grid: 0 on a phone, 16px at 1440px, 32px at 1920px
const MARGE_SURFACE = `round(down, max(0px, ${MARGE_PAGE} - var(--csp-space-8)), var(--csp-space-2))`

const SURFACE_OUVERTE: Valeurs = {
  '--csp-page-tabs-background-hover': 'var(--background-alt-grey-hover)',
  '--csp-page-tabs-background-active': 'var(--background-alt-grey-active)',
  // The hover background of a closed tab stops above the border of the surface
  '--csp-page-tabs-background-clip': 'padding-box',
  '--csp-page-tabs-border-width': '0px',
  '--csp-page-tabs-margin-bottom': '-1px',
  '--csp-page-tabs-position': 'relative',
  '--csp-page-tabs-background-current': ONGLET_OUVERT,
  '--csp-page-tabs-background-current-hover': 'var(--background-raised-grey-hover)',
  '--csp-page-tabs-border-color-current': 'transparent',
  '--csp-page-content-background': SURFACE,
  '--csp-page-content-border-width': '1px',
  '--csp-page-content-inset': MARGE_SURFACE,
  '--csp-page-content-inset-bottom': MARGE_SURFACE,
  '--csp-page-content-grow': '1',
  '--csp-page-content-max-width': 'none',
  '--csp-kanban-bleed-inline-end': `calc(${MARGE_PAGE} - ${MARGE_SURFACE} - 1px)`,
  '--csp-table-border-width': '0px',
  '--csp-callout-border-width': '0px',
}

// The hover grey of the DSFR leaves the blue label of the selected tab at 3.4:1 in the dark theme: the selected tab
// takes the grey one step above the surface
const SURFACE_OUVERTE_SOMBRE: Valeurs = {
  '--csp-page-tabs-background-hover': 'var(--background-default-grey-hover)',
  '--csp-page-tabs-background-active': 'var(--background-default-grey-active)',
  '--csp-page-tabs-background-current-hover': 'var(--background-overlap-grey)',
}

const MARGE_COLONNE = 'clamp(0px, 100vw - 48rem, var(--csp-space-2))'
// 54rem is the width of the panel in the kit at 1440px, where the CV is read at 58%
const PANNEAU_ANCRE = 'clamp(42rem, 100vw - 66rem, 54rem)'

// The main column is one surface on the canvas beside the navigation, with the page header and the tab row on it;
// from 105rem the candidature panel is docked as a second surface beside it
const COLONNE_SURFACE: Valeurs = {
  '--csp-surface-shadow': 'var(--raised-shadow)',
  '--csp-chrome-background': 'transparent',
  '--csp-app-shell-main-background': SURFACE,
  '--csp-app-shell-main-shadow': 'var(--csp-surface-shadow)',
  '--csp-app-shell-main-inset': MARGE_COLONNE,
  // A transparent border, drawn by the forced colors mode between the navigation and the main column
  '--csp-app-shell-main-border-width': '1px',
  '--csp-app-shell-main-border-color': 'transparent',
  '--csp-page-tabs-inset': `calc(${MARGE_PAGE} - var(--csp-space-4))`,
  '--csp-kanban-bleed-inline-end': MARGE_PAGE,
  '--csp-panel-width-docked': PANNEAU_ANCRE,
  '--csp-panel-page-offset': `calc(${PANNEAU_ANCRE} + ${MARGE_COLONNE})`,
  '--csp-panel-background-docked': SURFACE,
  '--csp-panel-inset-docked': MARGE_COLONNE,
  '--csp-panel-border-width-docked': '0px',
  '--csp-panel-shadow-docked': 'var(--csp-surface-shadow)',
}

// The shadows of the DSFR barely show on a dark canvas: both surfaces take the border of the surface role
const COLONNE_SURFACE_SOMBRE: Valeurs = {
  '--csp-app-shell-main-border-color': 'var(--csp-surface-border-color)',
  '--csp-panel-border-width-docked': '1px',
}

export const SURFACE_CONTENU: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  {
    id: 'onglet-ouvert',
    nom: 'Surface ouverte par l’onglet',
    valeurs: { ...CANEVAS, ...SURFACE_OUVERTE },
    sombre: { ...CANEVAS_SOMBRE, ...SURFACE_OUVERTE_SOMBRE },
  },
  {
    id: 'colonne-surface',
    nom: 'Colonne principale en surface',
    valeurs: { ...CANEVAS, ...COLONNE_SURFACE },
    sombre: { ...CANEVAS_SOMBRE, ...COLONNE_SURFACE_SOMBRE },
  },
]
