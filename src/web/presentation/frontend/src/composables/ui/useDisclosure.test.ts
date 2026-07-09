import { describe, expect, it } from 'vitest'
import { useDisclosure } from './useDisclosure'

describe('useDisclosure', () => {
  it('starts closed by default and honors initial state', () => {
    expect(useDisclosure().isOpen.value).toBe(false)
    expect(useDisclosure(true).isOpen.value).toBe(true)
  })

  it('opens, closes and toggles', () => {
    const { isOpen, open, close, toggle } = useDisclosure()
    open()
    expect(isOpen.value).toBe(true)
    close()
    expect(isOpen.value).toBe(false)
    toggle()
    expect(isOpen.value).toBe(true)
  })
})
