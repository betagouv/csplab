import type { RenderOptions } from '@testing-library/vue'
import type { Component } from 'vue'
import { PiniaColada } from '@pinia/colada'
import userEvent, { PointerEventsCheckLevel } from '@testing-library/user-event'
import { render } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { createMemoryHistory, createRouter } from 'vue-router'
import { routes } from '@/router'

export function setupUser(options: Parameters<typeof userEvent.setup>[0] = {}) {
  return userEvent.setup({ pointerEventsCheck: PointerEventsCheckLevel.Never, ...options })
}

export function createTestRouter() {
  return createRouter({ history: createMemoryHistory(), routes })
}

export async function renderWithApp(
  component: Component,
  { route = '/', ...options }: RenderOptions<Component> & { route?: string } = {},
) {
  const router = createTestRouter()
  await router.push(route)

  const result = render(component, {
    ...options,
    global: {
      ...options.global,
      plugins: [createPinia(), PiniaColada, router, ...(options.global?.plugins ?? [])],
    },
  })

  return { ...result, router }
}
