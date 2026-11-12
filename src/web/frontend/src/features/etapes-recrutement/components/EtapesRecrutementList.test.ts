import { screen, within } from '@testing-library/vue'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { HttpError, ValidationError } from '@/api/errors'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import { useToast } from '@/composables/ui/useToast'
import { ETAPES_RECRUTEMENT } from '@/test/fixtures/etapes'
import { renderWithApp, setupUser } from '@/test/render'
import { getEtapesOffre, initEtapesOffre, updateEtapesOffre } from '../api'
import { ETAPES_TEXTS_OFFRE } from '../constants/etape-recrutement'
import EtapesRecrutementList from './EtapesRecrutementList.vue'

vi.mock('../api', () => ({
  getEtapesOffre: vi.fn(),
  updateEtapesOffre: vi.fn(),
  initEtapesOffre: vi.fn(),
}))

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000001'
const RECRUTEMENT_UUID = '00000000-0000-0000-0000-000000000002'

const ETAPES = ETAPES_RECRUTEMENT

const REFUSAL_REASON = 'L\'étape cccc ne peut être supprimée car 3 candidatures sont en cours'

const Host = defineComponent({
  setup: () => () => h(CspToaster, null, () => h(EtapesRecrutementList, {
    params: { type: 'offre', organismeUuid: ORGANISME_UUID, recrutementUuid: RECRUTEMENT_UUID },
    texts: ETAPES_TEXTS_OFFRE,
  })),
})

async function render() {
  const user = setupUser()
  await renderWithApp(Host)
  await screen.findByText('Entretien')
  return user
}

async function openDeletion(nom: string) {
  const user = await render()
  await user.click(screen.getByRole('button', { name: `Actions pour ${nom}` }))
  await user.click(await screen.findByRole('menuitem', { name: 'Supprimer' }))
  await user.click(within(screen.getByRole('dialog', { name: 'Supprimer l\'étape' })).getByRole('button', { name: 'Supprimer' }))
  return user
}

async function openReset() {
  const user = await render()
  await user.click(screen.getByRole('button', { name: 'Réinitialiser' }))
  await user.click(within(screen.getByRole('dialog', { name: 'Réinitialiser les étapes' })).getByRole('button', { name: 'Réinitialiser' }))
  return user
}

async function chooseAction(nom: string, action: string) {
  const user = await render()
  await user.click(screen.getByRole('button', { name: `Actions pour ${nom}` }))
  await user.click(await screen.findByRole('menuitem', { name: action }))
  return user
}

function displayedNoms() {
  return screen.getAllByText(/^(Réception|Présélection|Entretien|Refus|Recrutement)$/).map(element => element.textContent)
}

async function addEtape(nom: string) {
  const user = await render()
  await user.click(screen.getByRole('button', { name: 'Ajouter une étape' }))
  const dialog = screen.getByRole('dialog', { name: 'Ajouter une étape' })
  await user.type(within(dialog).getByRole('textbox', { name: 'Nom de l\'étape' }), nom)
  await user.click(within(dialog).getByRole('button', { name: 'Ajouter' }))
  return user
}

describe('etapesRecrutementList', () => {
  beforeEach(() => {
    vi.mocked(getEtapesOffre).mockReset().mockResolvedValue(ETAPES)
    vi.mocked(updateEtapesOffre).mockReset()
    vi.mocked(initEtapesOffre).mockReset()
  })

  afterEach(() => {
    const { toasts, dismissToast } = useToast()
    toasts.value.forEach(toast => dismissToast(toast.id))
  })

  it('deletes an etape and closes the dialog', async () => {
    vi.mocked(updateEtapesOffre).mockResolvedValue(ETAPES.filter(etape => etape.uuid !== 'cccc'))
    await openDeletion('Entretien')

    await vi.waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    expect(screen.queryByText('Entretien')).not.toBeInTheDocument()
  })

  it('keeps the dialog open with the server reason when the deletion is refused', async () => {
    vi.mocked(updateEtapesOffre).mockRejectedValue(
      new ValidationError(400, 'Bad Request', { error: REFUSAL_REASON }, { error: [REFUSAL_REASON] }),
    )
    await openDeletion('Entretien')

    expect(await screen.findByText(REFUSAL_REASON)).toBeInTheDocument()
    expect(screen.getByText('La suppression de l\'étape a échoué')).toBeInTheDocument()
    expect(screen.getByRole('dialog', { name: 'Supprimer l\'étape' })).toBeInTheDocument()
    expect(screen.getByText('Entretien')).toBeInTheDocument()
  })

  it('resets the etapes and closes the dialog', async () => {
    vi.mocked(initEtapesOffre).mockResolvedValue(ETAPES.filter(etape => etape.uuid !== 'cccc'))
    await openReset()

    await vi.waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    expect(screen.queryByText('Entretien')).not.toBeInTheDocument()
  })

  it('keeps the dialog open when the reset fails', async () => {
    vi.mocked(initEtapesOffre).mockRejectedValue(new HttpError(500, 'Internal Server Error'))
    await openReset()

    expect(await screen.findByText('La réinitialisation des étapes a échoué')).toBeInTheDocument()
    expect(screen.getByRole('dialog', { name: 'Réinitialiser les étapes' })).toBeInTheDocument()
    expect(screen.getByText('Entretien')).toBeInTheDocument()
  })

  it('adds an etape and closes the dialog', async () => {
    vi.mocked(updateEtapesOffre).mockResolvedValue([...ETAPES.slice(0, 3), { uuid: 'ffff', nom: 'Test technique', categorie: 'EN_COURS' }, ...ETAPES.slice(3)])
    await addEtape('Test technique')

    await vi.waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    expect(screen.getByText('Test technique')).toBeInTheDocument()
  })

  it('keeps the dialog open with the typed name when the addition fails', async () => {
    vi.mocked(updateEtapesOffre).mockRejectedValue(new HttpError(500, 'Internal Server Error'))
    await addEtape('Test technique')

    expect(await screen.findByText('L\'ajout de l\'étape a échoué')).toBeInTheDocument()
    const dialog = screen.getByRole('dialog', { name: 'Ajouter une étape' })
    expect(within(dialog).getByRole('textbox', { name: 'Nom de l\'étape' })).toHaveValue('Test technique')
    expect(screen.getByText('Entretien')).toBeInTheDocument()
  })

  it('keeps the server order with a message when moving an etape fails', async () => {
    vi.mocked(updateEtapesOffre).mockRejectedValue(new HttpError(500, 'Internal Server Error'))
    await chooseAction('Entretien', 'Monter')

    expect(await screen.findByText('Le déplacement de l\'étape a échoué')).toBeInTheDocument()
    expect(updateEtapesOffre).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, ['aaaa', 'cccc', 'bbbb', 'dddd', 'eeee'].map(uuid => expect.objectContaining({ uuid })))
    expect(displayedNoms()).toEqual(ETAPES.map(etape => etape.nom))
  })

  it('keeps the dialog open with the typed name when renaming fails', async () => {
    vi.mocked(updateEtapesOffre).mockRejectedValue(new HttpError(500, 'Internal Server Error'))
    const user = await chooseAction('Entretien', 'Renommer')
    const dialog = screen.getByRole('dialog', { name: 'Renommer l\'étape' })
    const name = within(dialog).getByRole('textbox', { name: 'Nom de l\'étape' })
    await user.clear(name)
    await user.type(name, 'Entretien RH')
    await user.click(within(dialog).getByRole('button', { name: 'Renommer' }))

    expect(await screen.findByText('Le renommage de l\'étape a échoué')).toBeInTheDocument()
    expect(screen.getByRole('dialog', { name: 'Renommer l\'étape' })).toBeInTheDocument()
    expect(within(dialog).getByRole('textbox', { name: 'Nom de l\'étape' })).toHaveValue('Entretien RH')
  })
})
