import type { RecrutementDetailKanban } from '../types'
import type { RecrutementDetail } from '@/features/recrutements/types'
import { PiniaColada } from '@pinia/colada'
import { render, screen, within } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createRouter, createWebHistory } from 'vue-router'
import { useToast } from '@/composables/ui/useToast'
import { getRecrutementDetail } from '@/features/recrutements/api'
import { routes } from '@/router'
import { setupUser } from '@/test/render'
import { getRecrutementKanban, patchEtapeCandidatures } from '../api'
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

const ETAPE_ENTRETIEN = 'cccccccc-0001-0001-0001-000000000002'
const ETAPE_REFUS = 'cccccccc-0001-0001-0001-000000000003'

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
    {
      etape_uuid: ETAPE_ENTRETIEN,
      nom: 'Entretien',
      categorie: 'EN_COURS',
      candidatures: [],
    },
    {
      etape_uuid: ETAPE_REFUS,
      nom: 'Refus',
      categorie: 'REFUS',
      candidatures: [],
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
    vi.clearAllMocks()
    vi.mocked(getRecrutementKanban).mockResolvedValue(MOCK_KANBAN)
    vi.mocked(getRecrutementDetail).mockResolvedValue({
      etapes: MOCK_KANBAN.etapes.map(({ etape_uuid, nom, categorie }) => ({ etape_uuid, nom, categorie })),
    } as unknown as RecrutementDetail)
    vi.mocked(patchEtapeCandidatures).mockResolvedValue({ reussites: [CANDIDATURE_ALICE], echecs: [] })
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

  it('moves the candidature to another stage and opens the next one of its column', async () => {
    const user = setupUser()
    const { router } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))
    expect(await screen.findByRole('radio', { name: 'Réception des candidatures (étape actuelle)' })).toBeDisabled()
    await user.click(screen.getByRole('radio', { name: 'Entretien' }))
    await user.click(screen.getByRole('button', { name: 'Valider' }))

    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_BRUNO))
    expect(patchEtapeCandidatures).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, ETAPE_ENTRETIEN, [CANDIDATURE_ALICE])
  })

  it('confirms the move with a toast that reopens the moved candidature', async () => {
    const user = setupUser()
    const { router } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))
    await user.click(await screen.findByRole('radio', { name: 'Entretien' }))
    await user.click(screen.getByRole('button', { name: 'Valider' }))
    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_BRUNO))

    const toast = useToast().toasts.value.at(-1)
    expect(toast?.title).toBe('Alice Dupont est passé à l\'étape Entretien')
    expect(toast?.duration).toBe(10_000)

    toast?.action?.onSelect()

    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_ALICE))
    const navigation = within(screen.getByRole('navigation', { name: 'Navigation entre les candidatures de l\'étape' }))
    expect(await navigation.findByText('Étape : Entretien')).toBeInTheDocument()
  })

  it('asks for confirmation before refusing the candidature', async () => {
    const user = setupUser()
    const { router } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))
    await user.click(await screen.findByRole('radio', { name: 'Refus' }))
    await user.click(screen.getByRole('button', { name: 'Valider' }))

    const dialog = within(await screen.findByRole('dialog', { name: 'Refus de candidature' }))
    expect(patchEtapeCandidatures).not.toHaveBeenCalled()

    await user.click(dialog.getByRole('button', { name: 'Valider' }))

    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_BRUNO))
    expect(patchEtapeCandidatures).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, ETAPE_REFUS, [CANDIDATURE_ALICE])
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
