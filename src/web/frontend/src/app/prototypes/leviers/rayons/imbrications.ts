import type { DeckInterfaceCadre } from '../../DeckInterface.vue'

// The board of nested radii lays each case on a stage of fixed size, four per row, so that the comparison frames the
// same part of each case in every option
export const SCENE = { largeur: 320, hauteur: 200, ecart: 24, marge: 32, legende: 32 }

export interface Imbrication {
  id: string
  legende: string
  // Part of the stage that the comparison enlarges: whole controls and whole lines of text, with a margin
  zone: DeckInterfaceCadre
}

export const IMBRICATIONS: Imbrication[] = [
  { id: 'colonne', legende: 'Carte dans une colonne', zone: { x: 8, y: 8, width: 204, height: 108 } },
  { id: 'carte', legende: 'Boutons et case dans une carte', zone: { x: 8, y: 78, width: 120, height: 114 } },
  { id: 'menu', legende: 'Élément d’un menu ouvert', zone: { x: 8, y: 12, width: 196, height: 128 } },
  { id: 'recherche', legende: 'Champ et bouton accolés de la recherche', zone: { x: 8, y: 72, width: 176, height: 56 } },
  { id: 'segmente', legende: 'Segment survolé d’un contrôle segmenté', zone: { x: 8, y: 72, width: 240, height: 56 } },
  { id: 'onglet', legende: 'Onglet survolé sur son contenu', zone: { x: 8, y: 8, width: 144, height: 62 } },
  { id: 'focus', legende: 'Focus clavier d’un bouton', zone: { x: 8, y: 70, width: 104, height: 60 } },
]

// Part of the board, in its 1440 x 900 window, that shows the case at this index
export function cadreDe(index: number): DeckInterfaceCadre {
  const { largeur, hauteur, ecart, marge, legende } = SCENE
  const colonne = index % 4
  const rangee = Math.floor(index / 4)
  const { zone } = IMBRICATIONS[index]!
  return {
    ...zone,
    x: marge + colonne * (largeur + ecart) + zone.x,
    y: marge + rangee * (legende + hauteur + ecart) + legende + zone.y,
  }
}

// The dialog that adds a step, in its 1440 x 900 window: right end of the field, the add button and the bottom right
// corner of the dialog, down to its border
export const CHAMP_DU_DIALOGUE: DeckInterfaceCadre = { x: 790, y: 432, width: 122, height: 127 }
