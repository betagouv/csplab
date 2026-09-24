import type { Ref } from 'vue'
import { ref } from 'vue'

export interface Request<T> {
  readonly requested: T | null
  request: (value: T) => void
  clear: () => void
}

export function createRequest<T>(): Request<T> {
  const requested = ref<T | null>(null) as Ref<T | null>

  return {
    get requested() {
      return requested.value
    },
    request: (value: T) => {
      requested.value = value
    },
    clear: () => {
      requested.value = null
    },
  }
}
