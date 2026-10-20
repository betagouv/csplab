<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import type { OffreState } from '../../data/types'
import type { EtapeId } from './useEtapes'
import { clone } from '../../data/scenario'
import { provideOffre } from '../../data/useOffre'
import EtapeCandidature from './EtapeCandidature.vue'
import EtapeFinaliser from './EtapeFinaliser.vue'
import EtapeOffre from './EtapeOffre.vue'
import EtapePoste from './EtapePoste.vue'
import ShellSimple from './ShellSimple.vue'
import { ETAPES, provideEtapes, REGLES_EXCLUES } from './useEtapes'

// Une offre ouverte dans la version simplifiée. Remontée (via :key) pour reprendre un brouillon ou dupliquer.
const props = defineProps<{ preset: Preset, init?: OffreState }>()
const emit = defineEmits<{ reprendre: [preset: Preset], dupliquer: [state: OffreState] }>()

const store = provideOffre(props.preset, { exclure: REGLES_EXCLUES })
if (props.init) {
  Object.assign(store.state, clone(props.init))
}

const DEPART: Record<Preset, EtapeId> = {
  nouveau: 'poste',
  incomplet: 'poste',
  a_valider: 'finaliser',
  a_corriger: 'offre',
  pret: 'finaliser',
  sans_dar: 'poste',
  sans_validation: 'poste',
}
const nav = provideEtapes(DEPART[props.preset])
// Une offre reprise a déjà été parcourue : ses étapes complètes sont cochées d'emblée.
if (!['nouveau', 'sans_dar', 'sans_validation'].includes(props.preset) || props.init) {
  ETAPES.forEach(e => nav.visitees.value.add(e.id))
}
</script>

<template>
  <ShellSimple>
    <EtapePoste
      v-if="nav.etape.value === 'poste'"
      @reprendre="p => emit('reprendre', p)"
    />
    <EtapeOffre v-else-if="nav.etape.value === 'offre'" />
    <EtapeCandidature v-else-if="nav.etape.value === 'candidature'" />
    <EtapeFinaliser
      v-else
      @dupliquer="emit('dupliquer', JSON.parse(JSON.stringify(store.state)))"
    />
  </ShellSimple>
</template>
