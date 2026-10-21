// Navigation de la variante ATS : un petit routeur d'écrans, partagé par provide/inject.

import type { InjectionKey, Ref } from 'vue'
import { inject } from 'vue'

export type Ecran
  = | { nom: 'accueil' }
    | { nom: 'fiches' }
    | { nom: 'fiche', id: string, edition?: boolean }
    | { nom: 'offres', filtre?: string }
    | { nom: 'creation', mode?: 'fiche' | 'fichier' | 'manuel' | 'duplication', ficheId?: string, offreId?: string }
    | { nom: 'offre', id: string, onglet?: 'suivi' | 'redaction' | 'publication' }

export interface Nav {
  ecran: Ref<Ecran>
  aller: (e: Ecran) => void
  notifier: (texte: string) => void
  flash: Ref<string | null>
}

export const NAV: InjectionKey<Nav> = Symbol('nav-ats')

export function useNav(): Nav {
  return inject(NAV)!
}
