import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import BadgeCell from './BadgeCell.vue'

describe('badgeCell', () => {
  it('shows zero in a badge', () => {
    render(BadgeCell, { props: { value: 0 } })

    expect(screen.getByText('0')).toBeInTheDocument()
  })
})
