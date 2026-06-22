import type { Ref } from 'vue'
import { draggable } from '@atlaskit/pragmatic-drag-and-drop/element/adapter'
import { ref, watch } from 'vue'

export const SORTABLE_ITEM_TYPE = 'csp-sortable-item' as const

interface UseDraggableElementOptions {
  element: Ref<HTMLElement | null>
  dragHandle?: Ref<HTMLElement | null>
  enabled?: Ref<boolean>
  canDrag?: () => boolean
  getInitialData: () => Record<string, unknown>
}

export function useDraggableElement(options: UseDraggableElementOptions) {
  const isDragging = ref(false)
  const enabled = options.enabled ?? ref(true)

  watch(
    [options.element, () => options.dragHandle?.value, enabled],
    ([element, dragHandle, isEnabled], _, onCleanup) => {
      if (!element || !isEnabled)
        return

      const cleanup = draggable({
        element,
        dragHandle: dragHandle ?? undefined,
        canDrag: options.canDrag,
        getInitialData: options.getInitialData,
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
