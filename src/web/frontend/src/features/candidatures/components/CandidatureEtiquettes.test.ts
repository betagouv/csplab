import type { TagSummary } from '@/features/tags/types'
import { screen, within } from '@testing-library/vue'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { defineComponent, h } from 'vue'
import { HttpError } from '@/api/errors'
import CspToaster from '@/components/base/CspToast/CspToaster.vue'
import { useToast } from '@/composables/ui/useToast'
import { getTags } from '@/features/tags/api'
import { CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { TAG_INTERVIEW, TAG_SENIOR, TAG_TO_RECALL, TAGS } from '@/test/fixtures/tags'
import { renderWithApp, setupUser } from '@/test/render'
import { addCandidatureTag, removeCandidatureTag } from '../api'
import CandidatureEtiquettes from './CandidatureEtiquettes.vue'

vi.mock('../api', async importOriginal => ({
  ...await importOriginal<typeof import('../api')>(),
  addCandidatureTag: vi.fn(),
  removeCandidatureTag: vi.fn(),
}))

vi.mock('@/features/tags/api', () => ({
  getTags: vi.fn(),
}))

function renderEtiquettes(props: { tags: TagSummary[], editable: boolean }) {
  const Host = defineComponent({
    setup: () => () => h(CspToaster, null, () => h(CandidatureEtiquettes, { candidature: CANDIDATURE_PARAMS, ...props })),
  })
  return renderWithApp(Host)
}

async function openPicker(tags: TagSummary[] = []) {
  const user = setupUser()
  await renderEtiquettes({ tags, editable: true })
  await user.click(screen.getByRole('button', { name: 'Ajouter une étiquette à la candidature' }))
  const picker = await screen.findByRole('dialog', { name: 'Ajouter une étiquette à la candidature' })
  return { user, picker }
}

describe('candidatureEtiquettes', () => {
  afterEach(() => {
    vi.clearAllMocks()
    const { toasts, dismissToast } = useToast()
    toasts.value.forEach(toast => dismissToast(toast.id))
  })

  it('offers only the candidature tags of the organisme and adds one in a click', async () => {
    vi.mocked(getTags).mockResolvedValue(TAGS)
    vi.mocked(addCandidatureTag).mockResolvedValue()
    const { user, picker } = await openPicker([TAG_TO_RECALL])

    const list = await within(picker).findByRole('list', { name: 'Étiquettes' })
    expect(within(list).getAllByRole('listitem').map(row => row.textContent?.trim())).toEqual(['À rappelerDéjà ajoutée', 'Profil seniorAjouter'])

    await user.click(within(picker).getByRole('button', { name: 'Ajouter l\'étiquette Profil senior' }))

    expect(addCandidatureTag).toHaveBeenCalledWith({ ...CANDIDATURE_PARAMS, tagUuid: TAG_SENIOR.uuid })
  })

  it('says when the organisme has no candidature tag', async () => {
    vi.mocked(getTags).mockResolvedValue([TAG_INTERVIEW])
    const { picker } = await openPicker()

    expect(await within(picker).findByText('Aucune étiquette disponible.')).toBeInTheDocument()
  })

  it('removes a tag without confirmation', async () => {
    vi.mocked(removeCandidatureTag).mockResolvedValue()
    const user = setupUser()
    await renderEtiquettes({ tags: [TAG_TO_RECALL], editable: true })

    await user.click(screen.getByRole('button', { name: 'Retirer l\'étiquette À rappeler' }))

    expect(removeCandidatureTag).toHaveBeenCalledWith({ ...CANDIDATURE_PARAMS, tagUuid: TAG_TO_RECALL.uuid })
  })

  it('shows the tags without add or remove controls to a user who cannot manage them', async () => {
    await renderEtiquettes({ tags: [TAG_TO_RECALL], editable: false })

    expect(within(screen.getByRole('list', { name: 'Étiquettes de la candidature' })).getByText('À rappeler')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Ajouter une étiquette à la candidature' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Retirer l\'étiquette À rappeler' })).not.toBeInTheDocument()
  })

  it('keeps the picker open and says so when a tag cannot be added', async () => {
    vi.mocked(getTags).mockResolvedValue(TAGS)
    vi.mocked(addCandidatureTag).mockRejectedValue(new HttpError(500, 'Internal Server Error', undefined))
    const { user, picker } = await openPicker()

    await user.click(await within(picker).findByRole('button', { name: 'Ajouter l\'étiquette Profil senior' }))

    expect(await screen.findByText('L\'ajout de l\'étiquette a échoué')).toBeInTheDocument()
    expect(picker).toBeInTheDocument()
  })

  it('treats a tag already on the candidature as added', async () => {
    vi.mocked(getTags).mockResolvedValue(TAGS)
    vi.mocked(addCandidatureTag).mockRejectedValue(new HttpError(409, 'Conflict', undefined))
    const { user, picker } = await openPicker()

    await user.click(await within(picker).findByRole('button', { name: 'Ajouter l\'étiquette Profil senior' }))

    await vi.waitFor(() => expect(addCandidatureTag).toHaveBeenCalledOnce())
    expect(screen.queryByText('L\'ajout de l\'étiquette a échoué')).not.toBeInTheDocument()
  })

  it('says when a tag cannot be removed', async () => {
    vi.mocked(removeCandidatureTag).mockRejectedValue(new HttpError(500, 'Internal Server Error', undefined))
    const user = setupUser()
    await renderEtiquettes({ tags: [TAG_TO_RECALL], editable: true })

    await user.click(screen.getByRole('button', { name: 'Retirer l\'étiquette À rappeler' }))

    expect(await screen.findByText('Le retrait de l\'étiquette a échoué')).toBeInTheDocument()
  })

  it('warns and closes the picker when the tag was deleted meanwhile', async () => {
    vi.mocked(getTags).mockResolvedValue(TAGS)
    vi.mocked(addCandidatureTag).mockRejectedValue(new HttpError(404, 'Not Found', undefined))
    const { user, picker } = await openPicker()

    await user.click(await within(picker).findByRole('button', { name: 'Ajouter l\'étiquette Profil senior' }))

    expect(await screen.findByText('L\'étiquette a été supprimée')).toBeInTheDocument()
    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Ajouter une étiquette à la candidature' })).not.toBeInTheDocument())
  })
})
