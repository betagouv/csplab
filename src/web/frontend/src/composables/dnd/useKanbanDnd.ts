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

export interface KanbanDropEvent {
  sourceColumnId: string
  targetColumnId: string
  cardId: string
}

interface UseDraggableKanbanCardOptions {
  element: Ref<HTMLElement | null>
  boardId: string
  columnId: string
  cardId: string
  enabled?: Ref<boolean>
}

export function useDraggableKanbanCard(options: UseDraggableKanbanCardOptions) {
  const isDragging = ref(false)
  const enabled = options.enabled ?? ref(true)

  watch(
    [options.element, enabled],
    ([element, isEnabled], _, onCleanup) => {
      if (!element || !isEnabled) {
        return
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
        },
        onDrop: () => {
          isDragging.value = false
        },
      })

      onCleanup(cleanup)
    },
    { flush: 'post', immediate: true },
  )

  return { isDragging }
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

  onMounted(() => {
    cleanup = monitorForElements({
      canMonitor: ({ source }) => {
        const data = source.data as unknown as KanbanCardData
        return data.type === KANBAN_CARD_TYPE && data.boardId === options.boardId
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
        })
      },
    })
  })

  onUnmounted(() => {
    cleanup?.()
  })
}
