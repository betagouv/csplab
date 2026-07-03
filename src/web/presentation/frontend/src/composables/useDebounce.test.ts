import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { effectScope, nextTick, ref } from 'vue'
import { useDebounce } from './useDebounce'

describe('useDebounce', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => vi.useRealTimers())

  it('starts with the source value', () => {
    const source = ref('a')
    expect(useDebounce(source, 200).value).toBe('a')
  })

  it('delays updates until the delay has elapsed', async () => {
    const source = ref('a')
    const debounced = useDebounce(source, 200)

    source.value = 'b'
    await nextTick()
    expect(debounced.value).toBe('a')

    vi.advanceTimersByTime(200)
    expect(debounced.value).toBe('b')
  })

  it('only keeps the last value within the delay window', async () => {
    const source = ref('a')
    const debounced = useDebounce(source, 200)

    source.value = 'b'
    await nextTick()
    vi.advanceTimersByTime(100)
    source.value = 'c'
    await nextTick()
    vi.advanceTimersByTime(100)
    expect(debounced.value).toBe('a')

    vi.advanceTimersByTime(100)
    expect(debounced.value).toBe('c')
  })

  it('cancels a pending update when its scope is disposed', async () => {
    const source = ref('a')
    const scope = effectScope()
    const debounced = scope.run(() => useDebounce(source, 200))!

    source.value = 'b'
    await nextTick()
    scope.stop()
    vi.advanceTimersByTime(200)
    expect(debounced.value).toBe('a')
  })
})
