import type { EtapeRecrutement, UpdateEtapeRecrutement } from '../types'
import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { ORGANISME_UUID, RECRUTEMENT_UUID } from '@/test/fixtures/candidatures'
import { ENTRETIEN, ETAPES, ETAPES_RENAMED, PRESELECTION, RECEPTION, RECRUTEMENT, REFUS } from '@/test/fixtures/etapes-recrutement'
import {
  etapesOffre,
  etapesOffreInit,
  etapesOffreInitFailure,
  etapesOffreUpdate,
  etapesOffreUpdateFailure,
} from '@/test/handlers/etapes-recrutement'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import { ETAPES_TEXTS_OFFRE } from '../constants/etape-recrutement'
import EtapesRecrutementSection from './EtapesRecrutementSection.vue'

const Host = withToaster(EtapesRecrutementSection, {
  params: { type: 'offre', organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID },
  texts: ETAPES_TEXTS_OFFRE,
})

const NOUVELLE: EtapeRecrutement = { uuid: 'ffffffff-0001-0001-0001-000000000006', nom: 'Test technique', categorie: 'EN_COURS' }
const NOUVELLE_SAISIE: UpdateEtapeRecrutement = { nom: 'Test technique', categorie: 'EN_COURS' }

const REFUSAL_REASON = 'L\'étape Entretien ne peut être supprimée car 3 candidatures sont en cours'

function updateSpy() {
  return vi.fn<(organismeUuid: string, recrutementUuid: string, payload: UpdateEtapeRecrutement[]) => void>()
}

function displayedNoms() {
  return screen.getAllByText(/^(Réception|Présélection|Entretien|Test technique|Refus|Recrutement)$/).map(element => element.textContent)
}

async function openSection() {
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

async function confirmDeletion(user: ReturnType<typeof setupUser>, etape: EtapeRecrutement) {
  await chooseAction(user, etape, 'Supprimer')
  const dialog = await screen.findByRole('dialog', { name: 'Supprimer l\'étape' })
  expect(dialog).toHaveTextContent(`Voulez-vous vraiment supprimer l'étape « ${etape.nom} » ? Cette action est irréversible.`)
  await user.click(within(dialog).getByRole('button', { name: 'Supprimer' }))
}

async function confirmReset(user: ReturnType<typeof setupUser>) {
  await user.click(screen.getByRole('button', { name: 'Réinitialiser' }))
  await user.click(within(await screen.findByRole('dialog', { name: 'Réinitialiser les étapes' })).getByRole('button', { name: 'Réinitialiser' }))
}

describe('etapesRecrutementSection', () => {
  it('adds a new étape before the final étapes, with the spaces around its name removed, and closes the dialog', async () => {
    const sent = updateSpy()
    server.use(etapesOffreUpdate([RECEPTION, PRESELECTION, ENTRETIEN, NOUVELLE, REFUS, RECRUTEMENT], sent))
    const user = await openSection()

    await user.click(screen.getByRole('button', { name: 'Ajouter une étape' }))
    await submitName(user, ' Test technique ', 'Ajouter')

    expect(await screen.findByRole('button', { name: `Actions pour ${NOUVELLE.nom}` })).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, [RECEPTION, PRESELECTION, ENTRETIEN, NOUVELLE_SAISIE, REFUS, RECRUTEMENT])
    await vi.waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
  })

  it('adds a new étape at the end when no final étape exists', async () => {
    const sent = updateSpy()
    server.use(etapesOffre([RECEPTION, PRESELECTION]), etapesOffreUpdate([RECEPTION, PRESELECTION, NOUVELLE], sent))
    const user = await openSection()

    await user.click(screen.getByRole('button', { name: 'Ajouter une étape' }))
    await submitName(user, 'Test technique', 'Ajouter')

    await vi.waitFor(() => expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, [RECEPTION, PRESELECTION, NOUVELLE_SAISIE]))
  })

  it.each([
    { action: 'Ajouter une étape au-dessus', expected: [RECEPTION, NOUVELLE_SAISIE, PRESELECTION, ENTRETIEN, REFUS, RECRUTEMENT] },
    { action: 'Ajouter une étape en dessous', expected: [RECEPTION, PRESELECTION, NOUVELLE_SAISIE, ENTRETIEN, REFUS, RECRUTEMENT] },
  ])('adds a new étape from the menu entry $action', async ({ action, expected }) => {
    const sent = updateSpy()
    server.use(etapesOffreUpdate(ETAPES, sent))
    const user = await openSection()

    await chooseAction(user, PRESELECTION, action)
    await submitName(user, 'Test technique', 'Ajouter')

    await vi.waitFor(() => expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, expected))
  })

  it('keeps the dialog open with the typed name when the addition fails', async () => {
    server.use(etapesOffreUpdateFailure(500))
    const user = await openSection()

    await user.click(screen.getByRole('button', { name: 'Ajouter une étape' }))
    await submitName(user, 'Test technique', 'Ajouter')

    expect(await screen.findByRole('heading', { name: 'L\'ajout de l\'étape a échoué', hidden: true })).toBeInTheDocument()
    const dialog = screen.getByRole('dialog', { name: 'Ajouter une étape' })
    expect(within(dialog).getByRole('textbox', { name: 'Nom de l\'étape' })).toHaveValue('Test technique')
    expect(displayedNoms()).toEqual(ETAPES.map(({ nom }) => nom))
  })

  it('renames an étape', async () => {
    const sent = updateSpy()
    server.use(etapesOffreUpdate(ETAPES_RENAMED, sent))
    const user = await openSection()

    await chooseAction(user, PRESELECTION, 'Renommer')
    expect(screen.getByRole('textbox', { name: 'Nom de l\'étape' })).toHaveValue(PRESELECTION.nom)
    await submitName(user, 'Présélection RH', 'Renommer')

    expect(await screen.findByRole('button', { name: 'Actions pour Présélection RH' })).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, ETAPES_RENAMED)
  })

  it('keeps the dialog open with the typed name when renaming fails', async () => {
    server.use(etapesOffreUpdateFailure(500))
    const user = await openSection()

    await chooseAction(user, ENTRETIEN, 'Renommer')
    await submitName(user, 'Entretien RH', 'Renommer')

    expect(await screen.findByRole('heading', { name: 'Le renommage de l\'étape a échoué', hidden: true })).toBeInTheDocument()
    const dialog = screen.getByRole('dialog', { name: 'Renommer l\'étape' })
    expect(within(dialog).getByRole('textbox', { name: 'Nom de l\'étape' })).toHaveValue('Entretien RH')
  })

  it('deletes an étape once confirmed and shows the étapes the server answers', async () => {
    const sent = updateSpy()
    server.use(etapesOffreUpdate([RECEPTION, PRESELECTION, REFUS, RECRUTEMENT], sent))
    const user = await openSection()

    await confirmDeletion(user, ENTRETIEN)

    await vi.waitFor(() => expect(displayedNoms()).toEqual([RECEPTION.nom, PRESELECTION.nom, REFUS.nom, RECRUTEMENT.nom]))
    expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, [RECEPTION, PRESELECTION, REFUS, RECRUTEMENT])
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('keeps the dialog open with the server reason when the deletion is refused', async () => {
    server.use(etapesOffreUpdateFailure(400, { error: REFUSAL_REASON }))
    const user = await openSection()

    await confirmDeletion(user, ENTRETIEN)

    expect(await screen.findByText(REFUSAL_REASON)).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: 'La suppression de l\'étape a échoué', hidden: true })).toBeInTheDocument()
    expect(screen.getByRole('dialog', { name: 'Supprimer l\'étape' })).toBeInTheDocument()
    expect(displayedNoms()).toEqual(ETAPES.map(({ nom }) => nom))
  })

  it('moves an étape down by saving the new order', async () => {
    const sent = updateSpy()
    server.use(etapesOffreUpdate([RECEPTION, ENTRETIEN, PRESELECTION, REFUS, RECRUTEMENT], sent))
    const user = await openSection()

    await chooseAction(user, PRESELECTION, 'Descendre')

    await vi.waitFor(() => expect(displayedNoms()).toEqual([RECEPTION.nom, ENTRETIEN.nom, PRESELECTION.nom, REFUS.nom, RECRUTEMENT.nom]))
    expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, [RECEPTION, ENTRETIEN, PRESELECTION, REFUS, RECRUTEMENT])
  })

  it('keeps the server order with a message when moving an étape fails', async () => {
    server.use(etapesOffreUpdateFailure(500))
    const user = await openSection()

    await chooseAction(user, ENTRETIEN, 'Monter')

    expect(await screen.findByRole('heading', { name: 'Le déplacement de l\'étape a échoué' })).toBeInTheDocument()
    expect(displayedNoms()).toEqual(ETAPES.map(({ nom }) => nom))
  })

  it.each([RECEPTION, REFUS])('allows only renaming the étape $nom', async (etape) => {
    const user = await openSection()

    await user.click(screen.getByRole('button', { name: `Actions pour ${etape.nom}` }))

    expect(await screen.findByRole('menuitem', { name: 'Renommer' })).not.toHaveAttribute('aria-disabled', 'true')
    for (const action of ['Ajouter une étape au-dessus', 'Ajouter une étape en dessous', 'Monter', 'Descendre', 'Supprimer']) {
      expect(screen.getByRole('menuitem', { name: action })).toHaveAttribute('aria-disabled', 'true')
    }
  })

  it('allows adding above or below, moving up and deleting the last étape in progress, and disables moving it down', async () => {
    const user = await openSection()

    await user.click(screen.getByRole('button', { name: `Actions pour ${ENTRETIEN.nom}` }))

    await screen.findByRole('menuitem', { name: 'Renommer' })
    for (const action of ['Ajouter une étape au-dessus', 'Ajouter une étape en dessous', 'Monter', 'Supprimer']) {
      expect(screen.getByRole('menuitem', { name: action })).not.toHaveAttribute('aria-disabled', 'true')
    }
    expect(screen.getByRole('menuitem', { name: 'Descendre' })).toHaveAttribute('aria-disabled', 'true')
  })

  it('resets the étapes once confirmed and closes the dialog', async () => {
    server.use(etapesOffre(ETAPES_RENAMED), etapesOffreInit(ETAPES))
    const user = await openSection()

    await confirmReset(user)

    expect(await screen.findByRole('button', { name: `Actions pour ${PRESELECTION.nom}` })).toBeInTheDocument()
    await vi.waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
  })

  it('keeps the dialog open when the reset fails', async () => {
    server.use(etapesOffreInitFailure(500))
    const user = await openSection()

    await confirmReset(user)

    expect(await screen.findByRole('heading', { name: 'La réinitialisation des étapes a échoué', hidden: true })).toBeInTheDocument()
    expect(screen.getByRole('dialog', { name: 'Réinitialiser les étapes' })).toBeInTheDocument()
    expect(displayedNoms()).toEqual(ETAPES.map(({ nom }) => nom))
  })
})
