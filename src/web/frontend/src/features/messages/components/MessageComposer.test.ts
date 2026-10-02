import { PiniaColada } from '@pinia/colada'
import { render, screen } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { useToast } from '@/composables/ui/useToast'
import { setupUser } from '@/test/render'
import { replyToConversation } from '../api'
import MessageComposer from './MessageComposer.vue'

vi.mock('../api', () => ({
  replyToConversation: vi.fn(),
}))

const CANDIDATURE = {
  organismeUuid: '00000000-0000-0000-0000-000000000000',
  recrutementUuid: 'aaaaaaaa-0001-0001-0001-000000000001',
  candidatureUuid: 'dddddddd-0001-0001-0001-000000000001',
}
const CONVERSATION_UUID = 'ffffffff-0001-0001-0001-000000000001'

function renderComposer() {
  render(MessageComposer, {
    global: { plugins: [createPinia(), PiniaColada] },
    props: { candidature: CANDIDATURE, conversationUuid: CONVERSATION_UUID },
  })
  return screen.getByRole('textbox', { name: 'Écrivez votre message' })
}

describe('messageComposer', () => {
  beforeEach(() => {
    vi.mocked(replyToConversation).mockReset()
  })

  it('keeps the draft when sending fails', async () => {
    vi.mocked(replyToConversation).mockRejectedValue(new HttpError(500, 'Server Error', undefined))
    const user = setupUser()
    const field = renderComposer()

    await user.type(field, 'Bonjour')
    await user.click(screen.getByRole('button', { name: 'Envoyer' }))

    await vi.waitFor(() => expect(useToast().toasts.value.at(-1)?.title).toBe('L\'envoi du message a échoué'))
    expect(field).toHaveValue('Bonjour')
  })
})
