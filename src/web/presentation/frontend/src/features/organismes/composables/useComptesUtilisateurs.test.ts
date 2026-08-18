import type { CompteUtilisateur } from '../types'
import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { useComptesUtilisateurs } from './useComptesUtilisateurs'

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'

const mockGetComptes = vi.fn()
const mockCreateCompte = vi.fn()
const mockResend = vi.fn()

vi.mock('../api', async importOriginal => ({
  ...(await importOriginal<typeof import('../api')>()),
  getComptesUtilisateurs: (...args: unknown[]) => mockGetComptes(...args),
  createCompteUtilisateur: (...args: unknown[]) => mockCreateCompte(...args),
  resendInvitation: (...args: unknown[]) => mockResend(...args),
}))

const COMPTES: CompteUtilisateur[] = [
  {
    uuid: 'c1111111-1111-1111-1111-111111111111',
    prenom: 'Marie',
    nom: 'Dupont',
    email: 'marie.dupont@transition-eco.gouv.fr',
    type: 'gestionnaire',
    poste: 'Responsable RH',
    derniere_activite: '2026-08-18T08:00:00Z',
    creation_compte: '2025-10-01T08:00:00Z',
    invitation_en_attente: false,
  },
]

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountComptes() {
  let result!: ReturnType<typeof useComptesUtilisateurs>
  mount(defineComponent({
    setup() {
      result = useComptesUtilisateurs(ORGANISME_UUID)
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useComptesUtilisateurs', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetComptes.mockResolvedValue(COMPTES)
  })

  it('exposes the comptes of the organisme', async () => {
    const { comptes } = mountComptes()
    await flush()
    expect(mockGetComptes).toHaveBeenCalledWith(ORGANISME_UUID)
    expect(comptes.value).toEqual(COMPTES)
  })

  it('creates a compte and refetches the list', async () => {
    const payload = {
      email: 'nadia.klein@transition-eco.gouv.fr',
      nom: 'Klein',
      prenom: 'Nadia',
      poste: 'Assistante RH',
      type: 'agent' as const,
    }
    mockCreateCompte.mockResolvedValue({ ...COMPTES[0], uuid: 'c9', ...payload })
    const { create } = mountComptes()
    await flush()

    await create(payload)
    await flush()

    expect(mockCreateCompte).toHaveBeenCalledWith(ORGANISME_UUID, payload)
    expect(mockGetComptes).toHaveBeenCalledTimes(2)
  })

  it('resends an invitation', async () => {
    mockResend.mockResolvedValue(undefined)
    const { resend } = mountComptes()
    await flush()

    await resend(COMPTES[0].uuid)

    expect(mockResend).toHaveBeenCalledWith(ORGANISME_UUID, COMPTES[0].uuid)
  })
})
