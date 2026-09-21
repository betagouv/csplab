import { cleanup } from '@testing-library/vue'
import { afterEach, beforeAll, vi } from 'vitest'
import { createMediaQueryMock } from './browser'
import '@testing-library/jest-dom/vitest'

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
