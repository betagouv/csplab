import { screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { KANBAN_PATH, ORGANISME_UUID, RECRUTEMENT_DETAIL, RECRUTEMENT_UUID, roleOnOrganisme } from '@/test/fixtures/candidatures'
import { MEMBRE_EQUIPE, SECOND_MEMBRE_EQUIPE } from '@/test/fixtures/equipe'
import { RECRUTEMENTS_ACTIFS } from '@/test/fixtures/recrutements'
import { makeUser } from '@/test/fixtures/utilisateur'
import { equipe } from '@/test/handlers/equipe-recrutement'
import { recrutementDetail, recrutementDetailPending, recrutementsActifs } from '@/test/handlers/recrutements'
import { renderWithApp, setupUser } from '@/test/render'
import { server } from '@/test/server'

const EQUIPE_PATH = `${KANBAN_PATH}/equipe`
const OTHER_RECRUTEMENT_UUID = '00000000-0000-0000-0000-0000000000ff'
const RECRUTEMENT_DETAIL_AVEC_EQUIPE = {
  ...RECRUTEMENT_DETAIL,
  authorized_actions: ['list_recrutement_agents' as const, 'add_recrutement_agent' as const],
}

describe('recrutementView', () => {
  it('names the document after the tab and the recrutement', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    await vi.waitFor(() => expect(document.title).toBe('Candidatures - Chargé de mission'))
  })

  it('hides the équipe tab from an agent who cannot list the team', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    await screen.findAllByRole('tab', { name: /Candidatures/ })
    expect(screen.queryAllByRole('tab', { name: /Équipe de recrutement/ })).toHaveLength(0)
  })

  it('shows the équipe tab with the right to list the team', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    server.use(recrutementDetail(RECRUTEMENT_DETAIL_AVEC_EQUIPE))
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    expect(await screen.findAllByRole('tab', { name: /Équipe de recrutement/ })).not.toHaveLength(0)
  })

  it('opens the équipe tab from its own address', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('superviseur')]))
    server.use(recrutementDetail(RECRUTEMENT_DETAIL_AVEC_EQUIPE))
    await renderWithApp(RouterView, { route: EQUIPE_PATH })

    expect(await screen.findByRole('tab', { name: /Équipe de recrutement/, selected: true })).toBeInTheDocument()
    expect(await screen.findByRole('button', { name: 'Ajouter un membre' })).toBeInTheDocument()
  })

  it('keeps the candidatures search when coming back from another tab', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('superviseur')]))
    server.use(recrutementDetail(RECRUTEMENT_DETAIL_AVEC_EQUIPE))
    const user = setupUser()
    const { router } = await renderWithApp(RouterView, { route: KANBAN_PATH })

    await user.type(await screen.findByRole('searchbox', { name: 'Rechercher un candidat' }), 'Martin')
    await router.push(EQUIPE_PATH)
    await screen.findByRole('button', { name: 'Ajouter un membre' })
    await router.push(KANBAN_PATH)

    expect(await screen.findByRole('searchbox', { name: 'Rechercher un candidat' })).toHaveValue('Martin')
  })

  it('empties the candidatures search when moving to another recrutement', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    const user = setupUser()
    const { router } = await renderWithApp(RouterView, { route: KANBAN_PATH })

    await user.type(await screen.findByRole('searchbox', { name: 'Rechercher un candidat' }), 'Martin')
    await router.push(`/organismes/${ORGANISME_UUID}/recrutements/${OTHER_RECRUTEMENT_UUID}`)

    await vi.waitFor(() => expect(screen.getByRole('searchbox', { name: 'Rechercher un candidat' })).toHaveValue(''))
  })

  it('shows the équipe of the recrutement opened after another one', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('superviseur')]))
    const requested = vi.fn()
    server.use(recrutementDetail(RECRUTEMENT_DETAIL_AVEC_EQUIPE))
    const { router } = await renderWithApp(RouterView, { route: EQUIPE_PATH })
    await screen.findByText(MEMBRE_EQUIPE.email)

    server.use(equipe([SECOND_MEMBRE_EQUIPE], requested))
    await router.push(`/organismes/${ORGANISME_UUID}/recrutements/${OTHER_RECRUTEMENT_UUID}/equipe`)

    expect(await screen.findByText(SECOND_MEMBRE_EQUIPE.email)).toBeInTheDocument()
    expect(screen.queryByText(MEMBRE_EQUIPE.email)).not.toBeInTheDocument()
    expect(requested).toHaveBeenCalledWith(ORGANISME_UUID, OTHER_RECRUTEMENT_UUID)
  })

  it('refuses access to the équipe tab url for an agent', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    await renderWithApp(RouterView, { route: EQUIPE_PATH })

    expect(await screen.findByText('Vous n’avez pas accès à cette page.')).toBeInTheDocument()
    await vi.waitFor(() => expect(document.title).toBe('Accès refusé'))
  })

  it('hides the recrutement actions menu without the right to customize the étapes', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    server.use(recrutementDetail({ ...RECRUTEMENT_DETAIL, authorized_actions: ['get_recrutement'] }))
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    await screen.findByRole('heading', { name: RECRUTEMENT_DETAIL.intitule })
    expect(screen.queryByRole('button', { name: 'Actions sur le recrutement' })).not.toBeInTheDocument()
  })

  it('offers to customize the étapes with the right to do so', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    server.use(recrutementDetail({ ...RECRUTEMENT_DETAIL, authorized_actions: ['update_recrutement_etapes'] }))
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    expect(await screen.findByRole('button', { name: 'Actions sur le recrutement' })).toBeInTheDocument()
  })

  it('titles a recrutement opened from the list while its details load', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    const [recrutement] = RECRUTEMENTS_ACTIFS
    server.use(recrutementsActifs([{ ...recrutement, uuid: RECRUTEMENT_UUID }]), recrutementDetailPending())
    const user = setupUser()
    await renderWithApp(RouterView, { route: `/organismes/${ORGANISME_UUID}/recrutements` })

    await user.click(await screen.findByRole('button', { name: recrutement.intitule }))

    expect(await screen.findByRole('heading', { level: 1, name: recrutement.intitule })).toBeInTheDocument()
  })

  it('holds the title back while a recrutement opened from its address loads', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([roleOnOrganisme('agent')]))
    server.use(recrutementDetailPending())
    await renderWithApp(RouterView, { route: KANBAN_PATH })

    await screen.findAllByRole('tab', { name: /Candidatures/ })
    expect(screen.queryByRole('heading', { level: 1 })).not.toBeInTheDocument()
  })
})
