import type { InjectionKey } from 'vue'
import { inject, provide } from 'vue'

const CSP_DRAWER_FOOTER_KEY: InjectionKey<string> = Symbol('CspDrawerFooter')

export function provideCspDrawerFooter(footerId: string): void {
  provide(CSP_DRAWER_FOOTER_KEY, footerId)
}

export function useCspDrawerFooter(): string | null {
  return inject(CSP_DRAWER_FOOTER_KEY, null)
}
