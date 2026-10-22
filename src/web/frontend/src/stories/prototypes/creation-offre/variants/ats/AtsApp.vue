<script setup lang="ts">
import type { Ecran } from './nav'
import { provide, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CreationOffre from './CreationOffre.vue'
import FicheDetail from './FicheDetail.vue'
import FichesListe from './FichesListe.vue'
import { NAV } from './nav'
import OffreEspace from './OffreEspace.vue'
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

function aller(e: Ecran) {
  ecran.value = e
  // Hors des listes, on quitte leur route : un clic dans le menu y ramène toujours.
  void router.replace(['accueil', 'fiches', 'offres', 'parametres'].includes(e.nom) ? `/${e.nom}` : `/detail-${Date.now()}`)
  document.querySelector('.ats__main')?.scrollTo({ top: 0 })
}

watch(() => route.path, (p) => {
  const e = LISTES[p]
  if (e && e.nom !== ecran.value.nom) {
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
    :key="ecran.id"
    :onglet="ecran.onglet"
  />
</template>
