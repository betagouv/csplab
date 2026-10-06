import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getEtapesRecrutement } from '@/features/etapes-recrutement/api'
import { ORGANISME_DETAIL } from '@/test/fixtures/organismes'
import { renderWithApp } from '@/test/render'
import { getOrganismeDetail } from '../api'

vi.mock('../api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeDetail: vi.fn(),
}))

vi.mock('@/features/etapes-recrutement/api', () => ({
  getEtapesRecrutement: vi.fn(() => new Promise(() => {})),
}))

describe('organismeView', () => {
  it('opens the stages tab of the organisme from its address', async () => {
    vi.mocked(getOrganismeDetail).mockResolvedValue(ORGANISME_DETAIL)
    await renderWithApp(RouterView, { route: `/organismes/${ORGANISME_DETAIL.uuid}/etapes` })

    expect(await screen.findByRole('tab', { name: /Étapes de recrutement/, selected: true })).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Étapes de recrutement' })).toBeInTheDocument()
    expect(getEtapesRecrutement).toHaveBeenCalledWith(ORGANISME_DETAIL.uuid)
  })
})
