import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { useToast } from '@/composables/ui/useToast'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/features/candidatures/routes'
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

const CONVERSATION_UUID = 'ffffffff-0001-0001-0001-000000000001'

describe('newConversationForm', () => {
  it('opens the created conversation once it is sent', async () => {
    vi.mocked(createConversation).mockResolvedValue({
      uuid: CONVERSATION_UUID,
      objet: 'Convocation',
      creator: 'Marie Dupont',
      created_at: '2025-06-12T09:00:00Z',
      last_message_content: 'Bonjour',
      last_message_author: 'Marie Dupont',
      last_message_created_at: '2025-06-12T09:00:00Z',
    })
    const user = setupUser()
    const { router } = await renderWithApp(NewConversationForm, {
      route: NEW_CONVERSATION_PATH,
      props: { candidature: CANDIDATURE, routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.conversations },
    })

    await user.type(screen.getByRole('textbox', { name: /Sujet de la conversation/ }), 'Convocation')
    await user.type(screen.getByRole('textbox', { name: 'Écrivez votre message' }), 'Bonjour')
    await user.click(screen.getByRole('button', { name: 'Envoyer' }))

    await vi.waitFor(() => expect(router.currentRoute.value.name).toBe(CANDIDATURE_PANEL_ROUTE_NAMES.kanban.conversations.conversation))
    expect(router.currentRoute.value.params.conversationUuid).toBe(CONVERSATION_UUID)
  })

  it('keeps the typed content when the creation fails', async () => {
    vi.mocked(createConversation).mockRejectedValue(new HttpError(500, 'Server Error', undefined))
    const user = setupUser()
    const { router } = await renderWithApp(NewConversationForm, {
      route: NEW_CONVERSATION_PATH,
      props: { candidature: CANDIDATURE, routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.conversations },
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
