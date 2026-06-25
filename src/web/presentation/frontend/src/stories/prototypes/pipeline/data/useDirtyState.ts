import type { EtapePrototype } from './pipelineMock'
import { computed, ref, toRaw } from 'vue'

// Clone profond de données simples (sérialisables) en contournant les proxies
// réactifs Vue, que structuredClone refuse de cloner.
function clone(items: EtapePrototype[]): EtapePrototype[] {
  return items.map(e => ({ ...toRaw(e) }))
}

// Suit l'écart entre un état persisté (baseline) et l'état en cours d'édition.
// Sert aux prototypes de gestion d'état (commit explicite / hybride).
export function useDirtyState(initial: EtapePrototype[]) {
  const baseline = ref<EtapePrototype[]>(clone(initial))
  const draft = ref<EtapePrototype[]>(clone(initial))

  const isDirty = computed(() =>
    JSON.stringify(baseline.value) !== JSON.stringify(draft.value),
  )

  // Nombre d'étapes ajoutées, supprimées, renommées ou déplacées.
  const changeCount = computed(() => {
    const base = baseline.value
    const next = draft.value
    const baseById = new Map(base.map(e => [e.identifiant, e]))
    const nextById = new Map(next.map(e => [e.identifiant, e]))

    let count = 0
    for (const e of next) {
      const before = baseById.get(e.identifiant)
      if (!before)
        count++ // ajout
      else if (before.nom !== e.nom)
        count++ // renommage
    }
    for (const e of base) {
      if (!nextById.has(e.identifiant))
        count++ // suppression
    }
    // Réordonnancement : compte 1 si l'ordre des étapes communes a changé.
    const commonBase = base.filter(e => nextById.has(e.identifiant)).map(e => e.identifiant)
    const commonNext = next.filter(e => baseById.has(e.identifiant)).map(e => e.identifiant)
    if (JSON.stringify(commonBase) !== JSON.stringify(commonNext))
      count++

    return count
  })

  function commit() {
    baseline.value = clone(draft.value)
  }

  function reset() {
    draft.value = clone(baseline.value)
  }

  return { baseline, draft, isDirty, changeCount, commit, reset }
}
