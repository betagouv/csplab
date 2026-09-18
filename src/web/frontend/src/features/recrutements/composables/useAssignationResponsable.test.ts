import type { AgentRecherche } from '@/features/organismes/types'
import { PiniaColada, useQuery } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, nextTick } from 'vue'
import { RECRUTEMENTS_ACTIFS } from '../mock'
import { recrutementsActifsQuery } from '../queries'
import { useAssignationResponsable } from './useAssignationResponsable'

const mockGetRecrutementsActifs = vi.fn()
const mockSetRecrutementsResponsable = vi.fn()
const mockSearchAgentByEmail = vi.fn()
const mockCreateAgent = vi.fn()

vi.mock('../api', () => ({
  getRecrutementDetail: vi.fn(),
  getRecrutementsActifs: (...args: unknown[]) => mockGetRecrutementsActifs(...args),
  getRecrutementsArchives: vi.fn(),
  setRecrutementsResponsable: (...args: unknown[]) => mockSetRecrutementsResponsable(...args),
}))

vi.mock('@/features/organismes/api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeDetail: vi.fn(),
  getOrganismeAgents: vi.fn(),
  searchAgentByEmail: (...args: unknown[]) => mockSearchAgentByEmail(...args),
  createAgent: (...args: unknown[]) => mockCreateAgent(...args),
}))

const ORGANISME_UUID = '11111111-1111-1111-1111-111111111111'
const AGENT_ID = 'bbbbbbbb-0001-0001-0001-000000000001'
const NOUVEL_AGENT_ID = 'bbbbbbbb-0002-0002-0002-000000000002'
const EMAIL = 'jeanne.dupont@example.gouv.fr'

const AGENT: AgentRecherche = {
  agent_id: AGENT_ID,
  email: EMAIL,
  prenom: 'Jeanne',
  nom: 'Dupont',
  intitule_poste: 'Chargée de recrutement',
}

async function flush() {
  await new Promise(resolve => setTimeout(resolve, 0))
  await nextTick()
}

function mountAssignation() {
  let result!: ReturnType<typeof useAssignationResponsable>
  mount(defineComponent({
    setup() {
      result = useAssignationResponsable(ORGANISME_UUID)
      useQuery(() => recrutementsActifsQuery({ organismeUuid: ORGANISME_UUID }))
      return () => h('div')
    },
  }), {
    global: {
      plugins: [createPinia(), PiniaColada],
    },
  })
  return result
}

describe('useAssignationResponsable', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockGetRecrutementsActifs.mockResolvedValue({ results: RECRUTEMENTS_ACTIFS })
    mockSearchAgentByEmail.mockResolvedValue(AGENT)
    mockCreateAgent.mockResolvedValue({ ...AGENT, agent_id: NOUVEL_AGENT_ID, prenom: '', nom: '' })
    mockSetRecrutementsResponsable.mockResolvedValue({ reussites: ['rec-1'], echecs: [] })
  })

  it('refreshes the active recrutements once the found agent has been assigned', async () => {
    const result = mountAssignation()
    await flush()
    expect(mockGetRecrutementsActifs).toHaveBeenCalledTimes(1)

    await result.search(EMAIL)
    await result.assigner(['rec-1'])
    await flush()

    expect(result.status.value).toBe('found')
    expect(mockCreateAgent).not.toHaveBeenCalled()
    expect(mockSetRecrutementsResponsable).toHaveBeenCalledWith(ORGANISME_UUID, {
      recrutement_ids: ['rec-1'],
      agent_id: AGENT_ID,
    })
    expect(mockGetRecrutementsActifs).toHaveBeenCalledTimes(2)
  })

  it('creates the account before assigning when no agent matches the email', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    const result = mountAssignation()
    await flush()

    expect(await result.search(EMAIL)).toBe('not-found')

    await result.assigner(['rec-1'])

    expect(mockCreateAgent).toHaveBeenCalledWith({
      email: EMAIL,
      organisme_id: ORGANISME_UUID,
    })
    expect(mockSetRecrutementsResponsable).toHaveBeenCalledWith(ORGANISME_UUID, {
      recrutement_ids: ['rec-1'],
      agent_id: NOUVEL_AGENT_ID,
    })
  })

  it('does not assign anybody when the account creation fails', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    mockCreateAgent.mockRejectedValue(new Error('500'))
    const result = mountAssignation()
    await flush()
    await result.search(EMAIL)

    await expect(result.assigner(['rec-1'])).rejects.toThrow('500')
    expect(mockSetRecrutementsResponsable).not.toHaveBeenCalled()
  })

  it('refuses to assign when no responsable has been searched for', async () => {
    const result = mountAssignation()
    await flush()

    await expect(result.assigner(['rec-1'])).rejects.toThrow('Aucun responsable à assigner.')
    expect(mockSetRecrutementsResponsable).not.toHaveBeenCalled()
  })

  it('stays submitting from the account creation until the assignation is done', async () => {
    mockSearchAgentByEmail.mockResolvedValue(null)
    let acheverCreation!: (agent: unknown) => void
    let acheverAssignation!: (resultat: unknown) => void
    mockCreateAgent.mockReturnValue(new Promise((resolve) => {
      acheverCreation = resolve
    }))
    mockSetRecrutementsResponsable.mockReturnValue(new Promise((resolve) => {
      acheverAssignation = resolve
    }))

    const result = mountAssignation()
    await flush()
    await result.search(EMAIL)

    const enCours = result.assigner(['rec-1'])
    await flush()
    expect(result.submitting.value).toBe(true)

    acheverCreation({ ...AGENT, agent_id: NOUVEL_AGENT_ID })
    await flush()
    expect(result.submitting.value).toBe(true)

    acheverAssignation({ reussites: ['rec-1'], echecs: [] })
    await enCours
    await flush()
    expect(result.submitting.value).toBe(false)
  })

  it('rejects so that the caller can report the failure', async () => {
    mockSetRecrutementsResponsable.mockRejectedValue(new Error('403'))
    const result = mountAssignation()
    await flush()
    await result.search(EMAIL)

    await expect(result.assigner(['rec-1'])).rejects.toThrow('403')
  })
})
