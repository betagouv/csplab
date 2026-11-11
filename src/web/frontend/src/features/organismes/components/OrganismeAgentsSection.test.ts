import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { AGENT_RECHERCHE, CREATED_AGENT } from '@/test/fixtures/agents'
import { AGENT_ORGANISME } from '@/test/fixtures/organismes'
import { MTE_UUID } from '@/test/fixtures/utilisateur'
import { agentCreation, agentSearch, agentSearchFailure } from '@/test/handlers/agents'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import { getOrganismeAgents, setAgentRole, updateAgentRole } from '../api'
import OrganismeAgentsSection from './OrganismeAgentsSection.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  getOrganismeAgents: vi.fn(),
  setAgentRole: vi.fn(),
  updateAgentRole: vi.fn(),
}))

const Host = withToaster(OrganismeAgentsSection, { organismeUuid: MTE_UUID })

async function renderSection() {
  const view = await renderWithApp(Host)
  await screen.findByRole('button', { name: 'Actions pour Jeanne Dupont' })
  return view
}

async function searchFromAttachDrawer(user: ReturnType<typeof setupUser>, email: string) {
  await user.click(screen.getByRole('button', { name: 'Ajouter un utilisateur' }))
  await user.type(await screen.findByRole('searchbox', { name: /^Courriel/ }), email)
  await user.click(screen.getByRole('button', { name: 'Rechercher' }))
}

describe('organismeAgentsSection', () => {
  beforeEach(() => {
    vi.mocked(getOrganismeAgents).mockResolvedValue([AGENT_ORGANISME])
    vi.mocked(setAgentRole).mockReset()
    vi.mocked(updateAgentRole).mockReset()
  })

  it('surfaces a conflict on the email field when the agent is already attached', async () => {
    const user = setupUser()
    vi.mocked(setAgentRole).mockRejectedValue(new HttpError(409, 'Conflict'))
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Ajouter un utilisateur' }))
    await user.type(await screen.findByRole('searchbox', { name: /^Courriel/ }), AGENT_RECHERCHE.email)
    await user.click(screen.getByRole('button', { name: 'Rechercher' }))
    await user.click(await screen.findByRole('button', { name: 'Ajouter l\'utilisateur' }))

    expect(await screen.findByText('Cet utilisateur est déjà rattaché à l\'organisme.')).toBeInTheDocument()
    expect(screen.getByRole('dialog')).toBeInTheDocument()

    await user.type(screen.getByRole('searchbox', { name: /^Courriel/ }), 'x')
    expect(screen.queryByText('Cet utilisateur est déjà rattaché à l\'organisme.')).not.toBeInTheDocument()
  })

  it('attaches the account found by its email without creating one', async () => {
    const user = setupUser()
    const onSearch = vi.fn()
    const onCreation = vi.fn()
    server.use(agentSearch(AGENT_RECHERCHE, onSearch), agentCreation(CREATED_AGENT, onCreation))
    vi.mocked(setAgentRole).mockResolvedValue(AGENT_ORGANISME)
    await renderSection()

    await searchFromAttachDrawer(user, AGENT_RECHERCHE.email)
    expect(await screen.findByText(AGENT_RECHERCHE.intitule_poste)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Ajouter l\'utilisateur' }))

    expect(await screen.findByRole('heading', { name: 'Utilisateur ajouté' })).toBeInTheDocument()
    expect(onSearch).toHaveBeenCalledWith(MTE_UUID, AGENT_RECHERCHE.email)
    expect(onCreation).not.toHaveBeenCalled()
    expect(setAgentRole).toHaveBeenCalledWith(MTE_UUID, { agent_id: AGENT_RECHERCHE.uuid, role: 'agent' })
  })

  it('creates the account then attaches it when the email matches nobody', async () => {
    const user = setupUser()
    const onCreation = vi.fn()
    server.use(agentSearchFailure(404), agentCreation(CREATED_AGENT, onCreation))
    vi.mocked(setAgentRole).mockResolvedValue({ ...AGENT_ORGANISME, uuid: CREATED_AGENT.uuid })
    await renderSection()

    await searchFromAttachDrawer(user, CREATED_AGENT.email)
    expect(await screen.findByText(/Aucun compte ne correspond à ce courriel/)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Créer et ajouter' }))

    expect(await screen.findByRole('heading', { name: 'Utilisateur ajouté' })).toBeInTheDocument()
    expect(onCreation).toHaveBeenCalledWith({ email: CREATED_AGENT.email, organisme_id: MTE_UUID })
    expect(setAgentRole).toHaveBeenCalledWith(MTE_UUID, { agent_id: CREATED_AGENT.uuid, role: 'agent' })
  })

  it('replaces the found account with the creation notice when the next email matches nobody', async () => {
    const user = setupUser()
    await renderSection()

    await searchFromAttachDrawer(user, AGENT_RECHERCHE.email)
    await screen.findByText(AGENT_RECHERCHE.intitule_poste)
    server.use(agentSearchFailure(404))
    const email = screen.getByRole('searchbox', { name: /^Courriel/ })
    await user.clear(email)
    await user.type(email, CREATED_AGENT.email)
    await user.click(screen.getByRole('button', { name: 'Rechercher' }))

    expect(await screen.findByText(/Aucun compte ne correspond à ce courriel/)).toBeInTheDocument()
    expect(screen.queryByText(AGENT_RECHERCHE.intitule_poste)).not.toBeInTheDocument()
  })

  it('tells the user when the search fails and lets them search again', async () => {
    const user = setupUser()
    server.use(agentSearchFailure(500))
    await renderSection()

    await searchFromAttachDrawer(user, AGENT_RECHERCHE.email)

    expect(await screen.findByRole('heading', { name: 'La recherche a échoué', hidden: true })).toBeInTheDocument()
    expect(screen.getByRole('searchbox', { name: /^Courriel/ })).toBeEnabled()
    expect(screen.getByRole('button', { name: 'Ajouter l\'utilisateur' })).toBeDisabled()
  })

  it('keeps the created account when attaching it fails, and attaches it on retry without a second creation', async () => {
    const user = setupUser()
    const onCreation = vi.fn()
    server.use(agentSearchFailure(404), agentCreation(CREATED_AGENT, onCreation))
    vi.mocked(setAgentRole)
      .mockRejectedValueOnce(new HttpError(500, 'Erreur'))
      .mockResolvedValueOnce({ ...AGENT_ORGANISME, uuid: CREATED_AGENT.uuid })
    await renderSection()

    await searchFromAttachDrawer(user, CREATED_AGENT.email)
    await user.click(await screen.findByRole('button', { name: 'Créer et ajouter' }))
    expect(await screen.findByRole('heading', { name: 'L\'ajout de l\'utilisateur a échoué', hidden: true })).toBeInTheDocument()
    expect(screen.queryByText(/Aucun compte ne correspond à ce courriel/)).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Ajouter l\'utilisateur' }))

    expect(await screen.findByRole('heading', { name: 'Utilisateur ajouté' })).toBeInTheDocument()
    expect(onCreation).toHaveBeenCalledTimes(1)
    expect(setAgentRole).toHaveBeenLastCalledWith(MTE_UUID, { agent_id: CREATED_AGENT.uuid, role: 'agent' })
  })

  it('keeps the add button disabled from the account creation until the account is attached', async () => {
    const user = setupUser()
    let finishCreation!: () => void
    let finishAttachment!: (agent: typeof AGENT_ORGANISME) => void
    server.use(
      agentSearchFailure(404),
      agentCreation(CREATED_AGENT, () => new Promise((resolve) => {
        finishCreation = resolve
      })),
    )
    vi.mocked(setAgentRole).mockReturnValue(new Promise((resolve) => {
      finishAttachment = resolve
    }))
    await renderSection()

    await searchFromAttachDrawer(user, CREATED_AGENT.email)
    const submit = await screen.findByRole('button', { name: 'Créer et ajouter' })
    await user.click(submit)
    await vi.waitFor(() => expect(finishCreation).toBeDefined())
    expect(submit).toBeDisabled()

    finishCreation()
    await vi.waitFor(() => expect(setAgentRole).toHaveBeenCalled())
    expect(screen.getByRole('button', { name: 'Ajouter l\'utilisateur' })).toBeDisabled()

    finishAttachment({ ...AGENT_ORGANISME, uuid: CREATED_AGENT.uuid })

    expect(await screen.findByRole('heading', { name: 'Utilisateur ajouté' })).toBeInTheDocument()
  })

  it('starts a new search each time the drawer opens', async () => {
    const user = setupUser()
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Ajouter un utilisateur' }))
    await user.type(await screen.findByRole('searchbox', { name: /^Courriel/ }), AGENT_RECHERCHE.email)
    await user.click(screen.getByRole('button', { name: 'Rechercher' }))
    await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Ajouter l\'utilisateur' })).toBeEnabled())
    await user.click(screen.getByRole('button', { name: 'Annuler' }))
    await user.click(screen.getByRole('button', { name: 'Ajouter un utilisateur' }))

    expect(await screen.findByRole('searchbox', { name: /^Courriel/ })).toHaveValue('')
    expect(screen.getByRole('button', { name: 'Ajouter l\'utilisateur' })).toBeDisabled()
  })

  it('revokes a member with a revocation date after confirmation', async () => {
    const user = setupUser()
    vi.mocked(updateAgentRole).mockResolvedValue({ ...AGENT_ORGANISME, date_revocation: '2026-09-17T00:00:00Z' } as never)
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Actions pour Jeanne Dupont' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Révoquer' }))
    await user.click(await screen.findByRole('button', { name: 'Révoquer les accès' }))

    expect(await screen.findByText('Utilisateur révoqué')).toBeInTheDocument()
    expect(updateAgentRole).toHaveBeenCalledWith(MTE_UUID, expect.objectContaining({
      agent_id: AGENT_ORGANISME.uuid,
      date_revocation: expect.any(String),
    }))
  })

  it('changes the role from the access rights drawer', async () => {
    const user = setupUser()
    vi.mocked(updateAgentRole).mockResolvedValue({ ...AGENT_ORGANISME, role: 'superviseur' })
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Actions pour Jeanne Dupont' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Modifier les droits d\'accès' }))
    const save = await screen.findByRole('button', { name: 'Enregistrer les modifications' })
    expect(save).toBeDisabled()

    await user.click(screen.getByRole('radio', { name: /^Superviseur/ }))
    await user.click(save)

    expect(await screen.findByText('Rôle modifié')).toBeInTheDocument()
    expect(updateAgentRole).toHaveBeenCalledWith(MTE_UUID, { agent_id: AGENT_ORGANISME.uuid, role: 'superviseur' })
  })
})
