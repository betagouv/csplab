import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import CspTableToolbar from './CspTableToolbar.vue'

describe('cspTableToolbar', () => {
  it('replaces the count with the selection count', () => {
    render(CspTableToolbar, { props: { count: '12 éléments', selectionCount: 2 } })

    expect(screen.getByText('2 sélectionnés')).toBeInTheDocument()
    expect(screen.queryByText('12 éléments')).not.toBeInTheDocument()
  })

  it('shows the selection hint next to the selection count', () => {
    render(CspTableToolbar, { props: { count: '12 éléments', selectionCount: 2, selectionHint: 'Sélection conservée' } })

    expect(screen.getByText('2 sélectionnés')).toBeInTheDocument()
    expect(screen.getByText('Sélection conservée')).toBeInTheDocument()
    expect(screen.queryByText('12 éléments')).not.toBeInTheDocument()
  })
})
