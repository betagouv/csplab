import { cleanup } from '@testing-library/vue'
import { createHead } from '@unhead/vue/client'
import { config } from '@vue/test-utils'
import { afterAll, afterEach, beforeAll, vi } from 'vitest'
import { useToast } from '@/composables/ui/useToast'
import { createMediaQueryMock } from './browser'
import { makeUser } from './fixtures/utilisateur'
import { server } from './server'
import '@testing-library/jest-dom/vitest'

config.global.plugins.push(createHead())

vi.mock('@/api/utilisateur', async importOriginal => ({
  ...await importOriginal<typeof import('@/api/utilisateur')>(),
  getMe: vi.fn(async () => makeUser([])),
}))

beforeAll(() => {
  server.listen({ onUnhandledFrame: 'error' })
  Element.prototype.scrollIntoView = vi.fn()
  Element.prototype.hasPointerCapture = vi.fn(() => false)
  Element.prototype.releasePointerCapture = vi.fn()
  globalThis.ResizeObserver = class {
    observe = vi.fn()
    unobserve = vi.fn()
    disconnect = vi.fn()
  }
  Object.defineProperty(window, 'matchMedia', {
    configurable: true,
    writable: true,
    value: () => createMediaQueryMock(false),
  })
})

afterEach(() => {
  cleanup()
  server.resetHandlers()
  const { toasts, dismissToast } = useToast()
  toasts.value.forEach(toast => dismissToast(toast.id))
})

afterAll(() => {
  server.close()
})
