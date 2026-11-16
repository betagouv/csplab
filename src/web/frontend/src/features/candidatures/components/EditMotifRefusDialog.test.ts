import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { MOTIFS_REFUS } from '@/test/fixtures/candidatures'
import EditMotifRefusDialog from './EditMotifRefusDialog.vue'

describe('editMotifRefusDialog', () => {
  it('preselects the current motif once the motifs are loaded', async () => {
    const { rerender } = render(EditMotifRefusDialog, {
      props: { open: true, currentMotif: 'disponibilite', motifs: [] },
    })

    await rerender({ motifs: MOTIFS_REFUS })
    const select = await screen.findByRole('combobox', { name: /Motif de refus/ })
    expect(select).toHaveTextContent('Disponibilité')
    expect(screen.getByRole('button', { name: 'Enregistrer le motif' })).toBeDisabled()
  })
})
