import type { Candidature } from '../types'
import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { ref } from 'vue'
import { renderWithApp, setupUser } from '@/test/render'
import CandidatureKanbanCard from './CandidatureKanbanCard.vue'

vi.mock('@/composables/dnd/useKanbanDnd', () => ({
  useDraggableKanbanCard: () => ({ isDragging: ref(false) }),
}))

const KANBAN_PATH = '/organismes/00000000-0000-0000-0000-000000000000/recrutements/aaaaaaaa-0001-0001-0001-000000000001'
const ALICE = 'dddddddd-0001-0001-0001-000000000001'
const BOB = 'dddddddd-0001-0001-0001-000000000002'

const CANDIDATURE: Candidature = {
  uuid: ALICE,
  date_soumission: '2025-06-10T09:15:00Z',
  date_derniere_activite: '2025-06-11T10:00:00Z',
  candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000001', nom: 'Dupont', prenom: 'Alice' },
}

function renderCard(route: string) {
  return renderWithApp(CandidatureKanbanCard, {
    route,
    props: { candidature: CANDIDATURE, boardId: 'board', columnId: 'column', cardIndex: 0 },
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

  it('replaces the address when another panel is already open, so that going back returns to the kanban', async () => {
    const user = setupUser()
    const { router } = await renderCard(`${KANBAN_PATH}/candidatures/${BOB}`)
    const replace = vi.spyOn(router, 'replace')

    await user.click(screen.getByRole('link', { name: 'Alice Dupont' }))

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(`${KANBAN_PATH}/candidatures/${ALICE}`))
    expect(replace).toHaveBeenCalled()
  })

  it('replaces the address just the same when the open panel sits on another tab', async () => {
    const user = setupUser()
    const { router } = await renderCard(`${KANBAN_PATH}/candidatures/${BOB}/messages`)
    const replace = vi.spyOn(router, 'replace')

    await user.click(screen.getByRole('link', { name: 'Alice Dupont' }))

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(`${KANBAN_PATH}/candidatures/${ALICE}`))
    expect(replace).toHaveBeenCalled()
  })
})
