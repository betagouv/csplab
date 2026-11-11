import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { CANDIDATURE_ALICE, CANDIDATURE_PARAMS, KANBAN_PATH } from '@/test/fixtures/candidatures'
import { CONVERSATION, MESSAGE, REPLY } from '@/test/fixtures/messages'
import { conversations, conversationsFailure, reply } from '@/test/handlers/messages'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import MessagesSection from './MessagesSection.vue'

const MESSAGES_PATH = `${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}/messages`

const AUTRE_CONVERSATION = { ...CONVERSATION, uuid: 'ffffffff-0001-0001-0001-000000000002', objet: 'Pièces justificatives' }

const Host = withToaster(MessagesSection, {
  candidature: CANDIDATURE_PARAMS,
  candidatNom: 'Alice Dupont',
  routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.conversations,
})

function thread() {
  return within(screen.getByRole('region', { name: 'Fil de discussion' }))
}

describe('messagesSection', () => {
  it('reports a failed load instead of showing an empty list', async () => {
    server.use(conversationsFailure(500))

    await renderWithApp(Host, { route: MESSAGES_PATH })

    expect(await screen.findByText('Impossible de charger les conversations')).toBeInTheDocument()
    expect(screen.queryByText('Aucune conversation pour le moment')).not.toBeInTheDocument()
  })

  it('shows the opened conversation as read once its messages are loaded', async () => {
    server.use(conversations([{ ...CONVERSATION, is_unread: true }, { ...AUTRE_CONVERSATION, is_unread: true }]))

    const user = setupUser()
    await renderWithApp(Host, { route: MESSAGES_PATH })

    await user.click(await screen.findByRole('link', { name: /Convocation/ }))

    expect(await thread().findByText(MESSAGE.content)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Convocation/ })).not.toHaveTextContent('Non lue')
    expect(screen.getByRole('link', { name: /Pièces justificatives/ })).toHaveTextContent('Non lue')
  })

  it('shows the reply in the conversation it was sent from after opening another conversation during the sending', async () => {
    let release!: () => void
    const released = new Promise<void>((resolve) => {
      release = resolve
    })
    const loads = vi.fn()
    server.use(conversations([CONVERSATION, AUTRE_CONVERSATION], loads), reply(REPLY, () => released))
    const user = setupUser()
    await renderWithApp(Host, { route: `${MESSAGES_PATH}/${CONVERSATION.uuid}` })
    await thread().findByText(MESSAGE.content)

    await user.type(screen.getByRole('textbox', { name: 'Écrivez votre message' }), REPLY.content)
    await user.click(screen.getByRole('button', { name: 'Envoyer' }))
    await user.click(screen.getByRole('link', { name: /Pièces justificatives/ }))
    await thread().findByText(MESSAGE.content)
    release()

    expect(await screen.findByRole('heading', { name: 'Message envoyé' })).toBeInTheDocument()
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))
    expect(thread().queryByText(REPLY.content)).not.toBeInTheDocument()
    await user.click(screen.getByRole('link', { name: /Convocation/ }))
    expect(await thread().findByText(REPLY.content)).toBeInTheDocument()
  })
})
