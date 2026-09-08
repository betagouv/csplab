import type { InjectionKey } from 'vue'
import type { CandidaturePrototype } from './useCandidaturePrototype'
import { inject, provide } from 'vue'

const PROTO_KEY: InjectionKey<CandidaturePrototype> = Symbol('candidature-prototype')

export function provideCandidaturePrototype(proto: CandidaturePrototype): void {
  provide(PROTO_KEY, proto)
}

export function useCandidaturePrototypeContext(): CandidaturePrototype {
  const proto = inject(PROTO_KEY)
  if (!proto)
    throw new Error('useCandidaturePrototypeContext must be used under PrototypeApp')
  return proto
}
