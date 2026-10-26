import { screen } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ValidationError } from '@/api/errors'
import { renderWithApp, setupUser } from '@/test/render'
import { createOrganisme, getOrganismesList } from '../api'
import OrganismesSection from './OrganismesSection.vue'

vi.mock('../api', () => ({
  getOrganismesList: vi.fn(),
  createOrganisme: vi.fn(),
  updateOrganisme: vi.fn(),
}))

const SIRET = '11004601800021'
const SIRET_REFUSE = 'Ce SIRET est déjà utilisé ou n\'est pas valide.'

describe('organismesSection', () => {
  beforeEach(() => {
    vi.mocked(getOrganismesList).mockReset().mockResolvedValue([])
    vi.mocked(createOrganisme).mockReset().mockRejectedValue(new ValidationError(400, 'Bad Request', {}, { siret: ['Déjà utilisé'] }))
  })

  it('forgets the refused siret once the drawer is closed', async () => {
    const user = setupUser()
    await renderWithApp(OrganismesSection)

    await user.click(await screen.findByRole('button', { name: 'Ajouter un organisme' }))
    await user.type(await screen.findByRole('textbox', { name: 'Nom de l\'organisme' }), 'Nouvel organisme')
    await user.type(screen.getByRole('textbox', { name: 'SIRET de l\'organisme' }), SIRET)
    await user.click(screen.getByRole('radio', { name: 'Fonction Publique d\'État' }))
    await user.click(screen.getByRole('button', { name: 'Créer l\'organisme' }))
    expect(await screen.findByText(SIRET_REFUSE)).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Annuler' }))
    await user.click(screen.getByRole('button', { name: 'Ajouter un organisme' }))
    const siret = await screen.findByRole('textbox', { name: 'SIRET de l\'organisme' })
    expect(siret).toHaveValue('')
    await user.type(siret, SIRET)

    expect(screen.queryByText(SIRET_REFUSE)).not.toBeInTheDocument()
  })
})
