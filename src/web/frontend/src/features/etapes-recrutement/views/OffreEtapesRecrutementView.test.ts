import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { KANBAN_PATH, ORGANISME_UUID, RECRUTEMENT_DETAIL, RECRUTEMENT_UUID } from '@/test/fixtures/candidatures'
import { recrutementDetail } from '@/test/handlers/recrutements'
import { renderWithApp } from '@/test/render'
import { server } from '@/test/server'
import { getEtapesOffre } from '../api'

vi.mock('../api', () => ({
  getEtapesOffre: vi.fn(() => new Promise(() => {})),
}))

const ETAPES_PATH = `${KANBAN_PATH}/etapes-recrutement`

describe('offreEtapesRecrutementView', () => {
  it('loads the recrutement and its stages from the address', async () => {
    server.use(recrutementDetail({ ...RECRUTEMENT_DETAIL, authorized_actions: ['update_recrutement_etapes'] }))
    await renderWithApp(RouterView, { route: ETAPES_PATH })

    expect(await screen.findByRole('link', { name: 'Chargé de mission' })).toBeInTheDocument()
    expect(getEtapesOffre).toHaveBeenCalledWith({ organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID })
  })

  it('refuses the address without the right to customize the étapes', async () => {
    server.use(recrutementDetail({ ...RECRUTEMENT_DETAIL, authorized_actions: ['get_recrutement'] }))
    await renderWithApp(RouterView, { route: ETAPES_PATH })

    expect(await screen.findByText('Vous n’avez pas accès à cette page.')).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Personnaliser les étapes de ce recrutement' })).not.toBeInTheDocument()
  })
})
