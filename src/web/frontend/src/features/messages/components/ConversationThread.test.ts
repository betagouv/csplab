import { PiniaColada } from '@pinia/colada'
import { render, screen } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { describe, expect, it } from 'vitest'
import { CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { CONVERSATION_UUID, MESSAGE } from '@/test/fixtures/messages'
import { conversationMessages, conversationMessagesFailure } from '@/test/handlers/messages'
import { server } from '@/test/server'
import ConversationThread from './ConversationThread.vue'

const DOCUMENT_UUID = 'eeeeeeee-0001-0001-0001-000000000001'

function renderThread() {
  return render(ConversationThread, {
    global: { plugins: [createPinia(), PiniaColada] },
    props: { candidature: CANDIDATURE_PARAMS, conversationUuid: CONVERSATION_UUID },
  })
}

describe('conversationThread', () => {
  it('reports a failed load instead of an empty thread', async () => {
    server.use(conversationMessagesFailure(500))

    renderThread()

    expect(await screen.findByText('Impossible de charger les messages')).toBeInTheDocument()
    expect(screen.queryByRole('list')).not.toBeInTheDocument()
  })

  it('opens an attachment in a new tab', async () => {
    server.use(conversationMessages([{
      ...MESSAGE,
      documents: [{ uuid: DOCUMENT_UUID, nom: 'Diplome.pdf', type: 'piece_justificative', content_type: 'application/pdf', taille: 1024 }],
    }]))

    renderThread()

    const link = await screen.findByRole('link', { name: 'Ouvrir Diplome.pdf' })
    expect(link).toHaveAttribute('href', expect.stringMatching(new RegExp(`/documents/${DOCUMENT_UUID}$`)))
    expect(link).toHaveAttribute('target', '_blank')
  })
})
