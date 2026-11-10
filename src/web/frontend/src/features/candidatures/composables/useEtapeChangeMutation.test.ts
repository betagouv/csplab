import type { CandidatureDetail, ChangerEtapeResultat, RecrutementListe } from '../types'
import { PiniaColada, useQuery } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { useToast } from '@/composables/ui/useToast'
import {
  CANDIDAT_ALICE,
  CANDIDAT_BRUNO,
  CANDIDATURE_ALICE,
  CANDIDATURE_BRUNO,
  CANDIDATURE_LISTE,
  CANDIDATURE_PARAMS,
  candidatureDetail,
  ETAPE_ENTRETIEN,
  ETAPE_RECEPTION,
  ETAPE_REFUS,
  ORGANISME_UUID,
  RECRUTEMENT_UUID,
} from '@/test/fixtures/candidatures'
import { getCandidatureActivites, getCandidatureDetail, getCandidatureListe, patchEtapeCandidatures } from '../api'
import { candidatureDetailQuery, candidatureListeQuery } from '../queries'
import { useCandidatureActivites } from './useCandidatureActivites'
import { useEtapeChangeMutation } from './useEtapeChangeMutation'

vi.mock('../api', () => ({
  getCandidatureListe: vi.fn(),
  getCandidatureActivites: vi.fn(),
  getCandidatureDetail: vi.fn(),
  patchEtapeCandidatures: vi.fn(),
}))

function listeEtapes(liste: RecrutementListe | undefined) {
  return Object.fromEntries((liste?.results ?? []).map(row => [row.uuid, row.etape.uuid]))
}

const RECRUTEMENT = { organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID }
const CHANGE = { etapeCibleUuid: ETAPE_ENTRETIEN, candidatureUuids: [CANDIDATURE_ALICE] }

async function mountEtapeChangeMutation() {
  let context!: ReturnType<typeof useEtapeChangeMutation>
  let detail!: ReturnType<typeof useQuery<CandidatureDetail>>
  let liste!: ReturnType<typeof useQuery<RecrutementListe>>

  mount(defineComponent({
    setup() {
      liste = useQuery(candidatureListeQuery(RECRUTEMENT))
      useCandidatureActivites(CANDIDATURE_PARAMS)
      detail = useQuery(candidatureDetailQuery(CANDIDATURE_PARAMS))
      context = useEtapeChangeMutation(RECRUTEMENT)
      return () => h('div')
    },
  }), {
    global: { plugins: [createPinia(), PiniaColada] },
  })

  await vi.waitFor(() => expect(detail.data.value && liste.data.value).toBeDefined())
  return { context, detail, liste }
}

describe('useEtapeChangeMutation', () => {
  beforeEach(() => {
    vi.mocked(getCandidatureListe).mockReset().mockResolvedValue(CANDIDATURE_LISTE)
    vi.mocked(getCandidatureActivites).mockReset().mockResolvedValue({ count: 0, next: null, previous: null, results: [] })
    vi.mocked(getCandidatureDetail).mockReset().mockImplementation(async ({ candidatureUuid }) => candidatureDetail(candidatureUuid))
    vi.mocked(patchEtapeCandidatures).mockReset().mockResolvedValue({ reussites: [CANDIDATURE_ALICE], echecs: [] })
  })

  it('moves the candidatures in the list before the api answers', async () => {
    vi.mocked(patchEtapeCandidatures).mockImplementation(() => new Promise(() => {}))
    const { context, liste } = await mountEtapeChangeMutation()

    void context.changeEtape({ etapeCibleUuid: ETAPE_ENTRETIEN, candidatureUuids: [CANDIDATURE_ALICE, CANDIDATURE_BRUNO] }, [CANDIDAT_ALICE, CANDIDAT_BRUNO])

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

    const change = context.changeEtape(CHANGE, [CANDIDAT_ALICE])
    expect(detail.data.value?.etape_actuelle.uuid).toBe(ETAPE_ENTRETIEN)

    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalled())
    fail(new Error('boom'))
    await expect(change).resolves.toBe(false)
    expect(detail.data.value?.etape_actuelle.uuid).toBe(ETAPE_RECEPTION)
  })

  it('shows a success toast and reloads the list and the moved candidature once the change is saved', async () => {
    const { context } = await mountEtapeChangeMutation()

    await expect(context.changeEtape(CHANGE, [CANDIDAT_ALICE])).resolves.toBe(true)

    expect(useToast().toasts.value.at(-1)?.title).toBe('La candidature d\'Alice Dupont est passée à l\'étape Entretien')
    await vi.waitFor(() => expect(getCandidatureListe).toHaveBeenCalledTimes(2))
    await vi.waitFor(() => expect(getCandidatureActivites).toHaveBeenCalledTimes(2))
  })

  it('restores the list when the api call fails', async () => {
    vi.mocked(patchEtapeCandidatures).mockRejectedValue(new Error('boom'))
    const { context, liste } = await mountEtapeChangeMutation()
    vi.mocked(getCandidatureListe).mockImplementation(() => new Promise(() => {}))

    await expect(context.changeEtape(CHANGE, [CANDIDAT_ALICE])).resolves.toBe(false)

    expect(listeEtapes(liste.data.value)).toEqual(listeEtapes(CANDIDATURE_LISTE))
  })

  it('keeps a later move in the list when an earlier move fails', async () => {
    let failFirst!: (error: Error) => void
    vi.mocked(patchEtapeCandidatures)
      .mockImplementationOnce(() => new Promise<ChangerEtapeResultat>((_resolve, reject) => {
        failFirst = reject
      }))
      .mockImplementationOnce(() => new Promise(() => {}))
    const { context, liste } = await mountEtapeChangeMutation()
    vi.mocked(getCandidatureListe).mockImplementation(() => new Promise(() => {}))

    const first = context.changeEtape(CHANGE, [CANDIDAT_ALICE])
    void context.changeEtape({ etapeCibleUuid: ETAPE_REFUS, candidatureUuids: [CANDIDATURE_BRUNO] }, [CANDIDAT_BRUNO])
    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalledTimes(2))
    failFirst(new Error('boom'))

    await expect(first).resolves.toBe(false)
    expect(listeEtapes(liste.data.value)[CANDIDATURE_BRUNO]).toBe(ETAPE_REFUS)
  })
})
