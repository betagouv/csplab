import { render } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import ElapsedDaysCell from './ElapsedDaysCell.vue'

describe('elapsedDaysCell', () => {
  it.each([null, ''])('shows a dash for the empty value %j', (value) => {
    const { container } = render(ElapsedDaysCell, { props: { value } })

    expect(container.textContent?.trim()).toBe('-')
  })
})
