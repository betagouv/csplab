import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { getCandidatureListe } from '@/features/candidatures/api'
import { getEquipeRecrutement } from '@/features/equipe-recrutement/api'
import { CANDIDATURE_LISTE, KANBAN_PATH, ORGANISME_UUID, RECRUTEMENT_DETAIL, roleOnOrganisme } from '@/test/fixtures/candidatures'
import { makeUser } from '@/test/fixtures/utilisateur'
import { renderWithApp, setupUser } from '@/test/render'
import { getRecrutementDetail } from '../api'

vi.mock('@/features/candidatures/api', () => ({
  getCandidatureListe: vi.fn(),
  patchEtapeCandidatures: vi.fn(),
  getMotifsRefus: vi.fn(),
}))

vi.mock('../api', () => ({
  getRecrutementDetail: vi.fn(),
}))

vi.mock('@/features/equipe-recrutement/api', () => ({
  getEquipeRecrutement: vi.fn(),
}))

const EQUIPE_PATH = `${KANBAN_PATH}/equipe`
const OTHER_RECRUTEMENT_UUID = '00000000-0000-0000-0000-0000000000ff'
const RECRUTEMENT_DETAIL_AVEC_EQUIPE = {
  ...RECRUTEMENT_DETAIL,
  authorized_actions: ['list_recrutement_agents' as const, 'add_recrutement_agent' as const],
}

describe('recrutementView', () => {
  beforeEach(() => {
    vi.mocked(getRecrutementDetail).mockReset().mockResolvedValue(RECRUTEMENT_DETAIL)
    vi.mocked(getCandidatureListe).mockReset().mockResolvedValue(CANDIDATURE_LISTE)
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

  it('shows the équipe tab with the right to list the team', async () => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    vi.mocked(getRecrutementDetail).mockResolvedValue(RECRUTEMENT_DETAIL_AVEC_EQUIPE)
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    expect(await screen.findAllByRole('tab', { name: /Équipe de recrutement/ })).not.toHaveLength(0)
  })

  it('opens the équipe tab from its own address', async () => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([roleOnOrganisme('superviseur')]))
    vi.mocked(getRecrutementDetail).mockResolvedValue(RECRUTEMENT_DETAIL_AVEC_EQUIPE)
    await renderWithApp(RouterView, { route: EQUIPE_PATH })

    expect(await screen.findByRole('tab', { name: /Équipe de recrutement/, selected: true })).toBeInTheDocument()
    expect(await screen.findByRole('button', { name: 'Ajouter un membre' })).toBeInTheDocument()
  })

  it('keeps the candidatures search when coming back from another tab', async () => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([roleOnOrganisme('superviseur')]))
    vi.mocked(getRecrutementDetail).mockResolvedValue(RECRUTEMENT_DETAIL_AVEC_EQUIPE)
    const user = setupUser()
    const { router } = await renderWithApp(RouterView, { route: KANBAN_PATH })

    await user.type(await screen.findByRole('searchbox', { name: 'Rechercher un candidat' }), 'Martin')
    await router.push(EQUIPE_PATH)
    await screen.findByRole('button', { name: 'Ajouter un membre' })
    await router.push(KANBAN_PATH)

    expect(await screen.findByRole('searchbox', { name: 'Rechercher un candidat' })).toHaveValue('Martin')
  })

  it('empties the candidatures search when moving to another recrutement', async () => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    const user = setupUser()
    const { router } = await renderWithApp(RouterView, { route: KANBAN_PATH })

    await user.type(await screen.findByRole('searchbox', { name: 'Rechercher un candidat' }), 'Martin')
    await router.push(`/organismes/${ORGANISME_UUID}/recrutements/${OTHER_RECRUTEMENT_UUID}`)

    await vi.waitFor(() => expect(screen.getByRole('searchbox', { name: 'Rechercher un candidat' })).toHaveValue(''))
  })

  it('refuses access to the équipe tab url for an agent', async () => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    await renderWithApp(RouterView, { route: EQUIPE_PATH })

    expect(await screen.findByText('Vous n’avez pas accès à cette page.')).toBeInTheDocument()
    await vi.waitFor(() => expect(document.title).toBe('Accès refusé'))
  })

  it('hides the recrutement actions menu without the right to customize the étapes', async () => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    vi.mocked(getRecrutementDetail).mockResolvedValue({ ...RECRUTEMENT_DETAIL, authorized_actions: ['get_recrutement'] })
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    await screen.findByRole('heading', { name: RECRUTEMENT_DETAIL.intitule })
    expect(screen.queryByRole('button', { name: 'Actions sur le recrutement' })).not.toBeInTheDocument()
  })

  it('offers to customize the étapes with the right to do so', async () => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    vi.mocked(getRecrutementDetail).mockResolvedValue({ ...RECRUTEMENT_DETAIL, authorized_actions: ['update_recrutement_etapes'] })
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    expect(await screen.findByRole('button', { name: 'Actions sur le recrutement' })).toBeInTheDocument()
  })
})
