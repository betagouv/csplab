import type { Input } from '@atlaskit/pragmatic-drag-and-drop/types'
import type { Ref } from 'vue'
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
  const sourceIndex = ref<number | null>(null)
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
          if (options.canDrop && !options.canDrop(source.data)) {
            return false
          }
          return true
        },
        getData: options.getData,
        onDragEnter: ({ source }) => {
          isDraggedOver.value = true
          sourceIndex.value = typeof source.data.index === 'number' ? source.data.index : null
        },
        onDragLeave: () => {
          isDraggedOver.value = false
          sourceIndex.value = null
        },
        onDrop: () => {
          isDraggedOver.value = false
          sourceIndex.value = null
        },
      })

      onCleanup(cleanup)
    },
    { flush: 'post', immediate: true },
  )

  return { isDraggedOver, sourceIndex }
}
