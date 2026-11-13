import type { CreateOrganismePayload, UpdateOrganismePayload } from '../types'
import { useMutation, useQuery, useQueryCache } from '@pinia/colada'
import { computed, ref, watch } from 'vue'
import { organismeKeys } from '@/api/queryKeys'
import { useDebounce } from '@/composables/async/useDebounce'
import { createOrganisme, updateOrganisme } from '../api'
import { SEARCH_DEBOUNCE_MS, SEARCH_MIN_LENGTH } from '../constants/organisme'
import { invalidateOrganisme, organismesPageQuery } from '../queries'

export function useOrganismes() {
  const queryCache = useQueryCache()

  const page = ref(1)
  const search = ref('')
  const term = useDebounce(() => search.value.trim(), SEARCH_DEBOUNCE_MS)
  const filter = computed(() => (term.value.length >= SEARCH_MIN_LENGTH ? term.value : undefined))

  watch(filter, () => {
    page.value = 1
  }, { flush: 'sync' })

  const query = useQuery(() => organismesPageQuery({ page: page.value, filter: filter.value }))

  const createMutation = useMutation({
    mutation: (payload: CreateOrganismePayload) => createOrganisme(payload),
    onSettled: () => queryCache.invalidateQueries({ key: organismeKeys.list() }),
  })

  const updateMutation = useMutation({
    mutation: ({ organismeUuid, payload }: { organismeUuid: string, payload: UpdateOrganismePayload }) =>
      updateOrganisme(organismeUuid, payload),
    onSettled: (_data, _error, { organismeUuid }) => invalidateOrganisme(queryCache, { organismeUuid }),
  })

  return {
    page,
    search,
    organismes: computed(() => query.data.value?.results ?? []),
    count: computed(() => query.data.value?.count ?? 0),
    pending: query.isPending,
    error: query.error,
    create: createMutation.mutateAsync,
    creating: createMutation.isLoading,
    update: updateMutation.mutateAsync,
    updating: updateMutation.isLoading,
  }
}
