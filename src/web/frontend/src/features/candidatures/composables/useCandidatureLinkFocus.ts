import { nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'

export function useCandidatureLinkFocus(): void {
  const route = useRoute()

  watch(() => route.params.candidatureUuid, async (current, previous) => {
    if (current || typeof previous !== 'string') {
      return
    }
    await nextTick()
    document.querySelector<HTMLElement>(`a[data-candidature-uuid="${previous}"]`)?.focus()
  })
}
