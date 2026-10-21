// Navigation entre les espaces (fiches de poste, recrutements, offres), une fiche et un recrutement ouvert.

import type { InjectionKey } from 'vue'
import { inject, provide } from 'vue'

export type Page = 'fiches' | 'recrutements' | 'offres'

export interface AppNav {
  /** Espace d'où l'on vient : sert au fil d'Ariane et au retour. */
  origine: Page
  /** Revient à l'espace d'origine ; le travail est enregistré avant. */
  quitter: (message?: string) => void
  /** Ouvre la fiche de poste d'un recrutement (le travail est enregistré avant). */
  ouvrirFiche: (id: string) => void
}

const KEY: InjectionKey<AppNav> = Symbol('app')

export function provideApp(nav: AppNav) {
  provide(KEY, nav)
}

export function useApp(): AppNav {
  return inject(KEY, { origine: 'fiches', quitter: () => {}, ouvrirFiche: () => {} })
}

export const LIBELLES_PAGE: Record<Page, string> = {
  fiches: 'Fiches de poste',
  recrutements: 'Recrutements',
  offres: 'Mes offres',
}
