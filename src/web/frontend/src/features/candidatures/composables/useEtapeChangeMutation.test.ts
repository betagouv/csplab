import type { RecrutementListe } from '../types'
import { PiniaColada, useQuery } from '@pinia/colada'
import { render } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import {
  CANDIDAT_ALICE,
  CANDIDAT_BRUNO,
  CANDIDATURE_ALICE,
  CANDIDATURE_BRUNO,
  CANDIDATURE_LISTE,
  ETAPE_ENTRETIEN,
  ETAPE_REFUS,
  ORGANISME_UUID,
  RECRUTEMENT_UUID,
} from '@/test/fixtures/candidatures'
import { candidatureListe, etapeChangeFailure } from '@/test/handlers/candidatures'
import { server } from '@/test/server'
import { candidatureListeQuery } from '../queries'
import { useEtapeChangeMutation } from './useEtapeChangeMutation'

const RECRUTEMENT = { organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID }

async function mountEtapeChangeMutation() {
  let context!: ReturnType<typeof useEtapeChangeMutation>
  let liste!: ReturnType<typeof useQuery<RecrutementListe>>

  render(defineComponent({
    setup() {
      liste = useQuery(candidatureListeQuery(RECRUTEMENT))
      context = useEtapeChangeMutation(RECRUTEMENT)
      return () => h(CspToaster)
    },
  }), {
    global: { plugins: [createPinia(), PiniaColada] },
  })

  await vi.waitFor(() => expect(liste.data.value).toBeDefined())
  return { context, liste }
}

describe('useEtapeChangeMutation', () => {
  it('keeps a later move in the list when an earlier move fails', async () => {
    const answers = new Map<string | undefined, () => void>()
    server.use(etapeChangeFailure(500, payload => new Promise((resolve) => {
      answers.set(payload?.etape_cible_uuid, resolve)
    })))
    const { context, liste } = await mountEtapeChangeMutation()
    let reload!: () => void
    const reloading = new Promise<void>((resolve) => {
      reload = resolve
    })
    server.use(candidatureListe(CANDIDATURE_LISTE, () => reloading))

    const first = context.changeEtape({ etapeCibleUuid: ETAPE_ENTRETIEN, candidatureUuids: [CANDIDATURE_ALICE] }, [CANDIDAT_ALICE])
    const second = context.changeEtape({ etapeCibleUuid: ETAPE_REFUS, candidatureUuids: [CANDIDATURE_BRUNO] }, [CANDIDAT_BRUNO])
    await vi.waitFor(() => expect(answers.size).toBe(2))
    answers.get(ETAPE_ENTRETIEN)?.()

    await expect(first).resolves.toBe(false)
    expect(liste.data.value?.results.find(row => row.uuid === CANDIDATURE_BRUNO)?.etape.uuid).toBe(ETAPE_REFUS)

    answers.get(ETAPE_REFUS)?.()
    reload()
    await second
    await vi.waitFor(() => expect(liste.asyncStatus.value).toBe('idle'))
  })
})
