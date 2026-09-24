import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { renderWithApp } from '@/test/render'
import { getConversations } from '../api'
import MessagesSection from './MessagesSection.vue'

vi.mock('../api', () => ({
  getConversations: vi.fn(),
}))

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'
const CANDIDATURE_ALICE = 'dddddddd-0001-0001-0001-000000000001'

const MESSAGES_PATH = `/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}/candidatures/${CANDIDATURE_ALICE}/messages`

describe('messagesSection', () => {
  beforeEach(() => {
    vi.mocked(getConversations).mockReset()
  })

  it('reports a failed load instead of showing an empty list', async () => {
    vi.mocked(getConversations).mockRejectedValue(new HttpError(500, 'Server Error', undefined))

    await renderWithApp(MessagesSection, {
      route: MESSAGES_PATH,
      props: {
        organismeUuid: ORGANISME_UUID,
        recrutementUuid: RECRUTEMENT_UUID,
        candidatureUuid: CANDIDATURE_ALICE,
      },
    })

    expect(await screen.findByText('Impossible de charger les conversations')).toBeInTheDocument()
    expect(screen.queryByText('Aucune conversation pour le moment')).not.toBeInTheDocument()
  })
})
