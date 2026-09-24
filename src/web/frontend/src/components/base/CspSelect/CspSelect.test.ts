import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import CspSelect from './CspSelect.vue'

const OPTIONS = [
  { value: 'a', label: 'Option A' },
  { value: 'b', label: 'Option B' },
]

describe('cspSelect', () => {
  it('names the select with its hint and announces it as required', () => {
    render(CspSelect, { props: { options: OPTIONS, label: 'Libellé', hint: 'Texte d\'aide', required: true } })

    const select = screen.getByRole('combobox', { name: 'Libellé Texte d\'aide' })

    expect(select).toBeRequired()
  })

  it('describes the select with its error message', () => {
    render(CspSelect, { props: { options: OPTIONS, label: 'Libellé', error: true, errorMessage: 'Message d\'erreur' } })

    expect(screen.getByRole('combobox')).toHaveAccessibleDescription('Message d\'erreur')
  })
})
