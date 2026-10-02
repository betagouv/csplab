import type { Activite } from '../types'
import { screen, within } from '@testing-library/vue'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { renderWithApp } from '@/test/render'
import { getCandidatureActivites } from '../api'
import CandidatureHistorique from './CandidatureHistorique.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  getCandidatureActivites: vi.fn(),
}))

function activite(eventName: string): Activite {
  return {
    utilisateur_id: 'eeeeeeee-0001-0001-0001-000000000001',
    utilisateur_prenom: 'Marie',
    utilisateur_nom: 'Dupont',
    occurred_at: '2026-09-29T10:00:00',
    event_name: eventName,
  }
}

describe('candidatureHistorique', () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('lists every activity of the candidature with their count', async () => {
    const results = ['NoteAjoutee', 'CandidatureEtapeModifiee', 'NoteEditee', 'CandidatureRecue'].map(activite)
    vi.mocked(getCandidatureActivites).mockResolvedValue({ count: 4, results })
    await renderWithApp(CandidatureHistorique, { props: { candidature: CANDIDATURE_PARAMS } })

    expect(await screen.findByRole('heading', { name: '4 activités récentes' })).toBeInTheDocument()
    expect(within(screen.getByRole('list')).getAllByRole('listitem')).toHaveLength(4)
    expect(getCandidatureActivites).toHaveBeenCalledWith(CANDIDATURE_PARAMS, undefined)
  })
})
