import type { UpdateEtapeRecrutement } from '../types'
import type { RecrutementDetail } from '@/features/recrutements/types'
import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { RouterView } from 'vue-router'
import { KANBAN_PATH, ORGANISME_UUID, RECRUTEMENT_DETAIL, RECRUTEMENT_UUID } from '@/test/fixtures/candidatures'
import { ETAPES, ETAPES_RENAMED, PRESELECTION, RECEPTION } from '@/test/fixtures/etapes-recrutement'
import {
  etapesOffre,
  etapesOffreInit,
  etapesOffreUpdate,
  etapesOrganisme,
} from '@/test/handlers/etapes-recrutement'
import { recrutementDetail } from '@/test/handlers/recrutements'
import { renderWithApp, setupUser } from '@/test/render'
import { server } from '@/test/server'

const ETAPES_PATH = `${KANBAN_PATH}/etapes-recrutement`
const AUTHORIZED: RecrutementDetail = { ...RECRUTEMENT_DETAIL, authorized_actions: ['update_recrutement_etapes'] }

async function openAuthorizedPage() {
  server.use(recrutementDetail(AUTHORIZED))
  const user = setupUser()
  await renderWithApp(RouterView, { route: ETAPES_PATH })
  await screen.findByRole('button', { name: `Actions pour ${RECEPTION.nom}` })
  return user
}

async function renamePreselection(user: ReturnType<typeof setupUser>) {
  await user.click(screen.getByRole('button', { name: `Actions pour ${PRESELECTION.nom}` }))
  await user.click(await screen.findByRole('menuitem', { name: 'Renommer' }))
  const dialog = await screen.findByRole('dialog', { name: 'Renommer l\'étape' })
  const input = within(dialog).getByRole('textbox', { name: 'Nom de l\'étape' })
  await user.clear(input)
  await user.type(input, 'Présélection RH')
  await user.click(within(dialog).getByRole('button', { name: 'Renommer' }))
}

describe('offreEtapesRecrutementView', () => {
  it('loads the recrutement and its own étapes from the address', async () => {
    const offre = vi.fn()
    const organisme = vi.fn()
    server.use(etapesOffre(ETAPES, offre), etapesOrganisme(ETAPES, organisme))
    await openAuthorizedPage()

    expect(await screen.findByRole('link', { name: 'Chargé de mission' })).toBeInTheDocument()
    expect(offre).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID)
    expect(organisme).not.toHaveBeenCalled()
  })

  it('refuses the address without the right to customize the étapes', async () => {
    server.use(recrutementDetail({ ...RECRUTEMENT_DETAIL, authorized_actions: ['get_recrutement'] }))
    await renderWithApp(RouterView, { route: ETAPES_PATH })

    expect(await screen.findByText('Vous n’avez pas accès à cette page.')).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Personnaliser les étapes de ce recrutement' })).not.toBeInTheDocument()
  })

  it('saves the étapes of the recrutement, then reloads the recrutement and keeps the étapes the server answered', async () => {
    const offre = vi.fn()
    const sent = vi.fn<(organismeUuid: string, recrutementUuid: string, payload: UpdateEtapeRecrutement[]) => void>(() => {
      server.use(recrutementDetail({ ...AUTHORIZED, intitule: 'Chargée de mission' }))
    })
    server.use(etapesOffre(ETAPES, offre), etapesOffreUpdate(ETAPES_RENAMED, sent))
    const user = await openAuthorizedPage()

    await renamePreselection(user)

    expect(await screen.findByRole('link', { name: 'Chargée de mission' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Actions pour Présélection RH' })).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID, ETAPES_RENAMED)
    expect(offre).toHaveBeenCalledOnce()
  })

  it('resets the étapes of the recrutement to the model of the organisme, then reloads the recrutement', async () => {
    const requested = vi.fn<(organismeUuid: string, recrutementUuid: string) => void>(() => {
      server.use(recrutementDetail({ ...AUTHORIZED, intitule: 'Chargée de mission' }))
    })
    server.use(etapesOffre(ETAPES_RENAMED), etapesOffreInit(ETAPES, requested))
    const user = await openAuthorizedPage()
    expect(screen.getByRole('button', { name: 'Actions pour Présélection RH' })).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Réinitialiser' }))
    await user.click(within(await screen.findByRole('dialog', { name: 'Réinitialiser les étapes' })).getByRole('button', { name: 'Réinitialiser' }))

    expect(await screen.findByRole('link', { name: 'Chargée de mission' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: `Actions pour ${PRESELECTION.nom}` })).toBeInTheDocument()
    expect(requested).toHaveBeenCalledWith(ORGANISME_UUID, RECRUTEMENT_UUID)
  })
})
