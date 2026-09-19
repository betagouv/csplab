import { render, screen } from '@testing-library/vue'
import { afterEach, describe, expect, it, vi } from 'vitest'
import { useToast } from '@/composables/ui/useToast'
import { setupUser } from '@/test/render'
import CspToaster from './CspToaster.vue'

describe('cspToaster', () => {
  afterEach(() => {
    const { toasts, dismissToast } = useToast()
    for (const toast of toasts.value)
      dismissToast(toast.id)
  })

  it('runs the toast action and closes the toast', async () => {
    const user = setupUser()
    const onSelect = vi.fn()
    useToast().addToast({ title: 'Élément déplacé', action: { label: 'Annuler', onSelect } })
    render(CspToaster)

    await user.click(await screen.findByRole('button', { name: 'Annuler' }))

    expect(onSelect).toHaveBeenCalledOnce()
    await vi.waitFor(() => expect(useToast().toasts.value).toHaveLength(0))
  })
})
