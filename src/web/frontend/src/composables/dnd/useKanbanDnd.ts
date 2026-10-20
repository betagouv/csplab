import type { Ref } from 'vue'
import { autoScrollForElements } from '@atlaskit/pragmatic-drag-and-drop-auto-scroll/element'
import { draggable, dropTargetForElements, monitorForElements } from '@atlaskit/pragmatic-drag-and-drop/element/adapter'
import { onMounted, onUnmounted, ref, watch } from 'vue'

export const KANBAN_CARD_TYPE = 'kanban-card' as const

export interface KanbanCardData {
  type: typeof KANBAN_CARD_TYPE
  boardId: string
  columnId: string
  cardId: string
}

// Top left corner of the drag preview when the pointer released it, in viewport pixels
export interface KanbanPoint {
  x: number
  y: number
}

export interface KanbanDropEvent {
  sourceColumnId: string
  targetColumnId: string
  cardId: string
  releasedAt: KanbanPoint
}

interface UseDraggableKanbanCardOptions {
  element: Ref<HTMLElement | null>
  boardId: string
  columnId: string
  cardId: string
  enabled?: Ref<boolean>
}

// Card moved last to another column, read by the card that mounts in that column
const lastMovedCard = ref<{ key: string, releasedAt?: KanbanPoint } | null>(null)

export function markKanbanCardMoved(boardId: string, cardId: string, releasedAt?: KanbanPoint): void {
  lastMovedCard.value = { key: `${boardId}/${cardId}`, releasedAt }
}

export function useDraggableKanbanCard(options: UseDraggableKanbanCardOptions) {
  const isDragging = ref(false)
  const enabled = options.enabled ?? ref(true)
  const cardKey = `${options.boardId}/${options.cardId}`
  const move = lastMovedCard.value?.key === cardKey ? lastMovedCard.value : null
  const isJustMoved = ref(move !== null)

  function settleMove(): void {
    isJustMoved.value = false
    if (lastMovedCard.value?.key === cardKey) {
      lastMovedCard.value = null
    }
  }

  watch(
    [options.element, enabled],
    ([element, isEnabled], _, onCleanup) => {
      if (!element || !isEnabled) {
        return
      }

      // Without a drop animation, no animationend event settles the move
      if (isJustMoved.value && getComputedStyle(element).animationName === 'none') {
        settleMove()
      }
      // Offset of the released preview from the place of the card, that a drop animation can start from
      else if (isJustMoved.value && move?.releasedAt) {
        const { left, top } = element.getBoundingClientRect()
        element.style.setProperty('--csp-drop-offset-x', `${move.releasedAt.x - left}px`)
        element.style.setProperty('--csp-drop-offset-y', `${move.releasedAt.y - top}px`)
      }

      const cleanup = draggable({
        element,
        getInitialData: () => ({
          type: KANBAN_CARD_TYPE,
          boardId: options.boardId,
          columnId: options.columnId,
          cardId: options.cardId,
        }) as Record<string, unknown>,
        onDragStart: () => {
          isDragging.value = true
          lastMovedCard.value = null
        },
        onDrop: () => {
          isDragging.value = false
        },
      })

      onCleanup(cleanup)
    },
    { flush: 'post', immediate: true },
  )

  return { isDragging, isJustMoved, settleMove }
}

interface UseDropTargetKanbanColumnOptions {
  element: Ref<HTMLElement | null>
  boardId: string
  columnId: string
  enabled?: Ref<boolean>
}

export function useDropTargetKanbanColumn(options: UseDropTargetKanbanColumnOptions) {
  const isDraggedOver = ref(false)
  const enabled = options.enabled ?? ref(true)

  watch(
    [options.element, enabled],
    ([element, isEnabled], _, onCleanup) => {
      if (!element || !isEnabled) {
        return
      }

      const cleanup = dropTargetForElements({
        element,
        canDrop: ({ source }) => {
          const data = source.data as unknown as KanbanCardData
          return data.type === KANBAN_CARD_TYPE && data.boardId === options.boardId
        },
        getData: () => ({ columnId: options.columnId }),
        onDragEnter: () => {
          isDraggedOver.value = true
        },
        onDragLeave: () => {
          isDraggedOver.value = false
        },
        onDrop: () => {
          isDraggedOver.value = false
        },
      })

      onCleanup(cleanup)
    },
    { flush: 'post', immediate: true },
  )

  return { isDraggedOver }
}

interface UseKanbanBoardAutoScrollOptions {
  element: Ref<HTMLElement | null>
}

export function useKanbanBoardAutoScroll(options: UseKanbanBoardAutoScrollOptions) {
  watch(
    options.element,
    (element, _, onCleanup) => {
      if (!element) {
        return
      }

      const cleanup = autoScrollForElements({ element })

      onCleanup(cleanup)
    },
    { flush: 'post', immediate: true },
  )
}

interface UseKanbanBoardMonitorOptions {
  boardId: string
  onDrop: (event: KanbanDropEvent) => void
}

export function useKanbanBoardMonitor(options: UseKanbanBoardMonitorOptions) {
  let cleanup: (() => void) | null = null
  // Position of the pointer in the dragged card, which the drag preview keeps
  let grab: KanbanPoint = { x: 0, y: 0 }

  onMounted(() => {
    cleanup = monitorForElements({
      canMonitor: ({ source }) => {
        const data = source.data as unknown as KanbanCardData
        return data.type === KANBAN_CARD_TYPE && data.boardId === options.boardId
      },
      onDragStart: ({ source, location }) => {
        const { left, top } = source.element.getBoundingClientRect()
        grab = { x: location.initial.input.clientX - left, y: location.initial.input.clientY - top }
      },
      onDrop: ({ source, location }) => {
        const destination = location.current.dropTargets[0]
        if (!destination) {
          return
        }

        const sourceData = source.data as unknown as KanbanCardData
        const targetColumnId = destination.data.columnId as string

        if (!targetColumnId) {
          return
        }

        options.onDrop({
          sourceColumnId: sourceData.columnId,
          targetColumnId,
          cardId: sourceData.cardId,
          releasedAt: { x: location.current.input.clientX - grab.x, y: location.current.input.clientY - grab.y },
        })
      },
    })
  })

  onUnmounted(() => {
    cleanup?.()
  })
}
