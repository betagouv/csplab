<script setup lang="ts" generic="TRow">
import type {
  Column,
  Row,
  SortingState,
  Updater,
} from '@tanstack/vue-table'
import type {
  CspColumnDef,
  CspTableAlign,
  CspTableCellValue,
} from './table'
import {
  createColumnHelper,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useVueTable,
} from '@tanstack/vue-table'
import { computed } from 'vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

const props = withDefaults(defineProps<{
  rows: TRow[]
  columns: CspColumnDef<TRow>[]
  rowKey: (row: TRow) => string
  caption: string
  selectionMode?: 'none' | 'checkbox' | 'row'
  selectedIds?: Set<string>
  selectionLabel?: (row: TRow) => string
  size?: 'sm' | 'md' | 'lg'
  pageSize?: number
  manual?: boolean
  rowCount?: number
  emptyLabel?: string
}>(), {
  selectionMode: 'none',
  size: 'md',
  manual: false,
  emptyLabel: 'Aucun résultat',
})

const emit = defineEmits<{
  toggleRow: [id: string]
  toggleAll: [visibleIds: string[]]
}>()
const sort = defineModel<{ id: string, desc: boolean } | null>('sort', { default: null })
const page = defineModel<number>('page', { default: 1 })

const columnHelper = createColumnHelper<TRow>()

const tableColumns = computed(() =>
  props.columns.map(col =>
    columnHelper.accessor((row: TRow) => col.accessor?.(row) ?? '', {
      id: col.id,
      enableSorting: col.sortable ?? false,
      meta: { align: col.align, width: col.width, label: col.header },
    }),
  ),
)

const sortingState = computed<SortingState>(() => (sort.value ? [sort.value] : []))

const effectivePageSize = computed(() => props.pageSize ?? Math.max(props.rows.length, 1))

const paginationState = computed(() => ({
  pageIndex: Math.max(0, (page.value ?? 1) - 1),
  pageSize: effectivePageSize.value,
}))

function resolveUpdater<T>(updater: Updater<T>, previous: T): T {
  return typeof updater === 'function'
    ? (updater as (old: T) => T)(previous)
    : updater
}

const table = useVueTable({
  get data() {
    return props.rows
  },
  get columns() {
    return tableColumns.value
  },
  state: {
    get sorting() {
      return sortingState.value
    },
    get pagination() {
      return paginationState.value
    },
  },
  getRowId: row => props.rowKey(row),
  enableMultiSort: false,
  manualSorting: props.manual,
  manualPagination: props.manual,
  get rowCount() {
    return props.manual ? props.rowCount : undefined
  },
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  onSortingChange: (updater) => {
    const next = resolveUpdater(updater, sortingState.value)
    sort.value = next.length ? { id: next[0].id, desc: next[0].desc } : null
  },
  onPaginationChange: (updater) => {
    const next = resolveUpdater(updater, paginationState.value)
    page.value = next.pageIndex + 1
  },
})

const headers = computed(() => table.getHeaderGroups()[0]?.headers ?? [])
const displayRows = computed(() => table.getRowModel().rows)
const visibleIds = computed(() => displayRows.value.map(row => row.id))
const hasRowSelection = computed(() => props.selectionMode === 'row')
const hasSelectionColumn = computed(() => props.selectionMode !== 'none')
const colspan = computed(() => table.getVisibleLeafColumns().length + (hasSelectionColumn.value ? 1 : 0))

const allVisibleSelected = computed(() => {
  if (!props.selectedIds || visibleIds.value.length === 0) {
    return false
  }
  return visibleIds.value.every(id => props.selectedIds!.has(id))
})

const someVisibleSelected = computed(() => {
  if (!props.selectedIds) {
    return false
  }
  return !allVisibleSelected.value && visibleIds.value.some(id => props.selectedIds!.has(id))
})

const paginationContext = computed(() => {
  const total = props.manual ? (props.rowCount ?? 0) : table.getRowCount()
  const size = effectivePageSize.value
  const current = page.value
  return {
    page: current,
    pageCount: table.getPageCount(),
    pageSize: size,
    total,
    canPrevious: table.getCanPreviousPage(),
    canNext: table.getCanNextPage(),
    range: total === 0
      ? { from: 0, to: 0 }
      : { from: (current - 1) * size + 1, to: Math.min(current * size, total) },
    setPage: (value: number) => table.setPageIndex(value - 1),
    nextPage: () => table.nextPage(),
    previousPage: () => table.previousPage(),
  }
})

function toggleAllVisible(): void {
  emit('toggleAll', visibleIds.value)
}

function toggleRowSelection(id: string): void {
  emit('toggleRow', id)
}

function columnAlign(column: Column<TRow, unknown>): CspTableAlign | undefined {
  return column.columnDef.meta?.align
}

function columnWidth(column: Column<TRow, unknown>): string | undefined {
  return column.columnDef.meta?.width
}

function columnLabel(column: Column<TRow, unknown>): string {
  return column.columnDef.meta?.label ?? column.id
}

function alignClass(align: CspTableAlign | undefined, base: 'th' | 'td'): string | undefined {
  if (!align || align === 'start') {
    return undefined
  }
  return `csp-table__${base}--${align}`
}

function ariaSort(column: Column<TRow, unknown>): 'ascending' | 'descending' | 'none' {
  const direction = column.getIsSorted()
  if (direction === 'asc') {
    return 'ascending'
  }
  if (direction === 'desc') {
    return 'descending'
  }
  return 'none'
}

function sortIconName(column: Column<TRow, unknown>): string {
  const direction = column.getIsSorted()
  if (direction === 'asc') {
    return 'ri:arrow-up-line'
  }
  if (direction === 'desc') {
    return 'ri:arrow-down-line'
  }
  return 'ri:expand-up-down-line'
}

function isRowSelected(row: Row<TRow>): boolean {
  return props.selectedIds?.has(row.id) ?? false
}

function rowSelectionLabel(row: Row<TRow>): string {
  return props.selectionLabel?.(row.original) ?? 'Sélectionner la ligne'
}

function formatValue(value: CspTableCellValue): string {
  if (value === null || value === undefined || value === '') {
    return '-'
  }
  return String(value)
}

function onRowClick(row: Row<TRow>): void {
  if (hasRowSelection.value) {
    emit('toggleRow', row.id)
  }
}
</script>

<template>
  <div
    class="csp-table-wrapper"
    :class="`csp-table-wrapper--${size}`"
  >
    <div
      class="csp-table__scroll"
      tabindex="0"
      role="region"
      :aria-label="caption"
    >
      <table
        class="csp-table"
      >
        <caption class="sr-only csp-table__caption">
          {{ caption }}
        </caption>

        <thead class="csp-table__head">
          <tr>
            <th
              v-if="hasSelectionColumn"
              scope="col"
              class="csp-table__th csp-table__select"
              @click="toggleAllVisible"
            >
              <div
                class="csp-table__checkbox-wrapper"
                @click.stop
              >
                <CspCheckbox
                  variant="checkbox-only"
                  label="Tout sélectionner"
                  :model-value="allVisibleSelected"
                  :indeterminate="someVisibleSelected"
                  @update:model-value="toggleAllVisible"
                />
              </div>
            </th>

            <th
              v-for="header in headers"
              :key="header.id"
              scope="col"
              class="csp-table__th"
              :class="alignClass(columnAlign(header.column), 'th')"
              :aria-sort="header.column.getCanSort() ? ariaSort(header.column) : undefined"
              :style="columnWidth(header.column) ? { width: columnWidth(header.column) } : undefined"
            >
              <slot
                :name="`header-${header.column.id}`"
                :column="header.column"
                :label="columnLabel(header.column)"
                :sorted="header.column.getIsSorted()"
                :can-sort="header.column.getCanSort()"
                :toggle-sort="(event: Event) => header.column.getToggleSortingHandler()?.(event)"
              >
                <button
                  v-if="header.column.getCanSort()"
                  type="button"
                  class="csp-table__sort"
                  @click="header.column.getToggleSortingHandler()?.($event)"
                >
                  <span>{{ columnLabel(header.column) }}</span>
                  <CspIcon
                    class="csp-table__sort-icon"
                    :class="{ 'csp-table__sort-icon--inactive': !header.column.getIsSorted() }"
                    :name="sortIconName(header.column)"
                    :size="14"
                  />
                </button>
                <span v-else>{{ columnLabel(header.column) }}</span>
              </slot>
            </th>
          </tr>
        </thead>

        <tbody class="csp-table__body">
          <tr v-if="displayRows.length === 0">
            <td
              class="csp-table__empty"
              :colspan="colspan"
            >
              <slot name="empty">
                {{ emptyLabel }}
              </slot>
            </td>
          </tr>

          <tr
            v-for="row in displayRows"
            v-else
            :key="row.id"
            class="csp-table__row"
            :class="{
              'csp-table__row--selected': isRowSelected(row),
              'csp-table__row--selectable': hasRowSelection,
            }"
            :aria-selected="hasSelectionColumn ? isRowSelected(row) : undefined"
            @click="onRowClick(row)"
          >
            <td
              v-if="hasSelectionColumn"
              class="csp-table__td csp-table__select"
              @click.stop="toggleRowSelection(row.id)"
            >
              <div
                class="csp-table__checkbox-wrapper"
                @click.stop
              >
                <CspCheckbox
                  variant="checkbox-only"
                  :label="rowSelectionLabel(row)"
                  :model-value="isRowSelected(row)"
                  @update:model-value="() => toggleRowSelection(row.id)"
                />
              </div>
            </td>

            <td
              v-for="cell in row.getVisibleCells()"
              :key="cell.id"
              class="csp-table__td"
              :class="alignClass(columnAlign(cell.column), 'td')"
              :style="columnWidth(cell.column) ? { width: columnWidth(cell.column) } : undefined"
            >
              <slot
                :name="`cell-${cell.column.id}`"
                :row="row.original"
                :value="cell.getValue()"
              >
                {{ formatValue(cell.getValue() as CspTableCellValue) }}
              </slot>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div
      v-if="$slots.footer"
      class="csp-table__footer"
    >
      <slot
        name="footer"
        v-bind="paginationContext"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-table-wrapper {
  width: 100%;
  border: 1px solid var(--border-default-grey);
  overflow: hidden;

  &.csp-table-wrapper--sm {
    --csp-table-row-height: 2rem;
    --csp-table-header-padding: 0.5rem 0.75rem;
    --csp-table-footer-padding: 0.5rem 0.25rem 0.5rem 0.75rem;
    --csp-table-cell-padding: 0.5rem 0.75rem;
  }

  &.csp-table-wrapper--md {
    --csp-table-row-height: 3.25rem;
    --csp-table-header-padding: 0.75rem 0.75rem;
    --csp-table-footer-padding: 0.75rem 0.25rem 0.5rem 0.75rem;
    --csp-table-cell-padding: 0.75rem 0.75rem;
  }

  &.csp-table-wrapper--lg {
    --csp-table-row-height: 4rem;
    --csp-table-header-padding: 0.75rem 1rem;
    --csp-table-footer-padding: 0.75rem 0.25rem 0.75rem 1rem;
    --csp-table-cell-padding: 0.75rem 1rem;
  }
}

.csp-table__scroll {
  width: 100%;
  overflow-x: auto;

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: -2px;
  }
}

.csp-table {
  min-width: 100%;
  table-layout: auto;
  border-collapse: collapse;
  font-size: var(--csp-font-size-base);
}

.csp-table__head {
  background: var(--background-alt-grey);
  border-bottom: 1px solid var(--border-default-grey);
}

.csp-table__th {
  padding: var(--csp-table-header-padding);
  text-align: left;
  font-weight: 600;
  color: var(--text-mention-grey);
  white-space: nowrap;
}

.csp-table__th--center {
  text-align: center;
}

.csp-table__th--end {
  text-align: right;
}

.csp-table__sort {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  padding: 0;
  background: none;
  border: none;
  font: inherit;
  font-weight: 600;
  color: inherit;
  cursor: pointer;

  &:hover {
    color: var(--text-action-high-blue-france);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
    border-radius: 2px;
  }
}

.csp-table__sort-icon {
  flex: 0 0 auto;
  color: var(--text-mention-grey);
}

.csp-table__sort-icon--inactive {
  opacity: 0.4;
}

.csp-table__row {
  height: var(--csp-table-row-height);
  border-bottom: 1px solid var(--border-default-grey);

  &:last-child {
    border-bottom: none;
  }
}

.csp-table__row--selectable {
  cursor: pointer;

  &:hover {
    background: var(--background-alt-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: -2px;
  }
}

.csp-table__row--selected {
  background: var(--background-contrast-blue-france);

  &:hover {
    background: var(--background-contrast-blue-france);
  }
}

.csp-table__td {
  padding: var(--csp-table-cell-padding);
  vertical-align: middle;
  color: var(--text-default-grey);
}

.csp-table__td--center {
  text-align: center;
}

.csp-table__td--end {
  text-align: right;
}

.csp-table__select {
  width: 2.75rem;
  cursor: pointer;
}

.csp-table__checkbox-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.csp-table__empty {
  padding: 2rem 0.75rem;
  text-align: center;
  color: var(--text-mention-grey);
}

.csp-table__footer {
  padding: var(--csp-table-footer-padding);
  border-top: 1px solid var(--border-default-grey);
  background: var(--background-alt-grey);
}
</style>
