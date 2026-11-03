import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { setupUser } from '@/test/render'
import AssignResponsableForm from './AssignResponsableForm.vue'

function renderForm(props: Record<string, unknown> = {}) {
  return render(AssignResponsableForm, {
    props: { count: 2, summary: '2 recrutements sélectionnés', editable: true, status: 'idle', ...props },
  })
}

describe('assignResponsableForm', () => {
  it('disables the assignment until the search has answered', () => {
    renderForm()

    expect(screen.getByRole('button', { name: 'Assigner à 2 recrutements' })).toBeDisabled()
  })

  it('assigns the agent found for that email', async () => {
    const user = setupUser()
    const { emitted } = renderForm({ status: 'found', agent: AGENT_RECHERCHE })

    expect(await screen.findByText('Jeanne Dupont')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Assigner à 2 recrutements' }))

    expect(emitted('assign')).toEqual([[]])
  })

  it('announces the account creation when no agent matches the email', async () => {
    const user = setupUser()
    const { emitted } = renderForm({ status: 'not-found' })

    expect(await screen.findByText(/Un compte sera créé/)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Créer et assigner à 2 recrutements' }))

    expect(emitted('assign')).toEqual([[]])
  })

  it('asks to edit the selection it summarizes', async () => {
    const user = setupUser()
    const { emitted } = renderForm()

    expect(screen.getByText('2 recrutements sélectionnés')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Modifier la sélection' }))

    expect(emitted('editSelection')).toEqual([[]])
  })

  it('leaves out the count when a single offer is assigned', () => {
    renderForm({ count: 1, summary: 'Recrutement : Chargé de mission', editable: false })

    expect(screen.getByText('Recrutement : Chargé de mission')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Assigner un responsable' })).toBeDisabled()
  })
})
