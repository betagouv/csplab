import type { CspColumnDef } from './table'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { defineComponent, h } from 'vue'
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
      'class': 'stub-checkbox',
      'data-checked': String(props.modelValue),
      'data-indeterminate': String(props.indeterminate),
      'aria-label': props.label,
      'onClick': () => emit('update:modelValue', !props.modelValue),
    })
  },
})

const global = { stubs: { CspIcon: CspIconStub, CspCheckbox: CspCheckboxStub } }

function mountTable(props: Record<string, unknown> = {}, options: Record<string, unknown> = {}) {
  return mount(CspDataTable<Row>, {
    props: {
      rows: ROWS,
      columns: COLUMNS,
      rowKey: (r: Row) => r.id,
      caption: 'Tableau',
      ...props,
    },
    global,
    ...options,
  })
}

describe('cspDataTable: rendering', () => {
  it('renders one header per column and one row per item', () => {
    const wrapper = mountTable()
    expect(wrapper.findAll('.csp-table__head .csp-table__th')).toHaveLength(COLUMNS.length)
    expect(wrapper.findAll('.csp-table__body .csp-table__row')).toHaveLength(ROWS.length)
  })

  it('renders the accessor value by default and a dash for empty values', () => {
    const wrapper = mountTable({ rows: [{ id: '1', name: 'Alpha', city: '', count: 0 }] })
    const cells = wrapper.findAll('.csp-table__body .csp-table__td')
    expect(cells[0].text()).toBe('Alpha')
    expect(cells[1].text()).toBe('-')
    expect(cells[2].text()).toBe('0')
  })

  it('lets a cell slot override the default rendering', () => {
    const wrapper = mountTable({}, {
      slots: {
        'cell-name': (slotProps: { value: unknown }) =>
          h('span', { class: 'custom-cell' }, `X-${String(slotProps.value)}`),
      },
    })
    const custom = wrapper.findAll('.custom-cell')
    expect(custom).toHaveLength(ROWS.length)
    expect(custom[0].text()).toBe('X-Alpha')
  })
})

describe('cspDataTable: empty state', () => {
  it('shows the empty label spanning every column when there are no rows', () => {
    const wrapper = mountTable({ rows: [], emptyLabel: 'Rien à afficher' })
    const empty = wrapper.find('.csp-table__empty')
    expect(empty.exists()).toBe(true)
    expect(empty.text()).toBe('Rien à afficher')
    expect(empty.attributes('colspan')).toBe(String(COLUMNS.length))
  })
})

describe('cspDataTable: sorting', () => {
  it('renders a sort control only for sortable columns', () => {
    const wrapper = mountTable()
    expect(wrapper.findAll('.csp-table__sort')).toHaveLength(2)
  })

  it('sorts rows when a sortable header is clicked (asc then desc)', async () => {
    const wrapper = mountTable()
    const nameHeader = wrapper.findAll('.csp-table__head .csp-table__th')[0]

    await wrapper.findAll('.csp-table__sort')[0].trigger('click')
    expect(nameHeader.attributes('aria-sort')).toBe('ascending')

    await wrapper.findAll('.csp-table__sort')[0].trigger('click')
    expect(nameHeader.attributes('aria-sort')).toBe('descending')
    expect(wrapper.findAll('.csp-table__body tr:first-child .csp-table__td')[0].text()).toBe('Charlie')
  })

  it('maps the sort model to aria-sort', () => {
    const wrapper = mountTable({ sort: { id: 'name', desc: false } })
    const headers = wrapper.findAll('.csp-table__head .csp-table__th')
    expect(headers[0].attributes('aria-sort')).toBe('ascending')
    expect(headers[1].attributes('aria-sort')).toBeUndefined()
    expect(headers[2].attributes('aria-sort')).toBe('none')
  })
})

describe('cspDataTable: selection rendering', () => {
  it('renders a checkbox per row plus a header checkbox whenever a selection column is shown', () => {
    const checkbox = mountTable({ selectionMode: 'checkbox', selectedIds: new Set<string>() })
    expect(checkbox.findAll('.stub-checkbox')).toHaveLength(ROWS.length + 1)

    const row = mountTable({ selectionMode: 'row', selectedIds: new Set<string>() })
    expect(row.findAll('.stub-checkbox')).toHaveLength(ROWS.length + 1)
  })

  it('reflects all/indeterminate state on the header checkbox', () => {
    const all = mountTable({ selectionMode: 'checkbox', selectedIds: new Set(['1', '2', '3']) })
    expect(all.find('.csp-table__head .stub-checkbox').attributes('data-checked')).toBe('true')

    const partial = mountTable({ selectionMode: 'checkbox', selectedIds: new Set(['1']) })
    const header = partial.find('.csp-table__head .stub-checkbox')
    expect(header.attributes('data-checked')).toBe('false')
    expect(header.attributes('data-indeterminate')).toBe('true')
  })

  it('emits toggleAll with the visible ids from the header checkbox', async () => {
    const wrapper = mountTable({ selectionMode: 'checkbox', selectedIds: new Set<string>() })
    await wrapper.find('.csp-table__head .stub-checkbox').trigger('click')
    expect(wrapper.emitted('toggleAll')?.[0]).toEqual([['1', '2', '3']])
  })
})

describe('cspDataTable: selection modes', () => {
  it('checkbox mode: only the select cell toggles, not the rest of the row', async () => {
    const wrapper = mountTable({ selectionMode: 'checkbox', selectedIds: new Set<string>() })

    await wrapper.find('.csp-table__body .csp-table__row').trigger('click')
    expect(wrapper.emitted('toggleRow')).toBeUndefined()

    await wrapper.find('.csp-table__body .csp-table__select').trigger('click')
    expect(wrapper.emitted('toggleRow')?.[0]).toEqual(['1'])
  })

  it('row mode: clicking anywhere on the row toggles and reflects aria-selected', async () => {
    const wrapper = mountTable({ selectionMode: 'row', selectedIds: new Set(['1']) })
    const firstRow = wrapper.find('.csp-table__body .csp-table__row')

    expect(firstRow.attributes('aria-selected')).toBe('true')

    await firstRow.trigger('click')
    expect(wrapper.emitted('toggleRow')?.[0]).toEqual(['1'])
  })

  it('none mode: clicking a row never toggles', async () => {
    const wrapper = mountTable({ selectionMode: 'none', selectedIds: new Set<string>() })
    await wrapper.find('.csp-table__body .csp-table__row').trigger('click')
    expect(wrapper.emitted('toggleRow')).toBeUndefined()
  })
})

describe('cspDataTable: activation', () => {
  it('none mode: clicking a row never activates', async () => {
    const wrapper = mountTable({ activationMode: 'none' })
    await wrapper.find('.csp-table__body .csp-table__row').trigger('click')
    expect(wrapper.emitted('activate')).toBeUndefined()
  })

  it('row mode: clicking anywhere on the row activates with its id', async () => {
    const wrapper = mountTable({ activationMode: 'row' })
    await wrapper.find('.csp-table__body .csp-table__row').trigger('click')
    expect(wrapper.emitted('activate')?.[0]).toEqual(['1'])
  })

  it('cell mode: only the slot target activates, not a plain row click', async () => {
    const wrapper = mountTable({ activationMode: 'cell' }, {
      slots: {
        'cell-name': (slotProps: { value: unknown, activate?: () => void }) =>
          h('button', { class: 'cell-open', onClick: slotProps.activate }, String(slotProps.value)),
      },
    })

    await wrapper.find('.csp-table__body .csp-table__row').trigger('click')
    expect(wrapper.emitted('activate')).toBeUndefined()

    await wrapper.find('.cell-open').trigger('click')
    expect(wrapper.emitted('activate')?.[0]).toEqual(['1'])
  })

  it('does not pass an activate helper to cell slots outside cell mode', () => {
    const received: Array<(() => void) | undefined> = []
    mountTable({ activationMode: 'row' }, {
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
    const wrapper = mountTable({
      selectionMode: 'row',
      activationMode: 'row',
      selectedIds: new Set<string>(),
    })
    await wrapper.find('.csp-table__body .csp-table__row').trigger('click')
    expect(wrapper.emitted('activate')).toBeUndefined()
    expect(wrapper.emitted('toggleRow')?.[0]).toEqual(['1'])
  })
})

describe('cspDataTable: pagination', () => {
  it('renders only the rows of the current page', async () => {
    const wrapper = mountTable({ pageSize: 2, page: 1 })
    expect(wrapper.findAll('.csp-table__body .csp-table__row')).toHaveLength(2)

    await wrapper.setProps({ page: 2 })
    expect(wrapper.findAll('.csp-table__body .csp-table__row')).toHaveLength(1)
  })
})
