import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { nextTick, ref } from 'vue'
import { useMinimumPending } from './useMinimumPending'

describe('useMinimumPending', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('is inactive when pending never starts', () => {
    const pending = ref(false)
    const display = useMinimumPending(pending)

    expect(display.value).toBe(false)
  })

  it('holds the skeleton until the minimum duration elapses', async () => {
    const pending = ref(true)
    const display = useMinimumPending(pending, 400)

    vi.advanceTimersByTime(100)
    pending.value = false
    await nextTick()

    expect(display.value).toBe(true)

    vi.advanceTimersByTime(299)
    expect(display.value).toBe(true)

    vi.advanceTimersByTime(1)
    expect(display.value).toBe(false)
  })

  it('hides immediately when pending lasted longer than the minimum', async () => {
    const pending = ref(true)
    const display = useMinimumPending(pending, 400)

    vi.advanceTimersByTime(1000)
    pending.value = false
    await nextTick()

    expect(display.value).toBe(false)
  })

  it('stays visible when pending restarts during the hold', async () => {
    const pending = ref(true)
    const display = useMinimumPending(pending, 400)

    vi.advanceTimersByTime(100)
    pending.value = false
    await nextTick()
    pending.value = true
    await nextTick()

    vi.advanceTimersByTime(1000)
    expect(display.value).toBe(true)

    pending.value = false
    await nextTick()
    expect(display.value).toBe(false)
  })
})
