export interface CspDropdownMenuProps {
  sections: {
    items: {
      label: string
      icon?: string
      disabled?: boolean
      destructive?: boolean
      onSelect?: () => void
    }[]
  }[]
  align?: 'start' | 'center' | 'end'
  side?: 'top' | 'right' | 'bottom' | 'left'
  sideOffset?: number
  sideFlip?: boolean
}
