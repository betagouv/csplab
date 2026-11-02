import type { Tag } from '../types'
import { screen, within } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { HttpError } from '@/api/errors'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import { renderWithApp, setupUser } from '@/test/render'
import { createTag, getTags, updateTag } from '../api'
import TagsSection from './TagsSection.vue'

vi.mock('../api', () => ({
  getTags: vi.fn(),
  createTag: vi.fn(),
  updateTag: vi.fn(),
}))

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'

const TO_RECALL: Tag = { uuid: 'aaaaaaaa-0001-0001-0001-000000000001', name: 'À rappeler', category: 'candidature', color: 'bleu', usage_count: 0 }

const TAGS: Tag[] = [
  TO_RECALL,
  { uuid: 'aaaaaaaa-0001-0001-0001-000000000002', name: 'Profil senior', category: 'candidature', color: 'vert', usage_count: 0 },
  { uuid: 'aaaaaaaa-0001-0001-0001-000000000003', name: 'Entretien', category: 'note', color: 'jaune', usage_count: 0 },
]

const CREATED_TAG: Tag = { uuid: 'aaaaaaaa-0001-0001-0001-000000000004', name: 'Synthèse', category: 'note', color: 'bleu', usage_count: 0 }

const Host = defineComponent({
  setup: () => () => h(CspToaster, null, () => h(TagsSection, { organismeUuid: ORGANISME_UUID })),
})

function block(title: string) {
  return screen.getByRole('region', { name: title })
}

async function openEditDrawer(name: string) {
  const user = setupUser()
  await renderWithApp(Host)
  await user.click(await screen.findByRole('button', { name: `Modifier l'étiquette ${name}` }))
  return user
}

async function openDrawerFrom(title: string) {
  const user = setupUser()
  await renderWithApp(Host)
  await user.click(within(await screen.findByRole('region', { name: title })).getByRole('button', { name: 'Ajouter une étiquette' }))
  return user
}

describe('tagsSection', () => {
  beforeEach(() => {
    vi.mocked(getTags).mockReset().mockResolvedValue(TAGS)
    vi.mocked(createTag).mockReset()
    vi.mocked(updateTag).mockReset()
  })

  it('lists the tags of each category', async () => {
    await renderWithApp(Host)

    const candidature = await screen.findByRole('region', { name: 'Candidature' })
    expect(within(candidature).getByText('2 étiquettes')).toBeInTheDocument()
    expect(within(candidature).getAllByRole('listitem').map(item => item.textContent?.trim())).toEqual(['À rappeler', 'Profil senior'])
    expect(within(block('Note')).getByText('1 étiquette')).toBeInTheDocument()
    expect(within(block('Équipe de recrutement de l\'offre')).getByText('Aucune étiquette.')).toBeInTheDocument()
  })

  it('creates a tag in the category of the block', async () => {
    vi.mocked(createTag).mockResolvedValue(CREATED_TAG)
    const user = await openDrawerFrom('Note')
    vi.mocked(getTags).mockResolvedValue([...TAGS, CREATED_TAG])

    const save = screen.getByRole('button', { name: 'Enregistrer' })
    expect(screen.getByRole('radio', { name: 'Note' })).toBeChecked()
    await user.type(screen.getByRole('textbox', { name: /Libellé/ }), '   ')
    expect(save).toBeDisabled()

    await user.type(screen.getByRole('textbox', { name: /Libellé/ }), 'Synthèse ')
    expect(screen.getByRole('radio', { name: 'Bleu' })).toBeChecked()
    await user.click(screen.getByRole('radio', { name: 'Rouge' }))
    await user.click(save)

    expect(createTag).toHaveBeenCalledWith(ORGANISME_UUID, { name: 'Synthèse', category: 'note', color: 'rouge' })
    expect(await screen.findByText('Étiquette ajoutée')).toBeInTheDocument()
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(await within(block('Note')).findByText('2 étiquettes')).toBeInTheDocument()
  })

  it('edits the name and the color of a tag, and keeps its type', async () => {
    vi.mocked(updateTag).mockResolvedValue({ ...TO_RECALL, name: 'À relancer', color: 'rouge' })
    const user = await openEditDrawer('À rappeler')

    const drawer = screen.getByRole('dialog', { name: 'Modifier l\'étiquette' })
    const name = within(drawer).getByRole('textbox', { name: /Libellé/ })
    expect(name).toHaveValue('À rappeler')
    expect(within(drawer).getByText('Candidature')).toBeInTheDocument()
    expect(within(drawer).queryByRole('radio', { name: 'Note' })).not.toBeInTheDocument()
    expect(within(drawer).getByRole('radio', { name: 'Bleu' })).toBeChecked()

    await user.clear(name)
    await user.type(name, 'À relancer')
    await user.click(within(drawer).getByRole('radio', { name: 'Rouge' }))
    await user.click(within(drawer).getByRole('button', { name: 'Enregistrer' }))

    expect(updateTag).toHaveBeenCalledWith(ORGANISME_UUID, TO_RECALL.uuid, { name: 'À relancer', color: 'rouge' })
    expect(await screen.findByText('Étiquette modifiée')).toBeInTheDocument()
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('starts from an empty form each time the drawer opens', async () => {
    const user = await openDrawerFrom('Note')
    await user.type(screen.getByRole('textbox', { name: /Libellé/ }), 'Synthèse')
    await user.click(screen.getByRole('button', { name: 'Annuler' }))

    await user.click(within(block('Candidature')).getByRole('button', { name: 'Ajouter une étiquette' }))

    expect(await screen.findByRole('textbox', { name: /Libellé/ })).toHaveValue('')
    expect(screen.getByRole('radio', { name: 'Candidature' })).toBeChecked()
  })

  it('refuses emojis and angle brackets', async () => {
    const user = await openDrawerFrom('Candidature')

    await user.type(screen.getByRole('textbox', { name: /Libellé/ }), 'Top 👍')

    expect(screen.getByText('Les émojis et les caractères < > ne sont pas autorisés.')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Enregistrer' })).toBeDisabled()
  })

  it.each([
    { mode: 'creating', open: () => openDrawerFrom('Candidature'), status: 409, message: 'Une étiquette de ce type porte déjà ce libellé.' },
    { mode: 'creating', open: () => openDrawerFrom('Candidature'), status: 500, message: 'L\'ajout de l\'étiquette a échoué' },
    { mode: 'editing', open: () => openEditDrawer('Profil senior'), status: 409, message: 'Une étiquette de ce type porte déjà ce libellé.' },
    { mode: 'editing', open: () => openEditDrawer('Profil senior'), status: 500, message: 'La modification de l\'étiquette a échoué' },
  ])('keeps the drawer open and explains a $status while $mode', async ({ open, status, message }) => {
    vi.mocked(createTag).mockRejectedValue(new HttpError(status, 'Erreur'))
    vi.mocked(updateTag).mockRejectedValue(new HttpError(status, 'Erreur'))
    const user = await open()

    const name = screen.getByRole('textbox', { name: /Libellé/ })
    await user.clear(name)
    await user.type(name, 'À rappeler')
    await user.click(screen.getByRole('button', { name: 'Enregistrer' }))

    expect(await screen.findByText(message)).toBeInTheDocument()
    expect(screen.getByRole('dialog')).toBeInTheDocument()
  })

  it('keeps the duplicate error when only the case changes', async () => {
    vi.mocked(createTag).mockRejectedValue(new HttpError(409, 'Conflict'))
    const user = await openDrawerFrom('Candidature')
    const name = screen.getByRole('textbox', { name: /Libellé/ })

    await user.type(name, 'À rappeler')
    await user.click(screen.getByRole('button', { name: 'Enregistrer' }))
    await screen.findByText('Une étiquette de ce type porte déjà ce libellé.')
    await user.clear(name)
    await user.type(name, 'à RAPPELER')

    expect(screen.getByText('Une étiquette de ce type porte déjà ce libellé.')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Enregistrer' })).toBeDisabled()
  })

  it('clears the duplicate error once the type changes', async () => {
    vi.mocked(createTag).mockRejectedValue(new HttpError(409, 'Conflict'))
    const user = await openDrawerFrom('Candidature')

    await user.type(screen.getByRole('textbox', { name: /Libellé/ }), 'À rappeler')
    await user.click(screen.getByRole('button', { name: 'Enregistrer' }))
    await screen.findByText('Une étiquette de ce type porte déjà ce libellé.')
    await user.click(screen.getByRole('radio', { name: 'Note' }))

    expect(screen.queryByText('Une étiquette de ce type porte déjà ce libellé.')).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Enregistrer' })).toBeEnabled()
  })
})
