import type { EtapeRecrutement } from '../types'
import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { setupUser } from '@/test/render'
import ChangerEtapePopover from './ChangerEtapePopover.vue'

const ETAPES: EtapeRecrutement[] = [
  { etape_uuid: 'reception', nom: 'Réception des candidatures', categorie: 'ENTREE' },
  { etape_uuid: 'entretien', nom: 'Entretien', categorie: 'EN_COURS' },
  { etape_uuid: 'refus', nom: 'Refus', categorie: 'REFUS' },
]

function renderPopover() {
  return render(ChangerEtapePopover, { props: { etapes: ETAPES, currentEtapeUuid: 'reception' } })
}

describe('changerEtapePopover', () => {
  it('emits the chosen stage once validated', async () => {
    const user = setupUser()
    const { emitted } = renderPopover()

    await user.click(screen.getByRole('button', { name: 'Changer d\'étape' }))
    const validate = await screen.findByRole('button', { name: 'Valider' })
    expect(validate).toBeDisabled()
    expect(screen.getByRole('radio', { name: 'Réception des candidatures (étape actuelle)' })).toBeDisabled()

    await user.click(screen.getByRole('radio', { name: 'Entretien' }))
    await user.click(validate)

    expect(emitted('confirm')).toEqual([['entretien']])
    expect(screen.queryByRole('button', { name: 'Valider' })).not.toBeInTheDocument()
  })

  it('forgets the choice when closed without validating', async () => {
    const user = setupUser()
    renderPopover()

    await user.click(screen.getByRole('button', { name: 'Changer d\'étape' }))
    await user.click(await screen.findByRole('radio', { name: 'Refus' }))
    await user.keyboard('{Escape}')
    await user.click(screen.getByRole('button', { name: 'Changer d\'étape' }))

    expect(await screen.findByRole('button', { name: 'Valider' })).toBeDisabled()
  })
})
