import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import CspTextarea from './CspTextarea.vue'

describe('cspTextarea', () => {
  it('describes the field with its error message', () => {
    render(CspTextarea, { props: { label: 'Libellé', error: true, errorMessage: 'Message d\'erreur' } })

    expect(screen.getByRole('textbox', { name: 'Libellé' })).toHaveAccessibleDescription('Message d\'erreur')
  })
})
