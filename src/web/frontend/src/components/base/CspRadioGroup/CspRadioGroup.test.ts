import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import CspRadioGroup from './CspRadioGroup.vue'

const OPTIONS = [
  { value: 'a', label: 'Option A' },
  { value: 'b', label: 'Option B' },
]

describe('cspRadioGroup', () => {
  it('describes the group with its error message', () => {
    render(CspRadioGroup, {
      props: { modelValue: '', options: OPTIONS, label: 'Libellé', error: true, errorMessage: 'Message d\'erreur' },
    })

    expect(screen.getByRole('radiogroup')).toHaveAccessibleDescription('Message d\'erreur')
  })
})
