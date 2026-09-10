import type { InjectionKey } from 'vue'
import type { EquipePrototype } from './useEquipePrototype'
import { inject, provide } from 'vue'

const PROTO_KEY: InjectionKey<EquipePrototype> = Symbol('equipe-prototype')

export function provideEquipePrototype(proto: EquipePrototype): void {
  provide(PROTO_KEY, proto)
}

export function useEquipePrototypeContext(): EquipePrototype {
  const proto = inject(PROTO_KEY)
  if (!proto)
    throw new Error('useEquipePrototypeContext must be used under PrototypeApp')
  return proto
}
