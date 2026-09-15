import { describe, expect, it } from 'vitest'
import { createRequest } from './useRequest'

describe('createRequest', () => {
  it('holds the requested value until cleared', () => {
    const request = createRequest<{ id: number }>()
    expect(request.value.value).toBeNull()

    request.request({ id: 1 })
    expect(request.value.value).toEqual({ id: 1 })

    request.clear()
    expect(request.value.value).toBeNull()
  })

  it('keeps every request independent', () => {
    const first = createRequest<string>()
    const second = createRequest<string>()

    first.request('a')

    expect(second.value.value).toBeNull()
  })
})
