import { createPinia, setActivePinia } from 'pinia'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useCurrentUserStore } from './currentUser'

const mockGetMe = vi.fn()

vi.mock('@/api/utilisateur', () => ({
  getMe: () => mockGetMe(),
}))

describe('useCurrentUserStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('fetches user and exposes reactive state', async () => {
    const userData = { email: 'test@example.com', prenom: 'Jean', nom: 'Dupont' }
    mockGetMe.mockResolvedValue(userData)

    const store = useCurrentUserStore()

    expect(store.user).toBeNull()
    expect(store.loading).toBe(false)

    const promise = store.fetch()
    expect(store.loading).toBe(true)

    await promise

    expect(store.loading).toBe(false)
    expect(store.user).toEqual(userData)
    expect(store.displayName).toBe('Jean Dupont')
  })

  it('handles fetch error gracefully', async () => {
    const networkError = new Error('Network error')
    mockGetMe.mockRejectedValue(networkError)

    const store = useCurrentUserStore()

    await store.fetch()

    expect(store.user).toBeNull()
    expect(store.error).toBe(networkError)
  })

  it('deduplicates concurrent fetch calls', async () => {
    const userData = { email: 'test@example.com', prenom: 'Jean', nom: 'Dupont' }
    mockGetMe.mockResolvedValue(userData)

    const store = useCurrentUserStore()

    const promise1 = store.fetch()
    const promise2 = store.fetch()

    await Promise.all([promise1, promise2])

    expect(mockGetMe).toHaveBeenCalledTimes(1)
  })
})
