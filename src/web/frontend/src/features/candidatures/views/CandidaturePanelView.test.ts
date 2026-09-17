import type { RecrutementDetailKanban } from '../types'
import type { RecrutementDetail } from '@/features/recrutements/types'
import { PiniaColada } from '@pinia/colada'
import { flushPromises, mount } from '@vue/test-utils'
import { createPinia } from 'pinia'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { createRouter, createWebHistory, RouterView } from 'vue-router'
import { getRecrutementDetail } from '@/features/recrutements/api'
import { routes } from '@/router'
import { getRecrutementKanban } from '../api'
import CandidaturePanelView from './CandidaturePanelView.vue'

vi.mock('../api', () => ({
  getRecrutementKanban: vi.fn(),
  getCandidatureListe: vi.fn(),
  patchEtapeCandidatures: vi.fn(),
}))

vi.mock('@/features/recrutements/api', () => ({
  getRecrutementDetail: vi.fn(),
}))

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'
const RECRUTEMENT_UUID = 'aaaaaaaa-0001-0001-0001-000000000001'
const CANDIDATURE_ALICE = 'dddddddd-0001-0001-0001-000000000001'
const CANDIDATURE_INCONNUE = 'dddddddd-0001-0001-0001-000000000099'

const KANBAN_PATH = `/organismes/${ORGANISME_UUID}/recrutements/${RECRUTEMENT_UUID}`

const MOCK_KANBAN: RecrutementDetailKanban = {
  offer_id: RECRUTEMENT_UUID,
  etapes: [
    {
      etape_uuid: 'cccccccc-0001-0001-0001-000000000001',
      nom: 'Réception des candidatures',
      categorie: 'ENTREE',
      candidatures: [
        {
          uuid: CANDIDATURE_ALICE,
          date_soumission: '2025-06-10T09:15:00Z',
          date_derniere_activite: '2025-06-11T10:00:00Z',
          candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000001', nom: 'Dupont', prenom: 'Alice' },
        },
      ],
    },
  ],
}

async function mountPanel(paths: string[]) {
  window.history.replaceState(null, '', '/')
  const router = createRouter({ history: createWebHistory(), routes })
  await router.replace(paths[0]!)
  for (const path of paths.slice(1))
    await router.push(path)

  const wrapper = mount(defineComponent({
    setup: () => () => h(CandidaturePanelView),
  }), {
    attachTo: document.body,
    global: { plugins: [createPinia(), PiniaColada, router], stubs: { RouterView } },
  })
  await flushPromises()
  return { wrapper, router }
}

function panelText(): string {
  return document.querySelector('[role="dialog"]')?.textContent ?? ''
}

describe('candidaturePanelView', () => {
  beforeEach(() => {
    vi.mocked(getRecrutementKanban).mockResolvedValue(MOCK_KANBAN)
    vi.mocked(getRecrutementDetail).mockResolvedValue({ etapes: [] } as unknown as RecrutementDetail)
  })

  afterEach(() => {
    document.body.innerHTML = ''
  })

  it('shows the candidat name and submission date from the kanban data', async () => {
    const { wrapper } = await mountPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    await vi.waitFor(() => expect(panelText()).toContain('Alice Dupont'))
    expect(panelText()).toMatch(/Candidature il y a \d+ jours/)
    wrapper.unmount()
  })

  it('shows an empty state for a candidature absent from the kanban', async () => {
    const { wrapper } = await mountPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_INCONNUE}`])

    await vi.waitFor(() => expect(panelText()).toContain('Candidature introuvable'))
    wrapper.unmount()
  })

  it('goes back to the kanban when opened from it', async () => {
    const { wrapper, router } = await mountPanel([KANBAN_PATH, `${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])
    const back = vi.spyOn(router, 'back')

    document.querySelector<HTMLButtonElement>('button[aria-label="Fermer la candidature et revenir au kanban"]')!.click()

    expect(back).toHaveBeenCalled()
    wrapper.unmount()
  })

  it('replaces the address with the kanban when opened directly', async () => {
    const { wrapper, router } = await mountPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    document.querySelector<HTMLButtonElement>('button[aria-label="Fermer la candidature et revenir au kanban"]')!.click()
    await flushPromises()

    expect(router.currentRoute.value.name).toBe('recrutement-candidatures-kanban')
    wrapper.unmount()
  })
})
