import type { Edge } from '@atlaskit/pragmatic-drag-and-drop-hitbox/closest-edge'
import type { Input } from '@atlaskit/pragmatic-drag-and-drop/types'
import type { Ref } from 'vue'
import { attachClosestEdge, extractClosestEdge } from '@atlaskit/pragmatic-drag-and-drop-hitbox/closest-edge'
import { dropTargetForElements } from '@atlaskit/pragmatic-drag-and-drop/element/adapter'
import { ref, watch } from 'vue'

interface UseDropTargetElementOptions {
  element: Ref<HTMLElement | null>
  enabled?: Ref<boolean>
  canDrop?: (source: Record<string, unknown>) => boolean
  getData: (args: { input: Input, element: Element }) => Record<string, unknown>
}

export function useDropTargetElement(options: UseDropTargetElementOptions) {
  const isDraggedOver = ref(false)
  const closestEdge = ref<Edge | null>(null)
  const sourceIndex = ref<number | null>(null)
  const enabled = options.enabled ?? ref(true)

  watch(
    [options.element, enabled],
    ([element, isEnabled], _, onCleanup) => {
      if (!element || !isEnabled)
        return

      const cleanup = dropTargetForElements({
        element,
        canDrop: ({ source }) => {
          if (options.canDrop && !options.canDrop(source.data))
            return false
          return true
        },
        getData: ({ input, element: dropElement }) => attachClosestEdge(
          options.getData({ input, element: dropElement }),
          {
            input,
            element: dropElement,
            allowedEdges: ['top', 'bottom'],
          },
        ),
        onDragEnter: ({ self, source }) => {
          isDraggedOver.value = true
          closestEdge.value = extractClosestEdge(self.data)
          sourceIndex.value = typeof source.data.index === 'number' ? source.data.index : null
        },
        onDrag: ({ self }) => {
          closestEdge.value = extractClosestEdge(self.data)
        },
        onDragLeave: () => {
          isDraggedOver.value = false
          closestEdge.value = null
          sourceIndex.value = null
        },
        onDrop: () => {
          isDraggedOver.value = false
          closestEdge.value = null
          sourceIndex.value = null
        },
      })

      onCleanup(cleanup)
    },
    { flush: 'post', immediate: true },
  )

  return { isDraggedOver, closestEdge, sourceIndex }
}
