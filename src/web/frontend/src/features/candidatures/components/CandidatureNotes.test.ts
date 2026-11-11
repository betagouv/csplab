import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { CANDIDATURE_PARAMS, KANBAN_PATH, NOTE, SECONDE_NOTE } from '@/test/fixtures/candidatures'
import { candidatureNotes, candidatureNotesFailure, noteDeletion, noteUpdate, noteVisibiliteUpdate } from '@/test/handlers/candidatures'
import { renderWithApp, setupUser } from '@/test/render'
import { server } from '@/test/server'
import CandidatureNotes from './CandidatureNotes.vue'

const NOTES_PATH = `${KANBAN_PATH}/candidatures/${CANDIDATURE_PARAMS.candidatureUuid}/notes`

function renderNotes(route = NOTES_PATH) {
  return renderWithApp(CandidatureNotes, {
    route,
    props: { candidature: CANDIDATURE_PARAMS, routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.notes },
  })
}

async function chooseNoteAction(user: ReturnType<typeof setupUser>, action: string) {
  await user.click(await screen.findByRole('button', { name: 'Actions sur la note de Paul Bernard' }))
  await user.click(await screen.findByRole('menuitem', { name: action }))
}

describe('candidatureNotes', () => {
  it('lists the notes with their author and publication date', async () => {
    server.use(candidatureNotes([NOTE, SECONDE_NOTE]))
    await renderNotes()

    expect(await screen.findByRole('heading', { name: '2 notes' })).toBeInTheDocument()
    const [premiere, seconde] = screen.getAllByRole('listitem')
    expect(within(premiere).getByText('Marie Dupont')).toBeInTheDocument()
    expect(within(premiere).getByText('Profil solide')).toBeInTheDocument()
    expect(within(premiere).getByText('10/06/2025 à 09h15')).toBeInTheDocument()
    expect(within(seconde).getByText('Paul Bernard')).toBeInTheDocument()
    expect(within(seconde).getByText('À recontacter')).toBeInTheDocument()
  })

  it('says when the candidature has no note', async () => {
    server.use(candidatureNotes([]))
    await renderNotes()

    expect(await screen.findByText('Aucune note sur cette candidature')).toBeInTheDocument()
  })

  it.each([
    { cas: 'with notes', results: [NOTE] },
    { cas: 'without notes', results: [] },
  ])('opens the note form from the button $cas', async ({ results }) => {
    server.use(candidatureNotes(results))
    const user = setupUser()
    const { router } = await renderNotes()

    await user.click(await screen.findByRole('button', { name: 'Ajouter une note' }))

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(`${NOTES_PATH}/nouvelle`))
    expect(await screen.findByRole('textbox', { name: 'Nouvelle note' })).toBeInTheDocument()
  })

  it('keeps the notes listed while a new note is typed', async () => {
    server.use(candidatureNotes([SECONDE_NOTE]))
    await renderNotes(`${NOTES_PATH}/nouvelle`)

    expect(await screen.findByRole('textbox', { name: 'Nouvelle note' })).toBeInTheDocument()
    expect(await screen.findByText('À recontacter')).toBeInTheDocument()
  })

  it('shows an error when the notes cannot be loaded', async () => {
    server.use(candidatureNotesFailure(500))
    await renderNotes()

    expect(await screen.findByText('Les notes n\'ont pas pu être chargées.')).toBeInTheDocument()
  })

  it('offers no action on a note the user cannot change', async () => {
    server.use(candidatureNotes([NOTE, { ...SECONDE_NOTE, authorized_actions: [] }]))
    await renderNotes()

    expect(await screen.findByRole('button', { name: 'Actions sur la note de Marie Dupont' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Actions sur la note de Paul Bernard' })).not.toBeInTheDocument()
  })

  it('edits the note picked from its menu and keeps it private', async () => {
    const privee = { ...SECONDE_NOTE, est_privee: true }
    const sent = vi.fn()
    server.use(
      candidatureNotes([NOTE, privee]),
      noteUpdate((...args) => {
        sent(...args)
        server.use(candidatureNotes([NOTE, { ...privee, message: 'À recontacter demain' }]))
      }),
    )
    const user = setupUser()
    await renderNotes()

    await chooseNoteAction(user, 'Modifier la note')
    const field = await screen.findByRole('textbox', { name: 'Modifier la note' })
    expect(field).toHaveValue('À recontacter')
    expect(screen.getByRole('checkbox', { name: 'Note privée' })).toBeChecked()

    await user.type(field, ' demain')
    await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))

    expect(await screen.findByText('À recontacter demain')).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(SECONDE_NOTE.uuid, { message: 'À recontacter demain', est_privee: true })
  })

  it('deletes the note picked from its menu once confirmed', async () => {
    const deleted = vi.fn()
    server.use(
      candidatureNotes([NOTE, SECONDE_NOTE]),
      noteDeletion((noteUuid) => {
        deleted(noteUuid)
        server.use(candidatureNotes([NOTE]))
      }),
    )
    const user = setupUser()
    await renderNotes()

    await chooseNoteAction(user, 'Supprimer la note')
    const dialog = await screen.findByRole('dialog', { name: 'Supprimer la note' })
    await user.click(within(dialog).getByRole('button', { name: 'Supprimer la note' }))

    await vi.waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    expect(await screen.findByRole('heading', { name: '1 note' })).toBeInTheDocument()
    expect(deleted).toHaveBeenCalledWith(SECONDE_NOTE.uuid)
  })

  it('makes public the private note picked from its menu', async () => {
    const privee = { ...SECONDE_NOTE, est_privee: true }
    const sent = vi.fn()
    server.use(
      candidatureNotes([NOTE, privee]),
      noteVisibiliteUpdate((...args) => {
        sent(...args)
        server.use(candidatureNotes([NOTE, SECONDE_NOTE]))
      }),
    )
    const user = setupUser()
    await renderNotes()

    await screen.findByText('Privée')
    await chooseNoteAction(user, 'Rendre la note publique')

    await vi.waitFor(() => expect(screen.queryByText('Privée')).not.toBeInTheDocument())
    expect(sent).toHaveBeenCalledWith(SECONDE_NOTE.uuid, { est_privee: false })
  })
})
