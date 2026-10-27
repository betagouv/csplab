import { render } from '@testing-library/vue'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick, ref } from 'vue'
import { markKanbanCardMoved, useDraggableKanbanCard } from './useKanbanDnd'

const BOARD = 'kanban-1'

function renderCard(cardId: string, enabled = true) {
  const state = { isJustMoved: ref(false), isDropWaiting: ref(false) }
  const Card = defineComponent({
    setup() {
      const element = ref<HTMLElement | null>(null)
      const { isJustMoved, isDropWaiting } = useDraggableKanbanCard({ element, boardId: BOARD, columnId: 'colonne', cardId, enabled: ref(enabled) })
      state.isJustMoved = isJustMoved
      state.isDropWaiting = isDropWaiting
      return () => h('article', { 'ref': element, 'data-testid': cardId })
    },
  })
  return { ...render(Card), state }
}

function withDropMotion(value: string) {
  vi.spyOn(window, 'getComputedStyle').mockReturnValue({ getPropertyValue: () => value } as unknown as CSSStyleDeclaration)
}

// Each observed card is visible at this ratio
function observerAt(intersectionRatio: number) {
  return class {
    constructor(private readonly callback: IntersectionObserverCallback) {}
    observe() {
      this.callback([{ isIntersecting: true, intersectionRatio } as IntersectionObserverEntry], this as unknown as IntersectionObserver)
    }

    disconnect() {}
  }
}

// The card is visible as soon as it is observed
const VisibleObserver = observerAt(1)

describe('useDraggableKanbanCard', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('plays the drop motion of the card moved last once it is visible, and of no other card', async () => {
    withDropMotion('csp-raised-outline-drop 1200ms ease-out')
    vi.stubGlobal('IntersectionObserver', VisibleObserver)
    markKanbanCardMoved(BOARD, 'alice')
    const alice = renderCard('alice')
    const bruno = renderCard('bruno')
    await nextTick()

    expect(alice.state.isJustMoved.value).toBe(true)
    expect(alice.state.isDropWaiting.value).toBe(false)
    expect(bruno.state.isJustMoved.value).toBe(false)
  })

  it('holds the drop motion on its first frame while the card is mostly out of view', async () => {
    withDropMotion('csp-raised-outline-drop 1200ms ease-out')
    vi.stubGlobal('IntersectionObserver', observerAt(0.2))
    markKanbanCardMoved(BOARD, 'alice')
    const { state } = renderCard('alice')
    await nextTick()

    expect(state.isJustMoved.value).toBe(true)
    expect(state.isDropWaiting.value).toBe(true)
  })

  it('settles the move at once without a drop motion', async () => {
    withDropMotion('none')
    markKanbanCardMoved(BOARD, 'alice')
    const { state } = renderCard('alice')
    await nextTick()

    expect(state.isJustMoved.value).toBe(false)

    withDropMotion('csp-raised-outline-drop 1200ms ease-out')
    vi.stubGlobal('IntersectionObserver', VisibleObserver)
    const again = renderCard('alice')
    await nextTick()
    expect(again.state.isJustMoved.value).toBe(false)
  })

  it('settles the move when the drop motion of the card ends', async () => {
    withDropMotion('csp-raised-outline-drop 1200ms ease-out')
    vi.stubGlobal('IntersectionObserver', VisibleObserver)
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
