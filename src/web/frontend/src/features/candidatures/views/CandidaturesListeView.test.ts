import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { getRecrutementDetail } from '@/features/recrutements/api'
import {
  CANDIDATURE_ALICE,
  CANDIDATURES_PAGE,
  KANBAN_PATH,
  RECRUTEMENT_DETAIL,
} from '@/test/fixtures/candidatures'
import { renderWithApp, setupUser } from '@/test/render'
import { getCandidatures } from '../api'
import CandidaturesListeView from './CandidaturesListeView.vue'

vi.mock('../api', () => ({
  getCandidatures: vi.fn(),
  patchEtapeCandidatures: vi.fn(),
}))

vi.mock('@/features/recrutements/api', () => ({
  getRecrutementDetail: vi.fn(),
}))

function candidature(index: number) {
  const day = String(10 + index).padStart(2, '0')
  return {
    uuid: `dddddddd-0001-0001-0001-0000000000${String(index).padStart(2, '0')}`,
    date_soumission: `2025-06-${day}T09:15:00Z`,
    date_derniere_activite: `2025-06-${day}T10:00:00Z`,
    candidat: { uuid: `eeeeeeee-000${index}`, nom: `Nom${index}`, prenom: `Prenom${index}` },
    etape: CANDIDATURES_PAGE.results[0]!.etape,
  }
}

function pageOf(count: number) {
  const results = Array.from({ length: count }, (_, index) => candidature(index + 1))
  return { count, next: null, previous: null, results }
}

describe('candidaturesListeView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(getCandidatures).mockResolvedValue(CANDIDATURES_PAGE)
    vi.mocked(getRecrutementDetail).mockResolvedValue(RECRUTEMENT_DETAIL)
  })

  it('shows one page at a time and reorders on sort', async () => {
    const user = setupUser()
    vi.mocked(getCandidatures).mockResolvedValue(pageOf(8))
    await renderWithApp(CandidaturesListeView, { route: `${KANBAN_PATH}?vue=liste` })

    await vi.waitFor(() => expect(screen.getAllByRole('button', { name: /^Prenom/ })).toHaveLength(6))
    const first = () => screen.getAllByRole('button', { name: /^Prenom/ })[0]!
    expect(first()).toHaveTextContent('Prenom1 Nom1')

    const parDate = screen.getByRole('button', { name: /Date candidature/ })
    await user.click(parDate)
    await user.click(parDate)

    await vi.waitFor(() => expect(first()).toHaveTextContent('Prenom8 Nom8'))
    expect(screen.getAllByRole('button', { name: /^Prenom/ })).toHaveLength(6)
    expect(screen.getByRole('button', { name: 'Page 2' })).toBeInTheDocument()
  })

  it('opens the candidature panel from the candidat name', async () => {
    const user = setupUser()
    const { router } = await renderWithApp(CandidaturesListeView, { route: `${KANBAN_PATH}?vue=liste` })

    await user.click(await screen.findByRole('button', { name: 'Alice Dupont' }))

    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_ALICE))
    expect(router.currentRoute.value.query.vue).toBe('liste')
  })
})
