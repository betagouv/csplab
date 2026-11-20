import type { KanbanCard } from '../types'
import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { ref } from 'vue'
import { TAG_SENIOR, TAG_TO_RECALL } from '@/test/fixtures/tags'
import { renderWithApp, setupUser } from '@/test/render'
import CandidatureKanbanCard from './CandidatureKanbanCard.vue'

vi.mock('@/composables/dnd/useKanbanDnd', () => ({
  useDraggableKanbanCard: () => ({ isDragging: ref(false), isJustMoved: ref(false), isDropWaiting: ref(false) }),
}))

const KANBAN_PATH = '/organismes/00000000-0000-0000-0000-000000000000/recrutements/aaaaaaaa-0001-0001-0001-000000000001'
const ALICE = 'dddddddd-0001-0001-0001-000000000001'

const CANDIDATURE: KanbanCard = {
  uuid: ALICE,
  date_soumission: '2025-06-10T09:15:00Z',
  date_derniere_activite: '2025-06-11T10:00:00Z',
  unread_conversations: 0,
  tags: [],
  candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000001', nom: 'Dupont', prenom: 'Alice' },
}

function renderCard(route: string, candidature: KanbanCard = CANDIDATURE) {
  return renderWithApp(CandidatureKanbanCard, {
    route,
    props: { candidature, boardId: 'board', columnId: 'column', canChangeEtape: true },
  })
}

describe('candidatureKanbanCard', () => {
  it('opens the panel of its candidature from the keyboard, without being draggable itself', async () => {
    const user = setupUser()
    const { router } = await renderCard(KANBAN_PATH)
    const link = screen.getByRole('link', { name: 'Alice Dupont' })

    expect(link).toHaveAttribute('draggable', 'false')
    await user.tab()
    expect(link).toHaveFocus()
    await user.keyboard('{Enter}')

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(`${KANBAN_PATH}/candidatures/${ALICE}`))
  })

  it('shows the tags of the candidature under the date', async () => {
    await renderCard(KANBAN_PATH, { ...CANDIDATURE, tags: [TAG_TO_RECALL, TAG_SENIOR] })

    const tags = within(screen.getByRole('list', { name: 'Étiquettes d\'Alice Dupont' }))
    expect(tags.getAllByRole('listitem').map(item => item.textContent?.trim())).toEqual(['À rappeler', 'Profil senior'])
  })

  it('shows no tag list on a candidature without tags', async () => {
    await renderCard(KANBAN_PATH)

    expect(screen.queryByRole('list', { name: 'Étiquettes d\'Alice Dupont' })).not.toBeInTheDocument()
  })

  it('marks the card of the open candidature as current', async () => {
    await renderCard(`${KANBAN_PATH}/candidatures/${ALICE}`)

    expect(screen.getByRole('article')).toHaveAttribute('aria-current', 'true')
  })
})
