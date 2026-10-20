import type { LevierOption, Valeurs } from '../options'

const MARGE_PAGE = 'var(--csp-page-container-padding-inline)'
// The page margin less the inline padding of a tab: the first tab starts there, and its label lines up with the title
const RETRAIT = `calc(${MARGE_PAGE} - var(--csp-space-4))`

// The tabs of the kit keep their look. From md, every horizontal rule of the main column and of the candidature panel
// runs from the first tab to the same distance from the right edge: the line under the tabs, the line under the title
// of a page without tabs, the top line of a table toolbar and the line above the stacked aside of the panel. A header
// followed by tabs has no line of its own. The frame of the tab panel takes the rest of the page margin, and the
// content keeps its column
const ALIGNES: Valeurs = {
  '--csp-page-container-frame-margin-inline': RETRAIT,
  '--csp-page-container-frame-padding-inline': 'var(--csp-space-4)',
  '--csp-page-header-border-width-tabs': '0px',
  '--csp-page-header-border-inset': RETRAIT,
  '--csp-table-toolbar-border-outset': 'var(--csp-space-4)',
  '--csp-panel-header-border-width-tabs': '0px',
  '--csp-panel-tabs-inset': RETRAIT,
  '--csp-panel-aside-inset': RETRAIT,
  // The close button lines up with the content of the drawer
  '--csp-drawer-close-bleed': '0',
  // Forced colors: only the active tab keeps its bottom border
  '--csp-tabs-trigger-border-bottom-color-forced': 'Canvas',
}

export const ONGLETS_ALIGNES: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  { id: 'onglets-alignes', nom: 'Onglets alignés', valeurs: ALIGNES },
]
