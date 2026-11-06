import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getOrganismeDetail } from '@/api/organismes'
import { getMe } from '@/api/utilisateur'
import { ORGANISME_DETAIL } from '@/test/fixtures/organismes'
import { BRIANCON_UUID, makeUser, MTE_UUID, ORGANISME_BRIANCON, ORGANISME_INCONNU_UUID, ORGANISME_MTE } from '@/test/fixtures/utilisateur'
import { renderWithApp } from '@/test/render'

vi.mock('@/api/organismes', () => ({
  getOrganismeDetail: vi.fn(),
}))

function renderHome(organismeUuid: string) {
  return renderWithApp(RouterView, { route: `/organismes/${organismeUuid}/accueil` })
}

describe('homeView', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([
      { ...ORGANISME_MTE, authorized_actions: ['get_organisme', 'list_recrutements'] },
      { ...ORGANISME_BRIANCON, authorized_actions: ['list_recrutements'] },
    ]))
  })

  it('greets the user by their first name', async () => {
    await renderHome(MTE_UUID)

    expect(await screen.findByRole('heading', { level: 1, name: 'Bonjour Marie' })).toBeInTheDocument()
  })

  it('guides a superviseur towards the settings and the recrutements of the organisme', async () => {
    await renderHome(MTE_UUID)

    expect(await screen.findByRole('heading', { name: 'Prêt à démarrer les recrutements de votre organisme ?' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Inviter des membres' })).toHaveAttribute('href', `/organismes/${MTE_UUID}`)
    expect(screen.getByRole('link', { name: 'Définir les étapes' })).toHaveAttribute('href', `/organismes/${MTE_UUID}/etapes`)
    expect(screen.getByRole('link', { name: 'Voir les recrutements' })).toHaveAttribute('href', `/organismes/${MTE_UUID}/recrutements`)
  })

  it('shows the superviseur version to a staff member outside their organismes', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([], true))
    vi.mocked(getOrganismeDetail).mockResolvedValue({ ...ORGANISME_DETAIL, uuid: BRIANCON_UUID })
    await renderHome(BRIANCON_UUID)

    expect(await screen.findByRole('heading', { name: 'Prêt à démarrer les recrutements de votre organisme ?' })).toBeInTheDocument()
  })

  it('waits for the rights of a staff member outside their organismes before guiding them', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([], true))
    vi.mocked(getOrganismeDetail).mockReturnValue(new Promise(() => {}))
    await renderHome(BRIANCON_UUID)

    await screen.findByRole('heading', { level: 1, name: 'Bonjour Marie' })
    await vi.waitFor(() => expect(getOrganismeDetail).toHaveBeenCalled())

    expect(screen.queryByRole('heading', { name: 'Prêt à traiter vos premières candidatures ?' })).not.toBeInTheDocument()
  })

  it('guides an agent towards their recrutements, without links to the settings', async () => {
    await renderHome(BRIANCON_UUID)

    expect(await screen.findByRole('heading', { name: 'Prêt à traiter vos premières candidatures ?' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Voir mes recrutements' })).toHaveAttribute('href', `/organismes/${BRIANCON_UUID}/recrutements`)
    expect(screen.queryByRole('link', { name: 'Inviter des membres' })).not.toBeInTheDocument()
  })

  it('tells a user without any organisme how to join one', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([]))
    await renderWithApp(RouterView)

    expect(await screen.findByText('Vous n’êtes rattaché à aucun organisme')).toBeInTheDocument()
  })

  it('tells a user outside the organisme that they have no access', async () => {
    await renderHome(ORGANISME_INCONNU_UUID)

    expect(await screen.findByText('Vous n’avez pas accès à cette page.')).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: 'Voir mes recrutements' })).not.toBeInTheDocument()
  })

  it('opens the online help in a new window', async () => {
    await renderHome(BRIANCON_UUID)

    const help = await screen.findByRole('link', { name: 'Consulter l’aide en ligne' })
    expect(help).toHaveAttribute('target', '_blank')
    expect(help).toHaveAttribute('title', 'Consulter l’aide en ligne - nouvelle fenêtre')
  })
})
