import type { RowData } from '@tanstack/vue-table'
import type { Component } from 'vue'

export type CspTableAlign = 'start' | 'center' | 'end'

export type CspTableCellValue = string | number | null | undefined

export interface CspColumnDef<TRow> {
  id: string
  header: string
  sortable?: boolean
  align?: CspTableAlign
  width?: string
  accessor?: (row: TRow) => CspTableCellValue
  cellComponent?: Component
}

declare module '@tanstack/vue-table' {
  interface ColumnMeta<TData extends RowData, TValue> {
    _row?: TData
    _value?: TValue
    align?: CspTableAlign
    width?: string
    label?: string
    cellComponent?: Component
  }
}
