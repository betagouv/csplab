import type { LevierOption, Valeurs } from '../options'
import type { FondsPlanche } from './planche'
import { EN_TETE_ET_ONGLETS } from './planche'

// Grain of the page background: fractal noise in specks of mid grey, #808080, which darken a light background and
// lighten a dark one by the same amount, so that one image serves both themes. An SVG image cannot read a CSS variable,
// so the grey is written in the matrix. The fixed attachment lines up the grain drawn by the page header with the
// grain of the page around it.
const GRAIN_SVG = `<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='g' x='0' y='0' width='100%' height='100%' color-interpolation-filters='sRGB'><feTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.5 0 0 0 0 0.5 0 0 0 0 0.5 0.3 0 0 0 -0.12'/></filter><rect width='100%' height='100%' filter='url(#g)'/></svg>`
const GRAIN = `url("data:image/svg+xml,${encodeURIComponent(GRAIN_SVG)}") 0 0 / 200px 200px repeat fixed`

interface Teintes {
  // Light on the end corner, where the actions are
  lumiere: string
  // Tint that rises towards the end edge, under no text
  rampe?: string
  // Fill under the text, the page background unless the variant fills the surface
  fond?: string
  // Where the light is half gone, closer to the corner on a dark fill, where a light blue stands out more
  demi?: string
}

// One motif in three strengths, as the brand backgrounds of aides-simplifiees: discrete for the surfaces next to the
// working content, classic for the page header, contrast for a surface that stands out, such as the home page
const DISCRETE: Teintes = { lumiere: 'var(--blue-france-950-100)', rampe: 'var(--blue-cumulus-975-75)' }
const CLASSIQUE: Teintes = { lumiere: 'var(--blue-france-925-125)', rampe: 'var(--blue-cumulus-950-100)' }
const CONTRASTE: Teintes = {
  lumiere: 'var(--blue-france-main-525)',
  demi: '12%',
  fond: 'var(--background-action-high-blue-france)',
}
// The DSFR turns blue France 113 into a light blue in the dark theme; blue-france-975-sun-113 keeps it dark
const CONTRASTE_SOMBRE: Teintes = {
  ...CONTRASTE,
  fond: 'var(--blue-france-975-sun-113)',
}

function calque(image: string): string {
  return `${image} 0 0 / 100% 100% no-repeat`
}

// The light keeps a size in rem, so that it keeps its shape from a phone to a wide screen, and the start of the
// surface, where the title is, keeps the plain fill
function degrade({ lumiere, rampe, demi = '50%' }: Teintes): string[] {
  const lueur = calque(`radial-gradient(min(40rem, 60vw) 10rem at 100% 0%, ${lumiere}, ${demi}, transparent)`)
  return rampe ? [lueur, calque(`linear-gradient(90deg, transparent 35%, ${rampe})`)] : [lueur]
}

// A header laid on the page: the grain of the page over the gradient, over an opaque fill
function enTeteDePage(teintes: Teintes): string {
  const fond = teintes.fond ?? 'var(--csp-canvas-background)'
  return [GRAIN, ...degrade(teintes), calque(`linear-gradient(${fond}, ${fond})`)].join(', ')
}

// Empty state: a light behind the icon and the title that fades out before the edges, so that the empty state does not
// read as a box
function etatVide({ lumiere }: Teintes): string {
  return calque(`radial-gradient(closest-side, ${lumiere}, transparent)`)
}

function couleursDuTexte(titre: string, sousTitre: string): Valeurs {
  return {
    '--csp-page-header-color-highlighted': titre,
    '--csp-page-header-subtitle-color-highlighted': sousTitre,
  }
}

const TEXTE_CONTRASTE = couleursDuTexte('var(--text-inverted-blue-france)', 'var(--text-inverted-blue-france)')
const TEXTE_CONTRASTE_SOMBRE = couleursDuTexte('var(--text-title-grey)', 'var(--text-default-grey)')

// The option writes the gradient background of styles/themes/backdrops.css, that the DSFR theme takes as well
export const DEGRADE: LevierOption[] = [
  { id: 'kit', nom: 'Aujourd’hui', valeurs: {} },
  { id: 'degrade', nom: 'Dégradé et grain', valeurs: {}, attributs: { 'data-csp-backdrop': 'gradient' } },
]

// Each surface in the strength that the option gives it, for the board of the variants
export const PLANCHE_DEGRADE: FondsPlanche = {
  accueil: {
    variante: 'contraste',
    usage: 'en-tête de l’accueil',
    valeurs: { '--csp-page-header-backdrop-highlighted': enTeteDePage(CONTRASTE), ...TEXTE_CONTRASTE },
    sombre: { '--csp-page-header-backdrop-highlighted': enTeteDePage(CONTRASTE_SOMBRE), ...TEXTE_CONTRASTE_SOMBRE },
  },
  page: {
    variante: 'classique',
    usage: 'en-tête des pages',
    valeurs: { '--csp-page-header-backdrop': enTeteDePage(CLASSIQUE) },
    cadre: EN_TETE_ET_ONGLETS,
  },
  panneau: { variante: 'discrete', usage: 'en-tête du panneau' },
  etatVide: { variante: 'discrete', usage: 'états vides', valeurs: { '--csp-empty-state-backdrop': etatVide(DISCRETE) } },
  application: { usage: 'fond de l’application, grain' },
}
