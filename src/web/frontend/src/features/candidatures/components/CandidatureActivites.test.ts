import { screen, within } from '@testing-library/vue'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { ACTIVITE, CANDIDATURE_ALICE, CANDIDATURE_PARAMS, KANBAN_PATH } from '@/test/fixtures/candidatures'
import { candidatureActivites, candidatureActivitesFailure } from '@/test/handlers/candidatures'
import { renderWithApp } from '@/test/render'
import { server } from '@/test/server'
import CandidatureActivites from './CandidatureActivites.vue'

function renderActivites() {
  return renderWithApp(CandidatureActivites, {
    props: { candidature: CANDIDATURE_PARAMS, historiqueRouteName: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.tabs.historique },
  })
}

describe('candidatureActivites', () => {
  beforeEach(() => {
    vi.useFakeTimers({ toFake: ['Date'] })
    vi.setSystemTime(new Date('2026-09-29T12:00:00'))
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('lists the three latest activities with their author and age', async () => {
    const requested = vi.fn()
    server.use(candidatureActivites([
      ACTIVITE,
      { ...ACTIVITE, event_name: 'CandidatureEtapeModifiee', utilisateur_prenom: 'Paul', utilisateur_nom: 'Bernard' },
      { ...ACTIVITE, event_name: 'CandidatureRecue', utilisateur_prenom: '', utilisateur_nom: '' },
    ], requested))
    await renderActivites()

    const list = await screen.findByRole('list')
    const [note, etape, reception] = within(list).getAllByRole('listitem')
    expect(within(note).getByText('Note ajoutée')).toBeInTheDocument()
    expect(within(note).getByText('par Marie Dupont')).toBeInTheDocument()
    expect(within(note).getByText('il y a 2 heures')).toBeInTheDocument()
    expect(within(etape).getByText('Étape modifiée')).toBeInTheDocument()
    expect(within(etape).getByText('par Paul Bernard')).toBeInTheDocument()
    expect(within(reception).getByText('Candidature reçue')).toBeInTheDocument()
    expect(within(reception).queryByText(/^par /)).not.toBeInTheDocument()
    expect(requested).toHaveBeenCalledWith(CANDIDATURE_ALICE, '3')
  })

  it('links to the full activity history of the candidature', async () => {
    await renderActivites()

    expect(screen.getByRole('link', { name: 'Voir tout' })).toHaveAttribute('href', `${KANBAN_PATH}/candidatures/${CANDIDATURE_ALICE}/historique`)
    await screen.findByText('La candidature n\'a aucune activité')
  })

  it('names an unknown activity with a generic label', async () => {
    server.use(candidatureActivites([{ ...ACTIVITE, event_name: 'TagPose' }]))
    await renderActivites()

    expect(await screen.findByText('Activité')).toBeInTheDocument()
  })

  it('says when the candidature has no activity', async () => {
    await renderActivites()

    expect(await screen.findByText('La candidature n\'a aucune activité')).toBeInTheDocument()
  })

  it('shows an error when the activities cannot be loaded', async () => {
    server.use(candidatureActivitesFailure(500))
    await renderActivites()

    expect(await screen.findByText('Les activités n\'ont pas pu être chargées.')).toBeInTheDocument()
  })
})
