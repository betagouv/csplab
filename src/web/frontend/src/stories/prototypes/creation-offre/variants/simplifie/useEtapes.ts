// Navigation de la version simplifiée : 4 étapes, libres, sans assistant rigide.
// Les règles de complétude viennent du store commun (data/useOffre) ; on les regroupe ici par étape.

import type { InjectionKey, Ref } from 'vue'
import type { StepId } from '../../data/types'
import type { Manque } from '../../data/useOffre'
import { computed, inject, nextTick, provide, ref } from 'vue'
import { useOffre } from '../../data/useOffre'

export type EtapeId = 'poste' | 'offre' | 'candidature' | 'finaliser'

export const ETAPES: { id: EtapeId, libelle: string, court: string }[] = [
  { id: 'poste', libelle: 'Définir le poste', court: 'Poste' },
  { id: 'offre', libelle: 'Rédiger l\'offre', court: 'Offre' },
  { id: 'candidature', libelle: 'Conditions de candidature', court: 'Candidatures' },
  { id: 'finaliser', libelle: 'Vérifier et finaliser', court: 'Finaliser' },
]

/** Correspondance entre les rubriques du modèle de données et les 4 étapes affichées. */
export const ETAPE_DE: Record<StepId, EtapeId> = {
  besoin: 'poste',
  poste: 'poste',
  offre: 'offre',
  conditions: 'candidature',
  evaluation: 'candidature',
  validation: 'finaliser',
  diffusion: 'finaliser',
  recap: 'finaliser',
}

/** Règles du socle désactivées dans cette version : la fiche de poste et les profils deviennent facultatifs. */
export const REGLES_EXCLUES = ['missions', 'profils', 'motif']

interface Nav {
  etape: Ref<EtapeId>
  visitees: Ref<Set<EtapeId>>
  aller: (id: EtapeId | StepId, ancre?: string) => void
}

const KEY: InjectionKey<Nav> = Symbol('etapes')

export function provideEtapes(initiale: EtapeId): Nav {
  const etape = ref<EtapeId>(initiale)
  const visitees = ref(new Set<EtapeId>([initiale]))
  function aller(id: EtapeId | StepId, ancre?: string) {
    const cible = (ETAPES.some(e => e.id === id) ? id : ETAPE_DE[id as StepId]) as EtapeId
    etape.value = cible
    visitees.value.add(cible)
    nextTick(() => {
      const el = ancre ? document.getElementById(ancre) : null
      if (el) {
        el.scrollIntoView({ block: 'start' })
        ;(el.querySelector('input, textarea, button') as HTMLElement | null)?.focus({ preventScroll: true })
      }
      else {
        document.querySelector('.cs-main')?.scrollTo({ top: 0 })
      }
    })
  }
  const nav = { etape, visitees, aller }
  provide(KEY, nav)
  return nav
}

export function useEtapes() {
  const nav = inject(KEY)!
  const store = useOffre()

  /** Ce qui empêche de soumettre / publier, regroupé par étape (le contenu de « finaliser » ne bloque que la publication). */
  function manquesDe(id: EtapeId): Manque[] {
    return store.manques.value.filter(m => ETAPE_DE[m.stepId] === id)
  }

  /** Une étape est cochée quand elle a été ouverte et qu'il n'y manque rien : pas de compteur rouge. */
  function faite(id: EtapeId): boolean {
    if (id === 'finaliser') {
      return ['validee', 'publiee'].includes(store.state.statut)
    }
    return nav.visitees.value.has(id) && manquesDe(id).length === 0
  }

  const index = computed(() => ETAPES.findIndex(e => e.id === nav.etape.value))

  return { ...nav, manquesDe, faite, index }
}
