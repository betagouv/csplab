import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { CANDIDATURE_ALICE, CANDIDATURE_PARAMS, KANBAN_PATH } from '@/test/fixtures/candidatures'
import { noteCreation, noteCreationFailure } from '@/test/handlers/candidatures'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import CandidatureNewNoteForm from './CandidatureNewNoteForm.vue'

const NOTES_PATH = `${KANBAN_PATH}/candidatures/${CANDIDATURE_PARAMS.candidatureUuid}/notes`
const NEW_NOTE_PATH = `${NOTES_PATH}/nouvelle`

async function renderForm() {
  const user = setupUser()
  const { router } = await renderWithApp(
    withToaster(CandidatureNewNoteForm, { candidature: CANDIDATURE_PARAMS, routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.notes }),
    { route: NEW_NOTE_PATH },
  )
  return {
    user,
    router,
    field: screen.getByRole('textbox', { name: 'Nouvelle note' }),
    submit: screen.getByRole('button', { name: 'Enregistrer la note' }),
  }
}

describe('candidatureNewNoteForm', () => {
  it('saves the note and goes back to the notes', async () => {
    const sent = vi.fn()
    server.use(noteCreation(sent))
    const { user, router, field, submit } = await renderForm()

    await user.type(field, '  Profil solide  ')
    await user.click(submit)

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(NOTES_PATH))
    expect(await screen.findByRole('heading', { name: 'Note enregistrée' })).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(CANDIDATURE_ALICE, { message: 'Profil solide', est_privee: false })
  })

  it('keeps the typed note when the creation fails', async () => {
    server.use(noteCreationFailure(500))
    const { user, router, field, submit } = await renderForm()

    await user.type(field, 'Profil solide')
    await user.click(submit)

    expect(await screen.findByRole('heading', { name: 'L\'enregistrement de la note a échoué' })).toBeInTheDocument()
    expect(router.currentRoute.value.path).toBe(NEW_NOTE_PATH)
    expect(field).toHaveValue('Profil solide')
  })
})
