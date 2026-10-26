import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { CANDIDATURE_PARAMS, KANBAN_PATH } from '@/test/fixtures/candidatures'
import { renderWithApp, setupUser } from '@/test/render'
import CandidatureNoteEditor from './CandidatureNoteEditor.vue'

const NEW_NOTE_PATH = `${KANBAN_PATH}/candidatures/${CANDIDATURE_PARAMS.candidatureUuid}/notes/nouvelle`

describe('candidatureNoteEditor', () => {
  it('only allows saving once the initial message has changed', async () => {
    const user = setupUser()
    await renderWithApp(CandidatureNoteEditor, {
      route: NEW_NOTE_PATH,
      props: {
        title: 'Modifier la note',
        routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.notes,
        submitting: false,
        submit: vi.fn(),
        initialMessage: 'Profil solide',
      },
    })
    const submit = screen.getByRole('button', { name: 'Enregistrer la note' })

    expect(submit).toBeDisabled()

    await user.type(screen.getByRole('textbox', { name: 'Modifier la note' }), ' et motivé')

    expect(submit).toBeEnabled()
  })
})
