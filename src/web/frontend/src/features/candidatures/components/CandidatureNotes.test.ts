import type { Note } from '../types'
import { screen, within } from '@testing-library/vue'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { CANDIDATURE_PARAMS, KANBAN_PATH } from '@/test/fixtures/candidatures'
import { renderWithApp, setupUser } from '@/test/render'
import { deleteCandidatureNote, getCandidatureNotes, updateCandidatureNote, updateCandidatureNoteVisibilite } from '../api'
import CandidatureNotes from './CandidatureNotes.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  getCandidatureNotes: vi.fn(),
  updateCandidatureNote: vi.fn(),
  deleteCandidatureNote: vi.fn(),
  updateCandidatureNoteVisibilite: vi.fn(),
}))

function note(overrides: Partial<Note>): Note {
  return {
    uuid: 'ffffffff-0001-0001-0001-000000000001',
    candidature_id: CANDIDATURE_PARAMS.candidatureUuid,
    message: 'Profil solide',
    publie_par_id: 'eeeeeeee-0001-0001-0001-000000000001',
    publie_par_prenom: 'Marie',
    publie_par_nom: 'Dupont',
    publie_le: '2025-06-10T09:15:00',
    est_privee: false,
    ...overrides,
  }
}

const NOTES_PATH = `${KANBAN_PATH}/candidatures/${CANDIDATURE_PARAMS.candidatureUuid}/notes`

function renderNotes(route = NOTES_PATH) {
  return renderWithApp(CandidatureNotes, {
    route,
    props: { candidature: CANDIDATURE_PARAMS, routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.notes },
  })
}

describe('candidatureNotes', () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('lists the notes with their author and publication date', async () => {
    const results = [
      note({}),
      note({ uuid: 'ffffffff-0001-0001-0001-000000000002', message: 'À recontacter', publie_par_prenom: 'Paul', publie_par_nom: 'Bernard' }),
    ]
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 2, results })
    await renderNotes()

    expect(await screen.findByRole('heading', { name: '2 notes' })).toBeInTheDocument()
    const [premiere, seconde] = screen.getAllByRole('listitem').map(item => within(item))
    expect(premiere!.getByText('Marie Dupont')).toBeInTheDocument()
    expect(premiere!.getByText('Profil solide')).toBeInTheDocument()
    expect(premiere!.getByText('10/06/2025 à 09h15')).toBeInTheDocument()
    expect(seconde!.getByText('Paul Bernard')).toBeInTheDocument()
    expect(seconde!.getByText('À recontacter')).toBeInTheDocument()
  })

  it('says when the candidature has no note', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 0, results: [] })
    await renderNotes()

    expect(await screen.findByText('Aucune note sur cette candidature')).toBeInTheDocument()
  })

  it.each([
    { cas: 'with notes', results: [note({})] },
    { cas: 'without notes', results: [] },
  ])('opens the note form from the button $cas', async ({ results }) => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: results.length, results })
    const user = setupUser()
    const { router } = await renderNotes()

    await user.click(await screen.findByRole('button', { name: 'Ajouter une note' }))

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(`${NOTES_PATH}/nouvelle`))
    expect(await screen.findByRole('textbox', { name: 'Nouvelle note' })).toBeInTheDocument()
  })

  it('keeps the notes listed while a new note is typed', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 1, results: [note({ message: 'À recontacter' })] })
    await renderNotes(`${NOTES_PATH}/nouvelle`)

    expect(await screen.findByRole('textbox', { name: 'Nouvelle note' })).toBeInTheDocument()
    expect(screen.getByText('À recontacter')).toBeInTheDocument()
  })

  it('shows an error when the notes cannot be loaded', async () => {
    vi.mocked(getCandidatureNotes).mockRejectedValue(new HttpError(500, 'Internal Server Error', undefined))
    await renderNotes()

    expect(await screen.findByText('Les notes n\'ont pas pu être chargées.')).toBeInTheDocument()
  })

  it('edits the note picked from its menu and keeps it private', async () => {
    const results = [
      note({}),
      note({ uuid: 'ffffffff-0001-0001-0001-000000000002', message: 'À recontacter', publie_par_prenom: 'Paul', publie_par_nom: 'Bernard', est_privee: true }),
    ]
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 2, results })
    vi.mocked(updateCandidatureNote).mockResolvedValue()
    const user = setupUser()
    await renderNotes()

    await user.click(await screen.findByRole('button', { name: 'Actions sur la note de Paul Bernard' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Modifier la note' }))
    const field = await screen.findByRole('textbox', { name: 'Modifier la note' })
    expect(field).toHaveValue('À recontacter')
    expect(screen.getByRole('checkbox', { name: 'Note privée' })).toBeChecked()

    await user.type(field, ' demain')
    await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))

    expect(updateCandidatureNote).toHaveBeenCalledWith(
      { ...CANDIDATURE_PARAMS, noteUuid: 'ffffffff-0001-0001-0001-000000000002' },
      { message: 'À recontacter demain', est_privee: true },
    )
  })

  it('deletes the note picked from its menu once confirmed', async () => {
    const results = [
      note({}),
      note({ uuid: 'ffffffff-0001-0001-0001-000000000002', publie_par_prenom: 'Paul', publie_par_nom: 'Bernard' }),
    ]
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 2, results })
    vi.mocked(deleteCandidatureNote).mockResolvedValue()
    const user = setupUser()
    await renderNotes()

    await user.click(await screen.findByRole('button', { name: 'Actions sur la note de Paul Bernard' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Supprimer la note' }))
    const dialog = await screen.findByRole('dialog', { name: 'Supprimer la note' })
    await user.click(within(dialog).getByRole('button', { name: 'Supprimer la note' }))

    expect(deleteCandidatureNote).toHaveBeenCalledWith({ ...CANDIDATURE_PARAMS, noteUuid: 'ffffffff-0001-0001-0001-000000000002' })
    await vi.waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
  })

  it('makes public the private note picked from its menu', async () => {
    const results = [
      note({}),
      note({ uuid: 'ffffffff-0001-0001-0001-000000000002', publie_par_prenom: 'Paul', publie_par_nom: 'Bernard', est_privee: true }),
    ]
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 2, results })
    vi.mocked(updateCandidatureNoteVisibilite).mockResolvedValue()
    const user = setupUser()
    await renderNotes()

    await user.click(await screen.findByRole('button', { name: 'Actions sur la note de Paul Bernard' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Rendre la note publique' }))

    expect(updateCandidatureNoteVisibilite).toHaveBeenCalledWith(
      { ...CANDIDATURE_PARAMS, noteUuid: 'ffffffff-0001-0001-0001-000000000002' },
      { est_privee: false },
    )
  })
})
