import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { BRIANCON_UUID, makeUser, MTE_UUID, ORGANISME_INCONNU_UUID, ROLE_BRIANCON, ROLE_MTE } from '@/test/fixtures/utilisateur'
import { renderWithApp } from '@/test/render'

function renderHome(organismeUuid: string) {
  return renderWithApp(RouterView, { route: `/organismes/${organismeUuid}/accueil` })
}

describe('homeView', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON], false, [
      { uuid: MTE_UUID, nom: ROLE_MTE.nom, authorized_actions: ['get_organisme', 'list_recrutements'] },
      { uuid: BRIANCON_UUID, nom: ROLE_BRIANCON.nom, authorized_actions: ['list_recrutements'] },
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
    await renderHome(BRIANCON_UUID)

    expect(await screen.findByRole('heading', { name: 'Prêt à démarrer les recrutements de votre organisme ?' })).toBeInTheDocument()
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
