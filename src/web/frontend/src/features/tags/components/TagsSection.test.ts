import type { Tag } from '../types'
import { screen, within } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { HttpError } from '@/api/errors'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import { renderWithApp, setupUser } from '@/test/render'
import { createTag, getTags } from '../api'
import TagsSection from './TagsSection.vue'

vi.mock('../api', () => ({
  getTags: vi.fn(),
  createTag: vi.fn(),
}))

const ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'

const TAGS: Tag[] = [
  { uuid: 'aaaaaaaa-0001-0001-0001-000000000001', name: 'À rappeler', category: 'candidature', color: 'bleu', usage_count: 0 },
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
    await user.click(save)

    expect(createTag).toHaveBeenCalledWith(ORGANISME_UUID, { name: 'Synthèse', category: 'note', color: 'bleu' })
    expect(await screen.findByText('Étiquette ajoutée')).toBeInTheDocument()
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
    expect(await within(block('Note')).findByText('2 étiquettes')).toBeInTheDocument()
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
    [409, 'Une étiquette de ce type porte déjà ce libellé.'],
    [500, 'L\'ajout de l\'étiquette a échoué'],
  ])('keeps the drawer open and explains a %i', async (status, message) => {
    vi.mocked(createTag).mockRejectedValue(new HttpError(status, 'Erreur'))
    const user = await openDrawerFrom('Candidature')

    await user.type(screen.getByRole('textbox', { name: /Libellé/ }), 'À rappeler')
    await user.click(screen.getByRole('button', { name: 'Enregistrer' }))

    expect(await screen.findByText(message)).toBeInTheDocument()
    expect(screen.getByRole('dialog')).toBeInTheDocument()
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
