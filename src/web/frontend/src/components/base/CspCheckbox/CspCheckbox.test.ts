import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import CspCheckbox from './CspCheckbox.vue'

describe('cspCheckbox', () => {
  it('announces its hint as a description rather than as part of its name', () => {
    render(CspCheckbox, { props: { label: 'Note privée', hint: 'Visible par vous uniquement' } })

    const checkbox = screen.getByRole('checkbox', { name: 'Note privée' })
    expect(checkbox).toHaveAccessibleDescription('Visible par vous uniquement')
  })
})
