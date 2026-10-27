import { nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'

const VIEW_SWITCH = '.candidatures-view-switch'

export function useViewSwitchFocus(): void {
  const route = useRoute()

  watch(() => route.meta.candidaturesView, async () => {
    if (!document.activeElement?.closest(VIEW_SWITCH)) {
      return
    }
    await nextTick()
    document.querySelector<HTMLElement>(`${VIEW_SWITCH} input:checked`)?.focus()
  })
}
