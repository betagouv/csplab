import type { Component } from 'vue'
import type { KanbanDropEvent } from '@/composables/dnd/useKanbanDnd'
import { screen, within } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { useToast } from '@/composables/ui/useToast'
import { getRecrutementDetail } from '@/features/recrutements/api'
import {
  CANDIDATURE_ALICE,
  CANDIDATURE_BRUNO,
  CANDIDATURE_LISTE,
  ETAPE_ENTRETIEN,
  ETAPE_RECEPTION,
  ETAPE_REFUS,
  KANBAN_PATH,
  MOTIFS_REFUS,
  ORGANISME_UUID,
  RECRUTEMENT_DETAIL,
  RECRUTEMENT_UUID,
  roleOnOrganisme,
} from '@/test/fixtures/candidatures'
import { makeUser } from '@/test/fixtures/utilisateur'
import { renderWithApp, setupUser } from '@/test/render'
import { getCandidatureListe, getMotifsRefus, patchEtapeCandidatures } from '../api'

vi.mock('../api', () => ({
  getCandidatureListe: vi.fn(),
  patchEtapeCandidatures: vi.fn(),
  getMotifsRefus: vi.fn(),
}))

vi.mock('@/features/recrutements/api', () => ({
  getRecrutementDetail: vi.fn(),
}))

function renderKanbanPage(stubs: Record<string, Component> = {}) {
  return renderWithApp(RouterView, { route: KANBAN_PATH, global: { stubs } })
}

function dropButton(label: string, targetColumnId: string) {
  const event: KanbanDropEvent = { sourceColumnId: ETAPE_RECEPTION, targetColumnId, cardId: CANDIDATURE_ALICE }
  return { label, event }
}

const DROPS = [
  dropButton('Déposer dans sa colonne', ETAPE_RECEPTION),
  dropButton('Déposer en entretien', ETAPE_ENTRETIEN),
  dropButton('Déposer en refus', ETAPE_REFUS),
]

const DroppingBoard = defineComponent({
  emits: ['move'],
  setup(_, { emit }) {
    return () => DROPS.map(({ label, event }) => h('button', { onClick: () => emit('move', event) }, label))
  },
})

async function selectColumns(columns: string[], search?: string) {
  const user = setupUser()
  await renderKanbanPage()

  if (search) {
    await user.type(await screen.findByRole('searchbox', { name: 'Rechercher un candidat' }), `${search}{Enter}`)
  }
  for (const column of columns) {
    // CspCheckbox exposes both its reka button and its hidden native input as checkboxes.
    const [columnCheckbox] = await screen.findAllByRole('checkbox', { name: `Sélectionner la colonne ${column}` })
    await user.click(columnCheckbox!)
  }
  return user
}

async function refuseSelectedColumn(search?: string) {
  const user = await selectColumns(['Réception des candidatures'], search)
  await user.click(await screen.findByRole('button', { name: 'Refuser' }))

  return { user, dialog: within(await screen.findByRole('dialog', { name: 'Refus de candidature' })) }
}

describe('candidaturesKanbanView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    vi.mocked(getCandidatureListe).mockResolvedValue(CANDIDATURE_LISTE)
    vi.mocked(getMotifsRefus).mockResolvedValue(MOTIFS_REFUS)
    vi.mocked(getRecrutementDetail).mockResolvedValue(RECRUTEMENT_DETAIL)
    vi.mocked(patchEtapeCandidatures).mockResolvedValue({ reussites: [CANDIDATURE_ALICE, CANDIDATURE_BRUNO], echecs: [] })
  })

  it('shows the cards matching the search of the candidatures tab', async () => {
    const user = setupUser()
    await renderKanbanPage()

    await screen.findByRole('link', { name: 'Alice Dupont' })
    await user.type(screen.getByRole('searchbox', { name: 'Rechercher un candidat' }), 'Bruno{Enter}')

    await vi.waitFor(() => expect(screen.queryByRole('link', { name: 'Alice Dupont' })).not.toBeInTheDocument())
    expect(screen.getByRole('link', { name: 'Bruno Martin' })).toBeInTheDocument()
  })

  it('clears the search when another recrutement opens', async () => {
    const user = setupUser()
    const { router } = await renderKanbanPage()
    const search = await screen.findByRole('searchbox', { name: 'Rechercher un candidat' })
    await user.type(search, 'Bruno{Enter}')

    await router.push(`/organismes/${ORGANISME_UUID}/recrutements/aaaaaaaa-0001-0001-0001-000000000002`)

    await vi.waitFor(() => expect(screen.getByRole('searchbox', { name: 'Rechercher un candidat' })).toHaveValue(''))
  })

  it('keeps the focus on the view switch when the list opens', async () => {
    const user = setupUser()
    const { router } = await renderKanbanPage()

    await user.click(await screen.findByRole('radio', { name: /Liste/ }))

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(`${KANBAN_PATH}/liste`))
    await vi.waitFor(() => expect(screen.getByRole('radio', { name: /Liste/ })).toHaveFocus())
  })

  it('shows an error when the kanban fails to load', async () => {
    vi.mocked(getCandidatureListe).mockRejectedValue(new Error('boom'))
    await renderKanbanPage()

    expect(await screen.findByText('Une erreur est survenue lors du chargement des candidatures.')).toBeInTheDocument()
    expect(screen.queryByText(/^\d+ candidatures?$/)).not.toBeInTheDocument()
    expect(screen.getByRole('radio', { name: /Liste/ })).toBeInTheDocument()
  })

  it('keeps loading until the rights on the recrutement are known', async () => {
    vi.mocked(getRecrutementDetail).mockReturnValue(new Promise(() => {}))
    await renderKanbanPage()

    await vi.waitFor(() => expect(getCandidatureListe).toHaveBeenCalled())
    await new Promise(resolve => setTimeout(resolve, 500))

    expect(screen.getByRole('status', { name: 'Chargement des candidatures' })).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: 'Alice Dupont' })).not.toBeInTheDocument()
  })

  it('offers no selection without the right to change stages', async () => {
    vi.mocked(getRecrutementDetail).mockResolvedValue({ ...RECRUTEMENT_DETAIL, authorized_actions: [] })
    await renderKanbanPage()

    await screen.findByRole('link', { name: 'Alice Dupont' })
    expect(screen.queryAllByRole('checkbox', { name: /^Sélectionner la colonne/ })).toEqual([])
  })

  it.each([
    { cas: 'with', actions: ['change_etape_candidatures'] as const, draggable: 'true' },
    { cas: 'without', actions: [] as const, draggable: null },
  ])('lets the cards be dragged only $cas the right to change stages', async ({ actions, draggable }) => {
    vi.mocked(getRecrutementDetail).mockResolvedValue({ ...RECRUTEMENT_DETAIL, authorized_actions: [...actions] })
    await renderKanbanPage()

    const card = (await screen.findByRole('link', { name: 'Alice Dupont' })).closest('article')
    await vi.waitFor(() => expect(card?.getAttribute('draggable') ?? null).toBe(draggable))
  })

  it('asks for a motif before refusing a selection, and sends it', async () => {
    const { user, dialog } = await refuseSelectedColumn()

    expect(dialog.getByText(/Vous êtes sur le point de refuser 2 candidatures/)).toBeInTheDocument()
    expect(screen.queryByRole('dialog', { name: /Changer d'étape/ })).not.toBeInTheDocument()
    expect(patchEtapeCandidatures).not.toHaveBeenCalled()

    await user.click(dialog.getByRole('combobox', { name: /Motif de refus/ }))
    await user.click(await screen.findByRole('option', { name: 'Autre' }))
    await user.click(dialog.getByRole('button', { name: 'Valider le refus' }))

    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalledWith({ organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID }, {
      etapeCibleUuid: ETAPE_REFUS,
      candidatureUuids: [CANDIDATURE_ALICE, CANDIDATURE_BRUNO],
      motifRefus: 'autre',
    }))
  })

  it('counts in the refusal only the candidatures shown by the search', async () => {
    const { dialog } = await refuseSelectedColumn('Alice')

    expect(dialog.getByText(/Vous êtes sur le point de refuser la candidature de Alice/)).toBeInTheDocument()
  })

  it('shows in the toolbar the count of the selected candidatures shown by the search, in place of the candidatures count', async () => {
    await selectColumns(['Réception des candidatures'], 'Alice')

    expect(await screen.findByText('1 candidature sélectionnée')).toBeInTheDocument()
    expect(screen.queryByText(/^\d+ candidatures?$/)).not.toBeInTheDocument()
  })

  it('lists in the stage drawer only the selected candidatures shown by the search', async () => {
    const user = await selectColumns(['Réception des candidatures'], 'Alice')
    await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))

    const drawer = within(await screen.findByRole('dialog', { name: /Changer d'étape/ }))
    expect(drawer.getByRole('button', { name: /Alice/ })).toBeInTheDocument()
    expect(drawer.queryByRole('button', { name: /Bruno/ })).not.toBeInTheDocument()
  })

  it('offers no refusal for a selection already in the refusal stage', async () => {
    vi.mocked(getCandidatureListe).mockResolvedValue({
      ...CANDIDATURE_LISTE,
      results: CANDIDATURE_LISTE.results.map(candidature => candidature.uuid === CANDIDATURE_ALICE
        ? { ...candidature, etape: { uuid: ETAPE_REFUS, nom: 'Refus', categorie: 'REFUS' } }
        : candidature),
    })
    await selectColumns(['Refus'])

    expect(await screen.findByRole('button', { name: 'Changer d\'étape' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Refuser' })).not.toBeInTheDocument()
  })

  it('keeps the selection when the refusal is cancelled', async () => {
    const { user, dialog } = await refuseSelectedColumn()

    await user.click(dialog.getByRole('button', { name: 'Annuler' }))

    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Refus de candidature' })).not.toBeInTheDocument())
    expect(screen.getByText('2 candidatures sélectionnées')).toBeInTheDocument()
    expect(patchEtapeCandidatures).not.toHaveBeenCalled()
  })

  it('goes back to the stage drawer when a refusal picked in it is cancelled', async () => {
    const user = await selectColumns(['Réception des candidatures'])
    await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))
    const drawer = within(await screen.findByRole('dialog', { name: /Changer d'étape/ }))
    await user.click(drawer.getByRole('radio', { name: /Refus/ }))
    await user.click(drawer.getByRole('button', { name: 'Valider le changement d\'étape' }))
    const dialog = within(await screen.findByRole('dialog', { name: 'Refus de candidature' }))

    await user.click(dialog.getByRole('button', { name: 'Annuler' }))

    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Refus de candidature' })).not.toBeInTheDocument())
    expect(screen.getByRole('button', { name: 'Valider le changement d\'étape' })).toBeInTheDocument()
    expect(patchEtapeCandidatures).not.toHaveBeenCalled()
  })

  it('moves the selection to a stage, without the candidatures hidden by the search, and confirms it', async () => {
    const user = await selectColumns(['Réception des candidatures'], 'Alice')
    await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))
    const drawer = within(await screen.findByRole('dialog', { name: /Changer d'étape/ }))
    expect(drawer.getByRole('radio', { name: /^Réception des candidatures\s*Étape actuelle$/ })).toBeDisabled()
    await user.click(drawer.getByRole('radio', { name: /Entretien/ }))
    await user.click(drawer.getByRole('button', { name: 'Valider le changement d\'étape' }))

    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalledWith({ organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID }, {
      etapeCibleUuid: ETAPE_ENTRETIEN,
      candidatureUuids: [CANDIDATURE_ALICE],
    }))
    await vi.waitFor(() => expect(useToast().toasts.value.at(-1)?.title).toBe('La candidature d\'Alice Dupont est passée à l\'étape Entretien'))
  })

  it('sends a card dropped in another column, and ignores one dropped back in its own column', async () => {
    const user = setupUser()
    await renderKanbanPage({ CandidaturesKanbanBoard: DroppingBoard })

    await user.click(await screen.findByRole('button', { name: 'Déposer dans sa colonne' }))
    expect(patchEtapeCandidatures).not.toHaveBeenCalled()

    await user.click(screen.getByRole('button', { name: 'Déposer en entretien' }))
    expect(patchEtapeCandidatures).toHaveBeenCalledWith({ organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID }, {
      etapeCibleUuid: ETAPE_ENTRETIEN,
      candidatureUuids: [CANDIDATURE_ALICE],
    })
  })

  it('asks for a motif before refusing a card dropped in the refusal column, and sends it', async () => {
    const user = setupUser()
    await renderKanbanPage({ CandidaturesKanbanBoard: DroppingBoard })

    await user.click(await screen.findByRole('button', { name: 'Déposer en refus' }))
    const dialog = within(await screen.findByRole('dialog', { name: 'Refus de candidature' }))
    expect(dialog.getByText(/Vous êtes sur le point de refuser la candidature de Alice/)).toBeInTheDocument()
    expect(patchEtapeCandidatures).not.toHaveBeenCalled()

    await user.click(dialog.getByRole('combobox', { name: /Motif de refus/ }))
    await user.click(await screen.findByRole('option', { name: 'Autre' }))
    await user.click(dialog.getByRole('button', { name: 'Valider le refus' }))

    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalledWith({ organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID }, {
      etapeCibleUuid: ETAPE_REFUS,
      candidatureUuids: [CANDIDATURE_ALICE],
      motifRefus: 'autre',
    }))
  })
})
