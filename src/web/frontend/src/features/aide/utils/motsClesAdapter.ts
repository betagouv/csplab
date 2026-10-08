import type { AssistantAdapter, FaqEntree } from '../types'
import { normalizeSearchText } from '@/utils/search'
import { FAQ_ENTREES } from '../constants/faq'

export const POIDS_TITRE = 3
export const POIDS_MOT_CLE = 2
export const MARGE_MINIMUM = 2

export const MESSAGE_SANS_REPONSE = 'Aucune entrée ne se détache, parcourez les entrées ci-dessous.'

const LONGUEUR_MINIMUM_MOT = 4
const MOTS_VIDES = new Set([
  'comment',
  'pourquoi',
  'quand',
  'quel',
  'quelle',
  'quels',
  'quelles',
  'dans',
  'pour',
  'avec',
  'sans',
  'cette',
  'votre',
  'vous',
  'nous',
  'leur',
])

export interface EntreeClassee {
  entree: FaqEntree
  score: number
}

function decouperEnMots(texte: string): string[] {
  return normalizeSearchText(texte).split(/[^\p{L}\p{N}]+/u).filter(Boolean)
}

export function createClassement(entrees: readonly FaqEntree[] = FAQ_ENTREES) {
  const index = entrees.map(entree => ({
    entree,
    motsTitre: new Set(decouperEnMots(entree.question)),
    motsCles: entree.motsCles.map(motCle => ` ${decouperEnMots(motCle).join(' ')} `),
  }))

  return function classer(question: string): EntreeClassee[] {
    const motsQuestion = decouperEnMots(question)
    const questionBornee = ` ${motsQuestion.join(' ')} `
    const motsSignificatifs = [...new Set(motsQuestion.filter(
      mot => mot.length >= LONGUEUR_MINIMUM_MOT && !MOTS_VIDES.has(mot),
    ))]

    return index
      .map(({ entree, motsTitre, motsCles }) => ({
        entree,
        score: POIDS_TITRE * motsSignificatifs.filter(mot => motsTitre.has(mot)).length
          + POIDS_MOT_CLE * motsCles.filter(motCle => questionBornee.includes(motCle)).length,
      }))
      .sort((a, b) => b.score - a.score)
  }
}

export function createMotsClesAdapter(entrees: readonly FaqEntree[] = FAQ_ENTREES): AssistantAdapter {
  const classer = createClassement(entrees)

  return {
    async repondre(question) {
      const [meilleure, deuxieme] = classer(question)
      if (!meilleure) {
        return { reponse: MESSAGE_SANS_REPONSE, entreeId: null }
      }
      const marge = meilleure.score - (deuxieme?.score ?? 0)
      if (marge < MARGE_MINIMUM) {
        return { reponse: MESSAGE_SANS_REPONSE, entreeId: null }
      }
      return { reponse: meilleure.entree.reponse, entreeId: meilleure.entree.id }
    },
  }
}
