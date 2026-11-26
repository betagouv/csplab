import { PiniaColada } from '@pinia/colada'
import { render, screen } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_ALICE, CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { noteCreation, noteCreationFailure } from '@/test/handlers/candidatures'
import { setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import CandidatureNoteForm from './CandidatureNoteForm.vue'

function renderForm() {
  render(withToaster(CandidatureNoteForm, { candidature: CANDIDATURE_PARAMS }), {
    global: { plugins: [createPinia(), PiniaColada] },
  })
  return {
    field: screen.getByRole('textbox', { name: 'Ajouter une note' }),
    submit: screen.getByRole('button', { name: 'Enregistrer la note' }),
  }
}

describe('candidatureNoteForm', () => {
  it('keeps the save button inactive while the note is empty', async () => {
    const user = setupUser()
    const { field, submit } = renderForm()

    expect(submit).toBeDisabled()
    await user.type(field, '   ')
    expect(submit).toBeDisabled()
  })

  it('saves the note with its visibility, empties the form and confirms', async () => {
    const sent = vi.fn()
    server.use(noteCreation(sent))
    const user = setupUser()
    const { field, submit } = renderForm()
    const privee = screen.getByRole('checkbox', { name: 'Note privée' })

    await user.type(field, '  Profil solide  ')
    await user.click(privee)
    await user.click(submit)

    await vi.waitFor(() => expect(field).toHaveValue(''))
    expect(privee).not.toBeChecked()
    expect(await screen.findByRole('heading', { name: 'Note enregistrée' })).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(CANDIDATURE_ALICE, { message: 'Profil solide', est_privee: true })
  })

  it('keeps the note when the save fails', async () => {
    server.use(noteCreationFailure(500))
    const user = setupUser()
    const { field, submit } = renderForm()

    await user.type(field, 'Profil solide')
    await user.click(submit)

    expect(await screen.findByRole('heading', { name: 'L\'enregistrement de la note a échoué' })).toBeInTheDocument()
    expect(field).toHaveValue('Profil solide')
  })
})
