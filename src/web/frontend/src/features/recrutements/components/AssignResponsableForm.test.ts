import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { RECRUTEMENTS_ACTIFS } from '@/test/fixtures/recrutements'
import { setupUser } from '@/test/render'
import AssignResponsableForm from './AssignResponsableForm.vue'

const RECRUTEMENTS = RECRUTEMENTS_ACTIFS.slice(0, 2)

function renderForm(props: Record<string, unknown> = {}) {
  return render(AssignResponsableForm, {
    props: { recrutements: RECRUTEMENTS, status: 'idle', ...props },
  })
}

function dismissButton(intitule: string) {
  return screen.getByRole('button', { name: `Retirer ${intitule} de la sélection` })
}

describe('assignResponsableForm', () => {
  it('assigns the agent found for that email', async () => {
    const user = setupUser()
    const { emitted } = renderForm({ status: 'found', agent: AGENT_RECHERCHE })

    expect(await screen.findByText('Jeanne Dupont')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Assigner un responsable' }))

    expect(emitted('assign')).toEqual([[]])
  })

  it('announces the account creation when no agent matches the email', async () => {
    const user = setupUser()
    const { emitted } = renderForm({ status: 'not-found' })

    expect(await screen.findByText(/Un compte sera créé/)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Créer et assigner' }))

    expect(emitted('assign')).toEqual([[]])
  })

  it('shows one dismissible tag per selected offer', () => {
    renderForm()

    for (const recrutement of RECRUTEMENTS) {
      expect(dismissButton(recrutement.intitule)).toBeInTheDocument()
    }
    expect(screen.getByText('2 recrutements sélectionnés')).toBeInTheDocument()
  })

  it('asks to remove the offer whose tag is dismissed', async () => {
    const user = setupUser()
    const { emitted } = renderForm()

    await user.click(dismissButton(RECRUTEMENTS[1].intitule))

    expect(emitted('remove')).toEqual([[RECRUTEMENTS[1].uuid]])
  })
})
