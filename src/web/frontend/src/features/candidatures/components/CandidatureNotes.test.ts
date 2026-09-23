import type { Note } from '../types'
import { PiniaColada } from '@pinia/colada'
import { render, screen, within } from '@testing-library/vue'
import { createPinia } from 'pinia'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { HttpError } from '@/api/errors'
import { CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { getCandidatureNotes } from '../api'
import CandidatureNotes from './CandidatureNotes.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  getCandidatureNotes: vi.fn(),
}))

function note(overrides: Partial<Note>): Note {
  return {
    entity_id: 'ffffffff-0001-0001-0001-000000000001',
    candidature_id: CANDIDATURE_PARAMS.candidatureUuid,
    message: 'Profil solide',
    publie_par_id: 'eeeeeeee-0001-0001-0001-000000000001',
    publie_par_prenom: 'Marie',
    publie_par_nom: 'Dupont',
    publie_le: '2025-06-10T09:15:00Z',
    ...overrides,
  }
}

function renderNotes() {
  render(CandidatureNotes, {
    props: { candidature: CANDIDATURE_PARAMS },
    global: { plugins: [createPinia(), PiniaColada] },
  })
}

describe('candidatureNotes', () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('lists the notes with their author', async () => {
    const results = [
      note({}),
      note({ entity_id: 'ffffffff-0001-0001-0001-000000000002', message: 'À recontacter', publie_par_prenom: 'Paul', publie_par_nom: 'Bernard' }),
    ]
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 2, results })
    renderNotes()

    expect(await screen.findByRole('heading', { name: '2 notes' })).toBeInTheDocument()
    const [premiere, seconde] = screen.getAllByRole('listitem').map(item => within(item))
    expect(premiere!.getByText('Marie Dupont')).toBeInTheDocument()
    expect(premiere!.getByText('Profil solide')).toBeInTheDocument()
    expect(seconde!.getByText('Paul Bernard')).toBeInTheDocument()
    expect(seconde!.getByText('À recontacter')).toBeInTheDocument()
  })

  it('says when the candidature has no note', async () => {
    vi.mocked(getCandidatureNotes).mockResolvedValue({ count: 0, results: [] })
    renderNotes()

    expect(await screen.findByText('La candidature ne contient aucune note')).toBeInTheDocument()
  })

  it('shows an error when the notes cannot be loaded', async () => {
    vi.mocked(getCandidatureNotes).mockRejectedValue(new HttpError(500, 'Internal Server Error', undefined))
    renderNotes()

    expect(await screen.findByText('Les notes n\'ont pas pu être chargées.')).toBeInTheDocument()
  })
})
