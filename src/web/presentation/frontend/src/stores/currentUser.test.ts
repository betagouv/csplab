import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { getMe } from '@/api/utilisateur'
import { useCurrentUser } from './currentUser'

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

function mountUseCurrentUser() {
  let result!: ReturnType<typeof useCurrentUser>

  mount(defineComponent({
    setup() {
      result = useCurrentUser()
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })

  return result
}

describe('useCurrentUser', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset()
  })

  it('fetches user and exposes reactive state', async () => {
    const userData = { email: 'test@example.com', prenom: 'Jean', nom: 'Dupont' }
    vi.mocked(getMe).mockResolvedValue(userData)

    const { user, displayName, isPending } = mountUseCurrentUser()

    await vi.waitFor(() => expect(isPending.value).toBe(false))

    expect(user.value).toEqual(userData)
    expect(displayName.value).toBe('Jean Dupont')
  })

  it('handles fetch error gracefully', async () => {
    const networkError = new Error('Network error')
    vi.mocked(getMe).mockRejectedValue(networkError)

    const { user, error, isPending } = mountUseCurrentUser()

    await vi.waitFor(() => expect(isPending.value).toBe(false))

    expect(user.value).toBeNull()
    expect(error.value).toBe(networkError)
  })
})
