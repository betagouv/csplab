import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { createApp, defineComponent, h, nextTick } from 'vue'
import { useColorMode } from './useColorMode'

function createLocalStorageMock() {
  const storage = new Map<string, string>()

  return {
    getItem: (key: string) => storage.get(key) ?? null,
    setItem: (key: string, value: string) => storage.set(key, value),
    removeItem: (key: string) => storage.delete(key),
    clear: () => storage.clear(),
  }
}

function createMediaQueryMock(matches: boolean) {
  const listeners: Array<(e: MediaQueryListEvent) => void> = []

  return {
    matches,
    addEventListener: (_: string, handler: (e: MediaQueryListEvent) => void) => {
      listeners.push(handler)
    },
    removeEventListener: (_: string, handler: (e: MediaQueryListEvent) => void) => {
      const idx = listeners.indexOf(handler)
      if (idx >= 0)
        listeners.splice(idx, 1)
    },
    dispatchChange: (newMatches: boolean) => {
      listeners.forEach(handler => handler({ matches: newMatches } as MediaQueryListEvent))
    },
  }
}

function mountColorMode() {
  let context!: ReturnType<typeof useColorMode>

  const TestApp = defineComponent({
    setup() {
      context = useColorMode()
      return () => h('div')
    },
  })

  const el = document.createElement('div')
  const app = createApp(TestApp)
  app.mount(el)

  return {
    get context() {
      return context
    },
    unmount() {
      app.unmount()
    },
  }
}

describe('useColorMode', () => {
  let unmount: (() => void) | undefined
  let localStorageMock: ReturnType<typeof createLocalStorageMock>
  let mediaQueryMock: ReturnType<typeof createMediaQueryMock>

  beforeEach(() => {
    localStorageMock = createLocalStorageMock()
    mediaQueryMock = createMediaQueryMock(false)

    vi.stubGlobal('localStorage', localStorageMock)
    vi.stubGlobal('matchMedia', () => mediaQueryMock)
  })

  afterEach(() => {
    unmount?.()
    unmount = undefined
    vi.unstubAllGlobals()
    document.documentElement.removeAttribute('data-fr-theme')
  })

  it('setColorMode updates mode and persists to localStorage', async () => {
    const mounted = mountColorMode()
    unmount = mounted.unmount

    mounted.context.setColorMode('dark')
    await nextTick()

    expect(mounted.context.colorMode.value).toBe('dark')
    expect(mounted.context.isDark.value).toBe(true)
    expect(localStorageMock.getItem('csp_color_mode')).toBe('dark')
  })

  it('toggle switches between light and dark', async () => {
    const mounted = mountColorMode()
    unmount = mounted.unmount

    mounted.context.setColorMode('light')
    await nextTick()
    expect(mounted.context.isDark.value).toBe(false)

    mounted.context.toggle()
    await nextTick()
    expect(mounted.context.colorMode.value).toBe('dark')
    expect(mounted.context.isDark.value).toBe(true)

    mounted.context.toggle()
    await nextTick()
    expect(mounted.context.colorMode.value).toBe('light')
    expect(mounted.context.isDark.value).toBe(false)
  })

  it('applies data-fr-theme attribute to document', async () => {
    const mounted = mountColorMode()
    unmount = mounted.unmount

    mounted.context.setColorMode('light')
    await nextTick()

    expect(document.documentElement.getAttribute('data-fr-theme')).toBe('light')

    mounted.context.setColorMode('dark')
    await nextTick()

    expect(document.documentElement.getAttribute('data-fr-theme')).toBe('dark')
  })

  it('isDark reflects colorMode correctly', async () => {
    const mounted = mountColorMode()
    unmount = mounted.unmount

    mounted.context.setColorMode('light')
    await nextTick()
    expect(mounted.context.isDark.value).toBe(false)

    mounted.context.setColorMode('dark')
    await nextTick()
    expect(mounted.context.isDark.value).toBe(true)
  })

  it('responds to system preference changes in system mode', async () => {
    const mounted = mountColorMode()
    unmount = mounted.unmount

    mounted.context.setColorMode('system')
    await nextTick()

    const initialDark = mounted.context.isDark.value

    mediaQueryMock.dispatchChange(!initialDark)
    await nextTick()

    expect(mounted.context.isDark.value).toBe(!initialDark)
  })

  it('ignores system preference changes when not in system mode', async () => {
    const mounted = mountColorMode()
    unmount = mounted.unmount

    mounted.context.setColorMode('light')
    await nextTick()

    mediaQueryMock.dispatchChange(true)
    await nextTick()

    expect(mounted.context.isDark.value).toBe(false)
    expect(document.documentElement.getAttribute('data-fr-theme')).toBe('light')
  })

  it('reads mode from localStorage on mount', async () => {
    localStorageMock.setItem('csp_color_mode', 'light')

    const mounted = mountColorMode()
    unmount = mounted.unmount
    await nextTick()

    expect(mounted.context.colorMode.value).toBe('light')
  })
})
