import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { AGENT_RECHERCHE } from '@/test/fixtures/agents'
import { setupUser } from '@/test/render'
import { RECRUTEMENT_ROLE_OPTIONS } from '../constants/equipe-recrutement'
import AddTeamMemberForm from './AddTeamMemberForm.vue'

function renderForm(props: Record<string, unknown> = {}) {
  return render(AddTeamMemberForm, {
    props: { options: RECRUTEMENT_ROLE_OPTIONS, status: 'idle', organismeUuid: '00000000-0000-0000-0000-000000000000', tagsEditable: false, ...props },
  })
}

describe('addTeamMemberForm', () => {
  it('offers no role and disables the submission before the search has answered', () => {
    renderForm()

    expect(screen.queryByRole('radiogroup')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Ajouter le membre' })).toBeDisabled()
  })

  it('adds the found agent as contributeur by default', async () => {
    const user = setupUser()
    const { emitted } = renderForm({ status: 'found', agent: AGENT_RECHERCHE })

    expect(await screen.findByText('Jeanne Dupont')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))

    expect(emitted('add')).toEqual([['contributeur', null]])
  })

  it('adds the found agent with the chosen role', async () => {
    const user = setupUser()
    const { emitted } = renderForm({ status: 'found', agent: AGENT_RECHERCHE })

    await user.click(await screen.findByRole('radio', { name: /^Responsable/ }))
    await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))

    expect(emitted('add')).toEqual([['responsable', null]])
  })

  it('announces the account creation when no agent matches the email', async () => {
    renderForm({ status: 'not-found' })

    expect(await screen.findByText(/Un compte sera créé/)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Créer et ajouter' })).toBeInTheDocument()
  })
})
