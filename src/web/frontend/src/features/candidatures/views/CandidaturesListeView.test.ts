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

describe('candidaturesListeView', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(getCandidatures).mockResolvedValue(CANDIDATURES_PAGE)
    vi.mocked(getRecrutementDetail).mockResolvedValue(RECRUTEMENT_DETAIL)
  })

  it('opens the candidature panel from the candidat name', async () => {
    const user = setupUser()
    const { router } = await renderWithApp(CandidaturesListeView, { route: `${KANBAN_PATH}?vue=liste` })

    await user.click(await screen.findByRole('button', { name: 'Alice Dupont' }))

    await vi.waitFor(() => expect(router.currentRoute.value.params.candidatureUuid).toBe(CANDIDATURE_ALICE))
    expect(router.currentRoute.value.query.vue).toBe('liste')
  })
})
