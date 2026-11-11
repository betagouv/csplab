import { screen } from '@testing-library/vue'
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'
import { afterAll, afterEach, beforeAll, describe, expect, it } from 'vitest'
import { RouterView } from 'vue-router'
import { DEMO_ORGANISME } from '@/api/__mocks__/demo'
import { makeUser } from '@/test/fixtures/utilisateur'
import { renderWithApp } from '@/test/render'
import { recrutementsActifsFailure, recrutementsHandlers } from '../__mocks__/handlers'

const USER = makeUser([{ organisme_uuid: DEMO_ORGANISME.uuid, nom: DEMO_ORGANISME.nom, role: 'superviseur' }])
const server = setupServer(...recrutementsHandlers, http.get('*/utilisateur/me', () => HttpResponse.json(USER)))
const RECRUTEMENTS_PATH = `/organismes/${DEMO_ORGANISME.uuid}/recrutements`

describe('recrutementsView with the handlers shared with Storybook', () => {
  beforeAll(() => server.listen({ onUnhandledFrame: 'error' }))
  afterEach(() => server.resetHandlers())
  afterAll(() => server.close())

  it('lists the recrutements of the organisme', async () => {
    await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })

    expect(await screen.findByRole('checkbox', { name: 'Sélectionner Gestionnaire de paie' })).toBeInTheDocument()
  })

  it('shows an error when the recrutements fail to load', async () => {
    server.use(recrutementsActifsFailure)

    await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })

    expect(await screen.findByRole('alert')).toHaveTextContent('Une erreur est survenue lors du chargement des recrutements.')
  })
})
