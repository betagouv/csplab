import type { TagSummary } from '@/features/tags/types'
import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PARAMS } from '@/test/fixtures/candidatures'
import { TAG_INTERVIEW, TAG_SENIOR, TAG_TO_RECALL } from '@/test/fixtures/tags'
import {
  candidatureTagAddition,
  candidatureTagAdditionFailure,
  candidatureTagRemoval,
  candidatureTagRemovalFailure,
} from '@/test/handlers/candidatures'
import { tags } from '@/test/handlers/tags'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import CandidatureEtiquettes from './CandidatureEtiquettes.vue'

function renderEtiquettes(props: { tags: TagSummary[], editable: boolean }) {
  return renderWithApp(withToaster(CandidatureEtiquettes, { candidature: CANDIDATURE_PARAMS, ...props }))
}

async function openPicker(candidatureTags: TagSummary[] = []) {
  const user = setupUser()
  await renderEtiquettes({ tags: candidatureTags, editable: true })
  await user.click(screen.getByRole('button', { name: 'Ajouter une étiquette à la candidature' }))
  const picker = await screen.findByRole('dialog', { name: 'Ajouter une étiquette à la candidature' })
  return { user, picker }
}

describe('candidatureEtiquettes', () => {
  it('offers only the candidature tags of the organisme and adds one in a click', async () => {
    const added = vi.fn()
    server.use(candidatureTagAddition(added))
    const { user, picker } = await openPicker([TAG_TO_RECALL])

    const list = await within(picker).findByRole('list', { name: 'Étiquettes' })
    expect(within(list).getAllByRole('listitem').map(row => row.textContent?.trim())).toEqual(['À rappelerDéjà ajoutée', 'Profil seniorAjouter'])

    await user.click(within(picker).getByRole('button', { name: 'Ajouter l\'étiquette Profil senior' }))

    await vi.waitFor(() => expect(added).toHaveBeenCalledWith(CANDIDATURE_PARAMS.candidatureUuid, TAG_SENIOR.uuid))
  })

  it('says when the organisme has no candidature tag', async () => {
    server.use(tags([TAG_INTERVIEW]))
    const { picker } = await openPicker()

    expect(await within(picker).findByText('Aucune étiquette disponible.')).toBeInTheDocument()
  })

  it('removes a tag without confirmation', async () => {
    const removed = vi.fn()
    server.use(candidatureTagRemoval(removed))
    const user = setupUser()
    await renderEtiquettes({ tags: [TAG_TO_RECALL], editable: true })

    await user.click(screen.getByRole('button', { name: 'Retirer l\'étiquette À rappeler' }))

    await vi.waitFor(() => expect(removed).toHaveBeenCalledWith(CANDIDATURE_PARAMS.candidatureUuid, TAG_TO_RECALL.uuid))
  })

  it('shows the tags without add or remove controls to a user who cannot manage them', async () => {
    await renderEtiquettes({ tags: [TAG_TO_RECALL], editable: false })

    expect(within(screen.getByRole('list', { name: 'Étiquettes de la candidature' })).getByText('À rappeler')).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Ajouter une étiquette à la candidature' })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Retirer l\'étiquette À rappeler' })).not.toBeInTheDocument()
  })

  it('keeps the picker open and says so when a tag cannot be added', async () => {
    server.use(candidatureTagAdditionFailure(500))
    const { user, picker } = await openPicker()

    await user.click(await within(picker).findByRole('button', { name: 'Ajouter l\'étiquette Profil senior' }))

    expect(await screen.findByText('L\'ajout de l\'étiquette a échoué')).toBeInTheDocument()
    expect(picker).toBeInTheDocument()
  })

  it('treats a tag already on the candidature as added', async () => {
    const requested = vi.fn()
    server.use(candidatureTagAdditionFailure(409, requested))
    const { user, picker } = await openPicker()

    const button = await within(picker).findByRole('button', { name: 'Ajouter l\'étiquette Profil senior' })
    await user.click(button)

    await vi.waitFor(() => expect(requested).toHaveBeenCalledOnce())
    await vi.waitFor(() => expect(button).toBeEnabled())
    expect(screen.queryByText('L\'ajout de l\'étiquette a échoué')).not.toBeInTheDocument()
  })

  it('says when a tag cannot be removed', async () => {
    server.use(candidatureTagRemovalFailure(500))
    const user = setupUser()
    await renderEtiquettes({ tags: [TAG_TO_RECALL], editable: true })

    await user.click(screen.getByRole('button', { name: 'Retirer l\'étiquette À rappeler' }))

    expect(await screen.findByText('Le retrait de l\'étiquette a échoué')).toBeInTheDocument()
  })

  it('warns and closes the picker when the tag was deleted meanwhile', async () => {
    server.use(candidatureTagAdditionFailure(404))
    const { user, picker } = await openPicker()

    await user.click(await within(picker).findByRole('button', { name: 'Ajouter l\'étiquette Profil senior' }))

    expect(await screen.findByText('L\'étiquette a été supprimée')).toBeInTheDocument()
    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Ajouter une étiquette à la candidature' })).not.toBeInTheDocument())
  })
})
