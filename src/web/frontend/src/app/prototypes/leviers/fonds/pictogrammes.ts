import type { LevierOption, Valeurs } from '../options'
import type { FondsPlanche, FondSurfaceDessinee } from './planche'
import { EN_TETE_ET_ONGLETS } from './planche'

// A DSFR pictogram of the subject of the page sits in the page header and takes the place of the icon of an empty
// state. Its three layers take blue France tones of the palette, in three variants of the same treatment, as the
// brand backgrounds of aides-simplifiées: discrète and classique on the background of the page, contraste on blue
// France.

type Couleurs = [majeure: string, mineure: string, decorative: string]

// One pale tone for the lines, a paler one for the dots
const DISCRETE: Couleurs = [
  'var(--artwork-motif-blue-france)',
  'var(--artwork-motif-blue-france)',
  'var(--artwork-background-blue-france)',
]

// A pale tone for the lines of the major layer, the -main tone of blue France for those of the minor layer
const CLASSIQUE: Couleurs = [
  'var(--border-action-low-blue-france)',
  'var(--artwork-minor-blue-france)',
  'var(--artwork-decorative-blue-france)',
]

// The -main tone of blue France, between the background and the text of the contrast variant
const CONTRASTE_PICTOGRAMME: Couleurs = [
  'var(--border-default-blue-france)',
  'var(--border-default-blue-france)',
  'var(--border-default-blue-france)',
]

function pictogrammes([majeure, mineure, decorative]: Couleurs): Valeurs {
  return {
    '--csp-pictogram-major-color': majeure,
    '--csp-pictogram-minor-color': mineure,
    '--csp-pictogram-decorative-color': decorative,
  }
}

function enTete([majeure, mineure, decorative]: Couleurs): Valeurs {
  return {
    '--csp-page-header-pictogram-major-color': majeure,
    '--csp-page-header-pictogram-minor-color': mineure,
    '--csp-page-header-pictogram-decorative-color': decorative,
  }
}

const [majeure, mineure, decorative] = CONTRASTE_PICTOGRAMME

// The header of the home page on blue France
const CONTRASTE: Valeurs = {
  '--csp-page-header-background-highlighted': 'var(--background-action-high-blue-france)',
  '--csp-page-header-color-highlighted': 'var(--text-inverted-blue-france)',
  '--csp-page-header-subtitle-color-highlighted': 'var(--text-inverted-blue-france)',
  '--csp-page-header-pictogram-major-color-highlighted': majeure,
  '--csp-page-header-pictogram-minor-color-highlighted': mineure,
  '--csp-page-header-pictogram-decorative-color-highlighted': decorative,
}

// In the dark theme the action background of blue France turns light: the header keeps the blue France of the light
// theme, which the DSFR gives in the dark theme to the inverted text token only, with the title colour of the theme
const CONTRASTE_SOMBRE: Valeurs = {
  '--csp-page-header-background-highlighted': 'var(--text-inverted-blue-france)',
  '--csp-page-header-color-highlighted': 'var(--text-title-grey)',
  '--csp-page-header-subtitle-color-highlighted': 'var(--text-title-grey)',
}

// 176 px, near the 180 px that the DSFR gives as the largest size: the pictogram starts at the top of the breadcrumb row
// and the line under the header cuts its bottom
const RANGEES_AU_DESSUS = 'var(--csp-page-header-breadcrumb-height) + var(--csp-page-header-breadcrumb-gap)'
const EN_TETE: Valeurs = {
  '--csp-page-header-pictogram-display': 'block',
  '--csp-page-header-pictogram-size': '11rem',
  '--csp-page-header-pictogram-height': `calc(${RANGEES_AU_DESSUS} + var(--csp-page-header-title-height) + var(--csp-page-header-subtitle-gap) + var(--csp-page-header-subtitle-height) + var(--csp-page-header-padding-bottom))`,
  '--csp-page-header-pictogram-margin-block': `calc(-1 * (${RANGEES_AU_DESSUS})) calc(-1 * var(--csp-page-header-padding-bottom))`,
}

// 64 px in place of the 24 px icon
const ETATS_VIDES: Valeurs = {
  '--csp-empty-state-pictogram-display': 'block',
  '--csp-empty-state-pictogram-size': '4rem',
  '--csp-empty-state-icon-display-with-pictogram': 'none',
}

export const PICTOGRAMMES: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  // Both options write the pictograms background of styles/themes/backdrops.css, that the DSFR theme takes as well
  {
    id: 'pictogrammes-discret',
    nom: 'Pictogrammes, en-têtes discrets',
    valeurs: enTete(DISCRETE),
    attributs: { 'data-csp-backdrop': 'pictograms' },
  },
  {
    id: 'pictogrammes',
    nom: 'Pictogrammes, en-têtes classiques',
    valeurs: {},
    attributs: { 'data-csp-backdrop': 'pictograms' },
  },
]

// Each surface in the variant that the option with classic headers gives it, for the board of the variants
export const PLANCHE_PICTOGRAMMES: FondsPlanche = {
  accueil: { variante: 'contraste', usage: 'en-tête de l’accueil', valeurs: { ...EN_TETE, ...CONTRASTE }, sombre: { ...EN_TETE, ...CONTRASTE, ...CONTRASTE_SOMBRE } },
  page: { variante: 'classique', usage: 'en-tête des pages', valeurs: { ...EN_TETE, ...enTete(CLASSIQUE) }, cadre: EN_TETE_ET_ONGLETS },
  panneau: { usage: 'en-tête du panneau, sans pictogramme' },
  etatVide: { variante: 'classique', usage: 'états vides', valeurs: { ...ETATS_VIDES, ...pictogrammes(CLASSIQUE) } },
  application: { variante: 'discrete', usage: 'fond de l’application, points du pictogramme' },
}

// The empty states in the discrete variant, which no option gives them, for the comparison of the tracks in one variant
export const ETAT_VIDE_DISCRET: FondSurfaceDessinee = {
  variante: 'discrete',
  usage: 'états vides',
  valeurs: { ...ETATS_VIDES, ...pictogrammes(DISCRETE) },
}
