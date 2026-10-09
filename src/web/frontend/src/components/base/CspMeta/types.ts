export interface CspMetaCopy {
  action: string
  confirmation: string
}

export interface CspMetaItem {
  label: string
  icon?: string
  srLabel: string
  copy?: CspMetaCopy
}
