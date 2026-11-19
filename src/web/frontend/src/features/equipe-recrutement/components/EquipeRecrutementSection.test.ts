import type { Tag } from '@/features/tags/types'
import { screen, within } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { HttpError } from '@/api/errors'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import { searchAgentByEmail } from '@/features/agents/api'
import { getTags } from '@/features/tags/api'
import { RECRUTEMENT_DETAIL } from '@/test/fixtures/candidatures'
import { MEMBRE_EQUIPE, RECRUTEMENT_UUID } from '@/test/fixtures/equipe'
import { AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { MTE_UUID } from '@/test/fixtures/utilisateur'
import { recrutementDetail } from '@/test/handlers/recrutements'
import { renderWithApp, setupUser } from '@/test/render'
import { server } from '@/test/server'
import { addMembreEquipe, addMembreTag, getEquipeRecrutement, removeMembreTag, updateMembreEquipe } from '../api'
import EquipeRecrutementSection from './EquipeRecrutementSection.vue'

vi.mock('../api', () => ({
  getEquipeRecrutement: vi.fn(),
  addMembreEquipe: vi.fn(),
  updateMembreEquipe: vi.fn(),
  addMembreTag: vi.fn(),
  removeMembreTag: vi.fn(),
}))

vi.mock('@/features/tags/api', () => ({
  getTags: vi.fn(),
}))

vi.mock('@/features/agents/api', async importOriginal => ({
  ...await importOriginal<typeof import('@/features/agents/api')>(),
  searchAgentByEmail: vi.fn(),
}))

const NOUVEL_AGENT = { ...AGENT_RECHERCHE, uuid: 'bbbbbbbb-0002-0002-0002-000000000002', email: 'paul.bernard@example.gouv.fr' }

const RECRUTEMENT_DETAIL_EQUIPE_GERABLE = {
  ...RECRUTEMENT_DETAIL,
  authorized_actions: ['add_recrutement_agent' as const, 'update_recrutement_agent' as const, 'revoke_recrutement_agent' as const, 'manage_tag_on_member' as const],
}

const TAG_JURY: Tag = { uuid: 'aaaaaaaa-0003-0003-0003-000000000001', name: 'Jury', category: 'recrutement_agent', color: 'vert', usage_count: 0 }
const TAG_PRESELECTION: Tag = { uuid: 'aaaaaaaa-0003-0003-0003-000000000002', name: 'Présélection', category: 'recrutement_agent', color: 'bleu', usage_count: 0 }

const Host = defineComponent({
  setup: () => () => h(CspToaster, null, () =>
    h(EquipeRecrutementSection, { organismeUuid: MTE_UUID, recrutementUuid: RECRUTEMENT_UUID })),
})

const EQUIPE_PATH = `/organismes/${MTE_UUID}/recrutements/${RECRUTEMENT_UUID}/equipe`

async function renderSection() {
  const result = await renderWithApp(Host, { route: EQUIPE_PATH })
  await screen.findByRole('button', { name: 'Actions pour Jeanne Dupont' })
  return result
}

async function chooseTag(user: ReturnType<typeof setupUser>, name: string) {
  await user.click(screen.getByRole('button', { name: 'Actions pour Jeanne Dupont' }))
  await user.click(await screen.findByRole('menuitem', { name: 'Modifier l\'étiquette' }))
  await user.click(await screen.findByRole('combobox', { name: /Étiquette/ }))
  await user.click(await screen.findByRole('option', { name }))
  await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))
}

async function addMemberWithTag(user: ReturnType<typeof setupUser>, name: string) {
  await user.click(screen.getByRole('button', { name: 'Ajouter un membre' }))
  await user.type(await screen.findByRole('searchbox', { name: /Courriel de l'agent/ }), `${NOUVEL_AGENT.email}{Enter}`)
  await user.click(await screen.findByRole('combobox', { name: /Étiquette/ }))
  await user.click(await screen.findByRole('option', { name }))
  await user.click(screen.getByRole('button', { name: 'Ajouter le membre' }))
}

describe('equipeRecrutementSection', () => {
  beforeEach(() => {
    server.use(recrutementDetail(RECRUTEMENT_DETAIL_EQUIPE_GERABLE))
    vi.mocked(getEquipeRecrutement).mockReset().mockResolvedValue([MEMBRE_EQUIPE])
    vi.mocked(searchAgentByEmail).mockReset().mockResolvedValue(NOUVEL_AGENT)
    vi.mocked(addMembreEquipe).mockReset()
    vi.mocked(updateMembreEquipe).mockReset()
    vi.mocked(addMembreTag).mockReset().mockResolvedValue()
    vi.mocked(removeMembreTag).mockReset().mockResolvedValue()
    vi.mocked(getTags).mockReset().mockResolvedValue([TAG_JURY, TAG_PRESELECTION])
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
    expect(updateMembreEquipe).toHaveBeenCalledWith({ organismeUuid: MTE_UUID, recrutementUuid: RECRUTEMENT_UUID }, expect.objectContaining({ recrutement_role: 'contributeur' }))
  })

  it('shows the tag of each member in a column', async () => {
    vi.mocked(getEquipeRecrutement).mockResolvedValue([{ ...MEMBRE_EQUIPE, tags: [TAG_JURY] }])
    await renderSection()

    expect(within(screen.getByRole('row', { name: /Dupont Jeanne/ })).getByText('Jury')).toBeInTheDocument()
    expect(screen.getByRole('columnheader', { name: 'Étiquette' })).toBeInTheDocument()
  })

  it('replaces the tag of a member from the tag drawer', async () => {
    const user = setupUser()
    vi.mocked(getEquipeRecrutement).mockResolvedValue([{ ...MEMBRE_EQUIPE, tags: [TAG_JURY] }])
    await renderSection()

    await chooseTag(user, 'Présélection')

    expect(await screen.findByText('Étiquette enregistrée')).toBeInTheDocument()
    const params = { organismeUuid: MTE_UUID, recrutementUuid: RECRUTEMENT_UUID, agentUuid: MEMBRE_EQUIPE.uuid }
    expect(removeMembreTag).toHaveBeenCalledWith({ ...params, tagUuid: TAG_JURY.uuid })
    expect(addMembreTag).toHaveBeenCalledWith({ ...params, tagUuid: TAG_PRESELECTION.uuid })
  })

  it('tags a member without a tag from the tag drawer', async () => {
    const user = setupUser()
    await renderSection()

    await chooseTag(user, 'Jury')

    expect(await screen.findByText('Étiquette enregistrée')).toBeInTheDocument()
    expect(removeMembreTag).not.toHaveBeenCalled()
    expect(addMembreTag).toHaveBeenCalledWith({ organismeUuid: MTE_UUID, recrutementUuid: RECRUTEMENT_UUID, agentUuid: MEMBRE_EQUIPE.uuid, tagUuid: TAG_JURY.uuid })
  })

  it('removes the tag of a member by choosing no tag', async () => {
    const user = setupUser()
    vi.mocked(getEquipeRecrutement).mockResolvedValue([{ ...MEMBRE_EQUIPE, tags: [TAG_JURY] }])
    await renderSection()

    await chooseTag(user, 'Aucune étiquette')

    expect(await screen.findByText('Étiquette retirée')).toBeInTheDocument()
    expect(addMembreTag).not.toHaveBeenCalled()
  })

  it('tags the member it adds', async () => {
    const user = setupUser()
    vi.mocked(addMembreEquipe).mockResolvedValue({ ...MEMBRE_EQUIPE, uuid: NOUVEL_AGENT.uuid, email: NOUVEL_AGENT.email })
    await renderSection()

    await addMemberWithTag(user, 'Jury')

    await vi.waitFor(() => expect(addMembreTag).toHaveBeenCalledWith({ organismeUuid: MTE_UUID, recrutementUuid: RECRUTEMENT_UUID, agentUuid: NOUVEL_AGENT.uuid, tagUuid: TAG_JURY.uuid }))
  })

  it('says when the organisme has no member tag', async () => {
    const user = setupUser()
    vi.mocked(getTags).mockResolvedValue([])
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Actions pour Jeanne Dupont' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Modifier l\'étiquette' }))

    const select = await screen.findByRole('combobox', { name: /Étiquette/ })
    await vi.waitFor(() => expect(select).toHaveTextContent('Aucune étiquette disponible.'))
    expect(select).toBeDisabled()
  })

  it('says when the tag of a member cannot be changed', async () => {
    const user = setupUser()
    vi.mocked(addMembreTag).mockRejectedValue(new HttpError(500, 'Erreur'))
    await renderSection()

    await chooseTag(user, 'Jury')

    expect(await screen.findByText('La modification de l\'étiquette a échoué')).toBeInTheDocument()
  })

  it('says when the member or the tag no longer exists', async () => {
    const user = setupUser()
    vi.mocked(addMembreTag).mockRejectedValue(new HttpError(404, 'Not Found'))
    await renderSection()

    await chooseTag(user, 'Jury')

    expect(await screen.findByText('Ce membre ou cette étiquette n\'existe plus')).toBeInTheDocument()
  })

  it('says that the former tag was removed when the new one cannot be added', async () => {
    const user = setupUser()
    vi.mocked(getEquipeRecrutement).mockResolvedValue([{ ...MEMBRE_EQUIPE, tags: [TAG_JURY] }])
    vi.mocked(addMembreTag).mockRejectedValue(new HttpError(500, 'Erreur'))
    await renderSection()

    await chooseTag(user, 'Présélection')

    expect(await screen.findByText('L\'ancienne étiquette a été retirée, mais la nouvelle n\'a pas pu être posée')).toBeInTheDocument()
    expect(removeMembreTag).toHaveBeenCalledOnce()
  })

  it('says when the member is added but not tagged', async () => {
    const user = setupUser()
    vi.mocked(addMembreEquipe).mockResolvedValue({ ...MEMBRE_EQUIPE, uuid: NOUVEL_AGENT.uuid, email: NOUVEL_AGENT.email })
    vi.mocked(addMembreTag).mockRejectedValue(new HttpError(500, 'Erreur'))
    await renderSection()

    await addMemberWithTag(user, 'Jury')

    expect(await screen.findByText('Membre ajouté')).toBeInTheDocument()
    expect(await screen.findByText('L\'étiquette du membre n\'a pas pu être enregistrée')).toBeInTheDocument()
  })

  it('says when the tags of the organisme cannot be loaded', async () => {
    const user = setupUser()
    vi.mocked(getTags).mockRejectedValue(new HttpError(500, 'Erreur'))
    await renderSection()

    await user.click(screen.getByRole('button', { name: 'Actions pour Jeanne Dupont' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Modifier l\'étiquette' }))

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
