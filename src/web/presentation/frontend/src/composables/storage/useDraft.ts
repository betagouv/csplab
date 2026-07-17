import { computed, reactive } from 'vue'

function isSame(a: unknown, b: unknown): boolean {
  if (Array.isArray(a) && Array.isArray(b)) {
    return a.length === b.length && a.every((value, index) => value === b[index])
  }
  return a === b
}

export function useDraft<T extends Record<string, unknown>>(makeInitial: () => T) {
  const initial = makeInitial()
  const keys = Object.keys(initial) as (keyof T)[]

  const applied = reactive(makeInitial()) as T
  const draft = reactive(makeInitial()) as T

  const hasDiverged = computed(() => keys.some(key => !isSame(draft[key], applied[key])))

  const canReset = computed(() =>
    keys.some(key => !isSame(draft[key], initial[key]) || !isSame(applied[key], initial[key])),
  )

  function assign(target: T, source: T): void {
    for (const key of keys) {
      const value = source[key]
      target[key] = (Array.isArray(value) ? [...value] : value) as T[keyof T]
    }
  }

  function syncDraft(): void {
    assign(draft, applied)
  }

  function apply(): void {
    assign(applied, draft)
  }

  function reset(): void {
    assign(draft, makeInitial())
    assign(applied, makeInitial())
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
