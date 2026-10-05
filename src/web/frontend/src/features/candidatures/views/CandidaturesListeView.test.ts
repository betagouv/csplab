import { screen, within } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { getConversations } from '@/features/messages/api'
import { getRecrutementDetail } from '@/features/recrutements/api'
import {
  CANDIDATURE_ALICE,
  CANDIDATURE_BRUNO,
  CANDIDATURE_LISTE,
  candidatureDetail,
  ETAPE_ENTRETIEN,
  KANBAN_PATH,
  MOTIFS_REFUS,
  ORGANISME_UUID,
  RECRUTEMENT_DETAIL,
  RECRUTEMENT_UUID,
  roleOnOrganisme,
} from '@/test/fixtures/candidatures'
import { makeUser } from '@/test/fixtures/utilisateur'
import { renderWithApp, setupUser } from '@/test/render'
import { getCandidatureActivites, getCandidatureDetail, getCandidatureListe, getMotifsRefus, patchEtapeCandidatures } from '../api'

vi.mock('../api', () => ({
  getCandidatureDetail: vi.fn(),
  getRecrutementKanban: vi.fn(),
  getCandidatureListe: vi.fn(),
  patchEtapeCandidatures: vi.fn(),
  getMotifsRefus: vi.fn(),
  getCandidatureDocuments: vi.fn(() => new Promise(() => {})),
  candidatureDocumentUrl: vi.fn(),
  getCandidatureNotes: vi.fn(() => new Promise(() => {})),
  createCandidatureNote: vi.fn(),
  getCandidatureActivites: vi.fn(),
}))

vi.mock('@/features/recrutements/api', () => ({
  getRecrutementDetail: vi.fn(),
}))

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

vi.mock('@/features/messages/api', () => ({
  getConversations: vi.fn(),
}))

const LISTE_PATH = `${KANBAN_PATH}/liste`

async function renderListe() {
  const { router } = await renderWithApp(RouterView, { route: LISTE_PATH })
  const table = within(await screen.findByRole('table', { name: 'Candidatures' }))
  await table.findAllByRole('link')
  return { router, table }
}

function mockSevenRows() {
  const [row] = CANDIDATURE_LISTE.results
  const rows = Array.from({ length: 7 }, (_, index) => ({
    ...row!,
    uuid: `dddddddd-0002-0002-0002-00000000000${index + 1}`,
    candidat: { ...row!.candidat, prenom: `Candidat ${index + 1}` },
  }))
  vi.mocked(getCandidatureListe).mockResolvedValue({ ...CANDIDATURE_LISTE, count: rows.length, results: rows })
  vi.mocked(getCandidatureDetail).mockImplementation(async ({ candidatureUuid }) => ({ ...candidatureDetail(CANDIDATURE_ALICE), uuid: candidatureUuid }))
}

function sequenceNavigation() {
  return screen.findByRole('navigation', { name: 'Navigation entre les candidatures de la liste' })
}

describe('candidaturesListeView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    vi.mocked(getCandidatureListe).mockResolvedValue(CANDIDATURE_LISTE)
    vi.mocked(getRecrutementDetail).mockResolvedValue(RECRUTEMENT_DETAIL)
    vi.mocked(getCandidatureDetail).mockImplementation(async ({ candidatureUuid }) => candidatureDetail(candidatureUuid))
    vi.mocked(getMotifsRefus).mockResolvedValue(MOTIFS_REFUS)
    vi.mocked(patchEtapeCandidatures).mockResolvedValue({ reussites: [CANDIDATURE_ALICE], echecs: [] })
    vi.mocked(getConversations).mockResolvedValue({ count: 0, next: null, previous: null, results: [] })
    vi.mocked(getCandidatureActivites).mockResolvedValue({ count: 0, next: null, previous: null, results: [] })
  })

  it('opens the candidature beside the list and marks its row', async () => {
    const user = setupUser()
    const { router, table } = await renderListe()

    await user.click(table.getByRole('link', { name: 'Alice Dupont' }))

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(`${LISTE_PATH}/candidatures/${CANDIDATURE_ALICE}`))
    expect(await screen.findByRole('dialog')).toBeInTheDocument()
    expect(table.getByRole('link', { name: 'Alice Dupont', hidden: true }).closest('tr')).toHaveAttribute('aria-current', 'true')
    expect(table.getByRole('link', { name: 'Bruno Martin', hidden: true }).closest('tr')).not.toHaveAttribute('aria-current')
  })

  it('moves to the next candidature in the sorted order of the list', async () => {
    const user = setupUser()
    const { router, table } = await renderListe()

    await user.click(table.getByRole('button', { name: 'Date candidature' }))
    await user.click(table.getByRole('button', { name: 'Date candidature' }))
    await user.click(table.getByRole('link', { name: 'Bruno Martin' }))
    const navigation = within(await sequenceNavigation())

    expect(await navigation.findByText('Candidature 1 sur 2')).toBeInTheDocument()
    await user.click(navigation.getByRole('button', { name: 'Suivant' }))

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(`${LISTE_PATH}/candidatures/${CANDIDATURE_ALICE}`))
  })

  it('shows the page of the open candidature', async () => {
    mockSevenRows()
    const user = setupUser()
    const { table } = await renderListe()

    await user.click(table.getByRole('link', { name: 'Candidat 6 Dupont' }))
    await user.click(within(await sequenceNavigation()).getByRole('button', { name: 'Suivant' }))

    expect(await table.findByRole('link', { name: 'Candidat 7 Dupont', hidden: true })).toBeInTheDocument()
  })

  it('keeps the page of the open candidature after changing its stage', async () => {
    mockSevenRows()
    const user = setupUser()
    const { table } = await renderListe()

    await user.click(screen.getByRole('button', { name: 'Page suivante' }))
    await user.click(await table.findByRole('link', { name: 'Candidat 7 Dupont' }))
    await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))
    await user.click(await screen.findByRole('radio', { name: 'Entretien' }))
    await user.click(screen.getByRole('button', { name: 'Valider' }))
    await vi.waitFor(() => expect(getCandidatureListe).toHaveBeenCalledTimes(2))

    expect(await table.findByRole('link', { name: 'Candidat 7 Dupont', hidden: true })).toBeInTheDocument()
    expect(table.queryByRole('link', { name: 'Candidat 1 Dupont', hidden: true })).not.toBeInTheDocument()
  })

  it('stays on the candidature after changing its stage', async () => {
    const user = setupUser()
    const { router, table } = await renderListe()

    await user.click(table.getByRole('link', { name: 'Alice Dupont' }))
    const note = await screen.findByRole('textbox', { name: 'Ajouter une note' })
    await user.type(note, 'À rappeler')
    await user.click(screen.getByRole('button', { name: 'Changer d\'étape' }))
    await user.click(await screen.findByRole('radio', { name: 'Entretien' }))
    await user.click(screen.getByRole('button', { name: 'Valider' }))

    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      etapeCibleUuid: ETAPE_ENTRETIEN,
      candidatureUuids: [CANDIDATURE_ALICE],
    }))
    expect(router.currentRoute.value.path).toBe(`${LISTE_PATH}/candidatures/${CANDIDATURE_ALICE}`)
    expect(screen.queryByRole('dialog', { name: 'Modifications non enregistrées' })).not.toBeInTheDocument()
    expect(note).toHaveValue('À rappeler')
  })

  it('closes back to the list and focuses the link of the last candidature shown', async () => {
    const user = setupUser()
    const { router, table } = await renderListe()

    await user.click(table.getByRole('link', { name: 'Alice Dupont' }))
    await user.click(within(await sequenceNavigation()).getByRole('button', { name: 'Suivant' }))
    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_BRUNO))
    await user.click(screen.getByRole('button', { name: 'Fermer la candidature' }))

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(LISTE_PATH))
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    await vi.waitFor(() => expect(table.getByRole('link', { name: 'Bruno Martin' })).toHaveFocus())
  })
})
