import { PiniaColada } from '@pinia/colada'
import { render, screen } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { setupUser, withToaster } from '@/test/render'
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
  render(withToaster(MessageComposer, { candidature: CANDIDATURE, conversationUuid: CONVERSATION_UUID }), {
    global: { plugins: [createPinia(), PiniaColada] },
  })
  return { field: screen.getByRole('textbox', { name: 'Écrivez votre message' }) }
}

describe('messageComposer', () => {
  it('clears the draft and confirms once the message is sent', async () => {
    vi.mocked(replyToConversation).mockResolvedValue({ content: 'Bonjour', author: 'Camille Durand', created_at: '2026-10-01T10:00:00Z', documents: [] })
    const user = setupUser()
    const { field } = renderComposer()

    await user.type(field, 'Bonjour')
    await user.click(screen.getByRole('button', { name: 'Envoyer' }))

    expect(await screen.findByRole('heading', { name: 'Message envoyé' })).toBeInTheDocument()
    expect(field).toHaveValue('')
  })

  it('keeps the draft when sending fails', async () => {
    vi.mocked(replyToConversation).mockRejectedValue(new HttpError(500, 'Server Error', undefined))
    const user = setupUser()
    const { field } = renderComposer()

    await user.type(field, 'Bonjour')
    await user.click(screen.getByRole('button', { name: 'Envoyer' }))

    expect(await screen.findByRole('heading', { name: 'L\'envoi du message a échoué' })).toBeInTheDocument()
    expect(field).toHaveValue('Bonjour')
  })
})
