import type { MaybeRefOrGetter } from 'vue'
import { computed, ref, toValue } from 'vue'

type RowKey<T> = (row: T) => string

export function useTableSelection<T>(
  rows: MaybeRefOrGetter<T[]>,
  rowKey: RowKey<T>,
) {
  const selectedIds = ref(new Set<string>())

  const selected = computed(() =>
    toValue(rows).filter(row => selectedIds.value.has(rowKey(row))),
  )

  const count = computed(() => selected.value.length)

  function toggle(id: string): void {
    const next = new Set(selectedIds.value)
    if (!next.delete(id)) {
      next.add(id)
    }
    selectedIds.value = next
  }

  function toggleVisible(ids: string[]): void {
    const next = new Set(selectedIds.value)
    const allSelected = ids.length > 0 && ids.every(id => next.has(id))
    for (const id of ids) {
      if (allSelected) {
        next.delete(id)
      }
      else {
        next.add(id)
      }
    }
    selectedIds.value = next
  }

  function clear(): void {
    selectedIds.value = new Set()
  }

  return {
    selectedIds,
    selected,
    count,
    toggle,
    toggleVisible,
    clear,
  }
}
