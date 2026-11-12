import { PiniaColada } from '@pinia/colada'
import { mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h, ref } from 'vue'
import { CANDIDATURE_LISTE, ETAPE_REFUS, MOTIFS_REFUS, ORGANISME_UUID } from '@/test/fixtures/candidatures'
import { getMotifsRefus } from '../api'
import { useRefusCandidature } from './useRefusCandidature'

vi.mock('../api', () => ({
  getMotifsRefus: vi.fn(),
}))

function mountRefusCandidature(etapes = ref(CANDIDATURE_LISTE.etapes)) {
  let context!: ReturnType<typeof useRefusCandidature>

  mount(defineComponent({
    setup() {
      context = useRefusCandidature(ORGANISME_UUID, etapes)
      return () => h('div')
    },
  }), {
    global: { plugins: [createPinia(), PiniaColada] },
  })

  return context
}

describe('useRefusCandidature', () => {
  beforeEach(() => {
    vi.mocked(getMotifsRefus).mockReset().mockResolvedValue(MOTIFS_REFUS)
  })

  it('finds the refusal stage among the stages of the recrutement', () => {
    const etapes = ref(CANDIDATURE_LISTE.etapes.filter(etape => etape.categorie !== 'REFUS'))
    const refus = mountRefusCandidature(etapes)

    expect(refus.refusEtapeUuid.value).toBeNull()

    etapes.value = CANDIDATURE_LISTE.etapes
    expect(refus.refusEtapeUuid.value).toBe(ETAPE_REFUS)
  })
})
