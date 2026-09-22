import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { setupUser } from '@/test/render'
import { RECRUTEMENTS_ACTIFS } from '../mock'
import AssignationResponsableDrawer from './AssignationResponsableDrawer.vue'

const RECRUTEMENTS = RECRUTEMENTS_ACTIFS.slice(0, 2)

function renderDrawer(props: Record<string, unknown> = {}) {
  return render(AssignationResponsableDrawer, {
    props: { open: true, recrutements: RECRUTEMENTS, status: 'idle', ...props },
  })
}

function dismissButton(intitule: string) {
  return screen.getByRole('button', { name: `Retirer ${intitule} de la sélection` })
}

describe('assignationResponsableDrawer', () => {
  it('assigns the agent found for that email', async () => {
    const user = setupUser()
    const { emitted } = renderDrawer({ status: 'found', agent: AGENT_RECHERCHE })

    expect(await screen.findByText('Jeanne Dupont')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Assigner un responsable' }))

    expect(emitted('assign')).toEqual([[]])
  })

  it('announces the account creation when no agent matches the email', async () => {
    const user = setupUser()
    const { emitted } = renderDrawer({ status: 'not-found' })

    expect(await screen.findByText(/Un compte sera créé/)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Créer et assigner' }))

    expect(emitted('assign')).toEqual([[]])
  })

  it('shows one dismissible tag per selected offer', async () => {
    renderDrawer()

    await screen.findByRole('dialog')
    for (const recrutement of RECRUTEMENTS)
      expect(dismissButton(recrutement.intitule)).toBeInTheDocument()
    expect(screen.getByText('2 offres sélectionnées')).toBeInTheDocument()
  })

  it('asks to remove the offer whose tag is dismissed', async () => {
    const user = setupUser()
    const { emitted } = renderDrawer()

    await screen.findByRole('dialog')
    await user.click(dismissButton(RECRUTEMENTS[1].intitule))

    expect(emitted('remove')).toEqual([[RECRUTEMENTS[1].offer_id]])
  })

  it('closes itself once every offer has been removed', async () => {
    const { emitted, rerender } = renderDrawer()

    await screen.findByRole('dialog')
    await rerender({ recrutements: [] })

    expect(emitted('update:open')).toEqual([[false]])
  })
})
