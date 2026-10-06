import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { getEquipeRecrutement } from '@/features/equipe-recrutement/api'
import { getRecrutementDetail } from '@/features/recrutements/api'
import { KANBAN, KANBAN_PATH, RECRUTEMENT_DETAIL, roleOnOrganisme } from '@/test/fixtures/candidatures'
import { makeUser } from '@/test/fixtures/utilisateur'
import { renderWithApp } from '@/test/render'
import { getRecrutementKanban } from '../api'

vi.mock('../api', () => ({
  getRecrutementKanban: vi.fn(),
  getCandidatureListe: vi.fn(),
  patchEtapeCandidatures: vi.fn(),
  getMotifsRefus: vi.fn(),
}))

vi.mock('@/features/recrutements/api', () => ({
  getRecrutementDetail: vi.fn(),
}))

vi.mock('@/features/equipe-recrutement/api', () => ({
  getEquipeRecrutement: vi.fn(),
}))

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

const EQUIPE_PATH = `${KANBAN_PATH}/equipe`

describe('candidaturesView', () => {
  beforeEach(() => {
    vi.mocked(getRecrutementDetail).mockReset().mockResolvedValue(RECRUTEMENT_DETAIL)
    vi.mocked(getRecrutementKanban).mockReset().mockResolvedValue(KANBAN)
    vi.mocked(getEquipeRecrutement).mockReset().mockResolvedValue([])
  })

  it('names the document after the tab and the recrutement', async () => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    await vi.waitFor(() => expect(document.title).toBe('Candidatures - Chargé de mission'))
  })

  it('hides the équipe tab from an agent who cannot list the team', async () => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    await screen.findAllByRole('tab', { name: /Candidatures/ })
    expect(screen.queryAllByRole('tab', { name: /Équipe de recrutement/ })).toHaveLength(0)
  })

  it.each([
    ['a superviseur', makeUser([roleOnOrganisme('superviseur')])],
    ['a staff user', makeUser([], true)],
  ])('shows the équipe tab to %s', async (_, utilisateur) => {
    vi.mocked(getMe).mockReset().mockResolvedValue(utilisateur)
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    expect(await screen.findAllByRole('tab', { name: /Équipe de recrutement/ })).not.toHaveLength(0)
  })

  it('refuses access to the équipe tab url for an agent', async () => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    await renderWithApp(RouterView, { route: EQUIPE_PATH })

    expect(await screen.findByText('Vous n’avez pas accès à cette page.')).toBeInTheDocument()
    await vi.waitFor(() => expect(document.title).toBe('Accès refusé'))
  })
})
