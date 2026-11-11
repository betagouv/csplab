import { PiniaColada } from '@pinia/colada'
import { render, screen } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { CONVERSATION_UUID } from '@/test/fixtures/messages'
import { reply, replyFailure } from '@/test/handlers/messages'
import { setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import MessageComposer from './MessageComposer.vue'

function renderComposer() {
  render(withToaster(MessageComposer, { candidature: CANDIDATURE_PARAMS, conversationUuid: CONVERSATION_UUID }), {
    global: { plugins: [createPinia(), PiniaColada] },
  })
  return { field: screen.getByRole('textbox', { name: 'Écrivez votre message' }) }
}

describe('messageComposer', () => {
  it('sends the message to the conversation, then clears the draft and confirms', async () => {
    const sent = vi.fn()
    server.use(reply(undefined, (conversationUuid, payload) => sent(conversationUuid, payload.get('content'))))
    const user = setupUser()
    const { field } = renderComposer()

    await user.type(field, 'Merci, à bientôt')
    await user.click(screen.getByRole('button', { name: 'Envoyer' }))

    expect(await screen.findByRole('heading', { name: 'Message envoyé' })).toBeInTheDocument()
    expect(field).toHaveValue('')
    expect(sent).toHaveBeenCalledWith(CONVERSATION_UUID, 'Merci, à bientôt')
  })

  it('keeps the draft when sending fails', async () => {
    server.use(replyFailure(500))
    const user = setupUser()
    const { field } = renderComposer()

    await user.type(field, 'Merci, à bientôt')
    await user.click(screen.getByRole('button', { name: 'Envoyer' }))

    expect(await screen.findByRole('heading', { name: 'L\'envoi du message a échoué' })).toBeInTheDocument()
    expect(field).toHaveValue('Merci, à bientôt')
  })
})
