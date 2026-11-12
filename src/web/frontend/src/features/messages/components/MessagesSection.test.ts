import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { CANDIDATURE_PARAMS, KANBAN_PATH } from '@/test/fixtures/candidatures'
import { renderWithApp } from '@/test/render'
import { getConversations } from '../api'
import MessagesSection from './MessagesSection.vue'

vi.mock('../api', () => ({
  getConversations: vi.fn(),
}))

const MESSAGES_PATH = `${KANBAN_PATH}/candidatures/${CANDIDATURE_PARAMS.candidatureUuid}/messages`

describe('messagesSection', () => {
  beforeEach(() => {
    vi.mocked(getConversations).mockReset()
  })

  it('reports a failed load instead of showing an empty list', async () => {
    vi.mocked(getConversations).mockRejectedValue(new HttpError(500, 'Server Error', undefined))

    await renderWithApp(MessagesSection, {
      route: MESSAGES_PATH,
      props: {
        candidature: CANDIDATURE_PARAMS,
        candidatNom: 'Alice Dupont',
        routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.conversations,
      },
    })

    expect(await screen.findByText('Impossible de charger les conversations')).toBeInTheDocument()
    expect(screen.queryByText('Aucune conversation pour le moment')).not.toBeInTheDocument()
  })
})
