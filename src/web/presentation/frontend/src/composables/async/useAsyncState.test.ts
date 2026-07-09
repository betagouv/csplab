import { describe, expect, it } from 'vitest'
import { ref } from 'vue'
import { runAsyncAction, useAsyncState } from './useAsyncState'

describe('runAsyncAction', () => {
  it('toggles pending and clears error on success', async () => {
    const pending = ref(false)
    const error = ref<Error | null>(new Error('previous'))

    const promise = runAsyncAction(pending, error, async () => {
      expect(pending.value).toBe(true)
      expect(error.value).toBeNull()
    })

    expect(pending.value).toBe(true)
    await promise

    expect(pending.value).toBe(false)
    expect(error.value).toBeNull()
  })

  it('stores error and resets pending on failure', async () => {
    const pending = ref(false)
    const error = ref<Error | null>(null)
    const failure = new Error('Network error')

    await runAsyncAction(pending, error, async () => {
      throw failure
    })

    expect(pending.value).toBe(false)
    expect(error.value).toBe(failure)
  })
})

describe('useAsyncState', () => {
  it('exposes pending, error and run', async () => {
    const { pending, error, run } = useAsyncState()

    expect(pending.value).toBe(false)
    expect(error.value).toBeNull()

    await run(async () => {})

    expect(pending.value).toBe(false)
    expect(error.value).toBeNull()
  })

  it('accepts an initial pending value', () => {
    const { pending } = useAsyncState(true)
    expect(pending.value).toBe(true)
  })
})
