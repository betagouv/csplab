import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import CspSelect from './CspSelect.vue'

const OPTIONS = [
  { value: 'a', label: 'Option A' },
  { value: 'b', label: 'Option B' },
]

describe('cspSelect', () => {
  it('describes the select with its hint and announces it as required', () => {
    render(CspSelect, { props: { options: OPTIONS, label: 'Libellé', hint: 'Texte d\'aide', required: true } })

    const select = screen.getByRole('combobox', { name: 'Libellé' })

    expect(select).toHaveAccessibleDescription('Texte d\'aide')
    expect(select).toBeRequired()
  })
})
