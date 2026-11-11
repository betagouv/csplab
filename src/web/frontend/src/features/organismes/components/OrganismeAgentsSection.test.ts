import type { AgentOrganisme, SetAgentRolePayload, UpdateAgentRolePayload } from '../types'
import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { AGENT_RECHERCHE, CREATED_AGENT, NOUVEL_AGENT } from '@/test/fixtures/agents'
import { AGENT_ORGANISME } from '@/test/fixtures/organismes'
import { MTE_UUID } from '@/test/fixtures/utilisateur'
import { agentCreation, agentSearch, agentSearchFailure } from '@/test/handlers/agents'
import {
  organismeAgentAddition,
  organismeAgentAdditionFailure,
  organismeAgents,
  organismeAgentUpdate,
  organismeAgentUpdateFailure,
} from '@/test/handlers/organismes'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import OrganismeAgentsSection from './OrganismeAgentsSection.vue'

const NOUVEL_AGENT_ORGANISME: AgentOrganisme = {
  ...AGENT_ORGANISME,
  uuid: NOUVEL_AGENT.uuid,
  nom: NOUVEL_AGENT.nom,
  prenom: NOUVEL_AGENT.prenom,
  email: NOUVEL_AGENT.email,
  poste: NOUVEL_AGENT.intitule_poste,
}

const CREATED_AGENT_ORGANISME: AgentOrganisme = {
  ...AGENT_ORGANISME,
  uuid: CREATED_AGENT.uuid,
  nom: CREATED_AGENT.nom,
  prenom: CREATED_AGENT.prenom,
  email: CREATED_AGENT.email,
  poste: CREATED_AGENT.intitule_poste,
}

const Host = withToaster(OrganismeAgentsSection, { organismeUuid: MTE_UUID })

function additionSpy() {
  return vi.fn<(organismeUuid: string, payload: SetAgentRolePayload) => void>()
}

function updateSpy() {
  return vi.fn<(organismeUuid: string, payload: UpdateAgentRolePayload) => void>()
}

function listAfterAddition(agent: AgentOrganisme) {
  server.use(organismeAgents([AGENT_ORGANISME, agent]))
}

function watchAgentLoads() {
  const loads = vi.fn()
  server.use(organismeAgents([AGENT_ORGANISME], loads))
  return loads
}

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

async function chooseAction(user: ReturnType<typeof setupUser>, action: string) {
  await user.click(screen.getByRole('button', { name: 'Actions pour Jeanne Dupont' }))
  await user.click(await screen.findByRole('menuitem', { name: action }))
}

describe('organismeAgentsSection', () => {
  it('lists the accounts of the organisme', async () => {
    const loads = watchAgentLoads()
    await renderSection()

    expect(screen.getByText(AGENT_ORGANISME.email)).toBeInTheDocument()
    expect(loads).toHaveBeenCalledWith(MTE_UUID)
  })

  it('surfaces a conflict on the email field when the agent is already attached, until the email changes', async () => {
    const user = setupUser()
    const loads = watchAgentLoads()
    server.use(organismeAgentAdditionFailure(409))
    await renderSection()

    await searchFromAttachDrawer(user, AGENT_RECHERCHE.email)
    await user.click(await screen.findByRole('button', { name: 'Ajouter l\'utilisateur' }))

    expect(await screen.findByText('Cet utilisateur est déjà rattaché à l\'organisme.')).toBeInTheDocument()
    expect(screen.getByRole('dialog')).toBeInTheDocument()
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))

    await user.type(screen.getByRole('searchbox', { name: /^Courriel/ }), 'x')
    expect(screen.queryByText('Cet utilisateur est déjà rattaché à l\'organisme.')).not.toBeInTheDocument()
  })

  it('attaches the account found by its email without creating one, then lists it among the accounts', async () => {
    const user = setupUser()
    const searched = vi.fn()
    const created = vi.fn()
    const sent = additionSpy()
    server.use(
      agentSearch(NOUVEL_AGENT, searched),
      agentCreation(CREATED_AGENT, created),
      organismeAgentAddition(NOUVEL_AGENT_ORGANISME, (...args) => {
        sent(...args)
        server.use(organismeAgents([AGENT_ORGANISME, NOUVEL_AGENT_ORGANISME]))
      }),
    )
    await renderSection()

    await searchFromAttachDrawer(user, NOUVEL_AGENT.email)
    expect(await screen.findByText(NOUVEL_AGENT.intitule_poste)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Ajouter l\'utilisateur' }))

    expect(await screen.findByRole('heading', { name: 'Utilisateur ajouté' })).toBeInTheDocument()
    expect(await screen.findByText(NOUVEL_AGENT.email)).toBeInTheDocument()
    expect(searched).toHaveBeenCalledWith(MTE_UUID, NOUVEL_AGENT.email)
    expect(created).not.toHaveBeenCalled()
    expect(sent).toHaveBeenCalledWith(MTE_UUID, { agent_id: NOUVEL_AGENT.uuid, role: 'agent' })
  })

  it('creates the account then attaches it when the email matches nobody', async () => {
    const user = setupUser()
    const created = vi.fn()
    const sent = additionSpy()
    server.use(
      agentSearchFailure(404),
      agentCreation(CREATED_AGENT, created),
      organismeAgentAddition(CREATED_AGENT_ORGANISME, (...args) => {
        sent(...args)
        listAfterAddition(CREATED_AGENT_ORGANISME)
      }),
    )
    await renderSection()

    await searchFromAttachDrawer(user, CREATED_AGENT.email)
    expect(await screen.findByText(/Aucun compte ne correspond à ce courriel/)).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Créer et ajouter' }))

    expect(await screen.findByRole('heading', { name: 'Utilisateur ajouté' })).toBeInTheDocument()
    expect(created).toHaveBeenCalledWith({ email: CREATED_AGENT.email, organisme_id: MTE_UUID })
    expect(sent).toHaveBeenCalledWith(MTE_UUID, { agent_id: CREATED_AGENT.uuid, role: 'agent' })
    await screen.findByRole('cell', { name: CREATED_AGENT.email })
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
    const created = vi.fn()
    const sent = additionSpy()
    server.use(agentSearchFailure(404), agentCreation(CREATED_AGENT, created), organismeAgentAdditionFailure(500))
    await renderSection()

    await searchFromAttachDrawer(user, CREATED_AGENT.email)
    await user.click(await screen.findByRole('button', { name: 'Créer et ajouter' }))
    expect(await screen.findByRole('heading', { name: 'L\'ajout de l\'utilisateur a échoué', hidden: true })).toBeInTheDocument()
    expect(screen.queryByText(/Aucun compte ne correspond à ce courriel/)).not.toBeInTheDocument()

    server.use(organismeAgentAddition(CREATED_AGENT_ORGANISME, (...args) => {
      sent(...args)
      listAfterAddition(CREATED_AGENT_ORGANISME)
    }))
    await user.click(screen.getByRole('button', { name: 'Ajouter l\'utilisateur' }))

    expect(await screen.findByRole('heading', { name: 'Utilisateur ajouté' })).toBeInTheDocument()
    expect(created).toHaveBeenCalledTimes(1)
    expect(sent).toHaveBeenCalledWith(MTE_UUID, { agent_id: CREATED_AGENT.uuid, role: 'agent' })
    await screen.findByRole('cell', { name: CREATED_AGENT.email })
  })

  it('keeps the add button disabled from the account creation until the account is attached', async () => {
    const user = setupUser()
    let finishCreation!: () => void
    let finishAttachment!: () => void
    server.use(
      agentSearchFailure(404),
      agentCreation(CREATED_AGENT, () => new Promise((resolve) => {
        finishCreation = resolve
      })),
      organismeAgentAddition(CREATED_AGENT_ORGANISME, () => new Promise((resolve) => {
        finishAttachment = () => {
          listAfterAddition(CREATED_AGENT_ORGANISME)
          resolve()
        }
      })),
    )
    await renderSection()

    await searchFromAttachDrawer(user, CREATED_AGENT.email)
    const submit = await screen.findByRole('button', { name: 'Créer et ajouter' })
    await user.click(submit)
    await vi.waitFor(() => expect(finishCreation).toBeDefined())
    expect(submit).toBeDisabled()

    finishCreation()
    await vi.waitFor(() => expect(finishAttachment).toBeDefined())
    expect(screen.getByRole('button', { name: 'Ajouter l\'utilisateur' })).toBeDisabled()

    finishAttachment()

    expect(await screen.findByRole('heading', { name: 'Utilisateur ajouté' })).toBeInTheDocument()
    await screen.findByRole('cell', { name: CREATED_AGENT.email })
  })

  it('starts a new search each time the drawer opens', async () => {
    const user = setupUser()
    await renderSection()

    await searchFromAttachDrawer(user, AGENT_RECHERCHE.email)
    await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Ajouter l\'utilisateur' })).toBeEnabled())
    await user.click(screen.getByRole('button', { name: 'Annuler' }))
    await user.click(screen.getByRole('button', { name: 'Ajouter un utilisateur' }))

    expect(await screen.findByRole('searchbox', { name: /^Courriel/ })).toHaveValue('')
    expect(screen.getByRole('button', { name: 'Ajouter l\'utilisateur' })).toBeDisabled()
  })

  it('revokes an account with its role and a revocation date after confirmation', async () => {
    const user = setupUser()
    const loads = watchAgentLoads()
    const sent = updateSpy()
    server.use(organismeAgentUpdate(AGENT_ORGANISME, sent))
    await renderSection()

    await chooseAction(user, 'Révoquer')
    await user.click(await screen.findByRole('button', { name: 'Révoquer les accès' }))

    expect(await screen.findByRole('heading', { name: 'Utilisateur révoqué' })).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(MTE_UUID, {
      agent_id: AGENT_ORGANISME.uuid,
      role: AGENT_ORGANISME.role,
      date_revocation: expect.any(String),
    })
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))
  })

  it('changes the role from the access rights drawer, then shows the new role among the accounts', async () => {
    const user = setupUser()
    const sent = updateSpy()
    server.use(organismeAgentUpdate({ ...AGENT_ORGANISME, role: 'superviseur' }, (...args) => {
      sent(...args)
      server.use(organismeAgents([{ ...AGENT_ORGANISME, role: 'superviseur' }]))
    }))
    await renderSection()

    await chooseAction(user, 'Modifier les droits d\'accès')
    const save = await screen.findByRole('button', { name: 'Enregistrer les modifications' })
    expect(save).toBeDisabled()

    await user.click(screen.getByRole('radio', { name: /^Superviseur/ }))
    await user.click(save)

    expect(await screen.findByRole('heading', { name: 'Rôle modifié' })).toBeInTheDocument()
    expect(await screen.findByRole('cell', { name: 'Superviseur' })).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(MTE_UUID, { agent_id: AGENT_ORGANISME.uuid, role: 'superviseur' })
  })

  it('tells the user when the role change fails and keeps the drawer open', async () => {
    const user = setupUser()
    const loads = watchAgentLoads()
    server.use(organismeAgentUpdateFailure(500))
    await renderSection()

    await chooseAction(user, 'Modifier les droits d\'accès')
    await user.click(await screen.findByRole('radio', { name: /^Superviseur/ }))
    await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))

    expect(await screen.findByRole('heading', { name: 'La modification du rôle a échoué', hidden: true })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Enregistrer les modifications' })).toBeInTheDocument()
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))
  })
})
