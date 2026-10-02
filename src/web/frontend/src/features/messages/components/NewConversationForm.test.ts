import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { useToast } from '@/composables/ui/useToast'
import { renderWithApp, setupUser } from '@/test/render'
import { createConversation } from '../api'
import NewConversationForm from './NewConversationForm.vue'

vi.mock('../api', () => ({
  createConversation: vi.fn(),
}))

const CANDIDATURE = {
  organismeUuid: '00000000-0000-0000-0000-000000000000',
  recrutementUuid: 'aaaaaaaa-0001-0001-0001-000000000001',
  candidatureUuid: 'dddddddd-0001-0001-0001-000000000001',
}

const NEW_CONVERSATION_PATH = `/organismes/${CANDIDATURE.organismeUuid}/recrutements/${CANDIDATURE.recrutementUuid}/candidatures/${CANDIDATURE.candidatureUuid}/messages/nouveau`

describe('newConversationForm', () => {
  it('keeps the typed content when the creation fails', async () => {
    vi.mocked(createConversation).mockRejectedValue(new HttpError(500, 'Server Error', undefined))
    const user = setupUser()
    const { router } = await renderWithApp(NewConversationForm, {
      route: NEW_CONVERSATION_PATH,
      props: { candidature: CANDIDATURE },
    })

    await user.type(screen.getByRole('textbox', { name: /Sujet de la conversation/ }), 'Convocation')
    await user.type(screen.getByRole('textbox', { name: 'Écrivez votre message' }), 'Bonjour')
    await user.click(screen.getByRole('button', { name: 'Envoyer' }))

    await vi.waitFor(() => expect(useToast().toasts.value.at(-1)?.title).toBe('La création de la conversation a échoué'))
    expect(router.currentRoute.value.path).toBe(NEW_CONVERSATION_PATH)
    expect(screen.getByRole('textbox', { name: /Sujet de la conversation/ })).toHaveValue('Convocation')
    expect(screen.getByRole('textbox', { name: 'Écrivez votre message' })).toHaveValue('Bonjour')
  })
})
