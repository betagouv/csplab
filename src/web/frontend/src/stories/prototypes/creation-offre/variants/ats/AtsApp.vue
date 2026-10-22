<script setup lang="ts">
import type { Ecran } from './nav'
import { provide, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ApercuOffre from './ApercuOffre.vue'
import CreationOffre from './CreationOffre.vue'
import FicheDetail from './FicheDetail.vue'
import FichesListe from './FichesListe.vue'
import { NAV } from './nav'
import OffreEspace from './OffreEspace.vue'
import OffreFormulaire from './OffreFormulaire.vue'
import OffresListe from './OffresListe.vue'
import Parametres from './Parametres.vue'
import { appliquerParametreDar, db } from './store'
import TableauDeBord from './TableauDeBord.vue'

// Racine de la variante « ATS — fiches et offres ». Le menu latéral change la route ; la racine la suit.
const props = withDefaults(defineProps<{ depart?: Ecran, darObligatoire?: boolean }>(), { depart: () => ({ nom: 'accueil' }), darObligatoire: undefined })

// Démonstration : une story peut fixer le paramètre DAR de l'organisme.
if (props.darObligatoire !== undefined && db.organisme.darObligatoire !== props.darObligatoire) {
  db.organisme.darObligatoire = props.darObligatoire
  appliquerParametreDar()
}

const ecran = ref<Ecran>(props.depart)
const flash = ref<string | null>(null)
let timer: ReturnType<typeof setTimeout> | undefined

const router = useRouter()
const route = useRoute()
const LISTES: Record<string, Ecran> = { '/accueil': { nom: 'accueil' }, '/fiches': { nom: 'fiches' }, '/offres': { nom: 'offres' }, '/parametres': { nom: 'parametres' } }

// Chaque écran a son chemin : le menu, le fil d'Ariane et les boutons retour passent par la route.
function chemin(e: Ecran): string {
  if ('id' in e) {
    return `/${e.nom}/${e.id}`
  }
  return e.nom === 'creation' ? `/creation-${Date.now()}` : `/${e.nom}`
}
function suivreRoute(e: Ecran) {
  void router.replace(chemin(e))
}
// Le routeur de Storybook est partagé entre les stories : on l'aligne sur l'écran de départ.
suivreRoute(props.depart)

function aller(e: Ecran) {
  ecran.value = e
  suivreRoute(e)
  document.querySelector('.ats__main')?.scrollTo({ top: 0 })
}

const DETAILS = /^\/(offre|fiche|formulaire|apercu)\/(.+)$/
watch(() => route.path, (p) => {
  const d = DETAILS.exec(p)
  const e = LISTES[p] ?? (d ? { nom: d[1], id: d[2] } as Ecran : undefined)
  if (e && chemin(e) !== chemin(ecran.value)) {
    ecran.value = e
  }
})

function notifier(texte: string) {
  flash.value = texte
  clearTimeout(timer)
  timer = setTimeout(() => (flash.value = null), 4000)
}

provide(NAV, { ecran, aller, notifier, flash })
</script>

<template>
  <TableauDeBord v-if="ecran.nom === 'accueil'" />
  <FichesListe v-else-if="ecran.nom === 'fiches'" />
  <FicheDetail
    v-else-if="ecran.nom === 'fiche'"
    :id="ecran.id"
    :key="ecran.id"
    :edition="ecran.edition"
  />
  <OffresListe
    v-else-if="ecran.nom === 'offres'"
    :key="ecran.filtre ?? 'toutes'"
    :filtre="ecran.filtre"
  />
  <CreationOffre
    v-else-if="ecran.nom === 'creation'"
    :key="`${ecran.mode}-${ecran.ficheId}-${ecran.offreId}`"
    :mode="ecran.mode"
    :fiche-id="ecran.ficheId"
    :offre-id="ecran.offreId"
  />
  <Parametres v-else-if="ecran.nom === 'parametres'" />
  <OffreEspace
    v-else-if="ecran.nom === 'offre'"
    :id="ecran.id"
    :key="`o-${ecran.id}`"
  />
  <OffreFormulaire
    v-else-if="ecran.nom === 'formulaire'"
    :id="ecran.id"
    :key="`f-${ecran.id}`"
  />
  <ApercuOffre
    v-else-if="ecran.nom === 'apercu'"
    :id="ecran.id"
    :key="`a-${ecran.id}-${ecran.publier}`"
    :publier="ecran.publier"
  />
</template>
