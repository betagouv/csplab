import { screen, within } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { getRecrutementDetail } from '@/features/recrutements/api'
import {
  CANDIDATURE_ALICE,
  CANDIDATURE_BRUNO,
  ETAPE_REFUS,
  KANBAN,
  KANBAN_PATH,
  MOTIFS_REFUS,
  ORGANISME_UUID,
  RECRUTEMENT_DETAIL,
  RECRUTEMENT_UUID,
} from '@/test/fixtures/candidatures'
import { renderWithApp, setupUser } from '@/test/render'
import { getMotifsRefus, getRecrutementKanban, patchEtapeCandidatures } from '../api'
import CandidaturesKanbanView from './CandidaturesKanbanView.vue'

vi.mock('../api', () => ({
  getRecrutementKanban: vi.fn(),
  getCandidatureListe: vi.fn(),
  patchEtapeCandidatures: vi.fn(),
  getMotifsRefus: vi.fn(),
}))

vi.mock('@/features/recrutements/api', () => ({
  getRecrutementDetail: vi.fn(),
}))

async function refuseSelectedColumn() {
  const user = setupUser()
  await renderWithApp(CandidaturesKanbanView, { route: KANBAN_PATH })

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
})
