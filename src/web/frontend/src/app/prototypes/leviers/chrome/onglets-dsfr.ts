import type { LevierOption, Valeurs } from '../options'

// Tab component of the DSFR 1.14: framed triggers on the low blue France background, the current one on the default
// background with a 2px top line, 1rem bold labels, 0.5rem padding and 0.25rem margin on each side of a trigger, a
// focus ring 2px outside the trigger in the 4px that the list keeps around its triggers
const ONGLETS: Valeurs = {
  '--csp-tabs-framed': '1',
  '--csp-tabs-gap': 'var(--csp-space-2)',
  '--csp-tabs-focus-offset': '2px',
  '--csp-tabs-underline-width': '0px',
  '--csp-tabs-overline-width': '2px',
  '--csp-tabs-trigger-padding-block': 'var(--csp-space-2)',
  '--csp-tabs-trigger-size': 'var(--csp-font-size-md)',
  '--csp-tabs-trigger-line-height': '1.5rem',
  '--csp-tabs-trigger-weight': 'var(--csp-font-weight-bold)',
  '--csp-tabs-trigger-background': 'var(--background-action-low-blue-france)',
  '--csp-tabs-trigger-background-hover': 'var(--background-action-low-blue-france-hover)',
  '--csp-tabs-trigger-background-active': 'var(--background-action-low-blue-france-active)',
  '--csp-tabs-trigger-background-current': 'var(--background-default-grey)',
  '--csp-tabs-trigger-background-disabled': 'var(--background-disabled-grey)',
  // Colour and opacity of the shadow that the DSFR script draws on an overflowing list
  '--csp-tabs-overflow-shadow-color': 'rgb(22 22 22 / 80%)',
  // Forced colours: the current trigger opens onto its panel and takes the highlight colour, as in the DSFR
  '--csp-tabs-trigger-border-bottom-color-current-forced': 'Canvas',
  '--csp-tabs-trigger-color-current-forced': 'Highlight',
}

const ONGLETS_SOMBRE: Valeurs = {
  '--csp-tabs-overflow-shadow-color': '#161616',
}

// The frame of the tab panel starts under the title, at the page padding; inside it, the 2rem padding of the DSFR
// panel aligns the content with the label of the first tab, and the kanban scrolls up to the side lines of the frame
const CADRE: Valeurs = {
  '--csp-page-container-frame-margin-inline': 'var(--csp-page-container-padding-inline)',
  '--csp-page-container-frame-margin-bottom': 'var(--csp-page-content-padding-block)',
  '--csp-page-container-frame-padding': 'var(--csp-space-8)',
  '--csp-region-border-color': 'transparent',
  '--csp-region-border-color-drop': 'var(--border-default-grey)',
  '--csp-kanban-scroll-to-edge': '1',
}

// In the dark theme the drawer lies on the overlap background, lighter than the current tab: the panel of the
// candidature takes the default background of the current tab
const PANNEAU_SOMBRE: Valeurs = {
  '--csp-panel-background': 'var(--background-default-grey)',
}

const BLANC = 'var(--background-default-grey)'

// The frame stays open, without sides or bottom: from md, the line under the tabs and the top line of a table toolbar
// run from the first tab to the same distance from the right edge, the content keeps the column of the title, and the
// 2rem padding of the DSFR panel above and below
const FILET_CONTENU: Valeurs = {
  '--csp-page-container-frame-closed': '0',
  '--csp-page-container-frame-margin-inline': 'calc(var(--csp-page-container-padding-inline) - var(--csp-space-4))',
  '--csp-page-container-frame-margin-bottom': '0px',
  '--csp-page-container-frame-padding-inline': 'var(--csp-space-4)',
  '--csp-table-toolbar-border-outset': 'var(--csp-space-4)',
}

export const ONGLETS_DSFR: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  {
    id: 'cadre-fond-blanc',
    nom: 'Onglets du DSFR, cadre sur fond blanc',
    valeurs: { ...ONGLETS, ...CADRE },
    sombre: { ...ONGLETS_SOMBRE, ...PANNEAU_SOMBRE },
  },
  {
    id: 'filet-contenu',
    nom: 'Onglets du DSFR, filet le long du contenu',
    valeurs: { ...ONGLETS, ...CADRE, ...FILET_CONTENU },
    sombre: { ...ONGLETS_SOMBRE, ...PANNEAU_SOMBRE },
  },
  {
    id: 'cadre-fond-gris',
    nom: 'Onglets du DSFR, cadre blanc sur fond gris',
    valeurs: {
      ...ONGLETS,
      ...CADRE,
      '--csp-canvas-background': 'var(--background-alt-grey)',
      '--csp-page-container-frame-background': BLANC,
      '--csp-page-container-background': BLANC,
      '--csp-panel-background': BLANC,
      '--csp-panel-chrome-background': 'var(--background-alt-grey)',
    },
    // In the dark theme the alternative grey is darker than the overlap background of the drawer, which keeps it
    sombre: { ...ONGLETS_SOMBRE, '--csp-panel-chrome-background': 'var(--background-overlap-grey)' },
  },
]
