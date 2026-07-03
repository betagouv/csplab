import { computed, reactive } from 'vue'

export function useDraft<T extends Record<string, unknown>>(makeInitial: () => T) {
  const initial = makeInitial()
  const keys = Object.keys(initial) as (keyof T)[]

  const applied = reactive(makeInitial()) as T
  const draft = reactive(makeInitial()) as T

  const hasDiverged = computed(() => keys.some(key => draft[key] !== applied[key]))

  const canReset = computed(() =>
    keys.some(key => draft[key] !== initial[key] || applied[key] !== initial[key]),
  )

  function syncDraft(): void {
    Object.assign(draft, applied)
  }

  function apply(): void {
    Object.assign(applied, draft)
  }

  function reset(): void {
    Object.assign(draft, makeInitial())
    Object.assign(applied, makeInitial())
  }

  return {
    draft,
    applied,
    hasDiverged,
    canReset,
    syncDraft,
    apply,
    reset,
  }
}
