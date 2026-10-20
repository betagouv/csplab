import type { LevierOption } from '../options'

// The radius of the DSFR fields, badges, checkboxes and segmented control, and the steps on each side of it
const INTERIEUR = '0.125rem'
const BASE = '0.25rem'
const CONTENEUR = '0.375rem'

// Every element held or touched takes the radius of the DSFR fields. A large container takes one step more, and an
// element inset in a smaller gap than its container's radius takes the indicator radius. Messages with a side bar
// keep square corners, like the alerts of the DSFR
export const DISCRETS: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  {
    id: 'discrets',
    nom: 'Rayons discrets, 2, 4 et 6 px',
    valeurs: {
      '--csp-indicator-radius': INTERIEUR,
      '--csp-action-radius': BASE,
      '--csp-nav-control-radius': 'var(--csp-action-radius)',
      '--csp-field-radius': BASE,
      '--csp-surface-radius': BASE,
      '--csp-frame-radius': 'var(--csp-surface-radius)',
      '--csp-overlap-radius': BASE,
      '--csp-region-radius': CONTENEUR,
      '--csp-lifted-radius': CONTENEUR,
      '--csp-message-radius': '0',
      '--csp-menu-item-radius': 'var(--csp-indicator-radius)',
      '--csp-segmented-highlight-radius': 'var(--csp-indicator-radius)',
      // The category accent keeps its width up to the corners of a column
      '--csp-kanban-column-accent-radius': 'var(--csp-category-accent-width)',
    },
  },
]
