<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import type { OffreState } from '../../data/types'
import type { EtapeId } from './useEtapes'
import { provide, watch } from 'vue'
import { ranger } from '../../data/dossiers'
import { clone } from '../../data/scenario'
import { provideOffre } from '../../data/useOffre'
import { ORIGINES_DISCRETES } from '../../shared/origines'
import EtapeBesoinDar from './EtapeBesoinDar.vue'
import EtapeCandidature from './EtapeCandidature.vue'
import EtapeFinaliser from './EtapeFinaliser.vue'
import EtapeOffre from './EtapeOffre.vue'
import EtapePoste from './EtapePoste.vue'
import ShellSimple from './ShellSimple.vue'
import { provideApp } from './useApp'
import { ETAPES, provideEtapes, REGLES_EXCLUES } from './useEtapes'

// Une offre ouverte. Avec `init` (dossier de la session), les enregistrements sont rangés
// dans la liste ; sans `init` (état de démonstration), rien n'est conservé.
const props = defineProps<{ preset: Preset, init?: OffreState }>()
const emit = defineEmits<{ reprendre: [reference: string], dupliquer: [state: OffreState], quitter: [message?: string] }>()

const store = provideOffre(props.preset, {
  exclure: REGLES_EXCLUES,
  autosave: true,
  persister: props.init ? ranger : undefined,
})
if (props.init) {
  Object.assign(store.state, clone(props.init))
  store.lastSaved.value = props.init.modifieLe.toLowerCase().startsWith('aujourd') ? props.init.modifieLe.replace('Aujourd\'hui, ', 'à ') : props.init.modifieLe.toLowerCase()
}

// Les badges « repris de… » ne s'affichent que si la valeur a été modifiée (pour proposer « Rétablir »).
provide(ORIGINES_DISCRETES, true)

const PAR_STATUT: Record<OffreState['statut'], EtapeId> = {
  brouillon: 'poste',
  a_corriger: 'offre',
  a_valider: 'finaliser',
  validee: 'finaliser',
  creee: 'finaliser',
  publiee: 'finaliser',
}
const derniere = store.state.derniereEtape as EtapeId
const depart: EtapeId = ETAPES.some(e => e.id === derniere) && store.state.statut === 'brouillon'
  ? derniere
  : props.init ? PAR_STATUT[store.state.statut] : ({ a_valider: 'finaliser', a_corriger: 'offre', pret: 'finaliser', dar_paie: 'offre' } as Partial<Record<Preset, EtapeId>>)[props.preset] ?? 'poste'
const nav = provideEtapes(depart)
if (props.init?.besoin.intitule || !['nouveau', 'sans_dar', 'sans_validation'].includes(props.preset)) {
  ETAPES.forEach(e => nav.visitees.value.add(e.id))
}
watch(nav.etape, e => (store.state.derniereEtape = e))

provideApp({
  quitter: async () => {
    await store.enregistrer()
    const titre = store.state.besoin.intitule || store.state.reference
    emit('quitter', store.state.statut === 'brouillon'
      ? `Brouillon « ${titre} » enregistré. Vous pouvez le reprendre à tout moment.`
      : `« ${titre} » est à jour.`)
  },
})
</script>

<template>
  <ShellSimple>
    <EtapeBesoinDar v-if="nav.etape.value === 'poste' && store.darFigee.value" />
    <EtapePoste
      v-else-if="nav.etape.value === 'poste'"
      @reprendre="r => emit('reprendre', r)"
    />
    <EtapeOffre v-else-if="nav.etape.value === 'offre'" />
    <EtapeCandidature v-else-if="nav.etape.value === 'candidature'" />
    <EtapeFinaliser
      v-else
      @dupliquer="emit('dupliquer', JSON.parse(JSON.stringify(store.state)))"
    />
  </ShellSimple>
</template>
