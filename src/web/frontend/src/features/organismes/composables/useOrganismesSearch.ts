import { useQuery } from '@pinia/colada'
import { computed, ref } from 'vue'
import { useDebounce } from '@/composables/async/useDebounce'
import { organismesSearchQuery } from '../queries'

const SEARCH_DEBOUNCE_MS = 300
const SEARCH_MIN_LENGTH = 3

export function useOrganismesSearch() {
  const search = ref('')
  const term = useDebounce(() => search.value.trim(), SEARCH_DEBOUNCE_MS)
  const searchable = computed(() => term.value.length >= SEARCH_MIN_LENGTH)

  const query = useQuery(() => ({
    ...organismesSearchQuery(term.value),
    enabled: searchable.value,
  }))

  const results = computed(() => (searchable.value ? query.data.value ?? [] : []))

  return {
    search,
    results,
    searchable,
    pending: computed(() => searchable.value && query.isPending.value),
    error: query.error,
  }
}
