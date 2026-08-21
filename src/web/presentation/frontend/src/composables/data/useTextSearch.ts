import type { MaybeRefOrGetter } from 'vue'
import { computed, ref, toValue } from 'vue'
import { useDebounce } from '@/composables/async/useDebounce'
import { normalizeSearchText } from '@/utils/search'

const DEFAULT_DEBOUNCE_MS = 250

type SearchableText<T> = (row: T) => Array<string | null | undefined>

export function useTextSearch<T>(
  rows: MaybeRefOrGetter<T[]>,
  searchableText: SearchableText<T>,
  debounceMs = DEFAULT_DEBOUNCE_MS,
) {
  const search = ref('')
  const debouncedSearch = useDebounce(search, debounceMs)

  function matches(row: T): boolean {
    const term = normalizeSearchText(debouncedSearch.value.trim())
    if (!term) {
      return true
    }
    return searchableText(row).some(
      value => value != null && normalizeSearchText(value).includes(term),
    )
  }

  const filtered = computed(() => toValue(rows).filter(matches))

  return { search, filtered }
}
