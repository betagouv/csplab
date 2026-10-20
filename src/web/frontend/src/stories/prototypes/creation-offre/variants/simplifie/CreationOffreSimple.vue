<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import type { OffreState, SectionOffreId } from '../../data/types'
import { ref } from 'vue'
import { circuitPour } from '../../data/scenario'
import OffreAppSimple from './OffreAppSimple.vue'

// Racine de la version simplifiée : passage d'une offre à l'autre sans recharger la story.
const props = withDefaults(defineProps<{ preset?: Preset }>(), { preset: 'nouveau' })
const courant = ref<{ key: number, preset: Preset, init?: OffreState }>({ key: 0, preset: props.preset })

function reprendre(preset: Preset) {
  courant.value = { key: courant.value.key + 1, preset }
}

function dupliquer(s: OffreState) {
  const source = s.reference
  Object.assign(s, {
    reference: 'OFF-2026-0145',
    statut: 'brouillon',
    startMode: 'duplication',
    sourceLibelle: `${source} — ${s.besoin.intitule}`,
    circuit: circuitPour(s.organisation),
    remarques: [],
    contributions: [],
    dateDebutDiffusion: '',
    dateLimite: '',
    origines: { 'besoin.intitule': { origine: 'offre', valeur: s.besoin.intitule } },
    journal: [{ date: 'Aujourd\'hui', texte: `Offre dupliquée depuis ${source}` }],
  })
  s.canaux.forEach(c => (c.fait = []))
  s.besoin.darRef = ''
  s.besoin.darStatut = ''
  s.besoin.darApplicable = 'nsp'
  for (const id of Object.keys(s.offre) as SectionOffreId[]) {
    if (s.offre[id].texte) {
      s.offre[id].etat = 'reprise'
    }
  }
  courant.value = { key: courant.value.key + 1, preset: 'nouveau', init: s }
}
</script>

<template>
  <OffreAppSimple
    :key="courant.key"
    :preset="courant.preset"
    :init="courant.init"
    @reprendre="reprendre"
    @dupliquer="dupliquer"
  />
</template>
