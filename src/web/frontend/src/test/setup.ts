import { cleanup } from '@testing-library/vue'
import { createHead } from '@unhead/vue/client'
import { config } from '@vue/test-utils'
import { afterEach, beforeAll, vi } from 'vitest'
import { createMediaQueryMock } from './browser'
import '@testing-library/jest-dom/vitest'

config.global.plugins.push(createHead())

beforeAll(() => {
  Element.prototype.scrollIntoView = vi.fn()
  Element.prototype.hasPointerCapture = vi.fn(() => false)
  Element.prototype.releasePointerCapture = vi.fn()
  Object.defineProperty(window, 'matchMedia', {
    configurable: true,
    writable: true,
    value: () => createMediaQueryMock(false),
  })
})

afterEach(() => {
  cleanup()
})
