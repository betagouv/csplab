import { describe, expect, it } from 'vitest'
import { labelOptions } from './options'

describe('labelOptions', () => {
  it('builds one option per label, in declaration order', () => {
    expect(labelOptions({ a: 'Libellé A', b: 'Libellé B' })).toEqual([
      { value: 'a', label: 'Libellé A' },
      { value: 'b', label: 'Libellé B' },
    ])
  })
})
