import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import CspInput from './CspInput.vue'

describe('cspInput', () => {
  it('describes the field with its error message', () => {
    render(CspInput, { props: { label: 'Libellé', error: true, errorMessage: 'Message d\'erreur' } })

    expect(screen.getByRole('textbox', { name: 'Libellé' })).toHaveAccessibleDescription('Message d\'erreur')
  })
})
