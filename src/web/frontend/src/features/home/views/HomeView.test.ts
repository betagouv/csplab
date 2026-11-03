import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { BRIANCON_UUID, makeUser, MTE_UUID, ROLE_BRIANCON, ROLE_MTE } from '@/test/fixtures/utilisateur'
import { renderWithApp } from '@/test/render'

function renderHome(organismeUuid: string) {
  return renderWithApp(RouterView, { route: `/organismes/${organismeUuid}/accueil` })
}

describe('homeView', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([ROLE_MTE, ROLE_BRIANCON]))
  })

  it('greets the user by their first name', async () => {
    await renderHome(MTE_UUID)

    expect(await screen.findByRole('heading', { level: 1, name: 'Bonjour Marie' })).toBeInTheDocument()
  })

  it('guides a superviseur towards the settings and the recrutements of the organisme', async () => {
    await renderHome(MTE_UUID)

    expect(await screen.findByRole('heading', { name: 'Prêt à démarrer les recrutements de votre organisme ?' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Équipe de recrutement' })).toHaveAttribute('href', `/organismes/${MTE_UUID}`)
    expect(screen.getByRole('link', { name: 'Processus de recrutement' })).toHaveAttribute('href', `/organismes/${MTE_UUID}/etapes`)
    expect(screen.getByRole('link', { name: 'Recrutements' })).toHaveAttribute('href', `/organismes/${MTE_UUID}/recrutements`)
  })

  it('shows the superviseur version to a staff member outside their organismes', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([], true))
    await renderHome(BRIANCON_UUID)

    expect(await screen.findByRole('heading', { name: 'Prêt à démarrer les recrutements de votre organisme ?' })).toBeInTheDocument()
  })

  it('guides an agent towards their candidatures, without links to the settings', async () => {
    await renderHome(BRIANCON_UUID)

    expect(await screen.findByRole('heading', { name: 'Prêt à traiter vos premières candidatures ?' })).toBeInTheDocument()
    expect(screen.queryByRole('link', { name: 'Équipe de recrutement' })).not.toBeInTheDocument()
  })

  it('opens the online help in a new window', async () => {
    await renderHome(BRIANCON_UUID)

    const help = await screen.findByRole('link', { name: 'Consulter l’aide en ligne' })
    expect(help).toHaveAttribute('target', '_blank')
    expect(help).toHaveAttribute('title', 'Consulter l’aide en ligne - nouvelle fenêtre')
  })
})
