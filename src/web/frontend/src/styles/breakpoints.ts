export const BREAKPOINTS = {
  sm: '36em',
  md: '48em',
  lg: '62em',
  xl: '78em',
} as const

export type Breakpoint = keyof typeof BREAKPOINTS

export function from(breakpoint: Breakpoint): string {
  return `(width >= ${BREAKPOINTS[breakpoint]})`
}

export function below(breakpoint: Breakpoint): string {
  return `(width < ${BREAKPOINTS[breakpoint]})`
}
