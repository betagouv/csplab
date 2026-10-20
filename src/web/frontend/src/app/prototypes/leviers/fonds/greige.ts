import type { LevierOption, Valeurs } from '../options'
import type { FondsPlanche } from './planche'
import { EN_TETE_ET_ONGLETS } from './planche'

// The 6 px dot grid of the greige theme (styles/themes/greige.css), drawn as a halftone: the radius of each dot, up to
// 1.5 px, follows its place in the tile, so that the motif fades out towards the text. An SVG drawn as a background
// cannot read the CSS variables of the page: the colours are the hexadecimal values of the beige-gris-galet tokens of
// the DSFR named on each variant.
const PAS = 6
const RAYON = 1.5

// part gives the share of the full radius, from 0 to 1, of the dot centred at x, y
function trame(couleur: string, largeur: number, hauteur: number, part: (x: number, y: number) => number): string {
  const cercles: string[] = []
  for (let y = PAS / 2; y < hauteur; y += PAS) {
    for (let x = PAS / 2; x < largeur; x += PAS) {
      const rayon = RAYON * Math.max(0, part(x, y))
      if (rayon >= 0.3) {
        cercles.push(`<circle cx='${x}' cy='${y}' r='${rayon.toFixed(2)}'/>`)
      }
    }
  }
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='${largeur}' height='${hauteur}' fill='${couleur}'>${cercles.join('')}</svg>`
  return `url("data:image/svg+xml,${encodeURIComponent(svg)}")`
}

// Header: one row repeated down the surface, whose dots grow towards the end edge, where the actions are
const LONGUEUR_EN_TETE = 480

function trameEnTete(couleur: string): string {
  const image = trame(couleur, LONGUEUR_EN_TETE, PAS, x => (x / LONGUEUR_EN_TETE) ** 1.6)
  return `${image} right top / ${LONGUEUR_EN_TETE}px ${PAS}px repeat-y`
}

// Empty state: one column repeated across the surface, whose dots grow towards the top edge, in the top padding
const HAUTEUR_ETAT_VIDE = 40

function trameEtatVide(couleur: string): string {
  const image = trame(couleur, PAS, HAUTEUR_ETAT_VIDE, (_, y) => (1 - y / HAUTEUR_ETAT_VIDE) ** 1.6)
  return `${image} left top / ${PAS}px ${HAUTEUR_ETAT_VIDE}px repeat-x`
}

function aplat(couleur: string): string {
  return `linear-gradient(${couleur} 0 0)`
}

interface Variante {
  // Fill of the surface, none keeps the background of the surface
  fond?: string
  // Colour of the dots, as the hexadecimal value of a DSFR token
  points: string
}

// Light and dark values of each variant
interface Variantes {
  clair: Variante
  sombre: Variante
}

// Discreet: dots of --artwork-motif-beige-gris-galet (925-125, #eee4d9 and #2e2924) on the background of the surface
const DISCRETE: Variantes = {
  clair: { points: '#eee4d9' },
  sombre: { points: '#2e2924' },
}

// Classic: the same dots on the alt background of the family, --background-alt-beige-gris-galet (975-75)
const CLASSIQUE: Variantes = {
  clair: { fond: 'var(--background-alt-beige-gris-galet)', points: '#eee4d9' },
  sombre: { fond: 'var(--background-alt-beige-gris-galet)', points: '#2e2924' },
}

// Contrast: --background-action-high-beige-gris-galet, beige-gris-galet sun 407 (#6a6156), under dots darker than
// the fill, beige-gris-galet 850-200 in its dark value (#433829), which never lower the contrast of the white text. The
// dark theme keeps the light value of the token: its own value, moon 821, is a light beige that would outshine the
// whole screen.
const CONTRASTE: Variantes = {
  clair: { fond: 'var(--background-action-high-beige-gris-galet)', points: '#433829' },
  sombre: { fond: '#6a6156', points: '#433829' },
}

function calques(motif: string, fond?: string): string {
  return fond ? `${motif}, ${aplat(fond)}` : motif
}

// The page header takes the fill as the background of the chrome, which its tab row and the top bar of a phone share
function enTetePage({ fond, points }: Variante): Valeurs {
  const valeurs: Valeurs = {
    '--csp-page-header-backdrop': trameEnTete(points),
  }
  if (fond) {
    valeurs['--csp-chrome-background'] = fond
  }
  return valeurs
}

function enTetePanneau({ fond, points }: Variante): Valeurs {
  return { '--csp-drawer-header-backdrop': calques(trameEnTete(points), fond) }
}

function etatVide({ fond, points }: Variante): Valeurs {
  return { '--csp-empty-state-backdrop': calques(trameEtatVide(points), fond) }
}

// The tabs of the page lie on the chrome: on the classic fill, they take the hover and active states of that fill
const ONGLETS_CLASSIQUES: Valeurs = {
  '--csp-page-tabs-background-hover': 'var(--background-alt-beige-gris-galet-hover)',
  '--csp-page-tabs-background-active': 'var(--background-alt-beige-gris-galet-active)',
  '--csp-page-tabs-background-current-hover': 'var(--background-alt-beige-gris-galet-hover)',
}

// Background of the application: the grid of the greige theme without halftone, in the lightest step of the family,
// --artwork-background-beige-gris-galet (975-75), over the default background
const FOND_APPLICATION: Valeurs = {
  '--csp-canvas-backdrop': `radial-gradient(circle at ${PAS / 2}px ${PAS / 2}px, var(--artwork-background-beige-gris-galet) 0.9px, transparent 1.4px) 0 0 / ${PAS}px ${PAS}px repeat`,
}

// The neutral of the greige theme for the navigation and the kanban columns: the DSFR has no warm grey, and a quarter
// of beige-gris-galet in the grey of the same rank gives the warmth without a beige fill
const NEUTRE_RECHAUFFE: Valeurs = {
  '--background-alt-grey': 'color-mix(in oklab, var(--grey-975-75) 75%, var(--beige-gris-galet-950-100))',
  '--background-alt-grey-hover': 'color-mix(in oklab, var(--grey-975-75-hover) 75%, var(--beige-gris-galet-950-100-hover))',
  '--background-alt-grey-active': 'color-mix(in oklab, var(--grey-975-75-active) 75%, var(--beige-gris-galet-950-100-active))',
}

function toutes(variante: Variante): Valeurs {
  return { ...enTetePage(variante), ...enTetePanneau(variante), ...etatVide(variante) }
}

// Text on the contrast background: white in both themes, 6.1:1 on #6a6156
const TEXTE_CONTRASTE: Record<'clair' | 'sombre', Valeurs> = {
  clair: {
    '--text-title-grey': 'var(--text-inverted-grey)',
    '--text-default-grey': 'var(--text-inverted-grey)',
    '--text-mention-grey': 'var(--text-inverted-grey)',
    '--csp-empty-state-icon-color': 'var(--text-inverted-grey)',
    '--csp-page-header-border-color': 'transparent',
  },
  sombre: {
    '--text-default-grey': 'var(--text-title-grey)',
    '--text-mention-grey': 'var(--text-title-grey)',
    '--csp-empty-state-icon-color': 'var(--text-title-grey)',
    '--csp-page-header-border-color': 'transparent',
  },
}

// The contrast variant on the highlighted header of the home page, as the option would write it: the mechanism of the
// levers writes its values on the root element, where the white text would reach the whole application, so only the
// board shows it
function accueil({ fond, points }: Variante, texte: Valeurs, couleur: string): Valeurs {
  return {
    '--csp-page-header-backdrop-highlighted': trameEnTete(points),
    '--csp-page-header-background-highlighted': fond!,
    '--csp-page-header-color-highlighted': couleur,
    '--csp-page-header-subtitle-color-highlighted': couleur,
    ...texte,
  }
}

// Each surface in a variant of one of the options, for the board of the variants
export const PLANCHE_GREIGE: FondsPlanche = {
  accueil: {
    variante: 'contraste',
    usage: 'en-tête de l’accueil',
    valeurs: accueil(CONTRASTE.clair, TEXTE_CONTRASTE.clair, 'var(--text-inverted-grey)'),
    sombre: accueil(CONTRASTE.sombre, TEXTE_CONTRASTE.sombre, 'var(--text-title-grey)'),
  },
  page: {
    variante: 'classique',
    usage: 'en-tête des pages',
    valeurs: enTetePage(CLASSIQUE.clair),
    sombre: enTetePage(CLASSIQUE.sombre),
    cadre: EN_TETE_ET_ONGLETS,
  },
  panneau: { variante: 'discrete', usage: 'en-tête du panneau' },
  etatVide: { variante: 'discrete', usage: 'états vides', valeurs: etatVide(DISCRETE.clair), sombre: etatVide(DISCRETE.sombre) },
  application: { usage: 'fond de l’application, trame de points' },
}

export const GREIGE: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  {
    id: 'greige',
    nom: 'Greige classique',
    valeurs: { ...FOND_APPLICATION, ...NEUTRE_RECHAUFFE, ...toutes(CLASSIQUE.clair), ...ONGLETS_CLASSIQUES },
    sombre: toutes(CLASSIQUE.sombre),
  },
  {
    id: 'greige-discret',
    nom: 'Greige discret',
    valeurs: { ...FOND_APPLICATION, ...NEUTRE_RECHAUFFE, ...toutes(DISCRETE.clair) },
    sombre: toutes(DISCRETE.sombre),
  },
]
