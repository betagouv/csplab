import type { InjectionKey } from 'vue'
import type { CspTagSize } from './tag'
import { inject, provide } from 'vue'

export interface CspTagGroupContext {
  size?: CspTagSize
  disabled?: boolean
}

const CSP_TAG_GROUP_KEY: InjectionKey<CspTagGroupContext> = Symbol('CspTagGroup')

export function provideCspTagGroup(context: CspTagGroupContext): void {
  provide(CSP_TAG_GROUP_KEY, context)
}

export function useCspTagGroup(): CspTagGroupContext | null {
  return inject(CSP_TAG_GROUP_KEY, null)
}
