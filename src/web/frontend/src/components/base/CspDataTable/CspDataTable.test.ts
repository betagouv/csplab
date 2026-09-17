import type { CspColumnDef } from './table'
import { render, within } from '@testing-library/vue'
import { describe, expect, it } from 'vitest'
import { defineComponent, h } from 'vue'
import { setupUser } from '@/test/render'
import CspDataTable from './CspDataTable.vue'

interface Row {
  id: string
  name: string
  city: string
  count: number
}

const ROWS: Row[] = [
  { id: '1', name: 'Alpha', city: 'Paris', count: 3 },
  { id: '2', name: 'Bravo', city: 'Lyon', count: 1 },
  { id: '3', name: 'Charlie', city: 'Nantes', count: 2 },
]

const COLUMNS: CspColumnDef<Row>[] = [
  { id: 'name', header: 'Nom', sortable: true, accessor: r => r.name },
  { id: 'city', header: 'Ville', accessor: r => r.city },
  { id: 'count', header: 'Total', sortable: true, align: 'end', accessor: r => r.count },
]

const CspIconStub = defineComponent({
  name: 'CspIcon',
  props: { name: { type: String, required: true } },
  setup: props => () => h('i', { 'class': 'stub-icon', 'data-icon': props.name }),
})

const CspCheckboxStub = defineComponent({
  name: 'CspCheckbox',
  props: {
    label: { type: String, required: true },
    modelValue: { type: Boolean, default: false },
    indeterminate: { type: Boolean, default: false },
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    return () => h('button', {
      'type': 'button',
      'data-checked': String(props.modelValue),
      'data-indeterminate': String(props.indeterminate),
      'aria-label': props.label,
      'onClick': () => emit('update:modelValue', !props.modelValue),
    })
  },
})

const global = { stubs: { CspIcon: CspIconStub, CspCheckbox: CspCheckboxStub } }

function renderTable(props: Record<string, unknown> = {}, options: Record<string, unknown> = {}) {
  const result = render(CspDataTable<Row>, {
    props: { rows: ROWS, columns: COLUMNS, rowKey: (r: Row) => r.id, caption: 'Tableau', ...props },
    global,
    ...options,
  })
  const bodyRows = () => within(result.getAllByRole('rowgroup')[1]!).getAllByRole('row')
  const cellsOf = (row: HTMLElement) => within(row).getAllByRole('cell')
  return { ...result, bodyRows, cellsOf }
}

describe('cspDataTable: rendering', () => {
  it('renders one header per column and one row per item', () => {
    const { getAllByRole, bodyRows } = renderTable()
    expect(getAllByRole('columnheader')).toHaveLength(COLUMNS.length)
    expect(bodyRows()).toHaveLength(ROWS.length)
  })

  it('renders the accessor value by default and a dash for empty values', () => {
    const { bodyRows, cellsOf } = renderTable({ rows: [{ id: '1', name: 'Alpha', city: '', count: 0 }] })
    expect(cellsOf(bodyRows()[0]!).map(cell => cell.textContent)).toEqual(['Alpha', '-', '0'])
  })

  it('lets a cell slot override the default rendering', () => {
    const { getAllByText } = renderTable({}, {
      slots: {
        'cell-name': (slotProps: { value: unknown }) => h('span', `X-${String(slotProps.value)}`),
      },
    })
    expect(getAllByText(/^X-/).map(cell => cell.textContent)).toEqual(['X-Alpha', 'X-Bravo', 'X-Charlie'])
  })
})

describe('cspDataTable: empty state', () => {
  it('shows the empty label spanning every column when there are no rows', () => {
    const { getByRole } = renderTable({ rows: [], emptyLabel: 'Rien à afficher' })
    expect(getByRole('cell', { name: 'Rien à afficher' })).toHaveAttribute('colspan', String(COLUMNS.length))
  })
})

describe('cspDataTable: sorting', () => {
  it('renders a sort control only for sortable columns', () => {
    const { getByRole, queryByRole } = renderTable()
    expect(getByRole('button', { name: 'Nom' })).toBeInTheDocument()
    expect(getByRole('button', { name: 'Total' })).toBeInTheDocument()
    expect(queryByRole('button', { name: 'Ville' })).not.toBeInTheDocument()
  })

  it('sorts rows when a sortable header is clicked (asc then desc)', async () => {
    const user = setupUser()
    const { getByRole, bodyRows, cellsOf } = renderTable()

    await user.click(getByRole('button', { name: 'Nom' }))
    expect(getByRole('columnheader', { name: 'Nom' })).toHaveAttribute('aria-sort', 'ascending')

    await user.click(getByRole('button', { name: 'Nom' }))
    expect(getByRole('columnheader', { name: 'Nom' })).toHaveAttribute('aria-sort', 'descending')
    expect(cellsOf(bodyRows()[0]!)[0]).toHaveTextContent('Charlie')
  })

  it('maps the sort model to aria-sort', () => {
    const { getByRole } = renderTable({ sort: { id: 'name', desc: false } })
    expect(getByRole('columnheader', { name: 'Nom' })).toHaveAttribute('aria-sort', 'ascending')
    expect(getByRole('columnheader', { name: 'Ville' })).not.toHaveAttribute('aria-sort')
    expect(getByRole('columnheader', { name: 'Total' })).toHaveAttribute('aria-sort', 'none')
  })
})

describe('cspDataTable: selection rendering', () => {
  it('renders a checkbox per row plus a header checkbox whenever a selection column is shown', () => {
    const checkbox = renderTable({ selectionMode: 'checkbox', selectedIds: new Set<string>() })
    expect(checkbox.getAllByRole('button', { name: /sélectionner/i })).toHaveLength(ROWS.length + 1)
    checkbox.unmount()

    const row = renderTable({ selectionMode: 'row', selectedIds: new Set<string>() })
    expect(row.getAllByRole('button', { name: /sélectionner/i })).toHaveLength(ROWS.length + 1)
  })

  it('reflects all/indeterminate state on the header checkbox', () => {
    const all = renderTable({ selectionMode: 'checkbox', selectedIds: new Set(['1', '2', '3']) })
    expect(all.getByRole('button', { name: 'Tout sélectionner' })).toHaveAttribute('data-checked', 'true')
    all.unmount()

    const partial = renderTable({ selectionMode: 'checkbox', selectedIds: new Set(['1']) })
    const header = partial.getByRole('button', { name: 'Tout sélectionner' })
    expect(header).toHaveAttribute('data-checked', 'false')
    expect(header).toHaveAttribute('data-indeterminate', 'true')
  })

  it('emits toggleAll with the visible ids from the header checkbox', async () => {
    const user = setupUser()
    const { getByRole, emitted } = renderTable({ selectionMode: 'checkbox', selectedIds: new Set<string>() })

    await user.click(getByRole('button', { name: 'Tout sélectionner' }))

    expect(emitted().toggleAll?.[0]).toEqual([['1', '2', '3']])
  })
})

describe('cspDataTable: selection modes', () => {
  it('checkbox mode: only the select cell toggles, not the rest of the row', async () => {
    const user = setupUser()
    const { bodyRows, cellsOf, emitted } = renderTable({ selectionMode: 'checkbox', selectedIds: new Set<string>() })

    await user.click(cellsOf(bodyRows()[0]!)[1]!)
    expect(emitted().toggleRow).toBeUndefined()

    await user.click(cellsOf(bodyRows()[0]!)[0]!)
    expect(emitted().toggleRow?.[0]).toEqual(['1'])
  })

  it('row mode: clicking anywhere on the row toggles and reflects aria-selected', async () => {
    const user = setupUser()
    const { bodyRows, cellsOf, emitted } = renderTable({ selectionMode: 'row', selectedIds: new Set(['1']) })

    expect(bodyRows()[0]).toHaveAttribute('aria-selected', 'true')

    await user.click(cellsOf(bodyRows()[0]!)[2]!)
    expect(emitted().toggleRow?.[0]).toEqual(['1'])
  })

  it('none mode: clicking a row never toggles', async () => {
    const user = setupUser()
    const { bodyRows, cellsOf, emitted } = renderTable({ selectionMode: 'none', selectedIds: new Set<string>() })

    await user.click(cellsOf(bodyRows()[0]!)[0]!)
    expect(emitted().toggleRow).toBeUndefined()
  })
})

describe('cspDataTable: activation', () => {
  it('none mode: clicking a row never activates', async () => {
    const user = setupUser()
    const { bodyRows, cellsOf, emitted } = renderTable({ activationMode: 'none' })

    await user.click(cellsOf(bodyRows()[0]!)[0]!)
    expect(emitted().activate).toBeUndefined()
  })

  it('row mode: clicking anywhere on the row activates with its id', async () => {
    const user = setupUser()
    const { bodyRows, cellsOf, emitted } = renderTable({ activationMode: 'row' })

    await user.click(cellsOf(bodyRows()[0]!)[1]!)
    expect(emitted().activate?.[0]).toEqual(['1'])
  })

  it('cell mode: only the slot target activates, not a plain row click', async () => {
    const user = setupUser()
    const { bodyRows, cellsOf, getAllByRole, emitted } = renderTable({ activationMode: 'cell' }, {
      slots: {
        'cell-name': (slotProps: { value: unknown, activate?: () => void }) =>
          h('button', { onClick: slotProps.activate }, `Ouvrir ${String(slotProps.value)}`),
      },
    })

    await user.click(cellsOf(bodyRows()[0]!)[1]!)
    expect(emitted().activate).toBeUndefined()

    await user.click(getAllByRole('button', { name: 'Ouvrir Alpha' })[0]!)
    expect(emitted().activate?.[0]).toEqual(['1'])
  })

  it('does not pass an activate helper to cell slots outside cell mode', () => {
    const received: Array<(() => void) | undefined> = []
    renderTable({ activationMode: 'row' }, {
      slots: {
        'cell-name': (slotProps: { activate?: () => void }) => {
          received.push(slotProps.activate)
          return h('span', 'x')
        },
      },
    })
    expect(received.every(fn => fn === undefined)).toBe(true)
  })

  it('row activation is ignored while the row is selectable', async () => {
    const user = setupUser()
    const { bodyRows, cellsOf, emitted } = renderTable({
      selectionMode: 'row',
      activationMode: 'row',
      selectedIds: new Set<string>(),
    })

    await user.click(cellsOf(bodyRows()[0]!)[1]!)
    expect(emitted().activate).toBeUndefined()
    expect(emitted().toggleRow?.[0]).toEqual(['1'])
  })
})

describe('cspDataTable: pagination', () => {
  it('renders only the rows of the current page', async () => {
    const { bodyRows, rerender } = renderTable({ pageSize: 2, page: 1 })
    expect(bodyRows()).toHaveLength(2)

    await rerender({ page: 2 })
    expect(bodyRows()).toHaveLength(1)
  })
})
