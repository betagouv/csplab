// Navigation de la variante ATS : un petit routeur d'écrans, partagé par provide/inject.

import type { InjectionKey, Ref } from 'vue'
import type { EtapeFormulaire } from './aide'
import { inject } from 'vue'

export type Ecran
  = | { nom: 'accueil' }
    | { nom: 'fiches' }
    | { nom: 'fiche', id: string, edition?: boolean }
    | { nom: 'offres', filtre?: string }
    | { nom: 'recrutements', onglet?: 'en_cours' | 'clos' }
    | { nom: 'creation', mode?: 'fiche' | 'manuel' | 'duplication', ficheId?: string, offreId?: string }
    | { nom: 'offre', id: string }
    | { nom: 'formulaire', id: string, etape?: EtapeFormulaire }
    | { nom: 'apercu', id: string, publier?: boolean }
    | { nom: 'parametres' }

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
