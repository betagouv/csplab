import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { ETAPES, RECEPTION } from '@/test/fixtures/etapes-recrutement'
import { ORGANISME_DETAIL } from '@/test/fixtures/organismes'
import { etapesOrganisme } from '@/test/handlers/etapes-recrutement'
import { renderWithApp } from '@/test/render'
import { server } from '@/test/server'
import { getOrganismeDetail } from '../api'

vi.mock('../api', () => ({
  getOrganismesList: vi.fn(),
  getOrganismeDetail: vi.fn(),
}))

describe('organismeView', () => {
  it('opens the stages tab of the organisme from its address', async () => {
    const requested = vi.fn()
    server.use(etapesOrganisme(ETAPES, requested))
    vi.mocked(getOrganismeDetail).mockResolvedValue(ORGANISME_DETAIL)
    await renderWithApp(RouterView, { route: `/organismes/${ORGANISME_DETAIL.uuid}/etapes` })

    expect(await screen.findByRole('tab', { name: /Étapes de recrutement/, selected: true })).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Étapes de recrutement' })).toBeInTheDocument()
    expect(await screen.findByRole('button', { name: `Actions pour ${RECEPTION.nom}` })).toBeInTheDocument()
    expect(requested).toHaveBeenCalledWith(ORGANISME_DETAIL.uuid)
  })
})
