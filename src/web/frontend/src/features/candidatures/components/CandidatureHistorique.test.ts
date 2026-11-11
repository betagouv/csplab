import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { ACTIVITE, CANDIDATURE_ALICE, CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { candidatureActivites } from '@/test/handlers/candidatures'
import { renderWithApp } from '@/test/render'
import { server } from '@/test/server'
import CandidatureHistorique from './CandidatureHistorique.vue'

describe('candidatureHistorique', () => {
  it('lists every activity of the candidature with their count', async () => {
    const requested = vi.fn()
    const results = ['NoteAjoutee', 'CandidatureEtapeModifiee', 'NoteEditee', 'CandidatureRecue'].map(event_name => ({ ...ACTIVITE, event_name }))
    server.use(candidatureActivites(results, requested))
    await renderWithApp(CandidatureHistorique, { props: { candidature: CANDIDATURE_PARAMS } })

    expect(await screen.findByRole('heading', { name: '4 activités récentes' })).toBeInTheDocument()
    expect(within(screen.getByRole('list')).getAllByRole('listitem')).toHaveLength(4)
    expect(requested).toHaveBeenCalledWith(CANDIDATURE_ALICE, null)
  })
})
