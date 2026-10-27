import type { LevierOption } from '../options'

// The marked radii of styles/themes/shapes.css: an indicator, a control, a surface, a region, from 4 to 16 px
export const RAYONS_AFFIRMES: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  { id: 'affirmes', nom: 'Rayons affirmés par rôle, 4, 6, 10 et 16 px', valeurs: {}, attributs: { 'data-csp-shape': 'marked' } },
]
