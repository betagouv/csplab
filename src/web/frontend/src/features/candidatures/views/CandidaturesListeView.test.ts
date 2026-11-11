import type { CandidatureListe } from '../types'
import { screen, within } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { TABLE_PAGE_SIZE } from '@/components/base/CspDataTable/table'
import {
  CANDIDATURE_ALICE,
  CANDIDATURE_BRUNO,
  CANDIDATURE_LISTE,
  candidatureDetail,
  ETAPE_ENTRETIEN,
  etapeChangeBody,
  KANBAN_PATH,
  makeCandidatureRow,
  ORGANISME_UUID,
  RECRUTEMENT_UUID,
  roleOnOrganisme,
} from '@/test/fixtures/candidatures'
import { CONVERSATION } from '@/test/fixtures/messages'
import { RECRUTEMENTS_ACTIFS } from '@/test/fixtures/recrutements'
import { makeUser } from '@/test/fixtures/utilisateur'
import { candidature, candidatureListe, candidatureListeFailure, etapeChange, etapeChangeFailure } from '@/test/handlers/candidatures'
import { conversationMessages, conversations } from '@/test/handlers/messages'
import { recrutementsActifs } from '@/test/handlers/recrutements'
import { renderWithApp, setupUser } from '@/test/render'
import { server } from '@/test/server'

const LISTE_PATH = `${KANBAN_PATH}/liste`
const RECRUTEMENTS_PATH = `/organismes/${ORGANISME_UUID}/recrutements`

async function renderListe() {
  const { router } = await renderWithApp(RouterView, { route: LISTE_PATH })
  await screen.findByText(/^\d+ candidatures$/)
  const table = within(screen.getByRole('table', { name: 'Candidatures' }))
  await table.findAllByRole('link')
  return { router, table }
}

const ROW_COUNT = TABLE_PAGE_SIZE + 1

function twoPagesOfRows() {
  return Array.from({ length: ROW_COUNT }, (_, index) => makeCandidatureRow(index))
}

function listeOf(rows: CandidatureListe[]) {
  return candidatureListe({ ...CANDIDATURE_LISTE, count: rows.length, results: rows })
}

function serveTwoPagesOfRows() {
  server.use(listeOf(twoPagesOfRows()), candidature(candidatureUuid => ({ ...candidatureDetail(CANDIDATURE_ALICE), uuid: candidatureUuid })))
}

async function changeEtapeToEntretien(user: ReturnType<typeof setupUser>) {
  await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))
  await user.click(await screen.findByRole('radio', { name: 'Entretien' }))
  await user.click(screen.getByRole('button', { name: 'Valider' }))
}

function sequenceNavigation() {
  return screen.findByRole('navigation', { name: 'Navigation entre les candidatures de la liste' })
}

describe('candidaturesListeView', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
  })

  it('opens the candidature beside the list and marks its row', async () => {
    const user = setupUser()
    const { router, table } = await renderListe()

    await user.click(table.getByRole('link', { name: 'Alice Dupont' }))

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(`${LISTE_PATH}/candidatures/${CANDIDATURE_ALICE}`))
    expect(await screen.findByRole('dialog')).toBeInTheDocument()
    expect(table.getByRole('row', { name: /Alice Dupont/, hidden: true })).toHaveAttribute('aria-current', 'true')
    expect(table.getByRole('row', { name: /Bruno Martin/, hidden: true })).not.toHaveAttribute('aria-current')
  })

  it('shows the rows matching the search of the candidatures tab', async () => {
    const user = setupUser()
    const { table } = await renderListe()

    await user.type(screen.getByRole('searchbox', { name: 'Rechercher un candidat' }), 'Bruno{Enter}')

    await vi.waitFor(() => expect(table.queryByRole('link', { name: 'Alice Dupont' })).not.toBeInTheDocument())
    expect(table.getByRole('link', { name: 'Bruno Martin' })).toBeInTheDocument()
  })

  it('offers in the filters the stages of the list', async () => {
    const etapeAjoutee = { uuid: 'eeeeeeee-0001-0001-0001-000000000009', nom: 'Visite', categorie: 'EN_COURS' as const }
    server.use(candidatureListe({ ...CANDIDATURE_LISTE, etapes: [...CANDIDATURE_LISTE.etapes, etapeAjoutee] }))
    const user = setupUser()
    await renderListe()

    await user.click(screen.getByRole('button', { name: 'Filtres' }))

    expect((await screen.findAllByRole('checkbox', { name: 'Visite' })).length).toBeGreaterThan(0)
  })

  it('shows an error when the list fails to load', async () => {
    server.use(candidatureListeFailure(500))
    await renderWithApp(RouterView, { route: LISTE_PATH })

    expect(await screen.findByText('Une erreur est survenue lors du chargement des candidatures.')).toBeInTheDocument()
    expect(screen.queryByText(/^\d+ candidatures?$/)).not.toBeInTheDocument()
    expect(screen.getByRole('radio', { name: /Liste/ })).toBeInTheDocument()
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
    serveTwoPagesOfRows()
    const user = setupUser()
    const { table } = await renderListe()

    await user.click(table.getByRole('link', { name: `Candidat ${TABLE_PAGE_SIZE} Dupont` }))
    await user.click(within(await sequenceNavigation()).getByRole('button', { name: 'Suivant' }))

    expect(await table.findByRole('link', { name: `Candidat ${ROW_COUNT} Dupont`, hidden: true })).toBeInTheDocument()
  })

  it('opens the next candidature of the list after changing a stage, even when the list reorders', async () => {
    const [first, second, third] = [0, 1, 2].map(makeCandidatureRow)
    const others = twoPagesOfRows().slice(3)
    const sent = vi.fn()
    serveTwoPagesOfRows()
    server.use(etapeChange({ reussites: [third.uuid], echecs: [] }, (...args) => {
      sent(...args)
      server.use(listeOf([{ ...third, date_derniere_activite: '2025-06-20T10:00:00Z' }, first, second, ...others]))
    }))
    const user = setupUser()
    const { router, table } = await renderListe()

    await user.click(table.getByRole('button', { name: 'Dernière activité' }))
    await user.click(table.getByRole('button', { name: 'Dernière activité' }))
    await user.click(table.getByRole('link', { name: 'Candidat 3 Dupont' }))
    await changeEtapeToEntretien(user)

    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(makeCandidatureRow(3).uuid))
    await vi.waitFor(() => expect(table.getAllByRole('row', { hidden: true })[1]).toHaveAccessibleName(/Candidat 3 Dupont/))
    expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, etapeChangeBody(ETAPE_ENTRETIEN, [third.uuid]))
    const navigation = within(await sequenceNavigation())
    expect(await navigation.findByText(`Candidature 4 sur ${ROW_COUNT}`)).toBeInTheDocument()
    await user.click(navigation.getByRole('button', { name: 'Suivant' }))
    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(makeCandidatureRow(4).uuid))
  })

  it('shows the new stage of a moved candidature while the move is sent, and puts it back once the server rejects it', async () => {
    let reject!: () => void
    const loads = vi.fn()
    server.use(
      candidatureListe(CANDIDATURE_LISTE, loads),
      etapeChangeFailure(500, () => new Promise((resolve) => {
        reject = resolve
      })),
    )
    const user = setupUser()
    const { router, table } = await renderListe()
    const aliceRow = () => within(table.getByRole('row', { name: /Alice Dupont/, hidden: true }))

    await user.click(table.getByRole('link', { name: 'Alice Dupont' }))
    await changeEtapeToEntretien(user)
    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_BRUNO))
    const navigation = within(await sequenceNavigation())
    await user.click(navigation.getByRole('button', { name: 'Précédent' }))

    expect(await navigation.findByText('Étape : Entretien')).toBeInTheDocument()
    expect(aliceRow().getByText('Entretien')).toBeInTheDocument()

    await vi.waitFor(() => expect(reject).toBeDefined())
    reject()

    expect(await navigation.findByText('Étape : Réception des candidatures')).toBeInTheDocument()
    expect(aliceRow().getByText('Réception des candidatures')).toBeInTheDocument()
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))
  })

  it('closes the last candidature after changing its stage and keeps the page of the list', async () => {
    const rows = twoPagesOfRows()
    const last = makeCandidatureRow(TABLE_PAGE_SIZE)
    let respond!: () => void
    serveTwoPagesOfRows()
    server.use(etapeChange({ reussites: [last.uuid], echecs: [] }, () => new Promise((resolve) => {
      respond = () => {
        server.use(listeOf([last, ...rows.slice(0, TABLE_PAGE_SIZE)]))
        resolve()
      }
    })))
    const user = setupUser()
    const { router, table } = await renderListe()

    await user.click(screen.getByRole('button', { name: 'Page suivante' }))
    await user.click(await table.findByRole('link', { name: `Candidat ${ROW_COUNT} Dupont` }))
    await changeEtapeToEntretien(user)

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(LISTE_PATH))
    await vi.waitFor(() => expect(respond).toBeDefined())
    respond()
    expect(await table.findByRole('link', { name: `Candidat ${TABLE_PAGE_SIZE} Dupont` })).toBeInTheDocument()
    expect(table.queryByRole('link', { name: 'Candidat 1 Dupont' })).not.toBeInTheDocument()
  })

  it('keeps the sort of the list after a visit to the kanban', async () => {
    const user = setupUser()
    const { router, table } = await renderListe()

    await user.click(table.getByRole('button', { name: 'Dernière activité' }))
    await router.push(KANBAN_PATH)
    await router.push(LISTE_PATH)

    const sorted = within(await screen.findByRole('table', { name: 'Candidatures' }))
    expect(sorted.getByRole('columnheader', { name: 'Dernière activité' })).toHaveAttribute('aria-sort', 'ascending')
  })

  it('resets the sort of the list when another recrutement opens', async () => {
    const user = setupUser()
    const { router, table } = await renderListe()

    await user.click(table.getByRole('button', { name: 'Dernière activité' }))
    await router.push(`/organismes/${ORGANISME_UUID}/recrutements/aaaaaaaa-0001-0001-0001-000000000002/liste`)

    await vi.waitFor(() => expect(screen.getByRole('columnheader', { name: 'Dernière activité' })).not.toHaveAttribute('aria-sort', 'ascending'))
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

  it('updates the unread conversations of the candidature and of its recrutement once a conversation is read', async () => {
    const results = CANDIDATURE_LISTE.results.map(row => row.uuid === CANDIDATURE_ALICE ? { ...row, unread_conversations: 1 } : row)
    const [premier] = RECRUTEMENTS_ACTIFS
    const recrutement = { ...premier, uuid: RECRUTEMENT_UUID, intitule: 'Chargé de mission' }
    server.use(
      candidatureListe({ ...CANDIDATURE_LISTE, results }),
      recrutementsActifs([{ ...recrutement, unread_conversations: 1 }]),
      conversations([{ ...CONVERSATION, is_unread: true }]),
      conversationMessages(undefined, () => server.use(recrutementsActifs([recrutement]), candidatureListe())),
    )
    const user = setupUser()
    const { router } = await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })
    const recrutementRow = () => screen.findByRole('row', { name: /Chargé de mission/ })
    await within(await recrutementRow()).findByText('1 conversation non lue')
    await router.push(`${LISTE_PATH}/candidatures/${CANDIDATURE_ALICE}/messages`)
    const aliceRow = () => screen.findByRole('row', { name: /Alice Dupont/, hidden: true })
    await within(await aliceRow()).findByText('1 conversation non lue')

    await user.click(await screen.findByRole('link', { name: /Convocation/ }))

    expect(await within(await aliceRow()).findByText('Aucune conversation non lue')).toBeInTheDocument()
    await router.push(RECRUTEMENTS_PATH)
    expect(await within(await recrutementRow()).findByText('Aucune conversation non lue')).toBeInTheDocument()
  })
})
