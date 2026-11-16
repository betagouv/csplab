import { useQuery } from '@pinia/colada'
import { computed, ref } from 'vue'
import { useDebounce } from '@/composables/async/useDebounce'
import { SEARCH_DEBOUNCE_MS, SEARCH_MIN_LENGTH } from '../constants/organisme'
import { organismesSearchQuery } from '../queries'

export function useOrganismesSearch() {
  const search = ref('')
  const term = useDebounce(() => search.value.trim(), SEARCH_DEBOUNCE_MS)
  const searchable = computed(() => term.value.length >= SEARCH_MIN_LENGTH)

  const query = useQuery(() => ({
    ...organismesSearchQuery(term.value),
    enabled: searchable.value,
  }))

  const results = computed(() => (searchable.value ? query.data.value ?? [] : []))
  const tooShort = computed(() => search.value.trim().length < SEARCH_MIN_LENGTH)
  const searching = computed(() =>
    !tooShort.value && (term.value !== search.value.trim() || query.isPending.value),
  )

  return {
    search,
    results,
    tooShort,
    searching,
    error: query.error,
  }
}
