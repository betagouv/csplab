import { screen, waitFor } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { renderWithApp, setupUser } from '@/test/render'
import AideView from './AideView.vue'

function themeTitles(): string[] {
  return screen.getAllByRole('heading', { level: 2 }).map(heading => heading.textContent?.trim() ?? '')
}

describe('aideView', () => {
  it('lists the eight themes in the order of the FAQ', async () => {
    await renderWithApp(AideView, { route: '/aide' })

    expect(themeTitles()).toEqual([
      'Démarrer',
      'Candidatures',
      'Étapes',
      'Recrutements',
      'Organisme et équipe',
      'Notes, documents, messages',
      'Droits et rôles',
      'Problèmes courants',
    ])
  })

  it('lists every entry of the FAQ, closed', async () => {
    await renderWithApp(AideView, { route: '/aide' })

    expect(screen.getAllByRole('button', { expanded: false })).toHaveLength(56)
  })

  it('filters the entries on their keywords', async () => {
    const user = setupUser()
    await renderWithApp(AideView, { route: '/aide' })

    await user.type(screen.getByRole('searchbox', { name: 'Rechercher dans l\'aide' }), 'matrice')

    await waitFor(() => expect(themeTitles()).toEqual(['Droits et rôles']))
    expect(screen.getAllByRole('button', { expanded: false }).map(button => button.textContent?.trim()))
      .toEqual(['Qui peut faire quoi dans la plateforme ?'])
  })

  it('shows an empty state when nothing matches', async () => {
    const user = setupUser()
    await renderWithApp(AideView, { route: '/aide' })

    await user.type(screen.getByRole('searchbox', { name: 'Rechercher dans l\'aide' }), 'zzzz')

    expect(await screen.findByText('Aucune réponse ne correspond à votre recherche')).toBeInTheDocument()
    expect(screen.queryAllByRole('heading', { level: 2 })).toHaveLength(0)
  })

  it('opens an entry on its answer and location', async () => {
    const user = setupUser()
    await renderWithApp(AideView, { route: '/aide' })
    const question = screen.getByRole('button', { name: 'Comment voir les candidatures d\'une offre, en colonnes ou en liste ?' })

    await user.click(question)

    expect(question).toHaveAttribute('aria-expanded', 'true')
    const region = screen.getByRole('region', { name: 'Comment voir les candidatures d\'une offre, en colonnes ou en liste ?' })
    expect(region).toHaveTextContent('Ouvrez l\'offre depuis la liste des recrutements.')
    expect(region).toHaveTextContent('Où :')
  })
})
