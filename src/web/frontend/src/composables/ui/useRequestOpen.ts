import type { WritableComputedRef } from 'vue'
import type { Request } from './useRequest'
import { computed } from 'vue'

export function useRequestOpen<T>(request: Request<T>): WritableComputedRef<boolean> {
  return computed({
    get: () => request.requested !== null,
    set: (isOpen) => {
      if (!isOpen) {
        request.clear()
      }
    },
  })
}
