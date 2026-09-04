export type CspTagSize = 'sm' | 'md' | 'lg'

export type CspTagVariant = 'static' | 'clickable' | 'selectable' | 'dismissible'

export type CspTagRootKind = 'p' | 'a' | 'button' | 'toggle' | 'toggle-group-item'

export interface ResolveTagRootInput {
  variant: CspTagVariant
  inGroup: boolean
  disabled: boolean
  hasHref: boolean
}

export function resolveTagRoot(input: ResolveTagRootInput): CspTagRootKind {
  switch (input.variant) {
    case 'selectable':
      return input.inGroup ? 'toggle-group-item' : 'toggle'
    case 'clickable':
      return input.hasHref && !input.disabled ? 'a' : 'button'
    case 'dismissible':
      return 'button'
    case 'static':
      return 'p'
    default:
      return 'p'
  }
}

export function resolveDismissAriaLabel(
  explicitLabel: string | undefined,
  label: string | undefined,
): string | undefined {
  if (explicitLabel) {
    return explicitLabel
  }
  return label ? `Retirer le filtre ${label}` : undefined
}
