import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { HttpError } from '@/api/errors'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import { searchAgentByEmail } from '@/features/agents/api'
import { RECRUTEMENT_DETAIL } from '@/test/fixtures/candidatures'
import { MEMBRE_EQUIPE, RECRUTEMENT_UUID } from '@/test/fixtures/equipe'
import { AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { MTE_UUID } from '@/test/fixtures/utilisateur'
import { recrutementDetail } from '@/test/handlers/recrutements'
import { renderWithApp, setupUser } from '@/test/render'
import { server } from '@/test/server'
import { addMembreEquipe, getEquipeRecrutement, updateMembreEquipe } from '../api'
import EquipeRecrutementSection from './EquipeRecrutementSection.vue'

vi.mock('../api', () => ({
  getEquipeRecrutement: vi.fn(),
  addMembreEquipe: vi.fn(),
  updateMembreEquipe: vi.fn(),
}))

vi.mock('@/features/agents/api', async importOriginal => ({
  ...await importOriginal<typeof import('@/features/agents/api')>(),
  searchAgentByEmail: vi.fn(),
}))

const NOUVEL_AGENT = { ...AGENT_RECHERCHE, uuid: 'bbbbbbbb-0002-0002-0002-000000000002', email: 'paul.bernard@example.gouv.fr' }

const RECRUTEMENT_DETAIL_EQUIPE_GERABLE = {
  ...RECRUTEMENT_DETAIL,
  authorized_actions: ['add_recrutement_agent' as const, 'update_recrutement_agent' as const, 'revoke_recrutement_agent' as const],
}

const Host = defineComponent({
  setup: () => () => h(CspToaster, null, () =>
    h(EquipeRecrutementSection, { organismeUuid: MTE_UUID, recrutementUuid: RECRUTEMENT_UUID })),
})

const EQUIPE_PATH = `/organismes/${MTE_UUID}/recrutements/${RECRUTEMENT_UUID}/equipe`

async function renderSection() {
  const view = await renderWithApp(Host, { route: EQUIPE_PATH })
  await screen.findByRole('button', { name: 'Actions pour Jeanne Dupont' })
  return view
}

describe('equipeRecrutementSection', () => {
  beforeEach(() => {
    server.use(recrutementDetail(RECRUTEMENT_DETAIL_EQUIPE_GERABLE))
    vi.mocked(getEquipeRecrutement).mockReset().mockResolvedValue([MEMBRE_EQUIPE])
    vi.mocked(searchAgentByEmail).mockReset().mockResolvedValue(NOUVEL_AGENT)
    vi.mocked(addMembreEquipe).mockReset()
    vi.mocked(updateMembreEquipe).mockReset()
  })

  it('explains why the add failed with a 500', async () => {
    const user = setupUser()
    vi.mocked(addMembreEquipe).mockRejectedValue(new HttpError(500, 'Erreur'))
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Ajouter un membre' }))
    await user.type(
      await screen.findByRole('searchbox', { name: /Courriel de l'agent/ }),
      `${NOUVEL_AGENT.email}{Enter}`,
    )
    await user.click(await screen.findByRole('button', { name: 'Ajouter le membre' }))

    expect(await screen.findByText('L\'ajout du membre a échoué')).toBeInTheDocument()
  })

  it('surfaces a conflict until the email changes', async () => {
    const user = setupUser()
    vi.mocked(addMembreEquipe).mockRejectedValue(new HttpError(409, 'Conflict'))
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Ajouter un membre' }))
    const email = await screen.findByRole('searchbox', { name: /Courriel de l'agent/ })
    await user.type(email, `${NOUVEL_AGENT.email}{Enter}`)
    await user.click(await screen.findByRole('button', { name: 'Ajouter le membre' }))
    await screen.findByText('Cette personne fait déjà partie de l\'équipe.')

    await user.type(email, 'x')

    expect(screen.queryByText('Cette personne fait déjà partie de l\'équipe.')).not.toBeInTheDocument()
  })

  it('starts a new search each time the drawer opens', async () => {
    const user = setupUser()
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Ajouter un membre' }))
    await user.type(
      await screen.findByRole('searchbox', { name: /Courriel de l'agent/ }),
      `${NOUVEL_AGENT.email}{Enter}`,
    )
    await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Ajouter le membre' })).toBeEnabled())
    await user.click(screen.getByRole('button', { name: 'Annuler' }))
    await user.click(screen.getByRole('button', { name: 'Ajouter un membre' }))

    expect(await screen.findByRole('searchbox', { name: /Courriel de l'agent/ })).toHaveValue('')
    expect(screen.getByRole('button', { name: 'Ajouter le membre' })).toBeDisabled()
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

  it('changes the role from the access rights drawer', async () => {
    const user = setupUser()
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Actions pour Jeanne Dupont' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Modifier les droits d\'accès' }))
    await user.click(await screen.findByRole('radio', { name: /^Contributeur/ }))
    await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))

    expect(await screen.findByText('Rôle modifié')).toBeInTheDocument()
    expect(updateMembreEquipe).toHaveBeenCalledWith(MTE_UUID, RECRUTEMENT_UUID, expect.objectContaining({ recrutement_role: 'contributeur' }))
  })

  it('only lists the team without the right to manage it', async () => {
    server.use(recrutementDetail({ ...RECRUTEMENT_DETAIL, authorized_actions: ['list_recrutement_agents'] }))
    await renderWithApp(Host, { route: EQUIPE_PATH })

    await screen.findByText(MEMBRE_EQUIPE.email)
    expect(screen.queryByRole('button', { name: 'Ajouter un membre' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Actions pour Jeanne Dupont' })).not.toBeInTheDocument()
  })
})
