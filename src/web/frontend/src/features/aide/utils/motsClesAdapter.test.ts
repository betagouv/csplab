import type { FaqEntree } from '../types'
import { describe, expect, it } from 'vitest'
import { createClassement, createMotsClesAdapter, MESSAGE_SANS_REPONSE } from './motsClesAdapter'

function entree(id: string, question: string, motsCles: string[]): FaqEntree {
  return { id, theme: 'Démarrer', question, reponse: `Réponse ${id}`, ou: `Où ${id}`, motsCles }
}

const ENTREES: FaqEntree[] = [
  entree('documents', 'Comment récupérer les pièces jointes ?', ['télécharger', 'CV']),
  entree('kanban-a', 'Première entrée sur les colonnes', ['kanban']),
  entree('kanban-b', 'Seconde entrée sur les colonnes', ['kanban']),
]

const SANS_REPONSE = { reponse: MESSAGE_SANS_REPONSE, entreeId: null }

describe('createClassement', () => {
  it('ranks every entry by decreasing score, title words above keywords', () => {
    const classer = createClassement([
      entree('aucun', 'Autre question', []),
      entree('mot-cle', 'Encore une question', ['fichier']),
      entree('titre', 'Où est le fichier ?', []),
    ])

    expect(classer('fichier').map(classee => [classee.entree.id, classee.score])).toEqual([
      ['titre', 3],
      ['mot-cle', 2],
      ['aucun', 0],
    ])
  })
})

describe('createMotsClesAdapter', () => {
  it('finds an entry on a keyword, ignoring case and accents', async () => {
    const adapter = createMotsClesAdapter(ENTREES)

    expect(await adapter.repondre('TELECHARGER un fichier')).toEqual({
      reponse: 'Réponse documents',
      entreeId: 'documents',
    })
  })

  it('answers with the fallback message when nothing matches', async () => {
    const adapter = createMotsClesAdapter(ENTREES)

    expect(await adapter.repondre('zzzz')).toEqual(SANS_REPONSE)
  })

  it('never answers on a tie', async () => {
    const adapter = createMotsClesAdapter(ENTREES)

    expect(await adapter.repondre('le kanban')).toEqual(SANS_REPONSE)
  })

  it('does not answer when the best entry leads by one point only', async () => {
    const adapter = createMotsClesAdapter([
      entree('titre', 'Où est le fichier ?', []),
      entree('mot-cle', 'Autre question', ['fichier']),
    ])

    expect(await adapter.repondre('fichier')).toEqual(SANS_REPONSE)
  })

  it('ignores a question made only of stop words', async () => {
    const adapter = createMotsClesAdapter(ENTREES)

    expect(await adapter.repondre('comment est-ce que')).toEqual(SANS_REPONSE)
  })

  it('matches a short keyword as a whole word only', async () => {
    const adapter = createMotsClesAdapter(ENTREES)

    expect((await adapter.repondre('mon CV')).entreeId).toBe('documents')
    expect((await adapter.repondre('la cvthèque')).entreeId).toBeNull()
  })

  it('finds the rights matrix in the real FAQ', async () => {
    const adapter = createMotsClesAdapter()

    expect((await adapter.repondre('matrice des droits')).entreeId).toBe('droits-qui-fait-quoi')
  })

  it('weighs title words over keywords in the real FAQ', async () => {
    const adapter = createMotsClesAdapter()

    expect((await adapter.repondre('RETIRER UN COLLEGUE QUI QUITTE')).entreeId).toBe('org-revoquer')
  })

  it('answers on a keyword that also appears in the title in the real FAQ', async () => {
    const adapter = createMotsClesAdapter()

    expect((await adapter.repondre('collègue')).entreeId).toBe('org-ajouter-membre')
  })
})
