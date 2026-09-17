import type { RouteLocationRaw } from 'vue-router'
import { useRouter } from 'vue-router'

export function useReturnTo(fallback: () => RouteLocationRaw): () => void {
  const router = useRouter()

  return () => {
    if (router.options.history.state.back) {
      router.back()
      return
    }
    void router.replace(fallback())
  }
}
