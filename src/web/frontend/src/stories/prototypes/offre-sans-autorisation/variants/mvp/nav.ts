// Navigation du proto « Offres sans autorisation » : un petit routeur d'écrans, partagé par provide/inject.

import type { InjectionKey, Ref } from 'vue'
import { inject } from 'vue'

export type Ecran
  = | { nom: 'offres', filtre?: string }
    | { nom: 'creation', mode?: 'manuel' | 'duplication', offreId?: string }
    | { nom: 'rediger', id: string, etape?: number }
    | { nom: 'offre', id: string, section?: string }
    | { nom: 'publier', id: string }
    | { nom: 'recrutement', id: string }
    | { nom: 'recrutements', onglet?: 'en_cours' | 'clos' }
    | { nom: 'parametres' }

export interface Nav {
  ecran: Ref<Ecran>
  aller: (e: Ecran) => void
  notifier: (texte: string) => void
  flash: Ref<string | null>
}

export const NAV: InjectionKey<Nav> = Symbol('nav-offre-mvp')

export function useNav(): Nav {
  return inject(NAV)!
}
