import type { CandidatureDetail, ChangerEtapeResultat, PaginatedCandidatureListeList, RecrutementDetailKanban } from '../types'
import { PiniaColada, useQuery } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { getRecrutementDetail } from '@/features/recrutements/api'
import { recrutementDetailQuery } from '@/features/recrutements/queries'
import {
  CANDIDATURE_ALICE,
  CANDIDATURE_BRUNO,
  CANDIDATURE_LISTE,
  CANDIDATURE_PARAMS,
  candidatureDetail,
  ETAPE_ENTRETIEN,
  ETAPE_RECEPTION,
  ETAPE_REFUS,
  KANBAN,
  kanbanColumns,
  ORGANISME_UUID,
  RECRUTEMENT_DETAIL,
  RECRUTEMENT_UUID,
} from '@/test/fixtures/candidatures'
import { getCandidatureActivites, getCandidatureDetail, getCandidatureListe, getRecrutementKanban, patchEtapeCandidatures } from '../api'
import { candidatureDetailQuery, candidatureListeQuery, recrutementKanbanQuery } from '../queries'
import { moveCandidaturesInKanban } from '../utils/kanban'
import { useCandidatureActivites } from './useCandidatureActivites'
import { useEtapeChangeMutation } from './useEtapeChangeMutation'

vi.mock('../api', () => ({
  getRecrutementKanban: vi.fn(),
  getCandidatureListe: vi.fn(),
  getCandidatureActivites: vi.fn(),
  getCandidatureDetail: vi.fn(),
  patchEtapeCandidatures: vi.fn(),
}))

vi.mock('@/features/recrutements/api', () => ({
  getRecrutementDetail: vi.fn(),
}))

function listeEtapes(liste: PaginatedCandidatureListeList | undefined) {
  return Object.fromEntries((liste?.results ?? []).map(row => [row.uuid, row.etape.uuid]))
}

const RECRUTEMENT = { organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID }
const CHANGE = { etapeCibleUuid: ETAPE_ENTRETIEN, candidatureUuids: [CANDIDATURE_ALICE] }

async function mountEtapeChangeMutation() {
  let context!: ReturnType<typeof useEtapeChangeMutation>
  let kanban!: ReturnType<typeof useQuery<RecrutementDetailKanban>>
  let detail!: ReturnType<typeof useQuery<CandidatureDetail>>
  let liste!: ReturnType<typeof useQuery<PaginatedCandidatureListeList>>
  let recrutementDetail!: ReturnType<typeof useQuery<unknown>>

  mount(defineComponent({
    setup() {
      kanban = useQuery(recrutementKanbanQuery(RECRUTEMENT))
      liste = useQuery(candidatureListeQuery(RECRUTEMENT))
      recrutementDetail = useQuery(recrutementDetailQuery(RECRUTEMENT))
      useCandidatureActivites(CANDIDATURE_PARAMS)
      detail = useQuery(candidatureDetailQuery(CANDIDATURE_PARAMS))
      context = useEtapeChangeMutation(RECRUTEMENT)
      return () => h('div')
    },
  }), {
    global: { plugins: [createPinia(), PiniaColada] },
  })

  await vi.waitFor(() => expect(kanban.data.value && detail.data.value && liste.data.value && recrutementDetail.data.value).toBeDefined())
  return { context, kanban, detail, liste }
}

describe('useEtapeChangeMutation', () => {
  beforeEach(() => {
    vi.mocked(getRecrutementKanban).mockReset().mockResolvedValue(KANBAN)
    vi.mocked(getCandidatureListe).mockReset().mockResolvedValue(CANDIDATURE_LISTE)
    vi.mocked(getRecrutementDetail).mockReset().mockResolvedValue(RECRUTEMENT_DETAIL)
    vi.mocked(getCandidatureActivites).mockReset().mockResolvedValue({ count: 0, next: null, previous: null, results: [] })
    vi.mocked(getCandidatureDetail).mockReset().mockImplementation(async ({ candidatureUuid }) => candidatureDetail(candidatureUuid))
    vi.mocked(patchEtapeCandidatures).mockReset().mockResolvedValue({ reussites: [CANDIDATURE_ALICE], echecs: [] })
  })

  it('moves the candidatures in the kanban and the list before the api answers', async () => {
    vi.mocked(patchEtapeCandidatures).mockImplementation(() => new Promise(() => {}))
    const { context, kanban, liste } = await mountEtapeChangeMutation()

    void context.changeEtape({ etapeCibleUuid: ETAPE_ENTRETIEN, candidatureUuids: [CANDIDATURE_ALICE, CANDIDATURE_BRUNO] })

    expect(kanbanColumns(kanban.data.value)[ETAPE_ENTRETIEN]).toEqual([CANDIDATURE_ALICE, CANDIDATURE_BRUNO])
    expect(listeEtapes(liste.data.value)).toEqual({ [CANDIDATURE_ALICE]: ETAPE_ENTRETIEN, [CANDIDATURE_BRUNO]: ETAPE_ENTRETIEN })
    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      etapeCibleUuid: ETAPE_ENTRETIEN,
      candidatureUuids: [CANDIDATURE_ALICE, CANDIDATURE_BRUNO],
    }))
  })

  it('shows the new stage in the detail of the moved candidature, and restores it when the api call fails', async () => {
    let fail!: (error: Error) => void
    vi.mocked(patchEtapeCandidatures).mockImplementation(() => new Promise<ChangerEtapeResultat>((_resolve, reject) => {
      fail = reject
    }))
    const { context, detail } = await mountEtapeChangeMutation()
    vi.mocked(getCandidatureDetail).mockImplementation(() => new Promise(() => {}))

    const change = context.changeEtape(CHANGE)
    expect(detail.data.value?.etape_actuelle.uuid).toBe(ETAPE_ENTRETIEN)

    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalled())
    fail(new Error('boom'))
    await expect(change).resolves.toBe(false)
    expect(detail.data.value?.etape_actuelle.uuid).toBe(ETAPE_RECEPTION)
  })

  it('reloads the list and the moved candidature once the change is saved', async () => {
    const { context } = await mountEtapeChangeMutation()

    await expect(context.changeEtape(CHANGE)).resolves.toBe(true)

    await vi.waitFor(() => expect(getCandidatureListe).toHaveBeenCalledTimes(2))
    await vi.waitFor(() => expect(getCandidatureActivites).toHaveBeenCalledTimes(2))
    expect(getRecrutementKanban).toHaveBeenCalledTimes(1)
  })

  it('restores the kanban and the list when the api call fails', async () => {
    vi.mocked(patchEtapeCandidatures).mockRejectedValue(new Error('boom'))
    const { context, kanban, liste } = await mountEtapeChangeMutation()
    vi.mocked(getCandidatureListe).mockImplementation(() => new Promise(() => {}))

    await expect(context.changeEtape(CHANGE)).resolves.toBe(false)

    expect(kanbanColumns(kanban.data.value)).toEqual(kanbanColumns(KANBAN))
    expect(listeEtapes(liste.data.value)).toEqual(listeEtapes(CANDIDATURE_LISTE))
  })

  it('keeps a later move and reloads the kanban when an earlier move fails', async () => {
    let failFirst!: (error: Error) => void
    vi.mocked(patchEtapeCandidatures)
      .mockImplementationOnce(() => new Promise<ChangerEtapeResultat>((_resolve, reject) => {
        failFirst = reject
      }))
      .mockImplementationOnce(() => new Promise(() => {}))
    vi.mocked(getRecrutementKanban)
      .mockResolvedValueOnce(KANBAN)
      .mockResolvedValueOnce(moveCandidaturesInKanban(KANBAN, [CANDIDATURE_BRUNO], ETAPE_REFUS))
    const { context, kanban } = await mountEtapeChangeMutation()

    const first = context.changeEtape(CHANGE)
    void context.changeEtape({ etapeCibleUuid: ETAPE_REFUS, candidatureUuids: [CANDIDATURE_BRUNO] })
    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalledTimes(2))
    failFirst(new Error('boom'))

    await expect(first).resolves.toBe(false)
    await vi.waitFor(() => expect(getRecrutementKanban).toHaveBeenCalledTimes(2))
    expect(kanbanColumns(kanban.data.value)[ETAPE_REFUS]).toEqual([CANDIDATURE_BRUNO])
  })

  it('reloads the kanban when a later move changed it while an earlier one was saving', async () => {
    let saveFirst!: (resultat: ChangerEtapeResultat) => void
    vi.mocked(patchEtapeCandidatures)
      .mockImplementationOnce(() => new Promise<ChangerEtapeResultat>((resolve) => {
        saveFirst = resolve
      }))
      .mockImplementationOnce(() => new Promise(() => {}))
    const { context } = await mountEtapeChangeMutation()

    const first = context.changeEtape(CHANGE)
    void context.changeEtape({ etapeCibleUuid: ETAPE_REFUS, candidatureUuids: [CANDIDATURE_BRUNO] })
    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalledTimes(2))
    saveFirst({ reussites: [CANDIDATURE_ALICE], echecs: [] })

    await expect(first).resolves.toBe(true)
    await vi.waitFor(() => expect(getRecrutementKanban).toHaveBeenCalledTimes(2))
  })

  it('reloads the kanban when the api reports partial failures', async () => {
    vi.mocked(patchEtapeCandidatures).mockResolvedValue({
      reussites: [],
      echecs: [{ candidature_uuid: CANDIDATURE_ALICE, raison: 'conflit' }],
    })
    const { context } = await mountEtapeChangeMutation()

    await expect(context.changeEtape(CHANGE)).resolves.toBe(false)

    await vi.waitFor(() => expect(getRecrutementKanban).toHaveBeenCalledTimes(2))
  })
})
