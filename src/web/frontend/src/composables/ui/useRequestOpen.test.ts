import { describe, expect, it } from 'vitest'
import { createRequest } from './useRequest'
import { useRequestOpen } from './useRequestOpen'

describe('useRequestOpen', () => {
  it('is open while a value is requested', () => {
    const request = createRequest<string>()
    const open = useRequestOpen(request)
    expect(open.value).toBe(false)

    request.request('a')

    expect(open.value).toBe(true)
  })

  it('clears the request once closed', () => {
    const request = createRequest<string>()
    const open = useRequestOpen(request)
    request.request('a')

    open.value = false

    expect(request.requested).toBeNull()
  })
})
