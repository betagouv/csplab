import type { EtapeRecrutement, UpdateEtapeRecrutement } from '../types'
import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { ORGANISME_UUID } from '@/test/fixtures/candidatures'
import { ENTRETIEN, ETAPES, ETAPES_RENAMED, PRESELECTION, RECEPTION, RECRUTEMENT, REFUS } from '@/test/fixtures/etapes-recrutement'
import {
  etapesOrganisme,
  etapesOrganismeInit,
  etapesOrganismeUpdate,
  etapesOrganismeUpdateFailure,
} from '@/test/handlers/etapes-recrutement'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import { ETAPES_TEXTS_ORGANISME } from '../constants/etape-recrutement'
import EtapesRecrutementList from './EtapesRecrutementList.vue'

const Host = withToaster(EtapesRecrutementList, {
  params: { type: 'organisme', organismeUuid: ORGANISME_UUID },
  texts: ETAPES_TEXTS_ORGANISME,
})

const NOUVELLE: EtapeRecrutement = { uuid: 'ffffffff-0001-0001-0001-000000000006', nom: 'Test technique', categorie: 'EN_COURS' }

function etapeNames() {
  return screen.getAllByRole('button', { name: /^Actions pour / }).map(button => button.getAttribute('aria-label')?.replace('Actions pour ', ''))
}

async function openList() {
  const user = setupUser()
  await renderWithApp(Host)
  await screen.findByRole('button', { name: `Actions pour ${RECEPTION.nom}` })
  return user
}

async function chooseAction(user: ReturnType<typeof setupUser>, etape: EtapeRecrutement, action: string) {
  await user.click(screen.getByRole('button', { name: `Actions pour ${etape.nom}` }))
  await user.click(await screen.findByRole('menuitem', { name: action }))
}

async function submitName(user: ReturnType<typeof setupUser>, nom: string, confirm: string) {
  const dialog = await screen.findByRole('dialog')
  const input = within(dialog).getByRole('textbox', { name: 'Nom de l\'étape' })
  await user.clear(input)
  await user.type(input, nom)
  await user.click(within(dialog).getByRole('button', { name: confirm }))
}

const NOUVELLE_SAISIE: UpdateEtapeRecrutement = { nom: 'Test technique', categorie: 'EN_COURS' }

function updateSpy() {
  return vi.fn<(organismeUuid: string, payload: UpdateEtapeRecrutement[]) => void>()
}

describe('etapesRecrutementList', () => {
  it('lists the étapes of the organisme', async () => {
    const requested = vi.fn()
    server.use(etapesOrganisme(ETAPES, requested))
    await openList()

    expect(etapeNames()).toEqual(ETAPES.map(({ nom }) => nom))
    expect(requested).toHaveBeenCalledWith(ORGANISME_UUID)
  })

  it('adds a new étape before the final étapes, with the spaces around its name removed', async () => {
    const sent = updateSpy()
    server.use(etapesOrganismeUpdate([RECEPTION, PRESELECTION, ENTRETIEN, NOUVELLE, REFUS, RECRUTEMENT], sent))
    const user = await openList()

    await user.click(screen.getByRole('button', { name: 'Ajouter une étape' }))
    await submitName(user, ' Test technique ', 'Ajouter')

    await vi.waitFor(() => expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, [RECEPTION, PRESELECTION, ENTRETIEN, NOUVELLE_SAISIE, REFUS, RECRUTEMENT]))
    expect(await screen.findByRole('button', { name: `Actions pour ${NOUVELLE.nom}` })).toBeInTheDocument()
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('adds a new étape at the end when no final étape exists', async () => {
    const sent = updateSpy()
    server.use(etapesOrganisme([RECEPTION, PRESELECTION]), etapesOrganismeUpdate([RECEPTION, PRESELECTION, NOUVELLE], sent))
    const user = await openList()

    await user.click(screen.getByRole('button', { name: 'Ajouter une étape' }))
    await submitName(user, 'Test technique', 'Ajouter')

    await vi.waitFor(() => expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, [RECEPTION, PRESELECTION, NOUVELLE_SAISIE]))
  })

  it.each([
    { action: 'Ajouter une étape au-dessus', expected: [RECEPTION, NOUVELLE_SAISIE, PRESELECTION, ENTRETIEN, REFUS, RECRUTEMENT] },
    { action: 'Ajouter une étape en dessous', expected: [RECEPTION, PRESELECTION, NOUVELLE_SAISIE, ENTRETIEN, REFUS, RECRUTEMENT] },
  ])('adds a new étape from the menu entry $action', async ({ action, expected }) => {
    const sent = updateSpy()
    server.use(etapesOrganismeUpdate(ETAPES, sent))
    const user = await openList()

    await chooseAction(user, PRESELECTION, action)
    await submitName(user, 'Test technique', 'Renommer')

    await vi.waitFor(() => expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, expected))
  })

  it('renames an étape', async () => {
    const sent = updateSpy()
    server.use(etapesOrganismeUpdate(ETAPES_RENAMED, sent))
    const user = await openList()

    await chooseAction(user, PRESELECTION, 'Renommer')
    expect(screen.getByRole('textbox', { name: 'Nom de l\'étape' })).toHaveValue(PRESELECTION.nom)
    await submitName(user, 'Présélection RH', 'Renommer')

    await vi.waitFor(() => expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, ETAPES_RENAMED))
    expect(await screen.findByRole('button', { name: 'Actions pour Présélection RH' })).toBeInTheDocument()
  })

  it('deletes an étape once confirmed and shows the étapes the server answers', async () => {
    const sent = updateSpy()
    server.use(etapesOrganismeUpdate([RECEPTION, ENTRETIEN, REFUS, RECRUTEMENT], sent))
    const user = await openList()

    await chooseAction(user, PRESELECTION, 'Supprimer')
    const dialog = await screen.findByRole('dialog', { name: 'Supprimer l\'étape' })
    expect(dialog).toHaveTextContent('Voulez-vous vraiment supprimer l\'étape « Présélection » ? Cette action est irréversible.')
    await user.click(within(dialog).getByRole('button', { name: 'Supprimer' }))

    await vi.waitFor(() => expect(etapeNames()).toEqual([RECEPTION.nom, ENTRETIEN.nom, REFUS.nom, RECRUTEMENT.nom]))
    expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, [RECEPTION, ENTRETIEN, REFUS, RECRUTEMENT])
  })

  it('moves an étape down by saving the new order', async () => {
    const sent = updateSpy()
    server.use(etapesOrganismeUpdate([RECEPTION, ENTRETIEN, PRESELECTION, REFUS, RECRUTEMENT], sent))
    const user = await openList()

    await chooseAction(user, PRESELECTION, 'Descendre')

    await vi.waitFor(() => expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, [RECEPTION, ENTRETIEN, PRESELECTION, REFUS, RECRUTEMENT]))
    await vi.waitFor(() => expect(etapeNames()).toEqual([RECEPTION.nom, ENTRETIEN.nom, PRESELECTION.nom, REFUS.nom, RECRUTEMENT.nom]))
  })

  it.each([RECEPTION, REFUS])('allows only renaming the étape $nom', async (etape) => {
    const user = await openList()

    await user.click(screen.getByRole('button', { name: `Actions pour ${etape.nom}` }))

    expect(await screen.findByRole('menuitem', { name: 'Renommer' })).not.toHaveAttribute('aria-disabled', 'true')
    for (const action of ['Ajouter une étape au-dessus', 'Ajouter une étape en dessous', 'Monter', 'Descendre', 'Supprimer']) {
      expect(screen.getByRole('menuitem', { name: action })).toHaveAttribute('aria-disabled', 'true')
    }
  })

  it('allows adding above or below, moving up and deleting the last étape in progress, and disables moving it down', async () => {
    const user = await openList()

    await user.click(screen.getByRole('button', { name: `Actions pour ${ENTRETIEN.nom}` }))

    await screen.findByRole('menuitem', { name: 'Renommer' })
    for (const action of ['Ajouter une étape au-dessus', 'Ajouter une étape en dessous', 'Monter', 'Supprimer']) {
      expect(screen.getByRole('menuitem', { name: action })).not.toHaveAttribute('aria-disabled', 'true')
    }
    expect(screen.getByRole('menuitem', { name: 'Descendre' })).toHaveAttribute('aria-disabled', 'true')
  })

  it('resets the étapes once confirmed', async () => {
    const requested = vi.fn()
    server.use(etapesOrganisme(ETAPES.map(etape => ({ ...etape, nom: `${etape.nom} personnalisée` }))), etapesOrganismeInit(ETAPES, requested))
    const user = setupUser()
    await renderWithApp(Host)
    await screen.findByRole('button', { name: 'Actions pour Réception personnalisée' })

    await user.click(screen.getByRole('button', { name: 'Réinitialiser' }))
    const dialog = await screen.findByRole('dialog', { name: 'Réinitialiser les étapes' })
    await user.click(within(dialog).getByRole('button', { name: 'Réinitialiser' }))

    await vi.waitFor(() => expect(etapeNames()).toEqual(ETAPES.map(({ nom }) => nom)))
    expect(requested).toHaveBeenCalledWith(ORGANISME_UUID)
  })

  it('shows an error when saving the étapes fails', async () => {
    server.use(etapesOrganismeUpdateFailure(500))
    const user = await openList()

    await chooseAction(user, PRESELECTION, 'Renommer')
    await submitName(user, 'Présélection RH', 'Renommer')

    expect(await screen.findByRole('heading', { name: 'Erreur' })).toBeInTheDocument()
    expect(screen.getByText('Une erreur est survenue lors du chargement des étapes.')).toBeInTheDocument()
  })
})
