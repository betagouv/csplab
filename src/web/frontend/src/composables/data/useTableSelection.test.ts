import { describe, expect, it } from 'vitest'
import { ref } from 'vue'
import { useTableSelection } from './useTableSelection'

interface Row {
  id: string
  nom: string
}

const ROWS: Row[] = [
  { id: 'a', nom: 'Ministère de l\'Intérieur' },
  { id: 'b', nom: 'Préfecture de Paris' },
  { id: 'c', nom: 'Mairie de Lyon' },
  { id: 'd', nom: 'Conseil départemental du Nord' },
]

const rowKey = (row: Row): string => row.id

describe('useTableSelection', () => {
  it('toggles a row on and off', () => {
    const { toggle, selected, count } = useTableSelection(ROWS, rowKey)

    toggle('a')
    expect(selected.value.map(rowKey)).toEqual(['a'])
    expect(count.value).toBe(1)

    toggle('a')
    expect(count.value).toBe(0)
  })

  it('selects every visible row when some are not selected yet', () => {
    const { toggle, toggleVisible, selectedIds } = useTableSelection(ROWS, rowKey)

    toggle('a')
    toggleVisible(['a', 'b', 'c'])

    expect([...selectedIds.value]).toEqual(['a', 'b', 'c'])
  })

  it('deselects visible rows when they are all selected, leaving the others untouched', () => {
    const { toggle, toggleVisible, selectedIds } = useTableSelection(ROWS, rowKey)

    toggle('d')
    toggleVisible(['a', 'b'])
    toggleVisible(['a', 'b'])

    expect([...selectedIds.value]).toEqual(['d'])
  })

  it('ignores a selected row that left the list', () => {
    const rows = ref(ROWS)
    const { toggle, selected, count } = useTableSelection(rows, rowKey)

    toggle('a')
    toggle('b')
    rows.value = ROWS.filter(row => row.id !== 'b')

    expect(selected.value.map(rowKey)).toEqual(['a'])
    expect(count.value).toBe(1)
  })

  it('clears the selection', () => {
    const { toggleVisible, clear, count } = useTableSelection(ROWS, rowKey)

    toggleVisible(['a', 'b'])
    clear()

    expect(count.value).toBe(0)
  })
})
