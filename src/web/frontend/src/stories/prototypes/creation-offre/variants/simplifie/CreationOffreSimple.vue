<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import type { OffreState } from '../../data/types'
import type { Page } from './useApp'
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { lancerRecrutement, trouver } from '../../data/dossiers'
import { nouvelleFiche, rangerFiche, trouverFiche } from '../../data/fiches'
import FicheDetail from './FicheDetail.vue'
import FichesListe from './FichesListe.vue'
import ListeDossiers from './ListeDossiers.vue'
import OffreAppSimple from './OffreAppSimple.vue'

// Racine : référentiel des fiches de poste (point d'entrée) ⇄ fiche ⇄ recrutement ouvert,
// plus les pages de suivi « Recrutements » et « Mes offres ». Le menu latéral change la route.
const props = withDefaults(defineProps<{
  page?: Page
  fiche?: string
  ouvrir?: string
  vue?: 'besoin' | 'offre'
  preset?: Preset
}>(), { page: 'fiches', fiche: undefined, ouvrir: undefined, vue: 'besoin', preset: undefined })

type Ecran
  = | { mode: 'liste', page: Page, message?: string, filtre?: string }
    | { mode: 'fiche', key: number, id: string, edition?: boolean, message?: string }
    | { mode: 'dossier', key: number, origine: Page, vue: 'besoin' | 'offre', preset: Preset, init?: OffreState }
let key = 0

function initial(): Ecran {
  if (props.preset) {
    return { mode: 'dossier', key: key++, origine: props.page, vue: props.vue, preset: props.preset }
  }
  if (props.fiche && trouverFiche(props.fiche)) {
    return { mode: 'fiche', key: key++, id: props.fiche }
  }
  const s = props.ouvrir ? trouver(props.ouvrir) : undefined
  if (s) {
    return { mode: 'dossier', key: key++, origine: props.vue === 'offre' ? 'offres' : 'recrutements', vue: props.vue, preset: 'nouveau', init: s }
  }
  return { mode: 'liste', page: props.page }
}
const ecran = ref<Ecran>(initial())

const router = useRouter()
const route = useRoute()
/** Hors des listes, on quitte leur route : un clic dans le menu y ramène toujours. */
function horsListe() {
  void router.replace('/detail')
}
watch(() => route.path, (path) => {
  const page = path.slice(1)
  if (page === 'fiches' || page === 'recrutements' || page === 'offres') {
    ecran.value = { mode: 'liste', page }
  }
})

function ouvrirFiche(id: string, message?: string, edition = false) {
  ecran.value = { mode: 'fiche', key: key++, id, edition, message }
  horsListe()
}

function nouvelle() {
  const f = nouvelleFiche()
  rangerFiche(f)
  ouvrirFiche(f.id, undefined, true)
}

function ouvrir(reference: string, vue: 'besoin' | 'offre', origine: Page) {
  ecran.value = { mode: 'dossier', key: key++, origine, vue, preset: 'nouveau', init: trouver(reference) }
  horsListe()
}

function lancer(ficheId: string, parcours: 'dar' | 'direct', nbPostes: string) {
  const s = lancerRecrutement(trouverFiche(ficheId)!, parcours, nbPostes)
  ecran.value = { mode: 'dossier', key: key++, origine: 'recrutements', vue: parcours === 'dar' ? 'besoin' : 'offre', preset: 'nouveau', init: s }
}

function pageSuivi(p: Page): 'recrutements' | 'offres' {
  return p === 'offres' ? 'offres' : 'recrutements'
}

function quitter(origine: Page, message?: string) {
  ecran.value = { mode: 'liste', page: origine, message }
}

function dupliquer(s: OffreState) {
  // Dupliquer une offre = relancer un recrutement depuis la même fiche.
  if (s.ficheId) {
    ouvrirFiche(s.ficheId, 'Pour un nouveau recrutement sur ce poste, utilisez « Lancer un recrutement » : la fiche est reprise.')
  }
}
</script>

<template>
  <FichesListe
    v-if="ecran.mode === 'liste' && ecran.page === 'fiches'"
    :message="ecran.message"
    @ouvrir="id => ouvrirFiche(id)"
    @nouvelle="nouvelle"
  />
  <ListeDossiers
    v-else-if="ecran.mode === 'liste'"
    :key="`${ecran.page}-${ecran.filtre ?? ''}`"
    :page="pageSuivi(ecran.page)"
    :message="ecran.message"
    :filtre-initial="ecran.filtre"
    @ouvrir="r => ecran.mode === 'liste' && ouvrir(r, ecran.page === 'offres' ? 'offre' : 'besoin', ecran.page)"
    @voir-fiches="ecran = { mode: 'liste', page: 'fiches' }"
  />
  <FicheDetail
    v-else-if="ecran.mode === 'fiche'"
    :key="ecran.key"
    :fiche-id="ecran.id"
    :edition="ecran.edition"
    :message="ecran.message"
    @retour="ecran = { mode: 'liste', page: 'fiches' }"
    @ouvrir-recrutement="r => ouvrir(r, 'besoin', 'recrutements')"
    @lancer="lancer"
  />
  <OffreAppSimple
    v-else
    :key="ecran.key"
    :preset="ecran.preset"
    :init="ecran.init"
    :vue="ecran.vue"
    :origine="ecran.origine"
    @dupliquer="dupliquer"
    @quitter="(o, m) => quitter(o, m)"
    @fiche="id => ouvrirFiche(id)"
  />
</template>
