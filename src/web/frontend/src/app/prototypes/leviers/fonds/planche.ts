import type { DeckInterfaceCadre } from '../../DeckInterface.vue'
import type { Valeurs } from '../options'

export type FondVariante = 'discrete' | 'classique' | 'contraste'

const VARIANTES: Record<FondVariante, string> = {
  discrete: 'Discrète',
  classique: 'Classique',
  contraste: 'Contraste',
}

// A surface of the board: the variant that the track gives it, if any, and the place of the application where it serves
export interface FondSurface {
  variante?: FondVariante
  usage: string
}

// A surface that the board draws itself, with the values of its variant
export interface FondSurfaceDessinee extends FondSurface {
  valeurs: Valeurs
  // Values of the dark theme, in place of valeurs
  sombre?: Valeurs
}

// A page header that the board of the variants frames in a screen of the track, and that the comparison of the tracks
// draws itself
export interface FondEnTete extends FondSurfaceDessinee {
  // Part of the screen, in its 1440 x 900 window
  cadre: DeckInterfaceCadre
}

// Page header of a screen with tabs, down to the line under the tabs, with a margin
export const EN_TETE_ET_ONGLETS: DeckInterfaceCadre = { x: 257, y: 0, width: 1183, height: 206 }
// Page header of a screen without tabs, such as an error page, down to its line, with a margin
export const EN_TETE_SANS_ONGLETS: DeckInterfaceCadre = { x: 257, y: 0, width: 1183, height: 161 }

// The surfaces of a track, in the order of the board: home page header, page header, panel header, empty state and
// background of the application. The page header, the panel header and the background come from the screens of the
// track.
export interface FondsPlanche {
  accueil: FondSurfaceDessinee
  page: FondEnTete
  panneau: FondSurface
  etatVide: FondSurfaceDessinee
  application: FondSurface
}

export function legende({ variante, usage }: FondSurface): string {
  return variante ? `${VARIANTES[variante]}, ${usage}` : usage.charAt(0).toUpperCase() + usage.slice(1)
}

export function nomDeVariante(variante: FondVariante): string {
  return `Variante ${VARIANTES[variante].toLowerCase()}`
}

export function valeursDe(surface: FondSurfaceDessinee, sombre: boolean): Valeurs {
  return (sombre && surface.sombre) || surface.valeurs
}
