import { PiniaColada } from '@pinia/colada'
import { render, screen, within } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { createRouter, createWebHistory, RouterView } from 'vue-router'
import { HttpError } from '@/api/errors'
import { getMe } from '@/api/utilisateur'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import { useToast } from '@/composables/ui/useToast'
import { getConversations } from '@/features/messages/api'
import { getRecrutementDetail } from '@/features/recrutements/api'
import { routes } from '@/router/routes'
import {
  CANDIDATURE_ALICE,
  CANDIDATURE_BRUNO,
  candidatureDetail,
  ETAPE_ENTRETIEN,
  ETAPE_REFUS,
  KANBAN,
  KANBAN_PATH,
  MOTIFS_REFUS,
  ORGANISME_UUID,
  RECRUTEMENT_DETAIL,
  RECRUTEMENT_UUID,
  roleOnOrganisme,
} from '@/test/fixtures/candidatures'
import { makeUser } from '@/test/fixtures/utilisateur'
import { setupUser } from '@/test/render'
import { createCandidatureNote, getCandidatureActivites, getCandidatureDetail, getMotifsRefus, getRecrutementKanban, patchEtapeCandidatures } from '../api'

vi.mock('../api', () => ({
  getCandidatureDetail: vi.fn(),
  getRecrutementKanban: vi.fn(),
  getCandidatureListe: vi.fn(),
  patchEtapeCandidatures: vi.fn(),
  getMotifsRefus: vi.fn(),
  getCandidatureDocuments: vi.fn(() => new Promise(() => {})),
  candidatureDocumentUrl: vi.fn(),
  getCandidatureNotes: vi.fn(() => new Promise(() => {})),
  createCandidatureNote: vi.fn(),
  getCandidatureActivites: vi.fn(),
}))

vi.mock('@/features/recrutements/api', () => ({
  getRecrutementDetail: vi.fn(),
}))

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

vi.mock('@/features/messages/api', () => ({
  getConversations: vi.fn(),
}))

const CANDIDATURE_INCONNUE = 'dddddddd-0001-0001-0001-000000000099'

const RoutesWithToasts = defineComponent({
  render: () => h(CspToaster, null, { default: () => h(RouterView) }),
})

// Web history: closing the panel depends on the browser history state.
async function renderPanel(paths: string[]) {
  window.history.replaceState(null, '', '/')
  const router = createRouter({ history: createWebHistory(), routes })
  await router.replace(paths[0]!)
  for (const path of paths.slice(1)) {
    await router.push(path)
  }

  render(RoutesWithToasts, {
    global: { plugins: [createPinia(), PiniaColada, router] },
  })
  return { router, panel: within(await screen.findByRole('dialog')) }
}

function closeButton() {
  return screen.getByRole('button', { name: 'Fermer la candidature' })
}

describe('candidaturePanelView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    vi.mocked(getCandidatureDetail).mockImplementation(async ({ candidatureUuid }) => candidatureDetail(candidatureUuid))
    vi.mocked(getRecrutementKanban).mockResolvedValue(KANBAN)
    vi.mocked(getMotifsRefus).mockResolvedValue(MOTIFS_REFUS)
    vi.mocked(getRecrutementDetail).mockResolvedValue(RECRUTEMENT_DETAIL)
    vi.mocked(patchEtapeCandidatures).mockResolvedValue({ reussites: [CANDIDATURE_ALICE], echecs: [] })
    vi.mocked(getConversations).mockResolvedValue({ count: 0, next: null, previous: null, results: [] })
    vi.mocked(getCandidatureActivites).mockResolvedValue({ count: 0, next: null, previous: null, results: [] })
  })

  afterEach(() => {
    const { toasts, dismissToast } = useToast()
    toasts.value.forEach(toast => dismissToast(toast.id))
  })

  it('shows the candidat name and submission date from the candidature detail', async () => {
    const { panel } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    expect(await panel.findByText(/Candidature il y a \d+ jours/)).toBeInTheDocument()
    expect(panel.getByRole('heading', { name: 'Alice Dupont' })).toBeInTheDocument()
  })

  it('opens on the candidature tab, with the follow-up column beside it', async () => {
    const { router, panel } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    expect(await panel.findByRole('tab', { name: 'Candidature', selected: true })).toBeInTheDocument()
    expect(router.currentRoute.value.meta.tab).toBe('candidature')
    const suivi = within(panel.getByRole('complementary', { name: 'Suivi de la candidature' }))
    expect(suivi.getByRole('heading', { name: 'Dernières activités' })).toBeInTheDocument()
    expect(suivi.getByRole('heading', { name: 'Ajouter une note' })).toBeInTheDocument()
  })

  it('refreshes the latest activities once a note is saved', async () => {
    vi.mocked(createCandidatureNote).mockResolvedValue()
    const user = setupUser()
    const { panel } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])
    await vi.waitFor(() => expect(getCandidatureActivites).toHaveBeenCalledTimes(1))

    await user.type(await panel.findByRole('textbox', { name: 'Ajouter une note' }), 'À rappeler')
    await user.click(panel.getByRole('button', { name: 'Enregistrer la note' }))

    await vi.waitFor(() => expect(getCandidatureActivites).toHaveBeenCalledTimes(2))
  })

  it('moves to the next candidature of the column from the bottom bar', async () => {
    const user = setupUser()
    const { router } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])
    const navigation = within(await screen.findByRole('navigation', { name: 'Navigation entre les candidatures de l\'étape' }))

    expect(navigation.getByText('Candidature 1 sur 2')).toBeInTheDocument()
    expect(getCandidatureDetail).toHaveBeenCalledWith(expect.objectContaining({ candidatureUuid: CANDIDATURE_BRUNO }))
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
    expect(await screen.findByText('Alice Dupont est passé à l\'étape Entretien')).toBeInTheDocument()
  })

  it('asks for confirmation before refusing the candidature', async () => {
    const user = setupUser()
    const { router } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))
    await user.click(await screen.findByRole('radio', { name: 'Refus' }))
    await user.click(screen.getByRole('button', { name: 'Valider' }))

    const dialog = within(await screen.findByRole('dialog', { name: 'Refus de candidature' }))
    expect(patchEtapeCandidatures).not.toHaveBeenCalled()
    expect(dialog.getByRole('button', { name: 'Valider le refus' })).toBeDisabled()

    await user.click(dialog.getByRole('combobox', { name: /Motif de refus/ }))
    await user.click(await screen.findByRole('option', { name: 'Expérience insuffisante' }))
    await user.click(dialog.getByRole('button', { name: 'Valider le refus' }))

    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_BRUNO))
    expect(patchEtapeCandidatures).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      etapeCibleUuid: ETAPE_REFUS,
      candidatureUuids: [CANDIDATURE_ALICE],
      motifRefus: 'experience_insuffisante',
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

  it.each([
    ['documents', 'Documents'],
    ['notes', 'Notes'],
  ])('opens the %s tab from its own address', async (segment, label) => {
    const { router, panel } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}/${segment}`])

    expect(await panel.findByRole('tab', { name: label, selected: true })).toBeInTheDocument()
    expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_ALICE)
  })

  it('opens the history tab from its own address, with the full width', async () => {
    const { panel } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}/historique`])

    expect(await panel.findByRole('tab', { name: 'Historique d\'activité', selected: true })).toBeInTheDocument()
    expect(panel.queryByRole('complementary', { name: 'Suivi de la candidature' })).not.toBeInTheDocument()
  })

  it('shows the access message when the candidature detail answers not found', async () => {
    vi.mocked(getCandidatureDetail).mockRejectedValue(new HttpError(404, 'Not Found'))
    const { panel } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_INCONNUE}`])

    expect(await panel.findByText('Cette candidature n\'est pas accessible.')).toBeInTheDocument()
    expect(panel.getByText('Elle n\'existe pas ou ne vous est pas accessible. Contactez le superviseur de votre organisme si besoin.')).toBeInTheDocument()
    expect(await panel.findByRole('heading', { name: 'Candidature' })).toBeInTheDocument()
  })

  it.each([
    ['opened from the kanban', [KANBAN_PATH, `${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`]],
    ['opened directly', [`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`]],
    ['left on another tab', [KANBAN_PATH, `${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}/messages`]],
  ])('closes to the kanban when %s', async (_, paths) => {
    const user = setupUser()
    const { router } = await renderPanel(paths)

    await user.click(closeButton())

    await vi.waitFor(() => expect(router.currentRoute.value.name).toBe('recrutement-candidatures-kanban'))
  })

  it('gives the messages tab its own address and the full width', async () => {
    const user = setupUser()
    const { router, panel } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    await user.click(await panel.findByRole('tab', { name: 'Messages' }))

    await vi.waitFor(() =>
      expect(router.currentRoute.value.path).toBe(`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}/messages`),
    )
    expect(await panel.findByRole('tab', { name: 'Messages', selected: true })).toBeInTheDocument()
    expect(panel.queryByRole('complementary', { name: 'Suivi de la candidature' })).not.toBeInTheDocument()
  })

  it('returns to the previous tab on browser back', async () => {
    const user = setupUser()
    const { router, panel } = await renderPanel([KANBAN_PATH, `${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])

    await user.click(await panel.findByRole('tab', { name: 'Messages' }))
    await vi.waitFor(() => expect(router.currentRoute.value.meta.tab).toBe('messages'))

    router.back()

    await vi.waitFor(() => expect(router.currentRoute.value.meta.tab).toBe('candidature'))
  })

  describe('with a note being typed', () => {
    async function renderWithNote() {
      const user = setupUser()
      const rendered = await renderPanel([KANBAN_PATH, `${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`])
      const note = await rendered.panel.findByRole('textbox', { name: 'Ajouter une note' })
      await user.type(note, 'À rappeler')
      return { ...rendered, user, note }
    }

    function unsavedDialog() {
      return screen.findByRole('dialog', { name: 'Modifications non enregistrées' })
    }

    it.each([
      ['closing the panel', () => closeButton()],
      ['moving to the next candidature', () => screen.getByRole('button', { name: 'Suivant' })],
    ])('asks before %s and stays when the user keeps editing', async (_case, control) => {
      const { user, router, note } = await renderWithNote()

      await user.click(control())
      const dialog = within(await unsavedDialog())
      expect(dialog.getByText('Si vous quittez maintenant, votre saisie sera perdue.')).toBeInTheDocument()
      await user.click(dialog.getByRole('button', { name: 'Continuer l\'édition' }))

      await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Modifications non enregistrées' })).not.toBeInTheDocument())
      expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_ALICE)
      expect(note).toHaveValue('À rappeler')
    })

    it('leaves without the note when the user confirms', async () => {
      const { user, router, note } = await renderWithNote()

      await user.click(screen.getByRole('button', { name: 'Suivant' }))
      await user.click(within(await unsavedDialog()).getByRole('button', { name: 'Quitter sans enregistrer' }))

      await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_BRUNO))
      expect(note).toHaveValue('')
    })

    it('asks before going back to the kanban with the browser, and restores the address', async () => {
      const { user, router, note } = await renderWithNote()
      const candidaturePath = `${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}`

      router.back()
      const dialog = within(await unsavedDialog())
      expect(window.location.pathname).toBe(KANBAN_PATH)
      await user.click(dialog.getByRole('button', { name: 'Continuer l\'édition' }))

      await vi.waitFor(() => expect(window.location.pathname).toBe(candidaturePath))
      expect(router.currentRoute.value.path).toBe(candidaturePath)
      expect(note).toHaveValue('À rappeler')
    })

    it('returns to the note on Escape', async () => {
      const { user, router } = await renderWithNote()

      await user.click(closeButton())
      await unsavedDialog()
      await user.keyboard('{Escape}')

      await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Modifications non enregistrées' })).not.toBeInTheDocument())
      expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_ALICE)
    })

    it('asks before changing the stage', async () => {
      const { user, router } = await renderWithNote()

      await user.click(screen.getByRole('button', { name: 'Changer d\'étape' }))
      await user.click(await screen.findByRole('radio', { name: 'Entretien' }))
      await user.click(screen.getByRole('button', { name: 'Valider' }))

      const dialog = within(await unsavedDialog())
      expect(patchEtapeCandidatures).not.toHaveBeenCalled()
      await user.click(dialog.getByRole('button', { name: 'Quitter sans enregistrer' }))

      await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_BRUNO))
      expect(patchEtapeCandidatures).toHaveBeenCalledOnce()
    })

    it('keeps the note across tabs without asking', async () => {
      const { user, panel, note } = await renderWithNote()

      await user.click(panel.getByRole('tab', { name: 'Messages' }))
      await user.click(await panel.findByRole('tab', { name: 'Documents' }))

      expect(await panel.findByRole('tab', { name: 'Documents', selected: true })).toBeInTheDocument()
      expect(screen.queryByRole('dialog', { name: 'Modifications non enregistrées' })).not.toBeInTheDocument()
      expect(note).toHaveValue('À rappeler')
    })
  })

  it('reopens on the candidature tab when moving to the next candidature', async () => {
    const user = setupUser()
    const { router } = await renderPanel([`${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}/messages`])
    const navigation = within(await screen.findByRole('navigation', { name: 'Navigation entre les candidatures de l\'étape' }))

    await user.click(navigation.getByRole('button', { name: 'Suivant' }))

    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_BRUNO))
    expect(router.currentRoute.value.path).toBe(`${KANBAN_PATH}/candidatures/${CANDIDATURE_BRUNO}`)
    expect(router.currentRoute.value.meta.tab).toBe('candidature')
  })
})
