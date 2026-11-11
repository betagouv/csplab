import type { Note } from '../types'
import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { getTags } from '@/features/tags/api'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { CANDIDATURE_PARAMS, KANBAN_PATH } from '@/test/fixtures/candidatures'
import { TAG_INTERVIEW, TAG_SYNTHESIS, TAG_TO_RECALL } from '@/test/fixtures/tags'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { addCandidatureNoteTag, deleteCandidatureNote, getCandidatureNotes, removeCandidatureNoteTag, updateCandidatureNote, updateCandidatureNoteVisibilite } from '../api'
import CandidatureNotes from './CandidatureNotes.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  getCandidatureNotes: vi.fn(),
  updateCandidatureNote: vi.fn(),
  deleteCandidatureNote: vi.fn(),
  updateCandidatureNoteVisibilite: vi.fn(),
  addCandidatureNoteTag: vi.fn(),
  removeCandidatureNoteTag: vi.fn(),
}))

vi.mock('@/features/tags/api', () => ({
  getTags: vi.fn(),
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
    authorized_actions: ['update_note', 'delete_note'],
    tags: [],
    ...overrides,
  }
}

const NOTES_PATH = `${KANBAN_PATH}/candidatures/${CANDIDATURE_PARAMS.candidatureUuid}/notes`

async function openTagPicker() {
  vi.mocked(getTags).mockResolvedValue([TAG_INTERVIEW, TAG_SYNTHESIS, TAG_TO_RECALL])
  const user = setupUser()
  await renderNotes()
  await user.click(await screen.findByRole('button', { name: 'Actions sur la note de Marie Dupont' }))
  await user.click(await screen.findByRole('menuitem', { name: 'Ajouter une étiquette' }))
  const picker = await screen.findByRole('dialog', { name: 'Ajouter une étiquette' })
  await within(picker).findByRole('list', { name: 'Étiquettes' })
  return { user, picker }
}

const Host = withToaster(CandidatureNotes, { candidature: CANDIDATURE_PARAMS, routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.notes })

function renderNotes(route = NOTES_PATH) {
  return renderWithApp(Host, { route })
}

describe('candidatureNotes', () => {
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

  it('offers no action on a note the user cannot change', async () => {
    const results = [
      note({}),
      note({ uuid: 'ffffffff-0001-0001-0001-000000000002', publie_par_prenom: 'Paul', publie_par_nom: 'Bernard', authorized_actions: [] }),
    ]
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 2, results })
    await renderNotes()

    expect(await screen.findByRole('button', { name: 'Actions sur la note de Marie Dupont' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Actions sur la note de Paul Bernard' })).not.toBeInTheDocument()
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

  it('adds a note tag from the picker of the note menu and keeps the picker open', async () => {
    vi.mocked(getCandidatureNotes)
      .mockResolvedValueOnce({ count: 1, results: [note({ tags: [TAG_INTERVIEW] })] })
      .mockResolvedValue({ count: 1, results: [note({ tags: [TAG_INTERVIEW, TAG_SYNTHESIS] })] })
    vi.mocked(addCandidatureNoteTag).mockResolvedValue()
    const { user, picker } = await openTagPicker()

    const rows = within(within(picker).getByRole('list', { name: 'Étiquettes' })).getAllByRole('listitem')
    expect(rows.map(row => row.textContent?.trim())).toEqual(['EntretienDéjà ajoutée', 'SynthèseAjouter'])
    expect(within(picker).getByRole('button', { name: 'L\'étiquette Entretien est déjà ajoutée' })).toBeDisabled()

    await user.click(within(picker).getByRole('button', { name: 'Ajouter l\'étiquette Synthèse' }))

    expect(addCandidatureNoteTag).toHaveBeenCalledWith({ ...CANDIDATURE_PARAMS, noteUuid: note({}).uuid, tagUuid: TAG_SYNTHESIS.uuid })
    expect(await within(picker).findByRole('button', { name: 'L\'étiquette Synthèse est déjà ajoutée' })).toBeDisabled()
  })

  it('filters the tags of the picker by name, accents ignored', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 1, results: [note({})] })
    const { user, picker } = await openTagPicker()

    await user.type(within(picker).getByRole('searchbox', { name: 'Rechercher une étiquette' }), 'synthese')

    await vi.waitFor(() => {
      const rows = within(within(picker).getByRole('list', { name: 'Étiquettes' })).getAllByRole('listitem')
      expect(rows.map(row => row.textContent?.trim())).toEqual(['SynthèseAjouter'])
    })
  })

  it('says when no tag matches the search', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 1, results: [note({})] })
    const { user, picker } = await openTagPicker()

    await user.type(within(picker).getByRole('searchbox', { name: 'Rechercher une étiquette' }), 'zzz')

    expect(await within(picker).findByText('Aucune étiquette ne correspond.')).toBeInTheDocument()
  })

  it('offers an empty search when the picker is opened again', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 1, results: [note({})] })
    const { user, picker } = await openTagPicker()

    await user.type(within(picker).getByRole('searchbox', { name: 'Rechercher une étiquette' }), 'synth')
    await user.keyboard('{Escape}')
    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Ajouter une étiquette' })).not.toBeInTheDocument())
    expect(screen.getByRole('button', { name: 'Actions sur la note de Marie Dupont' })).toHaveFocus()

    await user.click(screen.getByRole('button', { name: 'Actions sur la note de Marie Dupont' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Ajouter une étiquette' }))
    const reopened = await screen.findByRole('dialog', { name: 'Ajouter une étiquette' })
    expect(within(reopened).getByRole('searchbox', { name: 'Rechercher une étiquette' })).toHaveValue('')
  })

  it('leaves the focus on the element clicked outside the picker', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 1, results: [note({})] })
    const { user } = await openTagPicker()

    await user.click(screen.getByText('Profil solide'))

    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Ajouter une étiquette' })).not.toBeInTheDocument())
    expect(screen.getByRole('button', { name: 'Actions sur la note de Marie Dupont' })).not.toHaveFocus()
  })

  it('keeps the picker open when a tag cannot be added', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 1, results: [note({})] })
    vi.mocked(addCandidatureNoteTag).mockRejectedValue(new HttpError(500, 'Internal Server Error', undefined))
    const { user, picker } = await openTagPicker()

    await user.click(within(picker).getByRole('button', { name: 'Ajouter l\'étiquette Synthèse' }))

    expect(await screen.findByText('L\'ajout de l\'étiquette a échoué')).toBeInTheDocument()
    expect(picker).toBeInTheDocument()
  })

  it('treats a tag already on the note as added', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 1, results: [note({})] })
    vi.mocked(addCandidatureNoteTag).mockRejectedValue(new HttpError(409, 'Conflict', undefined))
    const { user, picker } = await openTagPicker()

    await user.click(within(picker).getByRole('button', { name: 'Ajouter l\'étiquette Synthèse' }))

    await vi.waitFor(() => expect(addCandidatureNoteTag).toHaveBeenCalledOnce())
    expect(screen.queryByText('L\'ajout de l\'étiquette a échoué')).not.toBeInTheDocument()
  })

  it('warns and closes the picker when the tag or the note was deleted meanwhile', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 1, results: [note({})] })
    vi.mocked(addCandidatureNoteTag).mockRejectedValue(new HttpError(404, 'Not Found', undefined))
    const { user, picker } = await openTagPicker()

    await user.click(within(picker).getByRole('button', { name: 'Ajouter l\'étiquette Synthèse' }))

    expect(await screen.findByText('L\'étiquette ou la note a été supprimée')).toBeInTheDocument()
    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Ajouter une étiquette' })).not.toBeInTheDocument())
  })

  it('removes a tag from a note the user can change', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 1, results: [note({ tags: [TAG_INTERVIEW] })] })
    vi.mocked(removeCandidatureNoteTag).mockResolvedValue()
    const user = setupUser()
    await renderNotes()

    const tags = await screen.findByRole('list', { name: 'Étiquettes de la note de Marie Dupont' })
    expect(within(tags).getByText('Entretien')).toBeInTheDocument()
    await user.click(within(tags).getByRole('button', { name: 'Retirer l\'étiquette Entretien' }))

    expect(removeCandidatureNoteTag).toHaveBeenCalledWith({ ...CANDIDATURE_PARAMS, noteUuid: note({}).uuid, tagUuid: TAG_INTERVIEW.uuid })
  })

  it('refreshes the note without a message when its tag was removed meanwhile', async () => {
    vi.mocked(getCandidatureNotes)
      .mockResolvedValueOnce({ count: 1, results: [note({ tags: [TAG_INTERVIEW] })] })
      .mockResolvedValue({ count: 1, results: [note({})] })
    vi.mocked(removeCandidatureNoteTag).mockRejectedValue(new HttpError(404, 'Not Found', undefined))
    const user = setupUser()
    await renderNotes()

    await user.click(await screen.findByRole('button', { name: 'Retirer l\'étiquette Entretien' }))

    await vi.waitFor(() => expect(screen.queryByRole('list', { name: 'Étiquettes de la note de Marie Dupont' })).not.toBeInTheDocument())
    expect(screen.queryByText('Le retrait de l\'étiquette a échoué')).not.toBeInTheDocument()
  })

  it('says when a tag cannot be removed', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 1, results: [note({ tags: [TAG_INTERVIEW] })] })
    vi.mocked(removeCandidatureNoteTag).mockRejectedValue(new HttpError(500, 'Internal Server Error', undefined))
    const user = setupUser()
    await renderNotes()

    await user.click(await screen.findByRole('button', { name: 'Retirer l\'étiquette Entretien' }))

    expect(await screen.findByText('Le retrait de l\'étiquette a échoué')).toBeInTheDocument()
  })

  it('shows the tags of a note the user cannot change without a way to remove them', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 1, results: [note({ tags: [TAG_INTERVIEW], authorized_actions: [] })] })
    await renderNotes()

    const tags = await screen.findByRole('list', { name: 'Étiquettes de la note de Marie Dupont' })
    expect(within(tags).getByText('Entretien')).toBeInTheDocument()
    expect(within(tags).queryByRole('button')).not.toBeInTheDocument()
  })
})
