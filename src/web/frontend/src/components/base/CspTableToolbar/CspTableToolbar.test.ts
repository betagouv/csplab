import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import CspTableToolbar from './CspTableToolbar.vue'

describe('cspTableToolbar', () => {
  it('announces the selection count in a status region', async () => {
    const { rerender } = render(CspTableToolbar, { props: { count: '24 éléments' } })
    expect(screen.getByRole('status')).toHaveTextContent('')

    await rerender({ count: '24 éléments', selectionCount: 3, selectionLabel: '3 éléments sélectionnés' })

    expect(screen.getAllByText('3 éléments sélectionnés')).toHaveLength(2)
    expect(screen.getByRole('status')).toHaveTextContent('3 éléments sélectionnés')
  })
})
