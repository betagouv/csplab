import { screen } from '@testing-library/vue'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { useToast } from '@/composables/ui/useToast'
import { CANDIDATURE_PARAMS, KANBAN_PATH } from '@/test/fixtures/candidatures'
import { renderWithApp, setupUser } from '@/test/render'
import { createCandidatureNote } from '../api'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '../routes'
import CandidatureNewNoteForm from './CandidatureNewNoteForm.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  createCandidatureNote: vi.fn(),
}))

const NOTES_PATH = `${KANBAN_PATH}/candidatures/${CANDIDATURE_PARAMS.candidatureUuid}/notes`
const NEW_NOTE_PATH = `${NOTES_PATH}/nouvelle`

async function renderForm() {
  const user = setupUser()
  const { router } = await renderWithApp(CandidatureNewNoteForm, {
    route: NEW_NOTE_PATH,
    props: { candidature: CANDIDATURE_PARAMS, routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.notes },
  })
  return {
    user,
    router,
    field: screen.getByRole('textbox', { name: 'Ajouter une note' }),
    submit: screen.getByRole('button', { name: 'Enregistrer la note' }),
  }
}

describe('candidatureNewNoteForm', () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('saves the note and goes back to the notes', async () => {
    vi.mocked(createCandidatureNote).mockResolvedValue()
    const { user, router, field, submit } = await renderForm()

    await user.type(field, '  Profil solide  ')
    await user.click(submit)

    expect(createCandidatureNote).toHaveBeenCalledWith(CANDIDATURE_PARAMS, 'Profil solide')
    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(NOTES_PATH))
    expect(useToast().toasts.value.at(-1)?.title).toBe('Note enregistrée')
  })

  it('keeps the typed note when the creation fails', async () => {
    vi.mocked(createCandidatureNote).mockRejectedValue(new HttpError(500, 'Server Error', undefined))
    const { user, router, field, submit } = await renderForm()

    await user.type(field, 'Profil solide')
    await user.click(submit)

    await vi.waitFor(() => expect(useToast().toasts.value.at(-1)?.title).toBe('L\'enregistrement de la note a échoué'))
    expect(router.currentRoute.value.path).toBe(NEW_NOTE_PATH)
    expect(field).toHaveValue('Profil solide')
  })
})
