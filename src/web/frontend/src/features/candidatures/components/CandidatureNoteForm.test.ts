import { PiniaColada } from '@pinia/colada'
import { render, screen } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { useToast } from '@/composables/ui/useToast'
import { CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { setupUser } from '@/test/render'
import { createCandidatureNote } from '../api'
import CandidatureNoteForm from './CandidatureNoteForm.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  createCandidatureNote: vi.fn(),
}))

function renderForm() {
  render(CandidatureNoteForm, {
    props: { candidature: CANDIDATURE_PARAMS },
    global: { plugins: [createPinia(), PiniaColada] },
  })
  return {
    field: screen.getByRole('textbox', { name: 'Ajouter une note' }),
    submit: screen.getByRole('button', { name: 'Enregistrer la note' }),
  }
}

describe('candidatureNoteForm', () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('keeps the save button inactive while the note is empty', async () => {
    const user = setupUser()
    const { field, submit } = renderForm()

    expect(submit).toBeDisabled()
    await user.type(field, '   ')
    expect(submit).toBeDisabled()
  })

  it('saves the note, empties the field and confirms', async () => {
    vi.mocked(createCandidatureNote).mockResolvedValue()
    const user = setupUser()
    const { field, submit } = renderForm()

    await user.type(field, '  Profil solide  ')
    await user.click(submit)

    expect(createCandidatureNote).toHaveBeenCalledWith(CANDIDATURE_PARAMS, 'Profil solide')
    await vi.waitFor(() => expect(field).toHaveValue(''))
    expect(useToast().toasts.value.at(-1)?.title).toBe('Note enregistrée')
  })

  it('keeps the note when the save fails', async () => {
    vi.mocked(createCandidatureNote).mockRejectedValue(new HttpError(500, 'Internal Server Error', undefined))
    const user = setupUser()
    const { field, submit } = renderForm()

    await user.type(field, 'Profil solide')
    await user.click(submit)

    await vi.waitFor(() => expect(useToast().toasts.value.at(-1)?.title).toBe('L\'enregistrement de la note a échoué'))
    expect(field).toHaveValue('Profil solide')
  })
})
