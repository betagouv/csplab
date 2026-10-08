import { screen, waitFor } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { renderWithApp, setupUser } from '@/test/render'
import { FAQ_ENTREES, FAQ_THEMES } from '../constants/faq'
import { MESSAGE_SANS_REPONSE } from '../utils/motsClesAdapter'
import AideView from './AideView.vue'

function themeTitles(): string[] {
  return screen.getAllByRole('heading', { level: 2 }).map(heading => heading.textContent?.trim() ?? '')
}

async function rechercher(question: string) {
  const user = setupUser()
  await renderWithApp(AideView, { route: '/aide' })

  await user.type(screen.getByRole('searchbox', { name: 'Posez votre question' }), question)
  await user.click(screen.getByRole('button', { name: 'Rechercher' }))
}

describe('aideView', () => {
  it('lists the eight themes in the order of the FAQ', async () => {
    await renderWithApp(AideView, { route: '/aide' })

    expect(themeTitles()).toHaveLength(8)
    expect(themeTitles()).toEqual([...FAQ_THEMES])
  })

  it('lists every entry of the FAQ, closed', async () => {
    await renderWithApp(AideView, { route: '/aide' })

    expect(screen.getAllByRole('button', { expanded: false })).toHaveLength(56)
  })

  it('shows no assistant block before a question is asked', async () => {
    await renderWithApp(AideView, { route: '/aide' })

    expect(screen.queryByText('Assistant expérimental — réponses issues de la FAQ')).not.toBeInTheDocument()
  })

  it('filters the entries on their keywords once the question is submitted', async () => {
    const entree = FAQ_ENTREES.find(e => e.id === 'droits-qui-fait-quoi')!
    await rechercher('matrice')

    await waitFor(() => expect(themeTitles()).toEqual([entree.theme]))
    expect(screen.getAllByRole('button', { expanded: false }).map(button => button.textContent?.trim()))
      .toEqual([entree.question])
  })

  it('shows the closest entry above the filtered list', async () => {
    await rechercher('matrice')

    expect(await screen.findByText('Entrée la plus proche')).toBeInTheDocument()
    expect(screen.getByText('Assistant expérimental — réponses issues de la FAQ')).toBeInTheDocument()
    expect(screen.getAllByRole('button', { expanded: false })).toHaveLength(1)
  })

  it('does not filter while typing, before submitting', async () => {
    const user = setupUser()
    await renderWithApp(AideView, { route: '/aide' })

    await user.type(screen.getByRole('searchbox', { name: 'Posez votre question' }), 'matrice')
    // 300 ms : au-delà du délai d'un filtrage à la frappe (250 ms par défaut dans useTextSearch).
    await new Promise(resolve => setTimeout(resolve, 300))

    expect(screen.getAllByRole('button', { expanded: false })).toHaveLength(56)
    expect(screen.queryByText('Assistant expérimental — réponses issues de la FAQ')).not.toBeInTheDocument()
  })

  it('goes back to the full FAQ when the question is cleared, without submitting', async () => {
    const user = setupUser()
    await renderWithApp(AideView, { route: '/aide' })
    const champ = screen.getByRole('searchbox', { name: 'Posez votre question' })
    await user.type(champ, 'matrice')
    await user.click(screen.getByRole('button', { name: 'Rechercher' }))
    expect(await screen.findByText('Entrée la plus proche')).toBeInTheDocument()
    expect(screen.getAllByRole('button', { expanded: false })).toHaveLength(1)

    await user.clear(champ)

    await waitFor(() => expect(screen.getAllByRole('button', { expanded: false })).toHaveLength(56))
    expect(screen.queryByText('Assistant expérimental — réponses issues de la FAQ')).not.toBeInTheDocument()
  })

  it('submits the question with the Enter key', async () => {
    const user = setupUser()
    await renderWithApp(AideView, { route: '/aide' })

    await user.type(screen.getByRole('searchbox', { name: 'Posez votre question' }), 'zzzz{Enter}')

    expect(await screen.findByText('Aucune réponse ne correspond à votre recherche')).toBeInTheDocument()
    expect(screen.queryAllByRole('heading', { level: 2 })).toHaveLength(0)
  })

  it('shows only the empty state when no entry matches', async () => {
    await rechercher('zzzz')

    expect(await screen.findByText('Aucune réponse ne correspond à votre recherche')).toBeInTheDocument()
    expect(screen.queryByText('Assistant expérimental — réponses issues de la FAQ')).not.toBeInTheDocument()
    expect(screen.queryByText(MESSAGE_SANS_REPONSE)).not.toBeInTheDocument()
  })

  it('answers a natural sentence and keeps the answer in the filtered list', async () => {
    const entree = FAQ_ENTREES.find(e => e.id === 'org-revoquer')!
    await rechercher('comment retirer un collègue qui quitte le service ?')

    expect((await screen.findByText('Entrée la plus proche')).parentElement).toHaveTextContent(entree.question)
    expect(screen.getByRole('button', { name: entree.question })).toBeInTheDocument()
    expect(screen.queryByText('Aucune réponse ne correspond à votre recherche')).not.toBeInTheDocument()
  })

  it('invites to browse the list when no entry stands out', async () => {
    await rechercher('droits')

    expect(await screen.findByText(MESSAGE_SANS_REPONSE)).toBeInTheDocument()
    expect(screen.queryByText('Entrée la plus proche')).not.toBeInTheDocument()
    expect(screen.getAllByRole('button', { expanded: false })).toHaveLength(4)
  })

  it('opens an entry on its answer and location', async () => {
    const user = setupUser()
    await renderWithApp(AideView, { route: '/aide' })
    const entree = FAQ_ENTREES.find(e => e.id === 'cand-voir')!
    const question = screen.getByRole('button', { name: entree.question })

    await user.click(question)

    expect(question).toHaveAttribute('aria-expanded', 'true')
    const region = screen.getByRole('region', { name: entree.question })
    expect(region).toHaveTextContent(entree.reponse)
    expect(region).toHaveTextContent(`Où : ${entree.ou}`)
  })
})
