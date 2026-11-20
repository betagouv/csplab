import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { ORGANISME_UUID, USER_ORGANISME } from '@/test/fixtures/candidatures'
import { RECRUTEMENTS_ACTIFS, RECRUTEMENTS_ARCHIVES } from '@/test/fixtures/recrutements'
import { makeUser } from '@/test/fixtures/utilisateur'
import {
  recrutementsActifsFailure,
  recrutementsActifsPending,
  recrutementsArchives,
} from '@/test/handlers/recrutements'
import { renderWithApp, setupUser } from '@/test/render'
import { server } from '@/test/server'

const RECRUTEMENTS_PATH = `/organismes/${ORGANISME_UUID}/recrutements`
const [FIRST_RECRUTEMENT, SECOND_RECRUTEMENT] = RECRUTEMENTS_ACTIFS
const [FIRST_ARCHIVE] = RECRUTEMENTS_ARCHIVES

describe('recrutementsView', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([USER_ORGANISME]))
  })

  it('shows an error when the recrutements fail to load', async () => {
    server.use(recrutementsActifsFailure())

    await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })

    expect(await screen.findByRole('alert')).toHaveTextContent('Une erreur est survenue lors du chargement des recrutements.')
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
