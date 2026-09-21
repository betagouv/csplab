import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { CANDIDAT_ALICE, CANDIDAT_BRUNO, MOTIFS_REFUS } from '@/test/fixtures/candidatures'
import { setupUser } from '@/test/render'
import RefusCandidatureDialog from './RefusCandidatureDialog.vue'

describe('refusCandidatureDialog', () => {
  it('names the candidat and emits the chosen motif', async () => {
    const user = setupUser()
    const { emitted } = render(RefusCandidatureDialog, {
      props: { open: true, candidats: [CANDIDAT_ALICE], motifs: MOTIFS_REFUS },
    })

    const dialog = await screen.findByRole('dialog', { name: 'Refus de candidature' })
    expect(dialog).toHaveTextContent('Vous êtes sur le point de refuser la candidature de Alice Dupont.')
    expect(screen.getByRole('button', { name: 'Valider le refus' })).toBeDisabled()

    await user.click(screen.getByRole('combobox', { name: 'Motif de refus' }))
    await user.click(await screen.findByRole('option', { name: 'Disponibilité' }))
    await user.click(screen.getByRole('button', { name: 'Valider le refus' }))

    expect(emitted('confirm')).toEqual([['disponibilite']])
  })

  it('counts the candidatures of a batch refusal and cancels without choosing', async () => {
    const user = setupUser()
    const { emitted } = render(RefusCandidatureDialog, {
      props: { open: true, candidats: [CANDIDAT_ALICE, CANDIDAT_BRUNO], motifs: MOTIFS_REFUS },
    })

    expect(await screen.findByRole('dialog')).toHaveTextContent('Vous êtes sur le point de refuser 2 candidatures.')

    await user.click(screen.getByRole('button', { name: 'Annuler' }))

    expect(emitted('cancel')).toHaveLength(1)
    expect(emitted('confirm')).toBeUndefined()
  })

  it('says so when the motifs could not be loaded', async () => {
    render(RefusCandidatureDialog, {
      props: { open: true, candidats: [CANDIDAT_ALICE], motifs: [], motifsUnavailable: true },
    })

    expect(await screen.findByRole('alert')).toHaveTextContent('Les motifs de refus n\'ont pas pu être chargés.')
    expect(screen.getByRole('button', { name: 'Valider le refus' })).toBeDisabled()
  })
})
