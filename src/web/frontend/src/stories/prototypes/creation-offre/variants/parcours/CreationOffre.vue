<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import type { OffreState, SectionOffreId } from '../../data/types'
import { ref } from 'vue'
import { circuitPour } from '../../data/scenario'
import OffreApp from './OffreApp.vue'

// Racine du prototype : permet de passer d'une offre à l'autre (reprise d'un brouillon,
// duplication d'une offre publiée) sans recharger la story.
const props = withDefaults(defineProps<{ preset?: Preset }>(), { preset: 'nouveau' })

const courant = ref<{ key: number, preset: Preset, init?: OffreState, initStep?: 'besoin' }>({ key: 0, preset: props.preset })

function reprendre(preset: Preset) {
  courant.value = { key: courant.value.key + 1, preset }
}

function dupliquer(source: OffreState) {
  const s = source
  const ref0 = s.reference
  s.reference = 'OFF-2026-0145'
  s.statut = 'brouillon'
  s.startMode = 'duplication'
  s.sourceLibelle = `${ref0} — ${s.besoin.intitule}`
  s.circuit = circuitPour(s.organisation)
  s.remarques = []
  s.contributions = []
  s.dateDebutDiffusion = ''
  s.dateLimite = ''
  s.canaux.forEach(c => (c.fait = []))
  s.besoin.darRef = ''
  s.besoin.darStatut = ''
  s.origines = {}
  for (const id of Object.keys(s.offre) as SectionOffreId[]) {
    if (s.offre[id].texte) {
      s.offre[id].etat = 'reprise'
      s.origines[`offre.${id}`] = { origine: 'offre', valeur: s.offre[id].texte }
    }
  }
  s.origines['besoin.intitule'] = { origine: 'offre', valeur: s.besoin.intitule }
  s.journal = [{ date: 'Aujourd\'hui', texte: `Offre dupliquée depuis ${ref0}` }]
  courant.value = { key: courant.value.key + 1, preset: 'nouveau', init: s, initStep: 'besoin' }
}
</script>

<template>
  <OffreApp
    :key="courant.key"
    :preset="courant.preset"
    :init="courant.init"
    :init-step="courant.initStep"
    @reprendre="reprendre"
    @dupliquer="dupliquer"
  />
</template>
