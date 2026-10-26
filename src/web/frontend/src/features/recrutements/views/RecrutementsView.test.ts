import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { getMe } from '@/api/utilisateur'
import { searchAgentByEmail } from '@/features/agents/api'
import { ORGANISME_UUID, roleOnOrganisme } from '@/test/fixtures/candidatures'
import { AGENT_RECHERCHE } from '@/test/fixtures/organismes'
import { RECRUTEMENTS_ACTIFS } from '@/test/fixtures/recrutements'
import { makeUser } from '@/test/fixtures/utilisateur'
import { renderWithApp, setupUser } from '@/test/render'
import { getRecrutementsActifs, getRecrutementsArchives } from '../api'

vi.mock('../api', () => ({
  getRecrutementsActifs: vi.fn(),
  getRecrutementsArchives: vi.fn(),
  setRecrutementsResponsable: vi.fn(),
}))

vi.mock('@/features/agents/api', () => ({
  searchAgentByEmail: vi.fn(),
  createAgent: vi.fn(),
}))

vi.mock('@/api/utilisateur', () => ({
  getMe: vi.fn(),
}))

const RECRUTEMENTS_PATH = `/organismes/${ORGANISME_UUID}/recrutements`
const [PREMIER] = RECRUTEMENTS_ACTIFS

async function openAssignationFor(user: ReturnType<typeof setupUser>) {
  await renderWithApp(RouterView, { route: RECRUTEMENTS_PATH })
  await user.click(await screen.findByRole('checkbox', { name: `Sélectionner ${PREMIER.intitule}` }))
  await user.click(screen.getByRole('button', { name: 'Assigner un responsable' }))
}

describe('recrutementsView', () => {
  beforeEach(() => {
    vi.mocked(getMe).mockReset().mockResolvedValue(makeUser([roleOnOrganisme('superviseur')]))
    vi.mocked(getRecrutementsActifs).mockReset().mockResolvedValue({ count: RECRUTEMENTS_ACTIFS.length, results: RECRUTEMENTS_ACTIFS })
    vi.mocked(getRecrutementsArchives).mockReset().mockResolvedValue({ count: 0, results: [] })
    vi.mocked(searchAgentByEmail).mockReset().mockResolvedValue(AGENT_RECHERCHE)
  })

  it('starts a new search each time the assignation drawer opens', async () => {
    const user = setupUser()
    await openAssignationFor(user)

    await user.type(await screen.findByRole('searchbox', { name: /Responsable/ }), `${AGENT_RECHERCHE.email}{Enter}`)
    await screen.findByText('Jeanne Dupont')
    await user.click(screen.getByRole('button', { name: 'Annuler' }))
    await user.click(screen.getByRole('button', { name: 'Assigner un responsable' }))

    expect(await screen.findByRole('searchbox', { name: /Responsable/ })).toHaveValue('')
    expect(screen.queryByText('Jeanne Dupont')).not.toBeInTheDocument()
  })

  it('closes the assignation drawer once the last offer is removed', async () => {
    const user = setupUser()
    await openAssignationFor(user)

    await user.click(await screen.findByRole('button', { name: `Retirer ${PREMIER.intitule} de la sélection` }))

    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Assigner un responsable' })).not.toBeInTheDocument())
  })
})
