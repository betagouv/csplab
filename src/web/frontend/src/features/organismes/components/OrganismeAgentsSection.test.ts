import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { HttpError } from '@/api/errors'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import { AGENT_ORGANISME, AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { MTE_UUID } from '@/test/fixtures/utilisateur'
import { renderWithApp, setupUser } from '@/test/render'
import { getOrganismeAgents, searchAgentByEmail, setAgentRole, updateAgentRole } from '../api'
import OrganismeAgentsSection from './OrganismeAgentsSection.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  getOrganismeAgents: vi.fn(),
  searchAgentByEmail: vi.fn(),
  setAgentRole: vi.fn(),
  createAgent: vi.fn(),
  updateAgentRole: vi.fn(),
}))

const Host = defineComponent({
  setup: () => () => h(CspToaster, null, () => h(OrganismeAgentsSection, { organismeUuid: MTE_UUID })),
})

async function renderSection() {
  const result = await renderWithApp(Host)
  await screen.findByRole('button', { name: 'Actions pour Jeanne Dupont' })
  return result
}

describe('organismeAgentsSection', () => {
  beforeEach(() => {
    vi.mocked(getOrganismeAgents).mockReset().mockResolvedValue([AGENT_ORGANISME])
    vi.mocked(searchAgentByEmail).mockReset().mockResolvedValue(AGENT_RECHERCHE)
    vi.mocked(setAgentRole).mockReset()
    vi.mocked(updateAgentRole).mockReset()
  })

  it('surfaces a conflict on the email field when the agent is already attached', async () => {
    const user = setupUser()
    vi.mocked(setAgentRole).mockRejectedValue(new HttpError(409, 'Conflict'))
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Ajouter un membre' }))
    await user.type(await screen.findByRole('searchbox', { name: /Adresse électronique de l'agent/ }), AGENT_RECHERCHE.email)
    await user.click(screen.getByRole('button', { name: 'Rechercher' }))
    await user.click(await screen.findByRole('button', { name: 'Ajouter le membre' }))

    expect(await screen.findByText('Cet agent est déjà rattaché à l\'organisme.')).toBeInTheDocument()
    expect(screen.getByRole('dialog')).toBeInTheDocument()
  })

  it('revokes a member with a revocation date after confirmation', async () => {
    const user = setupUser()
    vi.mocked(updateAgentRole).mockResolvedValue({ ...AGENT_ORGANISME, date_revocation: '2026-09-17T00:00:00Z' } as never)
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Actions pour Jeanne Dupont' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Révoquer' }))
    await user.click(await screen.findByRole('button', { name: 'Révoquer les accès' }))

    expect(await screen.findByText('Membre révoqué')).toBeInTheDocument()
    expect(updateAgentRole).toHaveBeenCalledWith(MTE_UUID, expect.objectContaining({
      agent_id: AGENT_ORGANISME.agent_id,
      date_revocation: expect.any(String),
    }))
  })
})
