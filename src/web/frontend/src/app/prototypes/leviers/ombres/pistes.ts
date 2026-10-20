import type { LevierOption, Valeurs } from '../options'
import { SANS_OMBRE } from '../options'

const TRANSPARENT = 'transparent'

// In dark mode a shadow barely shows on a dark background: as in the DSFR, each layer takes a grey one step lighter
// than what holds it. A card takes the overlap grey over the kanban column, the panel the lifted grey of the DSFR, so
// that a menu opened over it stands out; the hover grey is the one of the kit in light mode.
const SOMBRE: Valeurs = {
  '--csp-raised-background': 'var(--background-overlap-grey)',
  '--csp-raised-background-hover': 'var(--background-default-grey-hover)',
  '--csp-drawer-background': 'var(--background-lifted-grey)',
}

// No shadow: a 1 px rule outlines what one grabs and what floats, and the scrim darkens the page under a modal layer
const A_PLAT: LevierOption = {
  id: 'a-plat',
  nom: 'À plat',
  valeurs: {
    '--csp-raised-shadow': SANS_OMBRE,
    '--csp-raised-shadow-hover': SANS_OMBRE,
    '--csp-raised-shadow-drag': SANS_OMBRE,
    '--csp-overlap-shadow': SANS_OMBRE,
    '--csp-lifted-shadow': SANS_OMBRE,
  },
  sombre: SOMBRE,
}

// The three shadows of the DSFR, one per layer, which keep their value whatever the state, as the card and the modal
// of the DSFR do. The shadow replaces the rule around cards and menus, as on the card with shadow and the menu of the
// DSFR; the panel and the dialogs keep theirs, since a 9 px shadow does not outline a layer the height of the screen.
// The DSFR darkens the shadows in dark mode.
const DSFR: LevierOption = {
  id: 'dsfr',
  nom: 'Ombres du DSFR',
  valeurs: {
    '--csp-raised-shadow': 'var(--raised-shadow)',
    '--csp-raised-shadow-hover': 'var(--raised-shadow)',
    '--csp-raised-shadow-drag': 'var(--raised-shadow)',
    '--csp-raised-border-color': TRANSPARENT,
    '--csp-overlap-shadow': 'var(--overlap-shadow)',
    '--csp-overlap-border-color': TRANSPARENT,
    '--csp-lifted-shadow': 'var(--lifted-shadow)',
  },
  sombre: SOMBRE,
}

// Share of the DSFR shadow colour, 16 % opaque in light mode and 32 % in dark mode
function teinte(part: number): string {
  return `color-mix(in srgb, var(--shadow-color) ${part}%, transparent)`
}

// Two layers, a close one that sets the contact and a wide diffuse one that sets the height, in the colour of the DSFR
// shadows: the DSFR shadows have a single short layer, which cannot draw a diffuse height. The card rises on hover to
// the height of a menu, and the place it leaves during a drag lies flat.
const PROCHE = `0 1px 2px ${teinte(40)}`
const SOULEVEE = `${PROCHE}, 0 10px 24px -6px ${teinte(100)}`

const DOUCES: LevierOption = {
  id: 'douces',
  nom: 'Ombres douces',
  valeurs: {
    '--csp-raised-shadow': `${PROCHE}, 0 2px 6px -2px ${teinte(40)}`,
    '--csp-raised-shadow-hover': SOULEVEE,
    '--csp-raised-shadow-drag': SANS_OMBRE,
    '--csp-overlap-shadow': SOULEVEE,
    '--csp-lifted-shadow': `0 8px 16px -4px ${teinte(60)}, 0 24px 48px -12px ${teinte(100)}`,
  },
  sombre: SOMBRE,
}

export const OMBRES: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  A_PLAT,
  DSFR,
  DOUCES,
]
