import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { createApp, defineComponent, h, nextTick } from 'vue'
import {
  provideSidebar,
  SIDEBAR_BREAKPOINT,
  SIDEBAR_KEYBOARD_SHORTCUT,
  SIDEBAR_STORAGE_KEY,
  useSidebar,
} from './useSidebar'

function setViewportWidth(width: number) {
  Object.defineProperty(window, 'innerWidth', {
    configurable: true,
    writable: true,
    value: width,
  })
  window.dispatchEvent(new Event('resize'))
}

function mountSidebar(options: Parameters<typeof provideSidebar>[0] = {}) {
  let context!: ReturnType<typeof provideSidebar>

  const TestApp = defineComponent({
    setup() {
      context = provideSidebar(options)
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

function mountSidebarWithChild(options: Parameters<typeof provideSidebar>[0] = {}) {
  let childSidebar!: ReturnType<typeof useSidebar>

  const Child = defineComponent({
    setup() {
      childSidebar = useSidebar()
      return () => h('span')
    },
  })

  const Parent = defineComponent({
    setup() {
      provideSidebar(options)
      return () => h(Child)
    },
  })

  const el = document.createElement('div')
  const app = createApp(Parent)
  app.mount(el)

  return {
    get sidebar() {
      return childSidebar
    },
    unmount() {
      app.unmount()
    },
  }
}

function createLocalStorageMock() {
  const storage = new Map<string, string>()

  return {
    getItem: (key: string) => storage.get(key) ?? null,
    setItem: (key: string, value: string) => storage.set(key, value),
    removeItem: (key: string) => storage.delete(key),
    clear: () => storage.clear(),
  }
}

describe('useSidebar', () => {
  let unmount: (() => void) | undefined
  let localStorageMock: ReturnType<typeof createLocalStorageMock>

  beforeEach(() => {
    localStorageMock = createLocalStorageMock()
    vi.stubGlobal('localStorage', localStorageMock)
    setViewportWidth(SIDEBAR_BREAKPOINT + 100)
  })

  afterEach(() => {
    unmount?.()
    unmount = undefined
    vi.unstubAllGlobals()
  })

  it('throws when used outside a provider', () => {
    const Orphan = defineComponent({
      setup() {
        useSidebar()
        return () => h('div')
      },
    })

    expect(() => createApp(Orphan).mount(document.createElement('div'))).toThrow(
      'useSidebar must be used within a CspSidebar provider',
    )
  })

  it('exposes sidebar context to child components', () => {
    const mounted = mountSidebarWithChild({ defaultExpanded: true })
    unmount = mounted.unmount

    expect(mounted.sidebar.isExpanded.value).toBe(true)
    expect(mounted.sidebar.state.value).toBe('expanded')
  })

  it('uses defaultExpanded when localStorage is empty', () => {
    const mounted = mountSidebar({ defaultExpanded: false })
    unmount = mounted.unmount

    expect(mounted.context.isExpanded.value).toBe(false)
    expect(mounted.context.state.value).toBe('collapsed')
  })

  it('reads initial expanded state from localStorage', () => {
    localStorageMock.setItem(SIDEBAR_STORAGE_KEY, 'false')

    const mounted = mountSidebar({ defaultExpanded: true })
    unmount = mounted.unmount

    expect(mounted.context.isExpanded.value).toBe(false)
  })

  it('persists expanded state to localStorage', () => {
    const mounted = mountSidebar({ persistState: true })
    unmount = mounted.unmount

    mounted.context.setExpanded(false)

    expect(localStorageMock.getItem(SIDEBAR_STORAGE_KEY)).toBe('false')
    expect(mounted.context.state.value).toBe('collapsed')
  })

  it('does not persist when persistState is false', () => {
    const mounted = mountSidebar({ persistState: false })
    unmount = mounted.unmount

    mounted.context.setExpanded(false)

    expect(localStorageMock.getItem(SIDEBAR_STORAGE_KEY)).toBeNull()
  })

  it('toggles expanded state on desktop', async () => {
    const mounted = mountSidebar({ defaultExpanded: true })
    unmount = mounted.unmount
    await nextTick()

    mounted.context.toggle()
    expect(mounted.context.isExpanded.value).toBe(false)

    mounted.context.toggle()
    expect(mounted.context.isExpanded.value).toBe(true)
  })

  it('toggles mobile drawer on small viewports', async () => {
    setViewportWidth(SIDEBAR_BREAKPOINT)

    const mounted = mountSidebar()
    unmount = mounted.unmount
    await nextTick()

    expect(mounted.context.isMobile.value).toBe(true)

    mounted.context.toggle()
    expect(mounted.context.isMobileOpen.value).toBe(true)
    expect(mounted.context.isExpanded.value).toBe(true)

    mounted.context.toggle()
    expect(mounted.context.isMobileOpen.value).toBe(false)
  })

  it('closes mobile drawer when viewport becomes desktop', async () => {
    setViewportWidth(SIDEBAR_BREAKPOINT)

    const mounted = mountSidebar()
    unmount = mounted.unmount
    await nextTick()

    mounted.context.setMobileOpen(true)
    expect(mounted.context.isMobileOpen.value).toBe(true)

    setViewportWidth(SIDEBAR_BREAKPOINT + 100)
    await nextTick()

    expect(mounted.context.isMobile.value).toBe(false)
    expect(mounted.context.isMobileOpen.value).toBe(false)
  })

  it('toggles on Ctrl+B keyboard shortcut', async () => {
    const mounted = mountSidebar({ defaultExpanded: true })
    unmount = mounted.unmount
    await nextTick()

    window.dispatchEvent(new KeyboardEvent('keydown', {
      key: SIDEBAR_KEYBOARD_SHORTCUT,
      ctrlKey: true,
      bubbles: true,
    }))
    await nextTick()

    expect(mounted.context.isExpanded.value).toBe(false)
  })
})
