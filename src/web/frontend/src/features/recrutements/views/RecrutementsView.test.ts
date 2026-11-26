import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { ORGANISME_UUID, RECRUTEMENT_DETAIL, RECRUTEMENT_UUID, USER_ORGANISME } from '@/test/fixtures/candidatures'
import { RECRUTEMENTS_ACTIFS, RECRUTEMENTS_ARCHIVES } from '@/test/fixtures/recrutements'
import { makeUser } from '@/test/fixtures/utilisateur'
import { equipe, membreUpdate } from '@/test/handlers/equipe-recrutement'
import {
  recrutementDetail,
  recrutementsActifs,
  recrutementsActifsFailure,
  recrutementsActifsPending,
  recrutementsArchives,
} from '@/test/handlers/recrutements'
import { renderWithApp, setupUser } from '@/test/render'
import { server } from '@/test/server'

const RECRUTEMENTS_PATH = `/organismes/${ORGANISME_UUID}/recrutements`
const [FIRST_RECRUTEMENT, SECOND_RECRUTEMENT] = RECRUTEMENTS_ACTIFS
const [FIRST_ARCHIVE] = RECRUTEMENTS_ARCHIVES
const EQUIPE_PATH = `${RECRUTEMENTS_PATH}/${RECRUTEMENT_UUID}/equipe`

describe('recrutementsView', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockResolvedValue(makeUser([USER_ORGANISME]))
  })

  it('shows an error when the recrutements fail to load', async () => {
    server.use(recrutementsActifsFailure())

    await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })

    expect(await screen.findByRole('alert')).toHaveTextContent('Une erreur est survenue lors du chargement des recrutements.')
  })

  it.each([
    {
      tab: 'en cours',
      path: RECRUTEMENTS_PATH,
      intitule: FIRST_RECRUTEMENT.intitule,
      list: (responsables: { nom: string }[]) => recrutementsActifs([{ ...FIRST_RECRUTEMENT, uuid: RECRUTEMENT_UUID, responsables }]),
    },
    {
      tab: 'terminés',
      path: `${RECRUTEMENTS_PATH}/archives`,
      intitule: FIRST_ARCHIVE.intitule,
      list: (responsables: { nom: string }[]) => recrutementsArchives([{ ...FIRST_ARCHIVE, uuid: RECRUTEMENT_UUID, responsables }]),
    },
  ])('removes from the recrutements $tab the responsable who left the équipe', async ({ path, intitule, list }) => {
    server.use(
      list([{ nom: 'Jeanne Dupont' }]),
      recrutementDetail({ ...RECRUTEMENT_DETAIL, authorized_actions: ['list_recrutement_agents', 'revoke_recrutement_agent'] }),
      membreUpdate(() => server.use(list([]), equipe([]))),
    )
    const user = setupUser()
    const { router } = await renderWithApp(RouterView, { route: path })
    await vi.waitFor(() => expect(screen.getByRole('row', { name: new RegExp(intitule) })).toHaveTextContent('Jeanne Dupont'))

    await router.push(EQUIPE_PATH)
    await user.click(await screen.findByRole('button', { name: 'Actions pour Jeanne Dupont' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Retirer de l\'équipe' }))
    await user.click(await screen.findByRole('button', { name: 'Retirer de l’équipe' }))
    await screen.findByText('Aucun membre rattaché à ce recrutement.')
    await router.push(path)

    await vi.waitFor(() => expect(screen.getByRole('row', { name: new RegExp(intitule) })).not.toHaveTextContent('Jeanne Dupont'))
  })

  it('loads the recrutements terminés once their tab opens', async () => {
    const requested = vi.fn()
    server.use(recrutementsArchives(RECRUTEMENTS_ARCHIVES, requested))
    const user = setupUser()
    await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })
    await screen.findByRole('button', { name: FIRST_RECRUTEMENT.intitule })
    expect(requested).not.toHaveBeenCalled()

    await user.click(screen.getByRole('tab', { name: /Recrutements terminés/ }))

    expect(await screen.findByRole('button', { name: FIRST_ARCHIVE.intitule })).toBeInTheDocument()
    expect(requested).toHaveBeenCalledWith(ORGANISME_UUID)
  })

  it('shows the recrutements terminés while the recrutements en cours are still loading', async () => {
    server.use(recrutementsActifsPending())
    const user = setupUser()
    await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })
    expect(await screen.findByRole('status', { name: 'Chargement des recrutements en cours' })).toBeInTheDocument()

    await user.click(screen.getByRole('tab', { name: /Recrutements terminés/ }))

    expect(await screen.findByRole('button', { name: FIRST_ARCHIVE.intitule })).toBeInTheDocument()
    expect(screen.queryByRole('status', { name: /Chargement des recrutements/ })).not.toBeInTheDocument()
  })

  it('keeps the search of the recrutements en cours after a visit to the recrutements terminés', async () => {
    const user = setupUser()
    await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })
    await user.type(await screen.findByRole('searchbox', { name: 'Rechercher un recrutement' }), FIRST_RECRUTEMENT.intitule)

    await user.click(screen.getByRole('tab', { name: /Recrutements terminés/ }))
    await screen.findByRole('button', { name: FIRST_ARCHIVE.intitule })
    await user.click(screen.getByRole('tab', { name: /Recrutements en cours/ }))

    expect(await screen.findByRole('searchbox', { name: 'Rechercher un recrutement' })).toHaveValue(FIRST_RECRUTEMENT.intitule)
    expect(screen.queryByRole('button', { name: SECOND_RECRUTEMENT.intitule })).not.toBeInTheDocument()
  })
})
