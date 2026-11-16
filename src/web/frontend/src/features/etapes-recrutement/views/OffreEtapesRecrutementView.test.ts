import { screen } from '@testing-library/vue'
import { afterEach, describe, expect, it, vi } from 'vitest'
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

const ETAPES_PATH = `${KANBAN_PATH}/etapes-recrutement`

describe('offreEtapesRecrutementView', () => {
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('loads the recrutement and its stages from the address', async () => {
    vi.mocked(getRecrutementDetail).mockResolvedValue({ ...RECRUTEMENT_DETAIL, authorized_actions: ['update_recrutement_etapes'] })
    await renderWithApp(RouterView, { route: ETAPES_PATH })

    expect(await screen.findByRole('link', { name: 'Chargé de mission' })).toBeInTheDocument()
    expect(await screen.findByRole('heading', { name: 'Personnaliser les étapes de ce recrutement' })).toBeInTheDocument()
    expect(getEtapesOffre).toHaveBeenCalledWith({ organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID })
  })

  it('refuses the address without the right to customize the étapes', async () => {
    vi.mocked(getRecrutementDetail).mockResolvedValue({ ...RECRUTEMENT_DETAIL, authorized_actions: ['get_recrutement'] })
    await renderWithApp(RouterView, { route: ETAPES_PATH })

    expect(await screen.findByText('Vous n’avez pas accès à cette page.')).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Personnaliser les étapes de ce recrutement' })).not.toBeInTheDocument()
    expect(getEtapesOffre).not.toHaveBeenCalled()
  })

  it('waits for the recrutement before showing the page or loading its étapes', async () => {
    vi.mocked(getRecrutementDetail).mockReturnValue(new Promise(() => {}))
    await renderWithApp(RouterView, { route: ETAPES_PATH })

    await vi.waitFor(() => expect(getRecrutementDetail).toHaveBeenCalled())
    expect(getEtapesOffre).not.toHaveBeenCalled()
    expect(screen.queryByRole('heading', { name: 'Personnaliser les étapes de ce recrutement' })).not.toBeInTheDocument()
    expect(screen.queryByText('Étapes de recrutement', { selector: 'h2' })).not.toBeInTheDocument()
    expect(screen.getByRole('status')).toHaveTextContent('Chargement du recrutement')
  })
})
