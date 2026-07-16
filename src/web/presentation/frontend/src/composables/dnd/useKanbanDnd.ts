import type { Edge } from '@atlaskit/pragmatic-drag-and-drop-hitbox/closest-edge'
import type { Ref } from 'vue'
import { attachClosestEdge, extractClosestEdge } from '@atlaskit/pragmatic-drag-and-drop-hitbox/closest-edge'
import { draggable, dropTargetForElements, monitorForElements } from '@atlaskit/pragmatic-drag-and-drop/element/adapter'
import { onMounted, onUnmounted, ref, watch } from 'vue'

export const KANBAN_CARD_TYPE = 'kanban-card' as const

export interface KanbanCardData {
  type: typeof KANBAN_CARD_TYPE
  boardId: string
  columnId: string
  cardId: string
  cardIndex: number
}

export interface KanbanDropEvent {
  sourceColumnId: string
  targetColumnId: string
  cardId: string
  cardIndex: number
}

interface UseDraggableKanbanCardOptions {
  element: Ref<HTMLElement | null>
  boardId: string
  columnId: string
  cardId: string
  cardIndex: number
  enabled?: Ref<boolean>
}

export function useDraggableKanbanCard(options: UseDraggableKanbanCardOptions) {
  const isDragging = ref(false)
  const enabled = options.enabled ?? ref(true)

  watch(
    [options.element, enabled],
    ([element, isEnabled], _, onCleanup) => {
      if (!element || !isEnabled)
        return

      const cleanup = draggable({
        element,
        getInitialData: () => ({
          type: KANBAN_CARD_TYPE,
          boardId: options.boardId,
          columnId: options.columnId,
          cardId: options.cardId,
          cardIndex: options.cardIndex,
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
  const closestEdge = ref<Edge | null>(null)
  const enabled = options.enabled ?? ref(true)

  watch(
    [options.element, enabled],
    ([element, isEnabled], _, onCleanup) => {
      if (!element || !isEnabled)
        return

      const cleanup = dropTargetForElements({
        element,
        canDrop: ({ source }) => {
          const data = source.data as unknown as KanbanCardData
          return data.type === KANBAN_CARD_TYPE && data.boardId === options.boardId
        },
        getData: ({ input, element: dropElement }) => attachClosestEdge(
          { columnId: options.columnId },
          { input, element: dropElement, allowedEdges: ['top', 'bottom'] },
        ),
        onDragEnter: ({ self }) => {
          isDraggedOver.value = true
          closestEdge.value = extractClosestEdge(self.data)
        },
        onDrag: ({ self }) => {
          closestEdge.value = extractClosestEdge(self.data)
        },
        onDragLeave: () => {
          isDraggedOver.value = false
          closestEdge.value = null
        },
        onDrop: () => {
          isDraggedOver.value = false
          closestEdge.value = null
        },
      })

      onCleanup(cleanup)
    },
    { flush: 'post', immediate: true },
  )

  return { isDraggedOver, closestEdge }
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
        if (!destination)
          return

        const sourceData = source.data as unknown as KanbanCardData
        const targetColumnId = destination.data.columnId as string

        if (!targetColumnId)
          return

        options.onDrop({
          sourceColumnId: sourceData.columnId,
          targetColumnId,
          cardId: sourceData.cardId,
          cardIndex: sourceData.cardIndex,
        })
      },
    })
  })

  onUnmounted(() => {
    cleanup?.()
  })
}
