// Navigation entre la liste des offres et l'édition d'une offre (racine de la version simplifiée).

import type { InjectionKey } from 'vue'
import { inject, provide } from 'vue'

export interface AppNav {
  /** Revient à la liste ; le brouillon est enregistré avant. */
  quitter: (message?: string) => void
}

const KEY: InjectionKey<AppNav> = Symbol('app')

export function provideApp(nav: AppNav) {
  provide(KEY, nav)
}

export function useApp(): AppNav {
  return inject(KEY, { quitter: () => {} })
}
