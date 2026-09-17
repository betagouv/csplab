import type { Ref } from 'vue'
import { onMounted, onUnmounted, ref } from 'vue'

export function useMediaQuery(query: string): Ref<boolean> {
  const matches = ref(false)
  let mediaQueryList: MediaQueryList | undefined

  function update(): void {
    matches.value = mediaQueryList?.matches ?? false
  }

  onMounted(() => {
    mediaQueryList = window.matchMedia(query)
    update()
    mediaQueryList.addEventListener('change', update)
  })

  onUnmounted(() => {
    mediaQueryList?.removeEventListener('change', update)
  })

  return matches
}
