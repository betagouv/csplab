import type { Ref } from 'vue'
import { ref } from 'vue'

export interface Request<T> {
  value: Ref<T | null>
  request: (value: T) => void
  clear: () => void
}

export function createRequest<T>(): Request<T> {
  const value = ref<T | null>(null) as Ref<T | null>

  return {
    value,
    request: (requested: T) => {
      value.value = requested
    },
    clear: () => {
      value.value = null
    },
  }
}
