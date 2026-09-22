import { describe, expect, it } from 'vitest'
import { createRequest } from './useRequest'

describe('createRequest', () => {
  it('holds the requested value until cleared', () => {
    const request = createRequest<{ id: number }>()
    expect(request.requested).toBeNull()

    request.request({ id: 1 })
    expect(request.requested).toEqual({ id: 1 })

    request.clear()
    expect(request.requested).toBeNull()
  })

  it('keeps every request independent', () => {
    const first = createRequest<string>()
    const second = createRequest<string>()

    first.request('a')

    expect(second.requested).toBeNull()
  })
})
