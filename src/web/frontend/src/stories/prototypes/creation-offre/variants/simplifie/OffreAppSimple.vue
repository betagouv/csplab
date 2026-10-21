<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import type { OffreState } from '../../data/types'
import type { Page } from './useApp'
import type { EtapeId } from './useEtapes'
import { onBeforeUnmount, provide, watch } from 'vue'
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
const props = withDefaults(defineProps<{ preset: Preset, init?: OffreState, vue?: 'besoin' | 'offre', origine?: Page }>(), {
  init: undefined,
  vue: 'besoin',
  origine: 'recrutements',
})
const emit = defineEmits<{ dupliquer: [state: OffreState], quitter: [origine: Page, message?: string], fiche: [id: string] }>()

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

// Vue « besoin » : la fiche de poste et sa validation. Vue « offre » : reprise là où l'on s'était arrêté.
const PAR_STATUT: Record<OffreState['statut'], EtapeId> = {
  brouillon: 'candidature',
  a_corriger: 'offre',
  a_valider: 'finaliser',
  validee: 'finaliser',
  creee: 'finaliser',
  publiee: 'finaliser',
}
const derniere = store.state.derniereEtape as EtapeId
const avecDar = store.state.besoin.darApplicable === 'oui'
const depart: EtapeId = (props.vue === 'besoin' && avecDar) || !store.state.offreDemarree
  ? 'poste'
  : ETAPES.some(e => e.id === derniere && e.id !== 'poste') && store.state.statut === 'brouillon'
    ? derniere
    : PAR_STATUT[store.state.statut]
const nav = provideEtapes(depart)
if (props.init?.besoin.intitule || !['nouveau', 'sans_dar', 'sans_validation'].includes(props.preset)) {
  ETAPES.forEach(e => nav.visitees.value.add(e.id))
}
watch(nav.etape, e => (store.state.derniereEtape = e))

provideApp({
  origine: props.origine,
  ouvrirFiche: async (id: string) => {
    await store.enregistrer()
    emit('fiche', id)
  },
  quitter: async () => {
    await store.enregistrer()
    const titre = store.state.titreAnnonce || store.state.besoin.intitule || store.state.reference
    const enCours = store.state.statut === 'brouillon' || (store.state.besoin.darApplicable === 'oui' && store.state.besoin.darStatut === 'a_demander')
    emit('quitter', props.origine, enCours
      ? `« ${titre} » enregistré. Vous pouvez reprendre à tout moment.`
      : `« ${titre} » est à jour.`)
  },
})

// Quitter par le menu latéral : les dernières saisies sont rangées immédiatement.
onBeforeUnmount(() => {
  if (store.dirty.value) {
    store.persist()
  }
})
</script>

<template>
  <ShellSimple>
    <EtapeBesoinDar v-if="nav.etape.value === 'poste' && store.darFigee.value" />
    <EtapePoste v-else-if="nav.etape.value === 'poste'" />
    <EtapeOffre v-else-if="nav.etape.value === 'offre'" />
    <EtapeCandidature v-else-if="nav.etape.value === 'candidature'" />
    <EtapeFinaliser
      v-else
      @dupliquer="emit('dupliquer', JSON.parse(JSON.stringify(store.state)))"
    />
  </ShellSimple>
</template>
