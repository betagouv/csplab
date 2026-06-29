import { describe, expect, it } from 'vitest'
import { useToast } from './useToast'

describe('useToast', () => {
  it('adds a toast with default variant and increments id', () => {
    const { toasts, addToast, dismissToast } = useToast()
    const initialCount = toasts.value.length

    const id = addToast({ title: 'Hello' })
    const added = toasts.value[toasts.value.length - 1]

    expect(added).toMatchObject({ id, title: 'Hello', variant: 'default' })
    expect(toasts.value).toHaveLength(initialCount + 1)

    dismissToast(id)
  })

  it('dismisses the targeted toast', () => {
    const { toasts, addToast, dismissToast } = useToast()

    const idA = addToast({ title: 'A', variant: 'error' })
    const idB = addToast({ title: 'B', variant: 'success' })

    dismissToast(idA)

    expect(toasts.value.find(t => t.id === idA)).toBeUndefined()
    expect(toasts.value.find(t => t.id === idB)).toBeDefined()

    dismissToast(idB)
  })
})
