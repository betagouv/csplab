import type { RenderOptions } from '@testing-library/vue'
import type { Component } from 'vue'
import { PiniaColada } from '@pinia/colada'
import userEvent, { PointerEventsCheckLevel } from '@testing-library/user-event'
import { render } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import { routes } from '@/router/routes'

export function setupUser(options: Parameters<typeof userEvent.setup>[0] = {}) {
  return userEvent.setup({ pointerEventsCheck: PointerEventsCheckLevel.Never, ...options })
}

export function createTestRouter() {
  return createRouter({ history: createMemoryHistory(), routes })
}

function createInstalledPinia() {
  const pinia = createPinia()
  createApp({}).use(pinia).use(PiniaColada)
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
