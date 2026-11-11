import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { CANDIDATURE_ALICE, CANDIDATURE_PARAMS, KANBAN_PATH } from '@/test/fixtures/candidatures'
import { CONVERSATION_UUID } from '@/test/fixtures/messages'
import { conversationCreation, conversationCreationFailure } from '@/test/handlers/messages'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import NewConversationForm from './NewConversationForm.vue'

const NEW_CONVERSATION_PATH = `${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}/messages/nouveau`

async function writeConversation() {
  const user = setupUser()
  const { router } = await renderWithApp(
    withToaster(NewConversationForm, { candidature: CANDIDATURE_PARAMS, routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.conversations }),
    { route: NEW_CONVERSATION_PATH },
  )

  await user.type(screen.getByRole('textbox', { name: /Sujet de la conversation/ }), 'Convocation')
  await user.type(screen.getByRole('textbox', { name: 'Écrivez votre message' }), 'Bonjour')
  await user.click(screen.getByRole('button', { name: 'Envoyer' }))
  return { router }
}

describe('newConversationForm', () => {
  it('sends the subject and the message, then opens the created conversation and confirms it', async () => {
    const sent = vi.fn()
    server.use(conversationCreation(undefined, (candidatureUuid, payload) =>
      sent(candidatureUuid, payload.get('objet'), payload.get('content'))))

    const { router } = await writeConversation()

    await vi.waitFor(() => expect(router.currentRoute.value.name).toBe(CANDIDATURE_PANEL_ROUTE_NAMES.kanban.conversations.conversation))
    expect(router.currentRoute.value.params.conversationUuid).toBe(CONVERSATION_UUID)
    expect(await screen.findByRole('heading', { name: 'Conversation créée' })).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(CANDIDATURE_ALICE, 'Convocation', 'Bonjour')
  })

  it('keeps the typed content when the creation fails', async () => {
    server.use(conversationCreationFailure(500))

    const { router } = await writeConversation()

    expect(await screen.findByRole('heading', { name: 'La création de la conversation a échoué' })).toBeInTheDocument()
    expect(router.currentRoute.value.path).toBe(NEW_CONVERSATION_PATH)
    expect(screen.getByRole('textbox', { name: /Sujet de la conversation/ })).toHaveValue('Convocation')
    expect(screen.getByRole('textbox', { name: 'Écrivez votre message' })).toHaveValue('Bonjour')
  })
})
