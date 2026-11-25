import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '@/router/names'
import { CANDIDATURE_PARAMS, KANBAN_PATH, NOTE, SECONDE_NOTE } from '@/test/fixtures/candidatures'
import { TAG_INTERVIEW, TAG_SYNTHESIS, TAG_TO_RECALL } from '@/test/fixtures/tags'
import {
  candidatureNotes,
  candidatureNotesFailure,
  noteDeletion,
  noteTagAddition,
  noteTagAdditionFailure,
  noteTagRemoval,
  noteTagRemovalFailure,
  noteUpdate,
  noteVisibiliteUpdate,
} from '@/test/handlers/candidatures'
import { tags } from '@/test/handlers/tags'
import { renderWithApp, setupUser, withToaster } from '@/test/render'
import { server } from '@/test/server'
import CandidatureNotes from './CandidatureNotes.vue'

const NOTES_PATH = `${KANBAN_PATH}/candidatures/${CANDIDATURE_PARAMS.candidatureUuid}/notes`

async function openTagPicker() {
  server.use(tags([TAG_INTERVIEW, TAG_SYNTHESIS, TAG_TO_RECALL]))
  const user = setupUser()
  await renderNotes()
  await user.click(await screen.findByRole('button', { name: 'Actions sur la note de Marie Dupont' }))
  await user.click(await screen.findByRole('menuitem', { name: 'Ajouter une étiquette' }))
  const picker = await screen.findByRole('dialog', { name: 'Ajouter une étiquette' })
  await within(picker).findByRole('list', { name: 'Étiquettes' })
  return { user, picker }
}

const Host = withToaster(CandidatureNotes, { candidature: CANDIDATURE_PARAMS, routes: CANDIDATURE_PANEL_ROUTE_NAMES.kanban.notes })

function renderNotes(route = NOTES_PATH) {
  return renderWithApp(Host, { route })
}

async function chooseNoteAction(user: ReturnType<typeof setupUser>, action: string) {
  await user.click(await screen.findByRole('button', { name: 'Actions sur la note de Paul Bernard' }))
  await user.click(await screen.findByRole('menuitem', { name: action }))
}

describe('candidatureNotes', () => {
  it('lists the notes with their author and publication date', async () => {
    server.use(candidatureNotes([NOTE, SECONDE_NOTE]))
    await renderNotes()

    expect(await screen.findByRole('heading', { name: '2 notes' })).toBeInTheDocument()
    const [premiere, seconde] = screen.getAllByRole('listitem')
    expect(within(premiere).getByText('Marie Dupont')).toBeInTheDocument()
    expect(within(premiere).getByText('Profil solide')).toBeInTheDocument()
    expect(within(premiere).getByText('10/06/2025 à 09h15')).toBeInTheDocument()
    expect(within(seconde).getByText('Paul Bernard')).toBeInTheDocument()
    expect(within(seconde).getByText('À recontacter')).toBeInTheDocument()
  })

  it('says when the candidature has no note', async () => {
    server.use(candidatureNotes([]))
    await renderNotes()

    expect(await screen.findByText('Aucune note sur cette candidature')).toBeInTheDocument()
  })

  it.each([
    { cas: 'with notes', results: [NOTE] },
    { cas: 'without notes', results: [] },
  ])('opens the note form from the button $cas', async ({ results }) => {
    server.use(candidatureNotes(results))
    const user = setupUser()
    const { router } = await renderNotes()

    await user.click(await screen.findByRole('button', { name: 'Ajouter une note' }))

    await vi.waitFor(() => expect(router.currentRoute.value.path).toBe(`${NOTES_PATH}/nouvelle`))
    expect(await screen.findByRole('textbox', { name: 'Nouvelle note' })).toBeInTheDocument()
  })

  it('keeps the notes listed while a new note is typed', async () => {
    server.use(candidatureNotes([SECONDE_NOTE]))
    await renderNotes(`${NOTES_PATH}/nouvelle`)

    expect(await screen.findByRole('textbox', { name: 'Nouvelle note' })).toBeInTheDocument()
    expect(await screen.findByText('À recontacter')).toBeInTheDocument()
  })

  it('shows an error when the notes cannot be loaded', async () => {
    server.use(candidatureNotesFailure(500))
    await renderNotes()

    expect(await screen.findByText('Les notes n\'ont pas pu être chargées.')).toBeInTheDocument()
  })

  it('offers no action on a note the user cannot change', async () => {
    server.use(candidatureNotes([NOTE, { ...SECONDE_NOTE, authorized_actions: [] }]))
    await renderNotes()

    expect(await screen.findByRole('button', { name: 'Actions sur la note de Marie Dupont' })).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Actions sur la note de Paul Bernard' })).not.toBeInTheDocument()
  })

  it('edits the note picked from its menu and keeps it private', async () => {
    const privee = { ...SECONDE_NOTE, est_privee: true }
    const sent = vi.fn()
    server.use(
      candidatureNotes([NOTE, privee]),
      noteUpdate((...args) => {
        sent(...args)
        server.use(candidatureNotes([NOTE, { ...privee, message: 'À recontacter demain' }]))
      }),
    )
    const user = setupUser()
    await renderNotes()

    await chooseNoteAction(user, 'Modifier la note')
    const field = await screen.findByRole('textbox', { name: 'Modifier la note' })
    expect(field).toHaveValue('À recontacter')
    expect(screen.getByRole('checkbox', { name: 'Note privée' })).toBeChecked()

    await user.type(field, ' demain')
    await user.click(screen.getByRole('button', { name: 'Enregistrer les modifications' }))

    expect(await screen.findByText('À recontacter demain')).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(SECONDE_NOTE.uuid, { message: 'À recontacter demain', est_privee: true })
  })

  it('deletes the note picked from its menu once confirmed', async () => {
    const deleted = vi.fn()
    server.use(
      candidatureNotes([NOTE, SECONDE_NOTE]),
      noteDeletion((noteUuid) => {
        deleted(noteUuid)
        server.use(candidatureNotes([NOTE]))
      }),
    )
    const user = setupUser()
    await renderNotes()

    await chooseNoteAction(user, 'Supprimer la note')
    const dialog = await screen.findByRole('dialog', { name: 'Supprimer la note' })
    await user.click(within(dialog).getByRole('button', { name: 'Supprimer la note' }))

    await vi.waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument())
    expect(await screen.findByRole('heading', { name: '1 note' })).toBeInTheDocument()
    expect(deleted).toHaveBeenCalledWith(SECONDE_NOTE.uuid)
  })

  it('makes public the private note picked from its menu', async () => {
    const privee = { ...SECONDE_NOTE, est_privee: true }
    const sent = vi.fn()
    server.use(
      candidatureNotes([NOTE, privee]),
      noteVisibiliteUpdate((...args) => {
        sent(...args)
        server.use(candidatureNotes([NOTE, SECONDE_NOTE]))
      }),
    )
    const user = setupUser()
    await renderNotes()

    await screen.findByText('Privée')
    await chooseNoteAction(user, 'Rendre la note publique')

    await vi.waitFor(() => expect(screen.queryByText('Privée')).not.toBeInTheDocument())
    expect(sent).toHaveBeenCalledWith(SECONDE_NOTE.uuid, { est_privee: false })
  })

  it('adds a note tag from the picker of the note menu and keeps the picker open', async () => {
    const added = vi.fn()
    server.use(
      candidatureNotes([{ ...NOTE, tags: [TAG_INTERVIEW] }]),
      noteTagAddition((...args) => {
        added(...args)
        server.use(candidatureNotes([{ ...NOTE, tags: [TAG_INTERVIEW, TAG_SYNTHESIS] }]))
      }),
    )
    const { user, picker } = await openTagPicker()

    const rows = within(within(picker).getByRole('list', { name: 'Étiquettes' })).getAllByRole('listitem')
    expect(rows.map(row => row.textContent?.trim())).toEqual(['EntretienDéjà ajoutée', 'SynthèseAjouter'])
    expect(within(picker).getByRole('button', { name: 'L\'étiquette Entretien est déjà ajoutée' })).toBeDisabled()

    await user.click(within(picker).getByRole('button', { name: 'Ajouter l\'étiquette Synthèse' }))

    expect(await within(picker).findByRole('button', { name: 'L\'étiquette Synthèse est déjà ajoutée' })).toBeDisabled()
    expect(added).toHaveBeenCalledWith(NOTE.uuid, TAG_SYNTHESIS.uuid)
  })

  it('filters the tags of the picker by name, accents ignored', async () => {
    const { user, picker } = await openTagPicker()

    await user.type(within(picker).getByRole('searchbox', { name: 'Rechercher une étiquette' }), 'synthese')

    await vi.waitFor(() => {
      const rows = within(within(picker).getByRole('list', { name: 'Étiquettes' })).getAllByRole('listitem')
      expect(rows.map(row => row.textContent?.trim())).toEqual(['SynthèseAjouter'])
    })
  })

  it('says when no tag matches the search', async () => {
    const { user, picker } = await openTagPicker()

    await user.type(within(picker).getByRole('searchbox', { name: 'Rechercher une étiquette' }), 'zzz')

    expect(await within(picker).findByText('Aucune étiquette ne correspond.')).toBeInTheDocument()
  })

  it('offers an empty search when the picker is opened again', async () => {
    const { user, picker } = await openTagPicker()

    await user.type(within(picker).getByRole('searchbox', { name: 'Rechercher une étiquette' }), 'synth')
    await user.keyboard('{Escape}')
    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Ajouter une étiquette' })).not.toBeInTheDocument())
    expect(screen.getByRole('button', { name: 'Actions sur la note de Marie Dupont' })).toHaveFocus()

    await user.click(screen.getByRole('button', { name: 'Actions sur la note de Marie Dupont' }))
    await user.click(await screen.findByRole('menuitem', { name: 'Ajouter une étiquette' }))
    const reopened = await screen.findByRole('dialog', { name: 'Ajouter une étiquette' })
    expect(within(reopened).getByRole('searchbox', { name: 'Rechercher une étiquette' })).toHaveValue('')
  })

  it('leaves the focus on the element clicked outside the picker', async () => {
    const { user } = await openTagPicker()

    await user.click(screen.getByText('Profil solide'))

    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Ajouter une étiquette' })).not.toBeInTheDocument())
    expect(screen.getByRole('button', { name: 'Actions sur la note de Marie Dupont' })).not.toHaveFocus()
  })

  it('keeps the picker open when a tag cannot be added', async () => {
    server.use(candidatureNotes([NOTE]), noteTagAdditionFailure(500))
    const { user, picker } = await openTagPicker()

    await user.click(within(picker).getByRole('button', { name: 'Ajouter l\'étiquette Synthèse' }))

    expect(await screen.findByText('L\'ajout de l\'étiquette a échoué')).toBeInTheDocument()
    expect(picker).toBeInTheDocument()
  })

  it('treats a tag already on the note as added', async () => {
    const requested = vi.fn()
    server.use(candidatureNotes([NOTE]), noteTagAdditionFailure(409, requested))
    const { user, picker } = await openTagPicker()

    const button = within(picker).getByRole('button', { name: 'Ajouter l\'étiquette Synthèse' })
    await user.click(button)

    await vi.waitFor(() => expect(requested).toHaveBeenCalledOnce())
    await vi.waitFor(() => expect(button).toBeEnabled())
    expect(screen.queryByText('L\'ajout de l\'étiquette a échoué')).not.toBeInTheDocument()
  })

  it('warns and closes the picker when the tag or the note was deleted meanwhile', async () => {
    server.use(candidatureNotes([NOTE]), noteTagAdditionFailure(404))
    const { user, picker } = await openTagPicker()

    await user.click(within(picker).getByRole('button', { name: 'Ajouter l\'étiquette Synthèse' }))

    expect(await screen.findByText('L\'étiquette ou la note a été supprimée')).toBeInTheDocument()
    await vi.waitFor(() => expect(screen.queryByRole('dialog', { name: 'Ajouter une étiquette' })).not.toBeInTheDocument())
  })

  it('removes a tag from a note the user can change', async () => {
    const removed = vi.fn()
    server.use(
      candidatureNotes([{ ...NOTE, tags: [TAG_INTERVIEW] }]),
      noteTagRemoval((...args) => {
        removed(...args)
        server.use(candidatureNotes([NOTE]))
      }),
    )
    const user = setupUser()
    await renderNotes()

    const tags = await screen.findByRole('list', { name: 'Étiquettes de la note de Marie Dupont' })
    expect(within(tags).getByText('Entretien')).toBeInTheDocument()
    await user.click(within(tags).getByRole('button', { name: 'Retirer l\'étiquette Entretien' }))

    await vi.waitFor(() => expect(screen.queryByRole('list', { name: 'Étiquettes de la note de Marie Dupont' })).not.toBeInTheDocument())
    expect(removed).toHaveBeenCalledWith(NOTE.uuid, TAG_INTERVIEW.uuid)
  })

  it('refreshes the note without a message when its tag was removed meanwhile', async () => {
    server.use(
      candidatureNotes([{ ...NOTE, tags: [TAG_INTERVIEW] }]),
      noteTagRemovalFailure(404, () => server.use(candidatureNotes([NOTE]))),
    )
    const user = setupUser()
    await renderNotes()

    await user.click(await screen.findByRole('button', { name: 'Retirer l\'étiquette Entretien' }))

    await vi.waitFor(() => expect(screen.queryByRole('list', { name: 'Étiquettes de la note de Marie Dupont' })).not.toBeInTheDocument())
    expect(screen.queryByText('Le retrait de l\'étiquette a échoué')).not.toBeInTheDocument()
  })

  it('says when a tag cannot be removed', async () => {
    server.use(candidatureNotes([{ ...NOTE, tags: [TAG_INTERVIEW] }]), noteTagRemovalFailure(500))
    const user = setupUser()
    await renderNotes()

    await user.click(await screen.findByRole('button', { name: 'Retirer l\'étiquette Entretien' }))

    expect(await screen.findByText('Le retrait de l\'étiquette a échoué')).toBeInTheDocument()
  })

  it('shows the tags of a note the user cannot change without a way to remove them', async () => {
    server.use(candidatureNotes([{ ...NOTE, tags: [TAG_INTERVIEW], authorized_actions: [] }]))
    await renderNotes()

    const tags = await screen.findByRole('list', { name: 'Étiquettes de la note de Marie Dupont' })
    expect(within(tags).getByText('Entretien')).toBeInTheDocument()
    expect(within(tags).queryByRole('button')).not.toBeInTheDocument()
  })
})
