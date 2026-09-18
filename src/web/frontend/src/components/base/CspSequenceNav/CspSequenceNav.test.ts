import { render, screen } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { setupUser } from '@/test/render'
import CspSequenceNav from './CspSequenceNav.vue'

describe('cspSequenceNav', () => {
  it('announces the position and emits the direction chosen', async () => {
    const user = setupUser()
    const { emitted } = render(CspSequenceNav, { props: { position: 2, total: 4, itemLabel: 'Page' } })

    expect(screen.getByRole('navigation')).toHaveTextContent('Page 2 sur 4')
    await user.click(screen.getByRole('button', { name: 'Précédent' }))
    await user.click(screen.getByRole('button', { name: 'Suivant' }))

    expect(Object.keys(emitted())).toEqual(expect.arrayContaining(['previous', 'next']))
  })

  it('hides the counter and blocks both directions when the position is unknown', () => {
    render(CspSequenceNav, { props: { position: null, total: 4, previousDisabled: true, nextDisabled: true } })

    expect(screen.getByRole('navigation')).not.toHaveTextContent('sur 4')
    expect(screen.getByRole('button', { name: 'Précédent' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Suivant' })).toBeDisabled()
  })
})
