import { PiniaColada } from '@pinia/colada'
import { render, screen, within } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import { useToast } from '@/composables/ui/useToast'
import { getRecrutementDetail } from '@/features/recrutements/api'
import { routes } from '@/router'
import {
  CANDIDATURE_ALICE,
  CANDIDATURE_BRUNO,
  ETAPE_ENTRETIEN,
  ETAPE_REFUS,
  KANBAN,
  KANBAN_PATH,
  ORGANISME_UUID,
  RECRUTEMENT_DETAIL,
  RECRUTEMENT_UUID,
} from '@/test/fixtures/candidatures'
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

const CANDIDATURE_INCONNUE = 'dddddddd-0001-0001-0001-000000000099'

const PanelWithToasts = defineComponent({
  render: () => h(CspToaster, null, { default: () => h(CandidaturePanelView) }),
})

// Web history: closing the panel depends on the browser history state.
async function renderPanel(paths: string[]) {
  window.history.replaceState(null, '', '/')
  const router = createRouter({ history: createWebHistory(), routes })
  await router.replace(paths[0]!)
  for (const path of paths.slice(1))
    await router.push(path)

  render(PanelWithToasts, {
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
    vi.mocked(getRecrutementKanban).mockResolvedValue(KANBAN)
    vi.mocked(getRecrutementDetail).mockResolvedValue(RECRUTEMENT_DETAIL)
    vi.mocked(patchEtapeCandidatures).mockResolvedValue({ reussites: [CANDIDATURE_ALICE], echecs: [] })
  })

  afterEach(() => {
    const { toasts, dismissToast } = useToast()
    toasts.value.forEach(toast => dismissToast(toast.id))
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
    expect(patchEtapeCandidatures).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      etapeCibleUuid: ETAPE_ENTRETIEN,
      candidatureUuids: [CANDIDATURE_ALICE],
    })
  })

  it('confirms the move with a toast that reopens the moved candidature', async () => {
    const user = setupUser()
    const { router } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))
    await user.click(await screen.findByRole('radio', { name: 'Entretien' }))
    await user.click(screen.getByRole('button', { name: 'Valider' }))
    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_BRUNO))

    expect(await screen.findByText('Alice Dupont est passé à l\'étape Entretien')).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: 'Revenir à cette candidature' }))

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
    expect(patchEtapeCandidatures).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      etapeCibleUuid: ETAPE_REFUS,
      candidatureUuids: [CANDIDATURE_ALICE],
    })
  })

  it.each([
    ['the server rejects the move', () => Promise.reject(new Error('boom')), 'Le changement d\'étape a échoué'],
    ['the server leaves the candidature at its stage', () => Promise.resolve({ reussites: [], echecs: [{ candidature_uuid: CANDIDATURE_ALICE, raison: 'conflit' }] }), 'Certaines candidatures n\'ont pas changé d\'étape'],
  ])('does not announce the move when %s', async (_case, response, message) => {
    const user = setupUser()
    vi.mocked(patchEtapeCandidatures).mockImplementation(response)
    await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))
    await user.click(await screen.findByRole('radio', { name: 'Entretien' }))
    await user.click(screen.getByRole('button', { name: 'Valider' }))

    expect(await screen.findByText(message)).toBeInTheDocument()
    expect(screen.queryByText(/est passé à l'étape/)).not.toBeInTheDocument()
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
