import type { Activite } from '../types'
import { PiniaColada } from '@pinia/colada'
import { render, screen, within } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { getCandidatureActivites } from '../api'
import CandidatureActivites from './CandidatureActivites.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  getCandidatureActivites: vi.fn(),
}))

function activite(overrides: Partial<Activite>): Activite {
  return {
    utilisateur_id: 'eeeeeeee-0001-0001-0001-000000000001',
    utilisateur_prenom: 'Marie',
    utilisateur_nom: 'Dupont',
    occurred_at: '2026-09-29T10:00:00',
    event_name: 'NoteAjoutee',
    ...overrides,
  }
}

function renderActivites() {
  render(CandidatureActivites, {
    props: { candidature: CANDIDATURE_PARAMS },
    global: { plugins: [createPinia(), PiniaColada] },
  })
}

describe('candidatureActivites', () => {
  beforeEach(() => {
    vi.useFakeTimers({ toFake: ['Date'] })
    vi.setSystemTime(new Date('2026-09-29T12:00:00'))
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.clearAllMocks()
  })

  it('lists the latest activities with their author and age', async () => {
    const results = [
      activite({}),
      activite({ event_name: 'CandidatureEtapeModifiee', utilisateur_prenom: 'Paul', utilisateur_nom: 'Bernard' }),
      activite({ event_name: 'CandidatureRecue', utilisateur_prenom: '', utilisateur_nom: '' }),
    ]
    vi.mocked(getCandidatureActivites).mockResolvedValue({ count: 3, results })
    renderActivites()

    const list = await screen.findByRole('list')
    const [note, etape, reception] = within(list).getAllByRole('listitem').map(item => within(item))
    expect(note!.getByText('Note ajoutée')).toBeInTheDocument()
    expect(note!.getByText('par Marie Dupont')).toBeInTheDocument()
    expect(note!.getByText('il y a 2 heures')).toBeInTheDocument()
    expect(etape!.getByText('Étape modifiée')).toBeInTheDocument()
    expect(etape!.getByText('par Paul Bernard')).toBeInTheDocument()
    expect(reception!.getByText('Candidature reçue')).toBeInTheDocument()
    expect(reception!.queryByText(/^par /)).not.toBeInTheDocument()
    expect(getCandidatureActivites).toHaveBeenCalledWith(CANDIDATURE_PARAMS, 3)
  })

  it('names an unknown activity with a generic label', async () => {
    vi.mocked(getCandidatureActivites).mockResolvedValue({ count: 1, results: [activite({ event_name: 'TagPose' })] })
    renderActivites()

    expect(await screen.findByText('Activité')).toBeInTheDocument()
  })

  it('says when the candidature has no activity', async () => {
    vi.mocked(getCandidatureActivites).mockResolvedValue({ count: 0, results: [] })
    renderActivites()

    expect(await screen.findByText('La candidature n\'a aucune activité')).toBeInTheDocument()
  })

  it('shows an error when the activities cannot be loaded', async () => {
    vi.mocked(getCandidatureActivites).mockRejectedValue(new HttpError(500, 'Internal Server Error', undefined))
    renderActivites()

    expect(await screen.findByText('Les activités n\'ont pas pu être chargées.')).toBeInTheDocument()
  })
})
