import type { LevierOption } from '../options'

// The discreet radii of styles/themes/shapes.css, that the DSFR and greige themes take as well: every element held or
// touched takes the radius of the DSFR fields, a large container one step more, an element inset in a smaller gap than
// its container's radius one step less
export const DISCRETS: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  { id: 'discrets', nom: 'Rayons discrets, 2, 4 et 6 px', valeurs: {}, attributs: { 'data-csp-shape': 'discreet' } },
]
