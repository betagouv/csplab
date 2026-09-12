import type { MembreEquipe } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { useEquipeRecrutement } from './useEquipeRecrutement'

const mockGetEquipeRecrutement = vi.fn()

vi.mock('../api', () => ({
  getEquipeRecrutement: (...args: unknown[]) => mockGetEquipeRecrutement(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'
const AUTRE_RECRUTEMENT_UUID = 'aaaaaaaa-0002-0002-0002-000000000002'

const MEMBRES: MembreEquipe[] = [
  {
    agent_id: 'bbbbbbbb-0001-0001-0001-000000000001',
    nom: 'Dupont',
    prenom: 'Jeanne',
    poste: 'Responsable recrutement',
    email: 'jeanne.dupont@example.gouv.fr',
    recrutement_role: 'responsable',
  },
]

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountEquipe(recrutementUuid = RECRUTEMENT_UUID) {
  let result!: ReturnType<typeof useEquipeRecrutement>
  const wrapper = mount(defineComponent({
    setup() {
      result = useEquipeRecrutement(ORGANISME_UUID, recrutementUuid)
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return { result, wrapper }
}

describe('useEquipeRecrutement', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetEquipeRecrutement.mockResolvedValue(MEMBRES)
  })

  it('exposes the members of the recrutement', async () => {
    const { result } = mountEquipe()
    expect(result.pending.value).toBe(true)

    await flush()

    expect(result.pending.value).toBe(false)
    expect(result.membres.value).toEqual(MEMBRES)
    expect(mockGetEquipeRecrutement).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID)
  })

  it('exposes an empty team while the members are loading', () => {
    const { result } = mountEquipe()
    expect(result.membres.value).toEqual([])
  })

  it('does not share the cache between two recrutements', async () => {
    mountEquipe()
    await flush()
    mountEquipe(AUTRE_RECRUTEMENT_UUID)
    await flush()

    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(2)
    expect(mockGetEquipeRecrutement).toHaveBeenLastCalledWith(
      ORGANISME_UUID,
      AUTRE_RECRUTEMENT_UUID,
    )
  })
})
