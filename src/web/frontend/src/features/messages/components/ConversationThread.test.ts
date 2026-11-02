import { PiniaColada } from '@pinia/colada'
import { render, screen } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { getConversationMessages } from '../api'
import ConversationThread from './ConversationThread.vue'

vi.mock('../api', () => ({
  getConversationMessages: vi.fn(),
}))

const CANDIDATURE = {
  organismeUuid: '00000000-0000-0000-0000-000000000000',
  recrutementUuid: 'aaaaaaaa-0001-0001-0001-000000000001',
  candidatureUuid: 'dddddddd-0001-0001-0001-000000000001',
}
const CONVERSATION_UUID = 'ffffffff-0001-0001-0001-000000000001'
const DOCUMENT_UUID = 'eeeeeeee-0001-0001-0001-000000000001'

function renderThread() {
  return render(ConversationThread, {
    global: { plugins: [createPinia(), PiniaColada] },
    props: { candidature: CANDIDATURE, conversationUuid: CONVERSATION_UUID },
  })
}

describe('conversationThread', () => {
  beforeEach(() => {
    vi.mocked(getConversationMessages).mockReset()
  })

  it('reports a failed load instead of an empty thread', async () => {
    vi.mocked(getConversationMessages).mockRejectedValue(new HttpError(500, 'Server Error', undefined))

    renderThread()

    expect(await screen.findByText('Impossible de charger les messages')).toBeInTheDocument()
    expect(screen.queryByRole('list')).not.toBeInTheDocument()
  })

  it('opens an attachment in a new tab', async () => {
    vi.mocked(getConversationMessages).mockResolvedValue({
      next: null,
      previous: null,
      results: [{
        content: 'Voici le document',
        author: 'Alice Dupont',
        created_at: '2026-10-20T10:00:00Z',
        documents: [{ uuid: DOCUMENT_UUID, nom: 'Diplome.pdf', type: 'piece_justificative', content_type: 'application/pdf', taille: 1024 }],
      }],
    })

    renderThread()

    const link = await screen.findByRole('link', { name: 'Ouvrir Diplome.pdf' })
    expect(link).toHaveAttribute('href', expect.stringMatching(new RegExp(`/documents/${DOCUMENT_UUID}$`)))
    expect(link).toHaveAttribute('target', '_blank')
  })
})
