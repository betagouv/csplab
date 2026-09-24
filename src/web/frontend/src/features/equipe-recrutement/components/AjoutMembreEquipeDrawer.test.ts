import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { setupUser } from '@/test/render'
import AjoutMembreEquipeDrawer from './AjoutMembreEquipeDrawer.vue'

function renderDrawer(props: Record<string, unknown> = {}) {
  return render(AjoutMembreEquipeDrawer, {
    props: { open: true, status: 'idle', ...props },
  })
}

describe('ajoutMembreEquipeDrawer', () => {
  it('offers no role and no submission before the search has answered', async () => {
    renderDrawer()

    await screen.findByRole('dialog', { name: 'Ajouter un membre' })
    expect(screen.queryByRole('radiogroup')).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Ajouter le membre|Créer et ajouter/ })).not.toBeInTheDocument()
  })

  it('adds the found agent as contributeur by default', async () => {
    const user = setupUser()
    const { emitted } = renderDrawer({ status: 'found', agent: AGENT_RECHERCHE })

    expect(await screen.findByText('Jeanne Dupont')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))

    expect(emitted('add')).toEqual([['contributeur']])
  })

  it('adds the found agent with the chosen role', async () => {
    const user = setupUser()
    const { emitted } = renderDrawer({ status: 'found', agent: AGENT_RECHERCHE })

    await user.click(await screen.findByRole('radio', { name: 'Responsable' }))
    await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))

    expect(emitted('add')).toEqual([['responsable']])
  })

  it('announces the account creation when no agent matches the email', async () => {
    renderDrawer({ status: 'not-found' })

    expect(await screen.findByText(/Un compte sera créé/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Créer et ajouter' })).toBeInTheDocument()
  })
})
