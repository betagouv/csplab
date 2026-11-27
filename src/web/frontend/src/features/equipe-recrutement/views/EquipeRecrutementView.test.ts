import type { MembreEquipePayload } from '../types'
import type { Tag } from '@/features/tags/types'
import { screen, within } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { NOUVEL_AGENT } from '@/test/fixtures/agents'
import { RECRUTEMENT_DETAIL } from '@/test/fixtures/candidatures'
import { EQUIPE, MEMBRE_EQUIPE, RECRUTEMENT_UUID, SECOND_MEMBRE_EQUIPE } from '@/test/fixtures/equipe'
import { MTE_UUID } from '@/test/fixtures/utilisateur'
import { agentCreation, agentSearch } from '@/test/handlers/agents'
import {
  equipe,
  membreAddition,
  membreAdditionFailure,
  membreTagAddition,
  membreTagAdditionFailure,
  membreTagRemoval,
  membreUpdate,
  membreUpdateFailure,
} from '@/test/handlers/equipe-recrutement'
import { recrutementDetail } from '@/test/handlers/recrutements'
import { tags, tagsFailure } from '@/test/handlers/tags'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import EquipeRecrutementView from './EquipeRecrutementView.vue'

const RECRUTEMENT_DETAIL_EQUIPE_GERABLE = {
  ...RECRUTEMENT_DETAIL,
  authorized_actions: ['add_recrutement_agent' as const, 'update_recrutement_agent' as const, 'revoke_recrutement_agent' as const, 'manage_tag_on_member' as const],
}

const TAG_JURY: Tag = { uuid: 'aaaaaaaa-0003-0003-0003-000000000001', name: 'Jury', category: 'recrutement_agent', color: 'vert', usage_count: 0 }
const TAG_PRESELECTION: Tag = { uuid: 'aaaaaaaa-0003-0003-0003-000000000002', name: 'Présélection', category: 'recrutement_agent', color: 'bleu', usage_count: 0 }

const MEMBRE_JURY = { ...MEMBRE_EQUIPE, tags: [TAG_JURY] }

const Host = withToaster(EquipeRecrutementView, { organismeUuid: MTE_UUID, recrutementUuid: RECRUTEMENT_UUID })

const EQUIPE_PATH = `/organismes/${MTE_UUID}/recrutements/${RECRUTEMENT_UUID}/equipe`

function payloadSpy() {
  return vi.fn<(organismeUuid: string, recrutementUuid: string, payload: MembreEquipePayload) => void>()
}

function watchTeamLoads() {
  const loads = vi.fn()
  server.use(equipe(EQUIPE, loads))
  return loads
}

async function renderView() {
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

async function chooseTag(user: ReturnType<typeof setupUser>, name: string) {
  await chooseAction(user, 'Modifier l\'étiquette')
  await user.click(await screen.findByRole('combobox', { name: /Étiquette/ }))
  await user.click(await screen.findByRole('option', { name }))
  await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))
}

async function addMemberWithTag(user: ReturnType<typeof setupUser>, name: string) {
  await searchNewAgent(user)
  await user.click(await screen.findByRole('combobox', { name: /Étiquette/ }))
  await user.click(await screen.findByRole('option', { name }))
  await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))
}

function watchTagChanges() {
  const added = vi.fn<(agentUuid: string, tagUuid: string) => void>()
  const removed = vi.fn<(agentUuid: string, tagUuid: string) => void>()
  server.use(membreTagAddition(added), membreTagRemoval(removed))
  return { added, removed }
}

describe('equipeRecrutementView', () => {
  beforeEach(() => {
    server.use(recrutementDetail(RECRUTEMENT_DETAIL_EQUIPE_GERABLE), agentSearch(NOUVEL_AGENT), tags([TAG_JURY, TAG_PRESELECTION]))
  })

  it('lists the members of the recrutement', async () => {
    const loads = watchTeamLoads()
    await renderView()

    expect(screen.getByText(MEMBRE_EQUIPE.email)).toBeInTheDocument()
    expect(loads).toHaveBeenCalledWith(MTE_UUID, RECRUTEMENT_UUID)
  })

  it('adds the found agent with the chosen role without creating an account, then lists them in the team', async () => {
    const user = setupUser()
    const sent = payloadSpy()
    const created = vi.fn()
    server.use(
      agentCreation(undefined, created),
      membreAddition(SECOND_MEMBRE_EQUIPE, (...args) => {
        sent(...args)
        server.use(equipe([MEMBRE_EQUIPE, SECOND_MEMBRE_EQUIPE]))
      }),
    )
    await renderView()

    await searchNewAgent(user)
    await user.click(await screen.findByRole('radio', { name: /^Recruteur/ }))
    await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))

    expect(await screen.findByRole('heading', { name: 'Membre ajouté' })).toBeInTheDocument()
    expect(await screen.findByText(SECOND_MEMBRE_EQUIPE.email)).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(MTE_UUID, RECRUTEMENT_UUID, { agent_id: NOUVEL_AGENT.uuid, recrutement_role: 'recruteur' })
    expect(created).not.toHaveBeenCalled()
  })

  it('explains why the add failed with a 500', async () => {
    const user = setupUser()
    const loads = watchTeamLoads()
    server.use(membreAdditionFailure(500))
    await renderView()

    await searchNewAgent(user)
    await user.click(await screen.findByRole('button', { name: 'Ajouter le membre' }))

    expect(await screen.findByRole('heading', { name: 'L\'ajout du membre a échoué', hidden: true })).toBeInTheDocument()
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))
  })

  it('surfaces a conflict until the email changes', async () => {
    const user = setupUser()
    const loads = watchTeamLoads()
    server.use(membreAdditionFailure(409))
    await renderView()

    await searchNewAgent(user)
    await user.click(await screen.findByRole('button', { name: 'Ajouter le membre' }))
    await screen.findByText('Cette personne fait déjà partie de l\'équipe.')
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))

    await user.type(screen.getByRole('searchbox', { name: /Courriel de l'agent/ }), 'x')

    expect(screen.queryByText('Cette personne fait déjà partie de l\'équipe.')).not.toBeInTheDocument()
  })

  it('starts a new search each time the drawer opens', async () => {
    const user = setupUser()
    await renderView()

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
    await renderView()

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
    await renderView()

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
    await renderView()

    await chooseAction(user, 'Modifier les droits d\'accès')
    await user.click(await screen.findByRole('radio', { name: /^Contributeur/ }))
    await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))

    expect(await screen.findByRole('heading', { name: 'Rôle modifié' })).toBeInTheDocument()
    expect(await screen.findByRole('cell', { name: 'Contributeur' })).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(MTE_UUID, RECRUTEMENT_UUID, { agent_id: MEMBRE_EQUIPE.uuid, recrutement_role: 'contributeur' })
  })

  it.each([
    { droit: 'without', authorizedActions: [], offered: false },
    { droit: 'with', authorizedActions: ['grant_recrutement_responsable' as const], offered: true },
  ])('offers the responsable role $droit the right to grant it', async ({ authorizedActions, offered }) => {
    const user = setupUser()
    server.use(recrutementDetail({
      ...RECRUTEMENT_DETAIL_EQUIPE_GERABLE,
      authorized_actions: [...RECRUTEMENT_DETAIL_EQUIPE_GERABLE.authorized_actions, ...authorizedActions],
    }))
    await renderView()

    await searchNewAgent(user)
    await screen.findByRole('radio', { name: /^Contributeur/ })

    expect(Boolean(screen.queryByRole('radio', { name: /^Responsable/ }))).toBe(offered)
  })

  it('shows the tag of each member in a column', async () => {
    server.use(equipe([MEMBRE_JURY]))
    await renderView()

    expect(within(screen.getByRole('row', { name: /Dupont Jeanne/ })).getByText('Jury')).toBeInTheDocument()
    expect(screen.getByRole('columnheader', { name: 'Étiquette' })).toBeInTheDocument()
  })

  it('replaces the tag of a member from the tag drawer', async () => {
    const user = setupUser()
    const { added, removed } = watchTagChanges()
    server.use(equipe([MEMBRE_JURY]))
    await renderView()

    await chooseTag(user, 'Présélection')

    expect(await screen.findByText('Étiquette enregistrée')).toBeInTheDocument()
    expect(removed).toHaveBeenCalledWith(MEMBRE_EQUIPE.uuid, TAG_JURY.uuid)
    expect(added).toHaveBeenCalledWith(MEMBRE_EQUIPE.uuid, TAG_PRESELECTION.uuid)
  })

  it('tags a member without a tag from the tag drawer', async () => {
    const user = setupUser()
    const { added, removed } = watchTagChanges()
    await renderView()

    await chooseTag(user, 'Jury')

    expect(await screen.findByText('Étiquette enregistrée')).toBeInTheDocument()
    expect(removed).not.toHaveBeenCalled()
    expect(added).toHaveBeenCalledWith(MEMBRE_EQUIPE.uuid, TAG_JURY.uuid)
  })

  it('removes the tag of a member by choosing no tag', async () => {
    const user = setupUser()
    const { added, removed } = watchTagChanges()
    server.use(equipe([MEMBRE_JURY]))
    await renderView()

    await chooseTag(user, 'Aucune étiquette')

    expect(await screen.findByText('Étiquette retirée')).toBeInTheDocument()
    expect(removed).toHaveBeenCalledWith(MEMBRE_EQUIPE.uuid, TAG_JURY.uuid)
    expect(added).not.toHaveBeenCalled()
  })

  it('tags the member it adds', async () => {
    const user = setupUser()
    const { added } = watchTagChanges()
    server.use(membreAddition(SECOND_MEMBRE_EQUIPE))
    await renderView()

    await addMemberWithTag(user, 'Jury')

    await vi.waitFor(() => expect(added).toHaveBeenCalledWith(SECOND_MEMBRE_EQUIPE.uuid, TAG_JURY.uuid))
  })

  it('says when the organisme has no member tag', async () => {
    const user = setupUser()
    server.use(tags([]))
    await renderView()

    await chooseAction(user, 'Modifier l\'étiquette')

    const select = await screen.findByRole('combobox', { name: /Étiquette/ })
    await vi.waitFor(() => expect(select).toHaveTextContent('Aucune étiquette disponible.'))
    expect(select).toBeDisabled()
  })

  it('says when the tag of a member cannot be changed', async () => {
    const user = setupUser()
    server.use(membreTagAdditionFailure(500))
    await renderView()

    await chooseTag(user, 'Jury')

    expect(await screen.findByText('La modification de l\'étiquette a échoué')).toBeInTheDocument()
  })

  it('says when the member or the tag no longer exists', async () => {
    const user = setupUser()
    server.use(membreTagAdditionFailure(404))
    await renderView()

    await chooseTag(user, 'Jury')

    expect(await screen.findByText('Ce membre ou cette étiquette n\'existe plus')).toBeInTheDocument()
  })

  it('says that the former tag was removed when the new one cannot be added', async () => {
    const user = setupUser()
    const { removed } = watchTagChanges()
    server.use(equipe([MEMBRE_JURY]), membreTagAdditionFailure(500))
    await renderView()

    await chooseTag(user, 'Présélection')

    expect(await screen.findByText('L\'ancienne étiquette a été retirée, mais la nouvelle n\'a pas pu être posée')).toBeInTheDocument()
    expect(removed).toHaveBeenCalledOnce()
  })

  it('only adds the new tag when saving again after a failed replacement', async () => {
    const user = setupUser()
    const removed = vi.fn()
    const reloads = vi.fn()
    server.use(
      equipe([MEMBRE_JURY]),
      membreTagRemoval((agentUuid, tagUuid) => {
        removed(agentUuid, tagUuid)
        server.use(equipe([MEMBRE_EQUIPE], reloads))
      }),
      membreTagAdditionFailure(500),
    )
    await renderView()
    await chooseTag(user, 'Présélection')
    await screen.findByText('L\'ancienne étiquette a été retirée, mais la nouvelle n\'a pas pu être posée')
    await vi.waitFor(() => expect(reloads).toHaveBeenCalled())

    const added = vi.fn()
    server.use(membreTagAddition(added))
    await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))

    expect(await screen.findByText('Étiquette enregistrée')).toBeInTheDocument()
    expect(removed).toHaveBeenCalledOnce()
    expect(added).toHaveBeenCalledWith(MEMBRE_EQUIPE.uuid, TAG_PRESELECTION.uuid)
  })

  it('says when the member is added but not tagged', async () => {
    const user = setupUser()
    server.use(membreAddition(SECOND_MEMBRE_EQUIPE), membreTagAdditionFailure(500))
    await renderView()

    await addMemberWithTag(user, 'Jury')

    expect(await screen.findByText('Membre ajouté')).toBeInTheDocument()
    expect(await screen.findByText('L\'étiquette du membre n\'a pas pu être enregistrée')).toBeInTheDocument()
  })

  it('says when the tags of the organisme cannot be loaded', async () => {
    const user = setupUser()
    server.use(tagsFailure(500))
    await renderView()

    await chooseAction(user, 'Modifier l\'étiquette')

    expect(await screen.findByText('Les étiquettes n\'ont pas pu être chargées.')).toBeInTheDocument()
    expect(screen.queryByText('Aucune étiquette disponible.')).not.toBeInTheDocument()
  })

  it('only lists the team without the right to manage it', async () => {
    server.use(recrutementDetail({ ...RECRUTEMENT_DETAIL, authorized_actions: ['list_recrutement_agents'] }))
    await renderWithApp(Host, { route: EQUIPE_PATH })

    await screen.findByText(MEMBRE_EQUIPE.email)
    expect(screen.queryByRole('button', { name: 'Ajouter un membre' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Actions pour Jeanne Dupont' })).not.toBeInTheDocument()
  })
})
