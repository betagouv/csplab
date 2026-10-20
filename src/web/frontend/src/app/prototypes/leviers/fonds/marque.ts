import type { LevierOption, Valeurs } from '../options'
import type { FondsPlanche, FondSurfaceDessinee } from './planche'
import { EN_TETE_SANS_ONGLETS } from './planche'

// The three circles of csplab-vertical-circles.svg: radius r, centres 1.5 r apart along the column, the middle circle
// the strongest. The column leans 30 degrees from the horizontal, top circle on the left, against the right edge of the
// surface, with the middle circle centred in its height.
interface Cercles {
  haut: string
  milieu: string
  bas: string
}

function cercle(x: string, y: string, rayon: string, couleur: string): string {
  return `radial-gradient(circle ${rayon} at ${x} ${y}, ${couleur} calc(${rayon} - 0.5px), transparent ${rayon}) no-repeat`
}

// The fade from the background keeps the start of the surface, where its text begins, clear of the circles
function motif({ haut, milieu, bas }: Cercles, rayon: string, fond: string): string {
  const x = (facteur: number) => `calc(100% - ${facteur} * ${rayon})`
  const y = (facteur: number) => `calc(50% + ${facteur} * ${rayon})`
  return [
    `linear-gradient(90deg, ${fond} 35%, transparent 75%) no-repeat`,
    // The strongest circle on top, as the darken blend of the identity backgrounds of aides-simplifiees shows it
    cercle(x(1.5), y(0), rayon, milieu),
    cercle(x(0.2), y(0.75), rayon, bas),
    cercle(x(2.8), y(-0.75), rayon, haut),
    `linear-gradient(${fond} 0 0)`,
  ].join(', ')
}

// Discreet variant: the three lightest blue France tints of the DSFR, for the large surfaces seen all day long. The middle one,
// blue-france-925-125, keeps the mention text at 4.5:1 in both themes, so the circles may pass under a text, on a phone
// for instance.
const DISCRETE: Cercles = {
  haut: 'var(--blue-france-975-75)',
  milieu: 'var(--blue-france-925-125)',
  bas: 'var(--blue-france-950-100)',
}

// Classic variant: the tints of the identity backgrounds of aides-simplifiees, blue-france-850-200 in the middle, for a
// surface seen now and then whose text keeps to the start
const CLASSIQUE: Cercles = {
  haut: 'var(--blue-france-950-100)',
  milieu: 'var(--blue-france-850-200)',
  bas: 'var(--blue-france-925-125)',
}

// A DSFR colour laid at partial opacity on blue France, as the circles of the section slide of the presentation theme
// are: the DSFR has no tint between blue France and its hover state
function voile(couleur: string, part: number, fond: string): string {
  return `color-mix(in srgb, var(${couleur}) ${part}%, ${fond})`
}

// Contrast variant: blue France with the circles of the section slide, light circles of low opacity. In the dark theme the
// DSFR turns its action background into a light blue; the surface keeps the dark blue France of the inverted text
// token, and the circles take the main blue, which both themes share.
const BLEU = 'var(--background-action-high-blue-france)'
const CONTRASTE: Cercles = {
  haut: voile('--blue-france-925-125', 14, BLEU),
  milieu: voile('--blue-france-main-525', 35, BLEU),
  bas: voile('--blue-france-925-125-active', 22, BLEU),
}
const BLEU_SOMBRE = 'var(--blue-france-975-sun-113)'
const CONTRASTE_SOMBRE: Cercles = {
  haut: voile('--blue-france-main-525', 14, BLEU_SOMBRE),
  milieu: voile('--blue-france-main-525', 35, BLEU_SOMBRE),
  bas: voile('--blue-france-main-525', 22, BLEU_SOMBRE),
}

const RAYON_EN_TETE = '7.5rem'
const RAYON_ETAT_VIDE = '5rem'

// Background of the application: the circles of the motif repeated as thin rings, 1.5 r apart in both directions. Each
// ring of the tile comes with its four neighbours, which cross its edges.
const RAYON_ANNEAU = 40
const PAS_ANNEAUX = RAYON_ANNEAU * 1.5

function anneaux(couleur: string): string {
  const anneau = (x: number, y: number) =>
    `radial-gradient(circle ${RAYON_ANNEAU}px at ${x}px ${y}px, transparent ${RAYON_ANNEAU - 1.5}px, ${couleur} ${RAYON_ANNEAU - 1}px, ${couleur} ${RAYON_ANNEAU}px, transparent ${RAYON_ANNEAU + 0.5}px) 0 0 / ${PAS_ANNEAUX}px ${PAS_ANNEAUX}px`
  const centre = PAS_ANNEAUX / 2
  return [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1]]
    .map(([dx, dy]) => anneau(centre + dx! * PAS_ANNEAUX, centre + dy! * PAS_ANNEAUX))
    .join(', ')
}

// Where each variant goes: the discreet one on the page headers, the header of the candidature panel and the empty
// states, the classic one on the header of the error pages, the contrast one on the header of the home page
const MARQUE_CLAIR: Valeurs = {
  '--csp-canvas-backdrop': anneaux('var(--blue-france-975-75)'),
  '--csp-page-header-backdrop': motif(DISCRETE, RAYON_EN_TETE, 'var(--csp-chrome-background)'),
  '--csp-panel-header-backdrop': motif(DISCRETE, RAYON_EN_TETE, 'var(--csp-panel-chrome-background)'),
  '--csp-empty-state-backdrop': motif(DISCRETE, RAYON_ETAT_VIDE, 'var(--background-default-grey)'),
  '--csp-empty-state-background': 'var(--background-default-grey)',
  '--csp-empty-state-frame-width': '1px',
  '--csp-error-page-header-backdrop': motif(CLASSIQUE, RAYON_EN_TETE, 'var(--csp-chrome-background)'),
  '--csp-page-header-backdrop-highlighted': motif(CONTRASTE, RAYON_EN_TETE, BLEU),
  '--csp-page-header-color-highlighted': 'var(--text-inverted-blue-france)',
  '--csp-page-header-subtitle-color-highlighted': 'var(--text-inverted-blue-france)',
}

const MARQUE_SOMBRE: Valeurs = {
  // On a dark background the blue of the lightest tint stands out more than on white: the rings take half of it
  '--csp-canvas-backdrop': anneaux('color-mix(in srgb, var(--blue-france-975-75) 50%, var(--csp-canvas-background))'),
  '--csp-page-header-backdrop-highlighted': motif(CONTRASTE_SOMBRE, RAYON_EN_TETE, BLEU_SOMBRE),
  '--csp-page-header-color-highlighted': 'var(--text-title-grey)',
  '--csp-page-header-subtitle-color-highlighted': 'var(--text-default-grey)',
}

export const MARQUE: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  { id: 'marque', nom: 'Motif de l’identité de csplab', valeurs: MARQUE_CLAIR, sombre: MARQUE_SOMBRE },
]

// Values of the option named by their keys
function parmi(valeurs: Valeurs, noms: `--${string}`[]): Valeurs {
  return Object.fromEntries(noms.map(nom => [nom, valeurs[nom]!]))
}

const ACCUEIL: `--${string}`[] = [
  '--csp-page-header-backdrop-highlighted',
  '--csp-page-header-color-highlighted',
  '--csp-page-header-subtitle-color-highlighted',
]

// Each surface in the variant that the option gives it, for the board of the variants. The classic variant serves the
// header of the error pages, whose title stands alone.
export const PLANCHE_MARQUE: FondsPlanche = {
  accueil: { variante: 'contraste', usage: 'en-tête de l’accueil', valeurs: parmi(MARQUE_CLAIR, ACCUEIL), sombre: parmi(MARQUE_SOMBRE, ACCUEIL) },
  page: {
    variante: 'classique',
    usage: 'en-tête des pages d’erreur',
    valeurs: { '--csp-page-header-backdrop': MARQUE_CLAIR['--csp-error-page-header-backdrop']! },
    cadre: EN_TETE_SANS_ONGLETS,
  },
  panneau: { variante: 'discrete', usage: 'en-tête du panneau' },
  etatVide: {
    variante: 'discrete',
    usage: 'états vides',
    valeurs: parmi(MARQUE_CLAIR, ['--csp-empty-state-backdrop', '--csp-empty-state-background', '--csp-empty-state-frame-width']),
  },
  application: { usage: 'fond de l’application, anneaux' },
}

// The page header of the working screens, in the discreet variant that the option gives it, for the comparison of the
// tracks
export const EN_TETE_DISCRET: FondSurfaceDessinee = {
  variante: 'discrete',
  usage: 'en-tête des pages',
  valeurs: parmi(MARQUE_CLAIR, ['--csp-page-header-backdrop']),
}
