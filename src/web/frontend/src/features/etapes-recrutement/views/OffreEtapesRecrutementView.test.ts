import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getRecrutementDetail } from '@/features/recrutements/api'
import { KANBAN_PATH, ORGANISME_UUID, RECRUTEMENT_DETAIL, RECRUTEMENT_UUID } from '@/test/fixtures/candidatures'
import { renderWithApp } from '@/test/render'
import { getEtapesOffre } from '../api'

vi.mock('../api', () => ({
  getEtapesOffre: vi.fn(() => new Promise(() => {})),
}))

vi.mock('@/features/recrutements/api', () => ({
  getRecrutementDetail: vi.fn(),
}))

describe('offreEtapesRecrutementView', () => {
  it('loads the recrutement and its stages from the address', async () => {
    vi.mocked(getRecrutementDetail).mockResolvedValue(RECRUTEMENT_DETAIL)
    await renderWithApp(RouterView, { route: `${KANBAN_PATH}/etapes-recrutement` })

    expect(await screen.findByRole('link', { name: 'Chargé de mission' })).toBeInTheDocument()
    expect(getEtapesOffre).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID)
  })
})
