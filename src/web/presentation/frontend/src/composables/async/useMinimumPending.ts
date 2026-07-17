import type { Ref } from 'vue'
import { onScopeDispose, readonly, ref, watch } from 'vue'

const DEFAULT_MIN_DURATION_MS = 400

export function useMinimumPending(
  pending: Ref<boolean>,
  minDurationMs = DEFAULT_MIN_DURATION_MS,
): Readonly<Ref<boolean>> {
  const display = ref(pending.value)
  let shownAt = pending.value ? Date.now() : 0
  let timer: ReturnType<typeof setTimeout> | undefined

  watch(pending, (isPending) => {
    clearTimeout(timer)

    if (isPending) {
      display.value = true
      shownAt = Date.now()
      return
    }

    const elapsed = Date.now() - shownAt
    if (elapsed >= minDurationMs) {
      display.value = false
    }
    else {
      timer = setTimeout(() => {
        display.value = false
      }, minDurationMs - elapsed)
    }
  })

  onScopeDispose(() => clearTimeout(timer))

  return readonly(display)
}
