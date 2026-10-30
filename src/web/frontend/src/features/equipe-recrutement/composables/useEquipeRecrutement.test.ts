import type { MembreEquipe } from '../types'
import { PiniaColada, useQueryCache } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { recrutementsActifsQuery, recrutementsArchivesQuery } from '@/features/recrutements/queries'
import { useEquipeRecrutement } from './useEquipeRecrutement'

const mockGetEquipeRecrutement = vi.fn()
const mockUpdateMembreEquipe = vi.fn()

vi.mock('../api', () => ({
  getEquipeRecrutement: (...args: unknown[]) => mockGetEquipeRecrutement(...args),
  updateMembreEquipe: (...args: unknown[]) => mockUpdateMembreEquipe(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'
const AUTRE_RECRUTEMENT_UUID = 'aaaaaaaa-0002-0002-0002-000000000002'

const MEMBRES: MembreEquipe[] = [
  {
    uuid: 'bbbbbbbb-0001-0001-0001-000000000001',
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
  let queryCache!: ReturnType<typeof useQueryCache>
  const wrapper = mount(defineComponent({
    setup() {
      result = useEquipeRecrutement(ORGANISME_UUID, recrutementUuid)
      queryCache = useQueryCache()
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return { result, wrapper, queryCache }
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
    expect(mockGetEquipeRecrutement).toHaveBeenCalledWith({ organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID })
  })

  it('exposes an empty team while the members are loading', () => {
    const { result } = mountEquipe()
    expect(result.membres.value).toEqual([])
  })

  it('revokes a member with their current role and a revocation date', async () => {
    const { result } = mountEquipe()
    await flush()

    await result.revoke(MEMBRES[0])

    expect(mockUpdateMembreEquipe).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      agent_id: MEMBRES[0].uuid,
      recrutement_role: MEMBRES[0].recrutement_role,
      date_revocation_recrutement: expect.any(String),
    })
  })

  it('refreshes the team once a member has been revoked', async () => {
    const { result } = mountEquipe()
    await flush()
    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(1)

    await result.revoke(MEMBRES[0])
    await flush()

    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(2)
  })

  it('marks the recrutement lists as outdated once a member has been revoked', async () => {
    const { result, queryCache } = mountEquipe()
    await flush()
    const listes = [
      queryCache.ensure(recrutementsActifsQuery({ organismeUuid: ORGANISME_UUID })),
      queryCache.ensure(recrutementsArchivesQuery({ organismeUuid: ORGANISME_UUID })),
    ]
    listes.forEach(entry => queryCache.setQueryData(entry.key, { count: 0, results: [] }))
    expect(listes.map(entry => entry.stale)).toEqual([false, false])

    await result.revoke(MEMBRES[0])

    expect(listes.map(entry => entry.stale)).toEqual([true, true])
  })

  it('changes the role of a member without revoking them', async () => {
    const { result } = mountEquipe()
    await flush()

    await result.changeRole({ membre: MEMBRES[0], role: 'contributeur' })

    expect(mockUpdateMembreEquipe).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      agent_id: MEMBRES[0].uuid,
      recrutement_role: 'contributeur',
    })
  })

  it('refreshes the team once a role has changed', async () => {
    const { result } = mountEquipe()
    await flush()
    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(1)

    await result.changeRole({ membre: MEMBRES[0], role: 'contributeur' })
    await flush()

    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(2)
  })

  it('does not share the cache between two recrutements', async () => {
    mountEquipe()
    await flush()
    mountEquipe(AUTRE_RECRUTEMENT_UUID)
    await flush()

    expect(mockGetEquipeRecrutement).toHaveBeenCalledTimes(2)
    expect(mockGetEquipeRecrutement).toHaveBeenLastCalledWith({
      organismeUuid: ORGANISME_UUID,
      recrutementUuid: AUTRE_RECRUTEMENT_UUID,
    })
  })
})
