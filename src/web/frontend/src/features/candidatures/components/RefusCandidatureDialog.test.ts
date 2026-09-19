import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { setupUser } from '@/test/render'
import RefusCandidatureDialog from './RefusCandidatureDialog.vue'

const CANDIDAT = { uuid: 'eeeeeeee-0001-0001-0001-000000000001', nom: 'Dupont', prenom: 'Alice' }

describe('refusCandidatureDialog', () => {
  it('names the candidat and emits the choice', async () => {
    const user = setupUser()
    const { emitted } = render(RefusCandidatureDialog, { props: { open: true, candidat: CANDIDAT } })

    const dialog = await screen.findByRole('dialog', { name: 'Refus de candidature' })
    expect(dialog).toHaveTextContent('Vous êtes sur le point de refuser la candidature de Alice Dupont.')

    await user.click(screen.getByRole('button', { name: 'Valider' }))
    await user.click(screen.getByRole('button', { name: 'Annuler' }))

    expect(emitted('confirm')).toHaveLength(1)
    expect(emitted('cancel')).toHaveLength(1)
  })
})
