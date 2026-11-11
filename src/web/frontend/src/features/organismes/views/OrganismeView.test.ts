import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { ETAPES, RECEPTION } from '@/test/fixtures/etapes-recrutement'
import { ORGANISME_DETAIL } from '@/test/fixtures/organismes'
import { etapesOrganisme } from '@/test/handlers/etapes-recrutement'
import { organismeDetail, organismeDetailFailure } from '@/test/handlers/organismes'
import { renderWithApp } from '@/test/render'
import { server } from '@/test/server'

const ORGANISME_ROUTE = `/organismes/${ORGANISME_DETAIL.uuid}`

describe('organismeView', () => {
  it('names the organisme of the address in the page header', async () => {
    const requested = vi.fn()
    server.use(organismeDetail(ORGANISME_DETAIL, requested))
    await renderWithApp(RouterView, { route: ORGANISME_ROUTE })

    expect(await screen.findByText(ORGANISME_DETAIL.nom)).toBeInTheDocument()
    expect(requested).toHaveBeenCalledWith(ORGANISME_DETAIL.uuid)
  })

  it('opens the stages tab of the organisme from its address', async () => {
    const requested = vi.fn()
    server.use(etapesOrganisme(ETAPES, requested))
    await renderWithApp(RouterView, { route: `${ORGANISME_ROUTE}/etapes` })

    expect(await screen.findByRole('tab', { name: /Étapes de recrutement/, selected: true })).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Étapes de recrutement' })).toBeInTheDocument()
    expect(await screen.findByRole('button', { name: `Actions pour ${RECEPTION.nom}` })).toBeInTheDocument()
    expect(requested).toHaveBeenCalledWith(ORGANISME_DETAIL.uuid)
  })

  it('shows the not found page when the organisme does not exist', async () => {
    server.use(organismeDetailFailure(404))
    await renderWithApp(RouterView, { route: ORGANISME_ROUTE })

    expect(await screen.findByText('Cette page n’existe pas.')).toBeInTheDocument()
  })

  it('shows the forbidden page when the organisme is refused', async () => {
    server.use(organismeDetailFailure(403))
    await renderWithApp(RouterView, { route: ORGANISME_ROUTE })

    expect(await screen.findByText('Vous n’avez pas accès à cette page.')).toBeInTheDocument()
  })
})
