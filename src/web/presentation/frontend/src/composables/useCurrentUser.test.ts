import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { useCurrentUser } from './useCurrentUser'

const mockGetMe = vi.fn()

vi.mock('@/api/utilisateur', () => ({
  getMe: () => mockGetMe(),
}))

describe('useCurrentUser', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('fetches user and exposes reactive state', async () => {
    const userData = { email: 'test@example.com', prenom: 'Jean', nom: 'Dupont' }
    mockGetMe.mockResolvedValue(userData)

    const { user, loading, fetch } = useCurrentUser()

    expect(user.value).toBeNull()
    expect(loading.value).toBe(false)

    const promise = fetch()
    expect(loading.value).toBe(true)

    await promise

    expect(loading.value).toBe(false)
    expect(user.value).toEqual(userData)
  })

  it('handles fetch error gracefully', async () => {
    const networkError = new Error('Network error')
    mockGetMe.mockRejectedValue(networkError)

    const { user, error, fetch } = useCurrentUser()

    await fetch()

    expect(user.value).toBeNull()
    expect(error.value).toBe(networkError)
  })

  it('deduplicates concurrent fetch calls', async () => {
    const userData = { email: 'test@example.com', prenom: 'Jean', nom: 'Dupont' }
    mockGetMe.mockResolvedValue(userData)

    const { fetch } = useCurrentUser()

    const promise1 = fetch()
    const promise2 = fetch()

    await Promise.all([promise1, promise2])

    expect(mockGetMe).toHaveBeenCalledTimes(1)
  })
})
