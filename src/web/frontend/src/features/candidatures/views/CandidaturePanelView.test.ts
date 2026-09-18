import type { RecrutementDetailKanban } from '../types'
import type { RecrutementDetail } from '@/features/recrutements/types'
import { PiniaColada } from '@pinia/colada'
import { render, screen, within } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createRouter, createWebHistory } from 'vue-router'
import { getRecrutementDetail } from '@/features/recrutements/api'
import { routes } from '@/router'
import { setupUser } from '@/test/render'
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
const CANDIDATURE_BRUNO = 'dddddddd-0001-0001-0001-000000000002'
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
        {
          uuid: CANDIDATURE_BRUNO,
          date_soumission: '2025-06-12T09:15:00Z',
          date_derniere_activite: '2025-06-12T10:00:00Z',
          candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000002', nom: 'Martin', prenom: 'Bruno' },
        },
      ],
    },
  ],
}

// Web history: closing the panel depends on the browser history state.
async function renderPanel(paths: string[]) {
  window.history.replaceState(null, '', '/')
  const router = createRouter({ history: createWebHistory(), routes })
  await router.replace(paths[0]!)
  for (const path of paths.slice(1))
    await router.push(path)

  render(CandidaturePanelView, {
    global: { plugins: [createPinia(), PiniaColada, router] },
  })
  return { router, panel: within(await screen.findByRole('dialog')) }
}

function closeButton() {
  return screen.getByRole('button', { name: 'Fermer la candidature et revenir au kanban' })
}

describe('candidaturePanelView', () => {
  beforeEach(() => {
    vi.mocked(getRecrutementKanban).mockResolvedValue(MOCK_KANBAN)
    vi.mocked(getRecrutementDetail).mockResolvedValue({ etapes: [] } as unknown as RecrutementDetail)
  })

  it('shows the candidat name and submission date from the kanban data', async () => {
    const { panel } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    expect(await panel.findByText(/Candidature il y a \d+ jours/)).toBeInTheDocument()
    expect(panel.getByRole('heading', { name: 'Alice Dupont' })).toBeInTheDocument()
  })

  it('opens on the candidature tab, with the follow-up column beside it', async () => {
    const { router, panel } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    expect(await panel.findByRole('tab', { name: 'Candidature', selected: true })).toBeInTheDocument()
    expect(router.currentRoute.value.meta.tab).toBe('candidature')
    expect(panel.getByRole('complementary', { name: 'Suivi de la candidature' })).toHaveTextContent('Activités, tags et note')
  })

  it('moves to the next candidature of the column from the bottom bar', async () => {
    const user = setupUser()
    const { router } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])
    const navigation = within(await screen.findByRole('navigation', { name: 'Navigation entre les candidatures de l\'étape' }))

    expect(navigation.getByText('Candidature 1 sur 2')).toBeInTheDocument()
    expect(navigation.getByText('Étape : Réception des candidatures')).toBeInTheDocument()
    expect(navigation.getByRole('button', { name: 'Précédent' })).toBeDisabled()

    await user.click(navigation.getByRole('button', { name: 'Suivant' }))

    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_BRUNO))
    expect(await navigation.findByText('Candidature 2 sur 2')).toBeInTheDocument()
    expect(navigation.getByRole('button', { name: 'Suivant' })).toBeDisabled()
  })

  it('shows an empty state for a candidature absent from the kanban', async () => {
    const { panel } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_INCONNUE}`])

    expect(await panel.findByText('Candidature introuvable')).toBeInTheDocument()
  })

  it('goes back to the kanban when opened from it', async () => {
    const user = setupUser()
    const { router } = await renderPanel([KANBAN_PATH, `${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])
    const back = vi.spyOn(router, 'back')

    await user.click(closeButton())

    expect(back).toHaveBeenCalled()
  })

  it('replaces the address with the kanban when opened directly', async () => {
    const user = setupUser()
    const { router } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    await user.click(closeButton())

    await vi.waitFor(() => expect(router.currentRoute.value.name).toBe('recrutement-candidatures-kanban'))
  })
})
