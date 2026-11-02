import { fireEvent, render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { setupUser } from '@/test/render'
import AttachAgentForm from './AttachAgentForm.vue'

function renderForm(props: Record<string, unknown> = {}) {
  return render(AttachAgentForm, { props: { status: 'idle', agent: null, ...props } })
}

function emailInput() {
  return screen.getByRole('searchbox', { name: /^Adresse électronique de l'agent/ })
}

describe('attachAgentForm', () => {
  it('rejects an invalid email without emitting a search', async () => {
    const user = setupUser()
    const { emitted } = renderForm()

    await user.type(emailInput(), 'jeanne.dupont')
    await user.click(screen.getByRole('button', { name: 'Rechercher' }))

    expect(emitted().search).toBeUndefined()
    expect(screen.getByText('Renseignez une adresse électronique valide.')).toBeInTheDocument()
  })

  it('emits the trimmed email on search', async () => {
    const user = setupUser()
    const { emitted } = renderForm()

    await user.type(emailInput(), '  jeanne.dupont@example.gouv.fr  ')
    await user.click(screen.getByRole('button', { name: 'Rechercher' }))

    expect(emitted().search).toEqual([['jeanne.dupont@example.gouv.fr']])
  })

  it('shows the matching agent without any editable identity field', async () => {
    renderForm({ status: 'found', agent: AGENT_RECHERCHE })

    expect(screen.getByText('Jeanne Dupont')).toBeInTheDocument()
    expect(screen.getByText('Responsable recrutement')).toBeInTheDocument()
    expect(screen.getByText('jeanne.dupont@example.gouv.fr')).toBeInTheDocument()
    expect(screen.queryByRole('textbox', { name: /nom|prénom/i })).not.toBeInTheDocument()
  })

  it('attaches the agent as membre by default', async () => {
    const user = setupUser()
    const { emitted } = renderForm({ status: 'found', agent: AGENT_RECHERCHE })

    await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))

    expect(emitted().add).toEqual([['agent']])
  })

  it('attaches the agent with the selected role', async () => {
    const user = setupUser()
    const { emitted } = renderForm({ status: 'found', agent: AGENT_RECHERCHE })

    await user.click(screen.getByRole('radio', { name: 'Superviseur' }))
    await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))

    expect(emitted().add).toEqual([['superviseur']])
  })

  it('offers to add a member only once the search has answered', async () => {
    renderForm()

    expect(screen.queryByRole('button', { name: /ajouter/i })).not.toBeInTheDocument()
  })

  it('creates and adds the member when no account matches', async () => {
    const user = setupUser()
    const { emitted } = renderForm({ status: 'not-found' })

    expect(screen.getByText(/Aucun compte ne correspond à cette adresse\./)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Créer et ajouter' }))

    expect(emitted().add).toEqual([['agent']])
  })

  it('asks for a reset when the email changes after a search', async () => {
    const { emitted } = renderForm({ status: 'found', agent: AGENT_RECHERCHE })

    await fireEvent.update(emailInput(), 'autre.agent@example.gouv.fr')

    expect(emitted().reset).toHaveLength(1)
  })
})
