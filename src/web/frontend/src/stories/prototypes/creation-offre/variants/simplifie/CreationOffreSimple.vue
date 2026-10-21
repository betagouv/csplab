<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import type { OffreState, SectionOffreId } from '../../data/types'
import type { Page } from './useApp'
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { nouveauDossier, ranger, trouver } from '../../data/dossiers'
import { circuitPour } from '../../data/scenario'
import ListeDossiers from './ListeDossiers.vue'
import OffreAppSimple from './OffreAppSimple.vue'

// Racine : « Mes besoins en recrutement » ⇄ « Mes offres » ⇄ dossier ouvert (vue besoin ou vue offre).
// Le menu latéral change la route ; la racine la suit.
const props = withDefaults(defineProps<{
  page?: Page
  ouvrir?: string
  vue?: 'besoin' | 'offre'
  preset?: Preset
}>(), { page: 'besoins', ouvrir: undefined, vue: 'besoin', preset: undefined })

type Ecran
  = | { mode: 'liste', page: Page, message?: string, filtre?: string }
    | { mode: 'dossier', key: number, origine: Page, vue: 'besoin' | 'offre', preset: Preset, init?: OffreState }
let key = 0

function initial(): Ecran {
  if (props.preset) {
    return { mode: 'dossier', key: key++, origine: props.page, vue: props.vue, preset: props.preset }
  }
  const s = props.ouvrir ? trouver(props.ouvrir) : undefined
  if (s) {
    return { mode: 'dossier', key: key++, origine: props.vue === 'offre' ? 'offres' : 'besoins', vue: props.vue, preset: 'nouveau', init: s }
  }
  return { mode: 'liste', page: props.page }
}
const ecran = ref<Ecran>(initial())

const router = useRouter()
const route = useRoute()
/** En ouvrant un dossier, on quitte la route de la liste : un clic dans le menu y ramène toujours. */
function versDossier() {
  void router.replace('/dossier')
}
watch(() => route.path, (path) => {
  if (path === '/besoins' || path === '/offres') {
    ecran.value = { mode: 'liste', page: path.slice(1) as Page }
  }
})

function ouvrir(reference: string, vue: 'besoin' | 'offre') {
  const origine = ecran.value.mode === 'liste' ? ecran.value.page : 'besoins'
  ecran.value = { mode: 'dossier', key: key++, origine, vue, preset: 'nouveau', init: trouver(reference) }
  versDossier()
}

function nouveau() {
  const s = nouveauDossier()
  ranger(s)
  ecran.value = { mode: 'dossier', key: key++, origine: 'besoins', vue: 'besoin', preset: 'nouveau', init: s }
  versDossier()
}

function quitter(origine: Page, message?: string) {
  ecran.value = { mode: 'liste', page: origine, message }
}

function dupliquer(s: OffreState) {
  const source = s.reference
  const neuf = nouveauDossier()
  Object.assign(s, {
    reference: neuf.reference,
    statut: 'brouillon',
    startMode: 'duplication',
    sourceLibelle: `${source} — ${s.titreAnnonce || s.besoin.intitule}`,
    circuit: circuitPour(s.organisation),
    remarques: [],
    contributions: [],
    dateDebutDiffusion: '',
    dateLimite: '',
    darContenu: null,
    origines: {},
    offreDemarree: false,
    derniereEtape: '',
    journal: [{ date: 'Aujourd\'hui', texte: `Besoin créé par duplication de ${source}` }],
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
  ecran.value = { mode: 'dossier', key: key++, origine: 'besoins', vue: 'besoin', preset: 'nouveau', init: s }
}
</script>

<template>
  <ListeDossiers
    v-if="ecran.mode === 'liste'"
    :key="`${ecran.page}-${ecran.filtre ?? ''}`"
    :page="ecran.page"
    :message="ecran.message"
    :filtre-initial="ecran.filtre"
    @ouvrir="r => ouvrir(r, ecran.mode === 'liste' && ecran.page === 'offres' ? 'offre' : 'besoin')"
    @nouveau="nouveau"
    @voir-besoins="f => (ecran = { mode: 'liste', page: 'besoins', filtre: f })"
  />
  <OffreAppSimple
    v-else
    :key="ecran.key"
    :preset="ecran.preset"
    :init="ecran.init"
    :vue="ecran.vue"
    :origine="ecran.origine"
    @reprendre="r => ouvrir(r, 'besoin')"
    @dupliquer="dupliquer"
    @quitter="(o, m) => quitter(o, m)"
  />
</template>
