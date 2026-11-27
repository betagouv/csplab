import type { RenderOptions } from '@testing-library/vue'
import type { Component } from 'vue'
import { PiniaColada } from '@pinia/colada'
import userEvent, { PointerEventsCheckLevel } from '@testing-library/user-event'
import { render } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { createApp, defineComponent, h, provide } from 'vue'
import { createMemoryHistory, createRouter, useRoute, viewDepthKey } from 'vue-router'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import { routes } from '@/router/routes'

export function setupUser(options: Parameters<typeof userEvent.setup>[0] = {}) {
  return userEvent.setup({ pointerEventsCheck: PointerEventsCheckLevel.Never, ...options })
}

export function withToaster(component: Component, props: Record<string, unknown> = {}) {
  return defineComponent({
    setup: () => () => h(CspToaster, null, () => h(component, props)),
  })
}

export function inRouterViewOf(component: Component, routeName: string) {
  return defineComponent({
    setup() {
      provide(viewDepthKey, useRoute().matched.findIndex(({ name }) => name === routeName) + 1)
      return () => h(component)
    },
  })
}

export function createTestRouter() {
  return createRouter({ history: createMemoryHistory(), routes })
}

// Router guards run before render and need pinia bound to an app.
function createInstalledPinia() {
  const pinia = createPinia()
  createApp({}).use(pinia)
  return pinia
}

export async function renderWithApp(
  component: Component,
  { route = '/', ...options }: RenderOptions<Component> & { route?: string } = {},
) {
  const pinia = createInstalledPinia()
  const router = createTestRouter()
  await router.push(route)

  const result = render(component, {
    ...options,
    global: {
      ...options.global,
      plugins: [pinia, PiniaColada, router, ...(options.global?.plugins ?? [])],
    },
  })

  return { ...result, router }
}
