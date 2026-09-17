import { afterEach, describe, expect, it, vi } from 'vitest'
import { createApp, defineComponent, h, nextTick } from 'vue'
import { useMediaQuery } from './useMediaQuery'

function createMediaQueryMock(matches: boolean) {
  const listeners = new Set<() => void>()
  return {
    matches,
    addEventListener: (_: string, listener: () => void) => listeners.add(listener),
    removeEventListener: (_: string, listener: () => void) => listeners.delete(listener),
    setMatches(value: boolean) {
      this.matches = value
      listeners.forEach(listener => listener())
    },
    get listenerCount() {
      return listeners.size
    },
  }
}

function mountQuery(query: string) {
  let matches!: ReturnType<typeof useMediaQuery>
  const app = createApp(defineComponent({
    setup() {
      matches = useMediaQuery(query)
      return () => h('div')
    },
  }))
  app.mount(document.createElement('div'))
  return {
    get matches() {
      return matches
    },
    unmount: () => app.unmount(),
  }
}

describe('useMediaQuery', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('reflects the query and follows its changes', async () => {
    const mock = createMediaQueryMock(false)
    const matchMedia = vi.fn(() => mock)
    vi.stubGlobal('matchMedia', matchMedia)

    const mounted = mountQuery('(width < 48em)')

    expect(matchMedia).toHaveBeenCalledWith('(width < 48em)')
    expect(mounted.matches.value).toBe(false)

    mock.setMatches(true)
    await nextTick()
    expect(mounted.matches.value).toBe(true)

    mounted.unmount()
    expect(mock.listenerCount).toBe(0)
  })
})
