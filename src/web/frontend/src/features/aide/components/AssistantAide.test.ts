import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { FAQ_ENTREES } from '../constants/faq'
import AssistantAide from './AssistantAide.vue'

function texteAffiche(texte: string): string {
  return texte.replace(/\s+/g, ' ').trim()
}

describe('assistantAide', () => {
  it('shows the experimental notice', () => {
    render(AssistantAide, { props: { pending: false } })

    expect(screen.getByText('Assistant expérimental — réponses issues de la FAQ')).toBeInTheDocument()
  })

  it('shows the closest entry with its answer and location', () => {
    const entree = FAQ_ENTREES.find(e => e.id === 'droits-qui-fait-quoi')!
    render(AssistantAide, {
      props: { pending: false, reponse: { reponse: entree.reponse, entreeId: entree.id } },
    })

    expect(screen.getByText('Entrée la plus proche')).toBeInTheDocument()
    expect(screen.getByText(entree.question)).toBeInTheDocument()
    expect(screen.getByText(texteAffiche(entree.reponse))).toBeInTheDocument()
    expect(screen.getByText(entree.ou)).toHaveTextContent(`Où : ${entree.ou}`)
  })

  it('shows the message alone when no entry matches', () => {
    render(AssistantAide, { props: { pending: false, reponse: { reponse: 'Aucune réponse trouvée', entreeId: null } } })

    expect(screen.getByText('Aucune réponse trouvée')).toBeInTheDocument()
    expect(screen.queryByText('Entrée la plus proche')).not.toBeInTheDocument()
    expect(screen.queryByText('Où :')).not.toBeInTheDocument()
  })

  it('shows a loading state while the assistant is answering', () => {
    render(AssistantAide, { props: { pending: true } })

    expect(screen.getByRole('status', { name: 'L\'assistant cherche une réponse' })).toBeInTheDocument()
  })

  it('shows an error when the assistant fails', () => {
    render(AssistantAide, { props: { pending: false, error: new Error('indisponible') } })

    expect(screen.getByRole('alert')).toHaveTextContent('L\'assistant n\'a pas pu répondre. Réessayez.')
  })
})
