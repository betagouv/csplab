import type { WritableComputedRef } from 'vue'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    tab?: string
  }
}

export function useRouteTab<T extends string>(
  routeNames: Record<T, string>,
  fallback: T,
): WritableComputedRef<T> {
  const route = useRoute()
  const router = useRouter()

  function isTab(value: unknown): value is T {
    return typeof value === 'string' && Object.hasOwn(routeNames, value)
  }

  return computed<T>({
    get: () => (isTab(route.meta.tab) ? route.meta.tab : fallback),
    set: (tab) => {
      void router.push({ name: routeNames[tab] })
    },
  })
}
