import { render, screen } from '@testing-library/vue'
import { describe, expect, it, vi } from 'vitest'
import { useToast } from '@/composables/ui/useToast'
import { setupUser } from '@/test/render'
import CspToaster from './CspToaster.vue'

describe('cspToaster', () => {
  it('runs the toast action and closes the toast', async () => {
    const user = setupUser()
    const onSelect = vi.fn()
    useToast().addToast({ title: 'Élément déplacé', action: { label: 'Annuler', onSelect } })
    render(CspToaster)

    await user.click(await screen.findByRole('button', { name: 'Annuler' }))

    expect(onSelect).toHaveBeenCalledOnce()
    await vi.waitFor(() => expect(screen.queryByRole('heading', { name: 'Élément déplacé' })).not.toBeInTheDocument())
  })
})
