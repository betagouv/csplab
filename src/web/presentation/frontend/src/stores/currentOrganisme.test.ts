import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { getMe } from '@/api/utilisateur'
import { useCurrentOrganisme } from './currentOrganisme'

function mountUseCurrentOrganisme() {
  let result!: ReturnType<typeof useCurrentOrganisme>

  mount(defineComponent({
    setup() {
      result = useCurrentOrganisme()
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })

  return result
}

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

describe('useCurrentOrganisme', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset()
  })

  it('fetches organisme and exposes reactive state', async () => {
    const userData = {
      email: 'test@example.com',
      prenom: 'Jean',
      nom: 'Dupont',
      organisme_roles: [{ organisme_uuid: 'a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1', nom: 'Ministère de la Transition Écologique', role: 'responsable' }],
    }
    vi.mocked(getMe).mockResolvedValue(userData)

    const { organisme, organismeUuid } = mountUseCurrentOrganisme()

    await vi.waitFor(() => expect(organisme.value).toEqual(userData.organisme_roles[0]))

    expect(organismeUuid.value).toBe('a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1')
  })

  it('handles fetch error gracefully', async () => {
    const networkError = new Error('Network error')
    vi.mocked(getMe).mockRejectedValue(networkError)

    const { organisme, organismeUuid } = mountUseCurrentOrganisme()

    await vi.waitFor(() => expect(organisme.value).toBeNull())

    expect(organismeUuid.value).toBeNull()
  })
})
