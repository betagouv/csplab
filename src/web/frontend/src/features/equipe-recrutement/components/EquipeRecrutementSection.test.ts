import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { HttpError } from '@/api/errors'
import { getMe } from '@/api/utilisateur'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import { searchAgentByEmail } from '@/features/organismes/api'
import { MEMBRE_EQUIPE, RECRUTEMENT_UUID } from '@/test/fixtures/equipe'
import { AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { makeUser, MTE_UUID, ROLE_MTE } from '@/test/fixtures/utilisateur'
import { renderWithApp, setupUser } from '@/test/render'
import { addMembreEquipe, getEquipeRecrutement, updateMembreEquipe } from '../api'
import EquipeRecrutementSection from './EquipeRecrutementSection.vue'

vi.mock('../api', () => ({
  getEquipeRecrutement: vi.fn(),
  addMembreEquipe: vi.fn(),
  updateMembreEquipe: vi.fn(),
}))

vi.mock('@/features/organismes/api', async importOriginal => ({
  ...await importOriginal<typeof import('@/features/organismes/api')>(),
  searchAgentByEmail: vi.fn(),
}))

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

const NOUVEL_AGENT = { ...AGENT_RECHERCHE, agent_id: 'bbbbbbbb-0002-0002-0002-000000000002', email: 'paul.bernard@example.gouv.fr' }

const Host = defineComponent({
  setup: () => () => h(CspToaster, null, () =>
    h(EquipeRecrutementSection, { organismeUuid: MTE_UUID, recrutementUuid: RECRUTEMENT_UUID })),
})

async function renderSection() {
  const result = await renderWithApp(Host, { route: `/organismes/${MTE_UUID}/recrutements/${RECRUTEMENT_UUID}/equipe` })
  await screen.findByRole('button', { name: 'Actions pour Jeanne Dupont' })
  return result
}

describe('equipeRecrutementSection', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([ROLE_MTE]))
    vi.mocked(getEquipeRecrutement).mockReset().mockResolvedValue([MEMBRE_EQUIPE])
    vi.mocked(searchAgentByEmail).mockReset().mockResolvedValue(NOUVEL_AGENT)
    vi.mocked(addMembreEquipe).mockReset()
    vi.mocked(updateMembreEquipe).mockReset()
  })

  it.each([
    [409, 'Cette personne fait déjà partie de l\'équipe.'],
    [500, 'L\'ajout du membre a échoué'],
  ])('explains why the add failed with a %i', async (status, message) => {
    const user = setupUser()
    vi.mocked(addMembreEquipe).mockRejectedValue(new HttpError(status, 'Erreur'))
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Ajouter un membre' }))
    await user.type(
      await screen.findByRole('searchbox', { name: /Adresse électronique de l'agent/ }),
      `${NOUVEL_AGENT.email}{Enter}`,
    )
    await user.click(await screen.findByRole('button', { name: 'Ajouter le membre' }))

    expect(await screen.findByText(message)).toBeInTheDocument()
  })

  it('tells the recruteur when the member to remove already left the team', async () => {
    const user = setupUser()
    vi.mocked(updateMembreEquipe).mockRejectedValue(new HttpError(404, 'Not found'))
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Actions pour Jeanne Dupont' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Retirer de l\'équipe' }))
    await user.click(await screen.findByRole('button', { name: 'Retirer de l’équipe' }))

    expect(await screen.findByText('Cet agent ne fait plus partie de l\'équipe')).toBeInTheDocument()
  })
})
