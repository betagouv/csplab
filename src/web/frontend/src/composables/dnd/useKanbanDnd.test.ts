import { render } from '@testing-library/vue'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick, ref } from 'vue'
import { markKanbanCardMoved, useDraggableKanbanCard } from './useKanbanDnd'

const BOARD = 'kanban-1'

function renderCard(cardId: string, enabled = true) {
  const state = { isJustMoved: ref(false) }
  const Card = defineComponent({
    setup() {
      const element = ref<HTMLElement | null>(null)
      const { isJustMoved } = useDraggableKanbanCard({ element, boardId: BOARD, columnId: 'colonne', cardId, enabled: ref(enabled) })
      state.isJustMoved = isJustMoved
      return () => h('article', { 'ref': element, 'data-testid': cardId })
    },
  })
  return { ...render(Card), state }
}

function withAnimation(animationName: string) {
  vi.spyOn(window, 'getComputedStyle').mockReturnValue({ animationName } as CSSStyleDeclaration)
}

describe('useDraggableKanbanCard', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('flags the card moved last when it mounts in its new column, and no other card', () => {
    markKanbanCardMoved(BOARD, 'alice')

    expect(renderCard('alice', false).state.isJustMoved.value).toBe(true)
    expect(renderCard('bruno', false).state.isJustMoved.value).toBe(false)
  })

  it('settles the move at once without a drop motion', async () => {
    withAnimation('none')
    markKanbanCardMoved(BOARD, 'alice')
    const { state } = renderCard('alice')
    await nextTick()

    expect(state.isJustMoved.value).toBe(false)
    expect(renderCard('alice', false).state.isJustMoved.value).toBe(false)
  })

  it('settles the move when the drop motion of the card ends', async () => {
    withAnimation('csp-raised-outline-drop')
    markKanbanCardMoved(BOARD, 'alice')
    const { getByTestId, state } = renderCard('alice')
    await nextTick()
    const card = getByTestId('alice')
    card.getAnimations = () => []

    expect(state.isJustMoved.value).toBe(true)
    card.dispatchEvent(new Event('animationend'))
    expect(state.isJustMoved.value).toBe(false)
  })
})
