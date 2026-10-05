import type { Component } from 'vue'
import type { KanbanDropEvent } from '@/composables/dnd/useKanbanDnd'
import { screen, within } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { getRecrutementDetail } from '@/features/recrutements/api'
import {
  CANDIDATURE_ALICE,
  CANDIDATURE_BRUNO,
  ETAPE_ENTRETIEN,
  ETAPE_RECEPTION,
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
import { renderWithApp, setupUser } from '@/test/render'
import { getMotifsRefus, getRecrutementKanban, patchEtapeCandidatures } from '../api'

vi.mock('../api', () => ({
  getRecrutementKanban: vi.fn(),
  getCandidatureListe: vi.fn(),
  patchEtapeCandidatures: vi.fn(),
  getMotifsRefus: vi.fn(),
}))

vi.mock('@/features/recrutements/api', () => ({
  getRecrutementDetail: vi.fn(),
}))

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

function renderKanbanPage(stubs: Record<string, Component> = {}) {
  return renderWithApp(RouterView, { route: KANBAN_PATH, global: { stubs } })
}

const CANDIDATURE_CHLOE = 'dddddddd-0001-0001-0001-000000000003'

const KANBAN_WITH_ENTRETIEN = {
  ...KANBAN,
  etapes: KANBAN.etapes.map(etape => etape.uuid === ETAPE_ENTRETIEN
    ? {
        ...etape,
        candidatures: [{
          uuid: CANDIDATURE_CHLOE,
          date_soumission: '2025-06-13T09:15:00Z',
          date_derniere_activite: '2025-06-13T10:00:00Z',
          candidat: { uuid: 'eeeeeeee-0001-0001-0001-000000000003', nom: 'Petit', prenom: 'Chloé' },
        }],
      }
    : etape),
}

function dropButton(label: string, targetColumnId: string) {
  const event: KanbanDropEvent = { sourceColumnId: ETAPE_RECEPTION, targetColumnId, cardId: CANDIDATURE_ALICE, cardIndex: 0 }
  return { label, event }
}

const DROPS = [dropButton('Déposer dans sa colonne', ETAPE_RECEPTION), dropButton('Déposer en entretien', ETAPE_ENTRETIEN)]

const DroppingBoard = defineComponent({
  emits: ['move'],
  setup(_, { emit }) {
    return () => DROPS.map(({ label, event }) => h('button', { onClick: () => emit('move', event) }, label))
  },
})

async function refuseSelectedColumn() {
  const user = setupUser()
  await renderKanbanPage()

  // CspCheckbox exposes both its reka button and its hidden native input as checkboxes.
  const [columnCheckbox] = await screen.findAllByRole('checkbox', { name: 'Sélectionner la colonne Réception des candidatures' })
  await user.click(columnCheckbox!)
  await user.click(await screen.findByRole('button', { name: 'Refuser' }))
  await user.click(await screen.findByRole('button', { name: 'Valider le changement d\'étape' }))

  return { user, dialog: within(await screen.findByRole('dialog', { name: 'Refus de candidature' })) }
}

describe('candidaturesKanbanView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    vi.mocked(getRecrutementKanban).mockResolvedValue(KANBAN)
    vi.mocked(getMotifsRefus).mockResolvedValue(MOTIFS_REFUS)
    vi.mocked(getRecrutementDetail).mockResolvedValue(RECRUTEMENT_DETAIL)
    vi.mocked(patchEtapeCandidatures).mockResolvedValue({ reussites: [CANDIDATURE_ALICE, CANDIDATURE_BRUNO], echecs: [] })
  })

  it('asks for a motif before refusing a selection, and sends it', async () => {
    const { user, dialog } = await refuseSelectedColumn()

    expect(dialog.getByText(/Vous êtes sur le point de refuser 2 candidatures/)).toBeInTheDocument()
    expect(patchEtapeCandidatures).not.toHaveBeenCalled()

    await user.click(dialog.getByRole('combobox', { name: /Motif de refus/ }))
    await user.click(await screen.findByRole('option', { name: 'Autre' }))
    await user.click(dialog.getByRole('button', { name: 'Valider le refus' }))

    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      etapeCibleUuid: ETAPE_REFUS,
      candidatureUuids: [CANDIDATURE_ALICE, CANDIDATURE_BRUNO],
      motifRefus: 'autre',
    }))
  })

  it('goes back to the stage drawer when the refusal is cancelled', async () => {
    const { user, dialog } = await refuseSelectedColumn()

    await user.click(dialog.getByRole('button', { name: 'Annuler' }))

    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Refus de candidature' })).not.toBeInTheDocument())
    expect(screen.getByRole('button', { name: 'Valider le changement d\'étape' })).toBeInTheDocument()
    expect(patchEtapeCandidatures).not.toHaveBeenCalled()
  })

  it('moves a selection to a stage without sending the selected candidatures already there', async () => {
    vi.mocked(getRecrutementKanban).mockResolvedValue(KANBAN_WITH_ENTRETIEN)
    const user = setupUser()
    await renderKanbanPage()

    // CspCheckbox exposes both its reka button and its hidden native input as checkboxes.
    for (const colonne of ['Réception des candidatures', 'Entretien']) {
      const [columnCheckbox] = await screen.findAllByRole('checkbox', { name: `Sélectionner la colonne ${colonne}` })
      await user.click(columnCheckbox!)
    }
    await user.type(screen.getByRole('searchbox', { name: 'Rechercher un candidat' }), 'Alice{Enter}')
    await user.click(await screen.findByRole('button', { name: 'Changer d\'étape' }))
    const drawer = within(await screen.findByRole('dialog', { name: /Changer d'étape/ }))
    await user.click(drawer.getByRole('radio', { name: /Entretien/ }))
    await user.click(drawer.getByRole('button', { name: 'Valider le changement d\'étape' }))

    await vi.waitFor(() => expect(patchEtapeCandidatures).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      etapeCibleUuid: ETAPE_ENTRETIEN,
      candidatureUuids: [CANDIDATURE_ALICE, CANDIDATURE_BRUNO],
    }))
  })

  it('sends a card dropped in another column, and ignores one dropped back in its own column', async () => {
    const user = setupUser()
    await renderKanbanPage({ CandidaturesKanbanBoard: DroppingBoard })

    await user.click(await screen.findByRole('button', { name: 'Déposer dans sa colonne' }))
    expect(patchEtapeCandidatures).not.toHaveBeenCalled()

    await user.click(screen.getByRole('button', { name: 'Déposer en entretien' }))
    expect(patchEtapeCandidatures).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, {
      etapeCibleUuid: ETAPE_ENTRETIEN,
      candidatureUuids: [CANDIDATURE_ALICE],
    })
  })
})
