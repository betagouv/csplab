import { screen, within } from '@testing-library/vue'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ValidationError } from '@/api/errors'
import { TABLE_PAGE_SIZE } from '@/components/base/CspDataTable/table'
import { ORGANISME } from '@/test/fixtures/organismes'
import { renderWithApp, setupUser } from '@/test/render'
import { createOrganisme, getOrganismesPage } from '../api'
import OrganismesSection from './OrganismesSection.vue'

vi.mock('../api', () => ({
  getOrganismesPage: vi.fn(),
  createOrganisme: vi.fn(),
  updateOrganisme: vi.fn(),
}))

const SIRET = '11004601800021'
const ORGANISMES_COUNT = 42

const REJECTED_SIRET_MESSAGE = 'Ce SIRET est déjà utilisé ou n\'est pas valide.'

describe('organismesSection', () => {
  beforeEach(() => {
    vi.mocked(getOrganismesPage).mockReset().mockResolvedValue({ count: 0, results: [] })
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
    expect(await screen.findByText(REJECTED_SIRET_MESSAGE)).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: 'Annuler' }))
    await user.click(screen.getByRole('button', { name: 'Ajouter un organisme' }))
    const siret = await screen.findByRole('textbox', { name: 'SIRET de l\'organisme' })
    expect(siret).toHaveValue('')
    await user.type(siret, SIRET)

    expect(screen.queryByText(REJECTED_SIRET_MESSAGE)).not.toBeInTheDocument()
  })

  it('shows the total count sent by the back and requests the next page', async () => {
    vi.mocked(getOrganismesPage).mockResolvedValue({
      count: ORGANISMES_COUNT,
      results: Array.from({ length: TABLE_PAGE_SIZE }, (_, index) => ({ ...ORGANISME, uuid: `organisme-${index}` })),
    })
    const user = setupUser()
    await renderWithApp(OrganismesSection)

    expect(await screen.findByText(`${ORGANISMES_COUNT} organismes`)).toBeInTheDocument()
    expect(screen.getByText(`Affichage de 1 à ${TABLE_PAGE_SIZE} sur ${ORGANISMES_COUNT}`)).toBeInTheDocument()

    await user.click(within(screen.getByRole('navigation', { name: 'Pagination' })).getByRole('button', { name: 'Page suivante' }))

    expect(getOrganismesPage).toHaveBeenLastCalledWith({ page: 2, filter: undefined })
  })
})
