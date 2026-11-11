import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { CANDIDATURE_PARAMS, KANBAN_PATH } from '@/test/fixtures/candidatures'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { createCandidatureNote } from '../api'
import CandidatureNewNoteForm from './CandidatureNewNoteForm.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  createCandidatureNote: vi.fn(),
}))

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
    vi.mocked(createCandidatureNote).mockResolvedValue()
    const { user, router, field, submit } = await renderForm()

    await user.type(field, '  Profil solide  ')
    await user.click(submit)

    expect(createCandidatureNote).toHaveBeenCalledWith(CANDIDATURE_PARAMS, { message: 'Profil solide', est_privee: false })
    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(NOTES_PATH))
    expect(await screen.findByRole('heading', { name: 'Note enregistrée' })).toBeInTheDocument()
  })

  it('keeps the typed note when the creation fails', async () => {
    vi.mocked(createCandidatureNote).mockRejectedValue(new HttpError(500, 'Server Error', undefined))
    const { user, router, field, submit } = await renderForm()

    await user.type(field, 'Profil solide')
    await user.click(submit)

    expect(await screen.findByRole('heading', { name: 'L\'enregistrement de la note a échoué' })).toBeInTheDocument()
    expect(router.currentRoute.value.path).toBe(NEW_NOTE_PATH)
    expect(field).toHaveValue('Profil solide')
  })
})
