import type { CreateOrganismePayload, OrganismesList, UpdateOrganismePayload } from '../types'
import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { getMe } from '@/api/utilisateur'
import { CREATED_ORGANISME, ORGANISME, ORGANISMES } from '@/test/fixtures/organismes'
import { makeUser, STAFF_ACTIONS } from '@/test/fixtures/utilisateur'
import { organismeCreation, organismeCreationFailure, organismes, organismesFailure, organismesPending, organismeUpdate } from '@/test/handlers/organismes'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import { ORGANISMES_PAGE_SIZE, SEARCH_DEBOUNCE_MS } from '../constants/organisme'
import OrganismesSection from './OrganismesSection.vue'

const REJECTED_SIRET_MESSAGE = 'Ce SIRET est déjà utilisé ou n\'est pas valide.'

const CREATED_ORGANISME_ROW: OrganismesList = {
  ...CREATED_ORGANISME,
  nombre_agents: 0,
  nombre_offres_publiees: 0,
  authorized_actions: [],
}

const Host = withToaster(OrganismesSection)

const ORGANISMES_COUNT = 250
const FULL_PAGE = Array.from({ length: ORGANISMES_PAGE_SIZE }, (_, index) => ({ ...ORGANISME, uuid: `organisme-${index}` }))

function watchRequests() {
  const requests = vi.fn<(query: { page: string | null, filter: string | null }) => void>()
  server.use(organismes(FULL_PAGE, requests, ORGANISMES_COUNT))
  return requests
}

function searchbox() {
  return screen.getByRole('searchbox', { name: 'Rechercher un organisme, un siret' })
}

function nextPage() {
  return within(screen.getByRole('navigation', { name: 'Pagination' })).getByRole('button', { name: 'Page suivante' })
}

function watchOrganismesLoads() {
  const loads = vi.fn()
  server.use(organismes(ORGANISMES, loads))
  return loads
}

async function renderSection() {
  const view = await renderWithApp(Host)
  await screen.findByText(ORGANISME.nom)
  return view
}

async function fillCreationForm(user: ReturnType<typeof setupUser>) {
  await user.click(screen.getByRole('button', { name: 'Ajouter un organisme' }))
  await user.type(await screen.findByRole('textbox', { name: 'Nom de l\'organisme' }), CREATED_ORGANISME.nom)
  await user.type(screen.getByRole('textbox', { name: 'SIRET de l\'organisme' }), CREATED_ORGANISME.siret)
  await user.click(screen.getByRole('radio', { name: 'Fonction Publique Territoriale' }))
}

describe('organismesSection', () => {
  it('lists the organismes', async () => {
    await renderWithApp(Host)

    expect(await screen.findByRole('cell', { name: ORGANISME.siret })).toBeInTheDocument()
  })

  it('creates an organisme with the entered details, then lists it', async () => {
    const user = setupUser()
    const sent = vi.fn<(payload: CreateOrganismePayload) => void>()
    server.use(organismeCreation(CREATED_ORGANISME, (payload) => {
      sent(payload)
      server.use(organismes([ORGANISME, CREATED_ORGANISME_ROW]))
    }))
    await renderSection()

    await fillCreationForm(user)
    await user.click(screen.getByRole('button', { name: 'Créer l\'organisme' }))

    expect(await screen.findByRole('heading', { name: 'Organisme créé' })).toBeInTheDocument()
    expect(await screen.findByText(CREATED_ORGANISME.siret)).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith({
      nom: CREATED_ORGANISME.nom,
      siret: CREATED_ORGANISME.siret,
      versant: CREATED_ORGANISME.versant,
      gestion_ats: true,
    })
  })

  it('tells the user when the creation fails and keeps the drawer open', async () => {
    const user = setupUser()
    const loads = watchOrganismesLoads()
    server.use(organismeCreationFailure(500))
    await renderSection()

    await fillCreationForm(user)
    await user.click(screen.getByRole('button', { name: 'Créer l\'organisme' }))

    expect(await screen.findByRole('heading', { name: 'La création de l\'organisme a échoué', hidden: true })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Créer l\'organisme' })).toBeInTheDocument()
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))
  })

  it('forgets the refused siret once the drawer is closed', async () => {
    const user = setupUser()
    const loads = watchOrganismesLoads()
    server.use(organismeCreationFailure(400))
    await renderSection()

    await fillCreationForm(user)
    await user.click(screen.getByRole('button', { name: 'Créer l\'organisme' }))
    expect(await screen.findByText(REJECTED_SIRET_MESSAGE)).toBeInTheDocument()
    await vi.waitFor(() => expect(loads).toHaveBeenCalledTimes(2))

    await user.click(screen.getByRole('button', { name: 'Annuler' }))
    await user.click(screen.getByRole('button', { name: 'Ajouter un organisme' }))
    const siret = await screen.findByRole('textbox', { name: 'SIRET de l\'organisme' })
    expect(siret).toHaveValue('')
    await user.type(siret, CREATED_ORGANISME.siret)

    expect(screen.queryByText(REJECTED_SIRET_MESSAGE)).not.toBeInTheDocument()
  })

  it('renames an organisme from its actions, then shows the new name in the list', async () => {
    vi.mocked(getMe).mockResolvedValue(makeUser([], STAFF_ACTIONS))
    const user = setupUser()
    const sent = vi.fn<(organismeUuid: string, payload: UpdateOrganismePayload) => void>()
    const renamed = { ...ORGANISME, nom: 'Organisme renommé' }
    server.use(organismeUpdate(renamed, (...args) => {
      sent(...args)
      server.use(organismes([renamed]))
    }))
    await renderSection()

    await user.click(screen.getByRole('button', { name: `Actions pour ${ORGANISME.nom}` }))
    await user.click(await screen.findByRole('menuitem', { name: 'Modifier l’organisme' }))
    const nom = await screen.findByRole('textbox', { name: 'Nom de l\'organisme' })
    await user.clear(nom)
    await user.type(nom, 'Organisme renommé')
    await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))

    expect(await screen.findByRole('heading', { name: 'Organisme modifié' })).toBeInTheDocument()
    expect(await screen.findByText('Organisme renommé')).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(ORGANISME.uuid, {
      nom: 'Organisme renommé',
      versant: ORGANISME.versant,
      gestion_ats: ORGANISME.gestion_ats,
    })
  })

  it('shows the total count sent by the back and requests the next page', async () => {
    const requests = watchRequests()
    const user = setupUser()
    await renderWithApp(Host)

    expect(await screen.findByText(`${ORGANISMES_COUNT} organismes`)).toBeInTheDocument()
    expect(screen.getByText(`Affichage de 1 à ${ORGANISMES_PAGE_SIZE} sur ${ORGANISMES_COUNT}`)).toBeInTheDocument()

    await user.click(nextPage())

    await vi.waitFor(() => expect(requests).toHaveBeenLastCalledWith({ page: '2', filter: null }))
  })

  it('keeps the current page displayed while the next one loads', async () => {
    watchRequests()
    const user = setupUser()
    await renderWithApp(Host)
    await screen.findByText(`${ORGANISMES_COUNT} organismes`)

    server.use(organismesPending())
    await user.click(nextPage())

    expect(screen.getAllByText(ORGANISME.siret)).toHaveLength(ORGANISMES_PAGE_SIZE)
  })

  it('filters with the trimmed term once it has three characters', async () => {
    const requests = watchRequests()
    const user = setupUser()
    await renderWithApp(Host)
    await screen.findByText(`${ORGANISMES_COUNT} organismes`)

    vi.useFakeTimers()
    await setupUser({ advanceTimers: vi.advanceTimersByTime }).type(searchbox(), ' ma')
    await vi.advanceTimersByTimeAsync(SEARCH_DEBOUNCE_MS)
    vi.useRealTimers()
    expect(requests).toHaveBeenCalledOnce()

    await user.type(searchbox(), 'irie ')

    await vi.waitFor(() => expect(requests).toHaveBeenLastCalledWith({ page: '1', filter: 'mairie' }))
    expect(requests).toHaveBeenCalledTimes(2)
  })

  it('goes back to the first page when the filter changes', async () => {
    const requests = watchRequests()
    const user = setupUser()
    await renderWithApp(Host)
    await user.click(await screen.findByRole('button', { name: 'Page suivante' }))
    await vi.waitFor(() => expect(requests).toHaveBeenLastCalledWith({ page: '2', filter: null }))

    await user.type(searchbox(), 'mairie')

    await vi.waitFor(() => expect(requests).toHaveBeenLastCalledWith({ page: '1', filter: 'mairie' }))
    expect(requests).not.toHaveBeenCalledWith({ page: '2', filter: 'mairie' })
  })

  it('keeps the search available when a search fails', async () => {
    const user = setupUser()
    await renderSection()

    server.use(organismesFailure(500))
    await user.type(searchbox(), 'mai')
    expect(await screen.findByText('Impossible de charger les organismes')).toBeInTheDocument()

    server.use(organismes([ORGANISME]))
    await user.type(searchbox(), 'rie')

    expect(await screen.findByText('1 organisme')).toBeInTheDocument()
    expect(screen.queryByText('Impossible de charger les organismes')).not.toBeInTheDocument()
  })
})
