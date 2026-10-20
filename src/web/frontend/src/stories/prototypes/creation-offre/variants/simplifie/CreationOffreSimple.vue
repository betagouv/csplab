<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import type { OffreState, SectionOffreId } from '../../data/types'
import { ref } from 'vue'
import { nouveauDossier, ranger, trouver, trouverParDar } from '../../data/dossiers'
import { circuitPour } from '../../data/scenario'
import ListeOffres from './ListeOffres.vue'
import OffreAppSimple from './OffreAppSimple.vue'

// Racine de la version simplifiée : liste des offres ⇄ édition d'une offre.
// `ouvrir` ouvre un dossier de la session ; `preset` ouvre un état de démonstration isolé (non rangé).
const props = withDefaults(defineProps<{ preset?: Preset, ouvrir?: string, depuisDar?: string, liste?: boolean }>(), {
  preset: 'nouveau',
  ouvrir: undefined,
  depuisDar: undefined,
  liste: false,
})

type Vue = { mode: 'liste', message?: string } | { mode: 'offre', key: number, preset: Preset, init?: OffreState }
let key = 0

function vueInitiale(): Vue {
  if (props.liste) {
    return { mode: 'liste' }
  }
  const trouve = props.depuisDar ? trouverParDar(props.depuisDar) : props.ouvrir ? trouver(props.ouvrir) : undefined
  const init = trouve ? demarrer(trouve) : undefined
  return { mode: 'offre', key: key++, preset: init ? 'nouveau' : props.preset, init }
}

/** Ouvrir une DAR sans offre démarre l'offre, préremplie à partir de la DAR. */
function demarrer(s: OffreState): OffreState {
  if (!s.offreDemarree) {
    s.offreDemarree = true
    s.derniereEtape = ''
    s.journal.push({ date: `Aujourd'hui, ${new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}`, texte: `Offre ${s.reference} démarrée à partir de la DAR ${s.besoin.darRef}` })
    ranger(s)
  }
  return s
}
const vue = ref<Vue>(vueInitiale())

function ouvrir(reference: string) {
  const s = trouver(reference)
  vue.value = { mode: 'offre', key: key++, preset: 'nouveau', init: s ? demarrer(s) : undefined }
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
