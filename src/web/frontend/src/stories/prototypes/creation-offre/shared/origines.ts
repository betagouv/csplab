import type { InjectionKey } from 'vue'

/** Fourni à `true` par une variante : les badges « repris de… » n'apparaissent que si la valeur a été modifiée. */
export const ORIGINES_DISCRETES: InjectionKey<boolean> = Symbol('origines-discretes')
