// Navigation entre les pages (besoins, offres) et un dossier ouvert.

import type { InjectionKey } from 'vue'
import { inject, provide } from 'vue'

export type Page = 'besoins' | 'offres'

export interface AppNav {
  /** Page d'où l'on vient : sert au fil d'Ariane et au retour. */
  origine: Page
  /** Revient à la page d'origine ; le travail est enregistré avant. */
  quitter: (message?: string) => void
}

const KEY: InjectionKey<AppNav> = Symbol('app')

export function provideApp(nav: AppNav) {
  provide(KEY, nav)
}

export function useApp(): AppNav {
  return inject(KEY, { origine: 'besoins', quitter: () => {} })
}

export const LIBELLES_PAGE: Record<Page, string> = {
  besoins: 'Mes besoins en recrutement',
  offres: 'Mes offres',
}
