import type { UpdateEtapeRecrutement } from '../types'
import { screen, within } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { ORGANISME_UUID } from '@/test/fixtures/candidatures'
import { ETAPES, ETAPES_RENAMED, PRESELECTION, RECEPTION } from '@/test/fixtures/etapes-recrutement'
import {
  etapesOrganisme,
  etapesOrganismeInit,
  etapesOrganismeUpdate,
} from '@/test/handlers/etapes-recrutement'
import { renderWithApp, setupUser } from '@/test/render'
import { server } from '@/test/server'
import OrganismeEtapesView from './OrganismeEtapesView.vue'

async function openView() {
  const user = setupUser()
  await renderWithApp(OrganismeEtapesView, { props: { organismeUuid: ORGANISME_UUID } })
  await screen.findByRole('button', { name: `Actions pour ${RECEPTION.nom}` })
  return user
}

describe('organismeEtapesView', () => {
  it('lists the étapes of the organisme', async () => {
    const requested = vi.fn()
    const initialized = vi.fn()
    server.use(etapesOrganisme(ETAPES, requested), etapesOrganismeInit(ETAPES, initialized))
    await openView()

    for (const etape of ETAPES) {
      expect(screen.getByRole('button', { name: `Actions pour ${etape.nom}` })).toBeInTheDocument()
    }
    expect(screen.getByRole('heading', { name: 'Étapes de recrutement' })).toBeInTheDocument()
    expect(screen.getByText('Modifications effectives pour les nouveaux recrutements')).toBeInTheDocument()
    expect(requested).toHaveBeenCalledWith(ORGANISME_UUID)
    expect(initialized).not.toHaveBeenCalled()
  })

  it('initializes the default étapes of an organisme that has none', async () => {
    const initialized = vi.fn()
    server.use(etapesOrganisme([]), etapesOrganismeInit(ETAPES, initialized))
    await openView()

    expect(initialized).toHaveBeenCalledWith(ORGANISME_UUID)
  })

  it('saves a change on the étapes of the organisme', async () => {
    const sent = vi.fn<(organismeUuid: string, payload: UpdateEtapeRecrutement[]) => void>()
    server.use(etapesOrganismeUpdate(ETAPES_RENAMED, sent))
    const user = await openView()

    await user.click(screen.getByRole('button', { name: `Actions pour ${PRESELECTION.nom}` }))
    await user.click(await screen.findByRole('menuitem', { name: 'Renommer' }))
    const dialog = await screen.findByRole('dialog', { name: 'Renommer l\'étape' })
    const input = within(dialog).getByRole('textbox', { name: 'Nom de l\'étape' })
    await user.clear(input)
    await user.type(input, 'Présélection RH')
    await user.click(within(dialog).getByRole('button', { name: 'Renommer' }))

    expect(await screen.findByRole('button', { name: 'Actions pour Présélection RH' })).toBeInTheDocument()
    expect(sent).toHaveBeenCalledWith(ORGANISME_UUID, ETAPES_RENAMED)
  })

  it('resets the étapes of the organisme to the default ones', async () => {
    const requested = vi.fn()
    server.use(etapesOrganisme(ETAPES_RENAMED), etapesOrganismeInit(ETAPES, requested))
    const user = await openView()

    await user.click(screen.getByRole('button', { name: 'Réinitialiser' }))
    await user.click(within(await screen.findByRole('dialog', { name: 'Réinitialiser les étapes' })).getByRole('button', { name: 'Réinitialiser' }))

    expect(await screen.findByRole('button', { name: `Actions pour ${PRESELECTION.nom}` })).toBeInTheDocument()
    expect(requested).toHaveBeenCalledWith(ORGANISME_UUID)
  })
})
