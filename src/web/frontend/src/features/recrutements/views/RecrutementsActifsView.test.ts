import { screen, within } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getOrganismeDetail } from '@/api/organismes'
import { getMe } from '@/api/utilisateur'
import { TABLE_PAGE_SIZE } from '@/components/base/CspDataTable/table'
import { searchAgentByEmail } from '@/features/agents/api'
import { getEquipeRecrutement } from '@/features/equipe-recrutement/api'
import { getOrganismeAgents } from '@/features/organismes/api'
import { ORGANISME_UUID, RECRUTEMENT_DETAIL, RECRUTEMENT_UUID, USER_ORGANISME } from '@/test/fixtures/candidatures'
import { MEMBRE_EQUIPE } from '@/test/fixtures/equipe'
import { AGENT_ORGANISME, AGENT_RECHERCHE, ORGANISME_DETAIL } from '@/test/fixtures/organismes'
import { RECRUTEMENTS_ACTIFS } from '@/test/fixtures/recrutements'
import { makeUser } from '@/test/fixtures/utilisateur'
import {
  recrutementDetail,
  recrutementsActifs,
  responsableAssignment,
} from '@/test/handlers/recrutements'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'

vi.mock('@/features/agents/api', () => ({
  searchAgentByEmail: vi.fn(),
  createAgent: vi.fn(),
}))

vi.mock('@/features/equipe-recrutement/api', () => ({
  getEquipeRecrutement: vi.fn(),
}))

vi.mock('@/api/organismes', () => ({
  getOrganismeDetail: vi.fn(),
}))

vi.mock('@/features/organismes/api', async importOriginal => ({
  ...await importOriginal<typeof import('@/features/organismes/api')>(),
  getOrganismeAgents: vi.fn(),
}))

const RECRUTEMENTS_PATH = `/organismes/${ORGANISME_UUID}/recrutements`
const ORGANISME_PATH = `/organismes/${ORGANISME_UUID}`
const EQUIPE_PATH = `${RECRUTEMENTS_PATH}/${RECRUTEMENT_UUID}/equipe`
const [FIRST_RECRUTEMENT, SECOND_RECRUTEMENT] = RECRUTEMENTS_ACTIFS
const SECOND_WITHOUT_RESPONSABLE = RECRUTEMENTS_ACTIFS.map(row => row.uuid === SECOND_RECRUTEMENT.uuid ? { ...row, responsables: [] } : row)
const TWO_PAGES_OF_RECRUTEMENTS = Array.from({ length: TABLE_PAGE_SIZE + 1 }, (_, index) => ({
  ...FIRST_RECRUTEMENT,
  uuid: `rec-page-${index}`,
  intitule: `Recrutement ${index}`,
}))

const RESPONSABLE_ASSIGNABLE = makeUser([
  { ...USER_ORGANISME, authorized_actions: ['set_recrutements_responsable'] },
])

async function submitAssignment(user: ReturnType<typeof setupUser>) {
  const drawer = within(await screen.findByRole('dialog', { name: 'Assigner un responsable' }))
  await user.type(drawer.getByRole('searchbox', { name: /Responsable/ }), `${AGENT_RECHERCHE.email}{Enter}`)
  await user.click(await drawer.findByRole('button', { name: 'Assigner un responsable' }))
}

async function assignResponsableTo(user: ReturnType<typeof setupUser>, intitule: string) {
  await user.click(await screen.findByRole('button', { name: `Assigner un responsable à ${intitule}` }))
  await submitAssignment(user)
}

async function openAssignmentFor(user: ReturnType<typeof setupUser>) {
  await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })
  await user.click(await screen.findByRole('checkbox', { name: `Sélectionner ${FIRST_RECRUTEMENT.intitule}` }))
  await user.click(screen.getByRole('button', { name: 'Assigner un responsable' }))
}

describe('recrutementsActifsView', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockResolvedValue(RESPONSABLE_ASSIGNABLE)
    vi.mocked(searchAgentByEmail).mockResolvedValue(AGENT_RECHERCHE)
  })

  it('starts a new search each time the assignment drawer opens', async () => {
    const user = setupUser()
    await openAssignmentFor(user)

    await user.type(await screen.findByRole('searchbox', { name: /Responsable/ }), `${AGENT_RECHERCHE.email}{Enter}`)
    await screen.findByText('Jeanne Dupont')
    await user.click(screen.getByRole('button', { name: 'Annuler' }))
    await user.click(screen.getByRole('button', { name: 'Assigner un responsable' }))

    expect(await screen.findByRole('searchbox', { name: /Responsable/ })).toHaveValue('')
    expect(screen.queryByText('Jeanne Dupont')).not.toBeInTheDocument()
  })

  it('closes the assignment drawer once the last offer is removed', async () => {
    const user = setupUser()
    await openAssignmentFor(user)

    await user.click(await screen.findByRole('button', { name: `Retirer ${FIRST_RECRUTEMENT.intitule} de la sélection` }))

    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Assigner un responsable' })).not.toBeInTheDocument())
  })

  it('counts the selected offers kept on other pages', async () => {
    server.use(recrutementsActifs(TWO_PAGES_OF_RECRUTEMENTS))
    const user = setupUser()
    await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })
    await user.click(await screen.findByRole('checkbox', { name: 'Sélectionner Recrutement 0' }))
    await user.click(screen.getByRole('checkbox', { name: 'Sélectionner Recrutement 1' }))
    expect(screen.queryByText(/sur d’autres pages/)).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Page suivante' }))

    expect(await screen.findByText('dont 2 sur d’autres pages')).toBeInTheDocument()
  })

  it('assigns a responsable to the only offer of the row, leaving the selection aside', async () => {
    const user = setupUser()
    const sent = vi.fn()
    server.use(
      recrutementsActifs(SECOND_WITHOUT_RESPONSABLE),
      responsableAssignment({ reussites: [SECOND_RECRUTEMENT.uuid], echecs: [] }, sent),
    )
    await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })

    await user.click(await screen.findByRole('checkbox', { name: `Sélectionner ${FIRST_RECRUTEMENT.intitule}` }))
    await assignResponsableTo(user, SECOND_RECRUTEMENT.intitule)

    await vi.waitFor(() => expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, {
      recrutement_ids: [SECOND_RECRUTEMENT.uuid],
      agent_id: AGENT_RECHERCHE.uuid,
    }))
  })

  it('announces a partial assignment when the backend skips a recrutement', async () => {
    const user = setupUser()
    server.use(responsableAssignment({
      reussites: [FIRST_RECRUTEMENT.uuid],
      echecs: [{ recrutement_uuid: SECOND_RECRUTEMENT.uuid, raison: 'archive' }],
    }))
    await renderWithApp(withToaster(RouterView), { route: RECRUTEMENTS_PATH })
    await user.click(await screen.findByRole('checkbox', { name: `Sélectionner ${FIRST_RECRUTEMENT.intitule}` }))
    await user.click(screen.getByRole('checkbox', { name: `Sélectionner ${SECOND_RECRUTEMENT.intitule}` }))
    await user.click(screen.getByRole('button', { name: 'Assigner un responsable' }))
    await submitAssignment(user)

    expect(await screen.findByText('Assignation partielle')).toBeInTheDocument()
    expect(screen.getByText(/est responsable de 1 recrutement, 1 recrutement ignoré\./)).toBeInTheDocument()
  })

  it('hides the responsable assignment without the right to assign one', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([USER_ORGANISME]))
    server.use(recrutementsActifs(RECRUTEMENTS_ACTIFS.map(row => ({ ...row, responsables: [] }))))
    await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })

    await screen.findByText(FIRST_RECRUTEMENT.intitule)
    expect(screen.queryByRole('checkbox')).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Assigner un responsable/ })).not.toBeInTheDocument()
  })

  it('shows the assigned responsable on the row of the recrutement', async () => {
    const user = setupUser()
    const assigned = SECOND_WITHOUT_RESPONSABLE.map(row => row.uuid === SECOND_RECRUTEMENT.uuid ? { ...row, responsables: [{ nom: 'Jeanne Dupont' }] } : row)
    server.use(
      recrutementsActifs(SECOND_WITHOUT_RESPONSABLE),
      responsableAssignment({ reussites: [SECOND_RECRUTEMENT.uuid], echecs: [] }, () => server.use(recrutementsActifs(assigned))),
    )
    await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })

    await assignResponsableTo(user, SECOND_RECRUTEMENT.intitule)

    await vi.waitFor(() => expect(screen.getByRole('row', { name: new RegExp(SECOND_RECRUTEMENT.intitule) })).toHaveTextContent('Jeanne Dupont'))
  })

  it('shows the assigned responsable in the équipe of the recrutement', async () => {
    vi.mocked(getEquipeRecrutement).mockReset().mockResolvedValueOnce([]).mockResolvedValue([MEMBRE_EQUIPE])
    server.use(
      recrutementsActifs([{ ...SECOND_RECRUTEMENT, uuid: RECRUTEMENT_UUID, responsables: [] }]),
      recrutementDetail({ ...RECRUTEMENT_DETAIL, authorized_actions: ['list_recrutement_agents'] }),
    )
    const user = setupUser()
    const { router } = await renderWithApp(RouterView, { route: EQUIPE_PATH })
    await screen.findByText('Aucun membre rattaché à ce recrutement.')

    await router.push(RECRUTEMENTS_PATH)
    await assignResponsableTo(user, SECOND_RECRUTEMENT.intitule)
    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Assigner un responsable' })).not.toBeInTheDocument())
    await router.push(EQUIPE_PATH)

    expect(await screen.findByText(MEMBRE_EQUIPE.email)).toBeInTheDocument()
  })

  it('shows the assigned responsable among the agents of the organisme', async () => {
    vi.mocked(getOrganismeDetail).mockResolvedValue({ ...ORGANISME_DETAIL, uuid: ORGANISME_UUID })
    vi.mocked(getOrganismeAgents).mockReset().mockResolvedValueOnce([]).mockResolvedValue([AGENT_ORGANISME])
    server.use(recrutementsActifs(SECOND_WITHOUT_RESPONSABLE))
    const user = setupUser()
    const { router } = await renderWithApp(RouterView, { route: ORGANISME_PATH })
    await screen.findByText('0 compte utilisateur')

    await router.push(RECRUTEMENTS_PATH)
    await assignResponsableTo(user, SECOND_RECRUTEMENT.intitule)
    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Assigner un responsable' })).not.toBeInTheDocument())
    await router.push(ORGANISME_PATH)

    expect(await screen.findByRole('row', { name: /Dupont Jeanne/ })).toBeInTheDocument()
  })
})
