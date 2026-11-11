import type { MembreEquipe, MembreEquipePayload } from '../types'
import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { NOUVEL_AGENT } from '@/test/fixtures/agents'
import { RECRUTEMENT_DETAIL } from '@/test/fixtures/candidatures'
import { EQUIPE, MEMBRE_EQUIPE, RECRUTEMENT_UUID } from '@/test/fixtures/equipe'
import { MTE_UUID } from '@/test/fixtures/utilisateur'
import { agentCreation, agentSearch } from '@/test/handlers/agents'
import {
  equipe,
  membreAddition,
  membreAdditionFailure,
  membreUpdate,
  membreUpdateFailure,
} from '@/test/handlers/equipe-recrutement'
import { recrutementDetail } from '@/test/handlers/recrutements'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import EquipeRecrutementSection from './EquipeRecrutementSection.vue'

const NOUVEAU_MEMBRE: MembreEquipe = {
  uuid: NOUVEL_AGENT.uuid,
  prenom: NOUVEL_AGENT.prenom,
  nom: NOUVEL_AGENT.nom,
  poste: NOUVEL_AGENT.intitule_poste,
  email: NOUVEL_AGENT.email,
  recrutement_role: 'recruteur',
}

const RECRUTEMENT_DETAIL_EQUIPE_GERABLE = {
  ...RECRUTEMENT_DETAIL,
  authorized_actions: ['add_recrutement_agent' as const, 'update_recrutement_agent' as const, 'revoke_recrutement_agent' as const],
}

const Host = withToaster(EquipeRecrutementSection, { organismeUuid: MTE_UUID, recrutementUuid: RECRUTEMENT_UUID })

const EQUIPE_PATH = `/organismes/${MTE_UUID}/recrutements/${RECRUTEMENT_UUID}/equipe`

function payloadSpy() {
  return vi.fn<(organismeUuid: string, recrutementUuid: string, payload: MembreEquipePayload) => void>()
}

function watchTeamLoads() {
  const loads = vi.fn()
  server.use(equipe(EQUIPE, loads))
  return loads
}

async function renderSection() {
  const view = await renderWithApp(Host, { route: EQUIPE_PATH })
  await screen.findByRole('button', { name: 'Actions pour Jeanne Dupont' })
  return view
}

async function searchNewAgent(user: ReturnType<typeof setupUser>) {
  await user.click(screen.getByRole('button', { name: 'Ajouter un membre' }))
  await user.type(
    await screen.findByRole('searchbox', { name: /Courriel de l'agent/ }),
    `${NOUVEL_AGENT.email}{Enter}`,
  )
}

async function chooseAction(user: ReturnType<typeof setupUser>, action: string) {
  await user.click(screen.getByRole('button', { name: 'Actions pour Jeanne Dupont' }))
  await user.click(await screen.findByRole('menuitem', { name: action }))
}

describe('equipeRecrutementSection', () => {
  beforeEach(() => {
    server.use(recrutementDetail(RECRUTEMENT_DETAIL_EQUIPE_GERABLE), agentSearch(NOUVEL_AGENT))
  })

  it('lists the members of the recrutement', async () => {
    const loads = watchTeamLoads()
    await renderSection()

    expect(screen.getByText(MEMBRE_EQUIPE.email)).toBeInTheDocument()
    expect(loads).toHaveBeenCalledWith(MTE_UUID, RECRUTEMENT_UUID)
  })

  it('adds the found agent with the chosen role without creating an account, then lists them in the team', async () => {
    const user = setupUser()
    const sent = payloadSpy()
    const created = vi.fn()
    server.use(
      agentCreation(undefined, created),
      membreAddition(NOUVEAU_MEMBRE, (...args) => {
        sent(...args)
        server.use(equipe([MEMBRE_EQUIPE, NOUVEAU_MEMBRE]))
      }),
    )
    await renderSection()

    await searchNewAgent(user)
    await user.click(await screen.findByRole('radio', { name: /^Recruteur/ }))
    await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))

    expect(await screen.findByRole('heading', { name: 'Membre ajouté' })).toBeInTheDocument()
    expect(await screen.findByText(NOUVEAU_MEMBRE.email)).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(MTE_UUID, RECRUTEMENT_UUID, { agent_id: NOUVEL_AGENT.uuid, recrutement_role: 'recruteur' })
    expect(created).not.toHaveBeenCalled()
  })

  it('explains why the add failed with a 500', async () => {
    const user = setupUser()
    const loads = watchTeamLoads()
    server.use(membreAdditionFailure(500))
    await renderSection()

    await searchNewAgent(user)
    await user.click(await screen.findByRole('button', { name: 'Ajouter le membre' }))

    expect(await screen.findByRole('heading', { name: 'L\'ajout du membre a échoué', hidden: true })).toBeInTheDocument()
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))
  })

  it('surfaces a conflict until the email changes', async () => {
    const user = setupUser()
    const loads = watchTeamLoads()
    server.use(membreAdditionFailure(409))
    await renderSection()

    await searchNewAgent(user)
    await user.click(await screen.findByRole('button', { name: 'Ajouter le membre' }))
    await screen.findByText('Cette personne fait déjà partie de l\'équipe.')
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))

    await user.type(screen.getByRole('searchbox', { name: /Courriel de l'agent/ }), 'x')

    expect(screen.queryByText('Cette personne fait déjà partie de l\'équipe.')).not.toBeInTheDocument()
  })

  it('starts a new search each time the drawer opens', async () => {
    const user = setupUser()
    await renderSection()

    await searchNewAgent(user)
    await vi.waitFor(() => expect(screen.getByRole('button', { name: 'Ajouter le membre' })).toBeEnabled())
    await user.click(screen.getByRole('button', { name: 'Annuler' }))
    await user.click(screen.getByRole('button', { name: 'Ajouter un membre' }))

    expect(await screen.findByRole('searchbox', { name: /Courriel de l'agent/ })).toHaveValue('')
    expect(screen.getByRole('button', { name: 'Ajouter le membre' })).toBeDisabled()
  })

  it('removes a member with their role and a revocation date, then empties the team', async () => {
    const user = setupUser()
    const sent = payloadSpy()
    server.use(membreUpdate((...args) => {
      sent(...args)
      server.use(equipe([]))
    }))
    await renderSection()

    await chooseAction(user, 'Retirer de l\'équipe')
    await user.click(await screen.findByRole('button', { name: 'Retirer de l’équipe' }))

    expect(await screen.findByRole('heading', { name: 'Membre retiré' })).toBeInTheDocument()
    expect(await screen.findByText('Aucun membre rattaché à ce recrutement.')).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(MTE_UUID, RECRUTEMENT_UUID, {
      agent_id: MEMBRE_EQUIPE.uuid,
      recrutement_role: MEMBRE_EQUIPE.recrutement_role,
      date_revocation_recrutement: expect.any(String),
    })
  })

  it('tells the recruteur when the member to remove already left the team', async () => {
    const user = setupUser()
    const loads = watchTeamLoads()
    server.use(membreUpdateFailure(404))
    await renderSection()

    await chooseAction(user, 'Retirer de l\'équipe')
    await user.click(await screen.findByRole('button', { name: 'Retirer de l’équipe' }))

    expect(await screen.findByRole('heading', { name: 'Cet agent ne fait plus partie de l\'équipe', hidden: true })).toBeInTheDocument()
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))
  })

  it('changes the role from the access rights drawer without revoking the member, then shows the new role in the team', async () => {
    const user = setupUser()
    const sent = payloadSpy()
    server.use(membreUpdate((...args) => {
      sent(...args)
      server.use(equipe([{ ...MEMBRE_EQUIPE, recrutement_role: 'contributeur' }]))
    }))
    await renderSection()

    await chooseAction(user, 'Modifier les droits d\'accès')
    await user.click(await screen.findByRole('radio', { name: /^Contributeur/ }))
    await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))

    expect(await screen.findByRole('heading', { name: 'Rôle modifié' })).toBeInTheDocument()
    expect(await screen.findByRole('cell', { name: 'Contributeur' })).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(MTE_UUID, RECRUTEMENT_UUID, { agent_id: MEMBRE_EQUIPE.uuid, recrutement_role: 'contributeur' })
  })

  it('only lists the team without the right to manage it', async () => {
    server.use(recrutementDetail({ ...RECRUTEMENT_DETAIL, authorized_actions: ['list_recrutement_agents'] }))
    await renderWithApp(Host, { route: EQUIPE_PATH })

    await screen.findByText(MEMBRE_EQUIPE.email)
    expect(screen.queryByRole('button', { name: 'Ajouter un membre' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Actions pour Jeanne Dupont' })).not.toBeInTheDocument()
  })
})
