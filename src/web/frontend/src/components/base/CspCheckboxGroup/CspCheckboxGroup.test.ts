import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import CspCheckboxGroup from './CspCheckboxGroup.vue'

const OPTIONS = [
  { value: 'a', label: 'Option A' },
  { value: 'b', label: 'Option B' },
]

describe('cspCheckboxGroup', () => {
  it('describes the group with its error message', () => {
    render(CspCheckboxGroup, {
      props: { modelValue: [], options: OPTIONS, label: 'Libellé', error: true, errorMessage: 'Message d\'erreur' },
    })

    expect(screen.getByRole('group')).toHaveAccessibleDescription('Message d\'erreur')
  })
})
