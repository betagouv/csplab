<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import type { OffreState, SectionOffreId } from '../../data/types'
import { ref } from 'vue'
import { nouveauDossier, ranger, trouver } from '../../data/dossiers'
import { circuitPour } from '../../data/scenario'
import ListeOffres from './ListeOffres.vue'
import OffreAppSimple from './OffreAppSimple.vue'

// Racine de la version simplifiée : liste des offres ⇄ édition d'une offre.
// `ouvrir` ouvre un dossier de la session ; `preset` ouvre un état de démonstration isolé (non rangé).
const props = withDefaults(defineProps<{ preset?: Preset, ouvrir?: string, liste?: boolean }>(), {
  preset: 'nouveau',
  ouvrir: undefined,
  liste: false,
})

type Vue = { mode: 'liste', message?: string } | { mode: 'offre', key: number, preset: Preset, init?: OffreState }
let key = 0

function vueInitiale(): Vue {
  if (props.liste) {
    return { mode: 'liste' }
  }
  const init = props.ouvrir ? trouver(props.ouvrir) : undefined
  return { mode: 'offre', key: key++, preset: init ? 'nouveau' : props.preset, init }
}
const vue = ref<Vue>(vueInitiale())

function ouvrir(reference: string) {
  vue.value = { mode: 'offre', key: key++, preset: 'nouveau', init: trouver(reference) }
}

function nouvelle() {
  vue.value = { mode: 'offre', key: key++, preset: 'nouveau', init: nouveauDossier() }
}

function quitter(message?: string) {
  vue.value = { mode: 'liste', message }
}

function dupliquer(s: OffreState) {
  const source = s.reference
  const neuf = nouveauDossier()
  Object.assign(s, {
    reference: neuf.reference,
    statut: 'brouillon',
    startMode: 'duplication',
    sourceLibelle: `${source} — ${s.besoin.intitule}`,
    circuit: circuitPour(s.organisation),
    remarques: [],
    contributions: [],
    dateDebutDiffusion: '',
    dateLimite: '',
    darContenu: null,
    origines: {},
    derniereEtape: 'poste',
    journal: [{ date: 'Aujourd\'hui', texte: `Dossier créé par duplication de ${source}` }],
  })
  s.canaux.forEach(c => (c.fait = []))
  s.besoin.darRef = ''
  s.besoin.darStatut = ''
  s.besoin.darApplicable = 'nsp'
  s.besoin.codesPostes = []
  for (const id of Object.keys(s.offre) as SectionOffreId[]) {
    if (s.offre[id].texte) {
      s.offre[id].etat = 'reprise'
    }
  }
  ranger(s)
  vue.value = { mode: 'offre', key: key++, preset: 'nouveau', init: s }
}
</script>

<template>
  <ListeOffres
    v-if="vue.mode === 'liste'"
    :message="vue.message"
    @ouvrir="ouvrir"
    @nouvelle="nouvelle"
  />
  <OffreAppSimple
    v-else
    :key="vue.key"
    :preset="vue.preset"
    :init="vue.init"
    @reprendre="ouvrir"
    @dupliquer="dupliquer"
    @quitter="quitter"
  />
</template>
