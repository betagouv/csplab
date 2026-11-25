<script setup lang="ts">
import type { Ecran } from './nav'
import { provide, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NAV } from './nav'
import OffreEspace from './OffreEspace.vue'
import OffresListe from './OffresListe.vue'
import Parametres from './Parametres.vue'
import PublierOffre from './PublierOffre.vue'
import RecrutementOffre from './RecrutementOffre.vue'
import RecrutementsListe from './RecrutementsListe.vue'
import RedactionOffre from './RedactionOffre.vue'
import { db, nouvelleOffre, retraitsAutomatiques, UTILISATEUR } from './store'

// Racine du proto « Offres sans autorisation ». Le menu latéral change la route ; la racine la suit.
// `publier` : simule un agent sans le droit « Publier » (il prépare l'offre, un autre la met en ligne).
const props = withDefaults(defineProps<{ depart?: Ecran, publier?: boolean }>(), { depart: () => ({ nom: 'offres' }), publier: true })

const moi = db.organisme.agents.find(a => a.nom === UTILISATEUR)
if (moi) {
  moi.publier = props.publier
}
retraitsAutomatiques()

const ecran = ref<Ecran>(props.depart.nom === 'creation' ? { nom: 'rediger', id: nouvelleOffre(undefined, 'manuel').id } : props.depart)
const flash = ref<string | null>(null)
let timer: ReturnType<typeof setTimeout> | undefined

const router = useRouter()
const route = useRoute()
const LISTES: Record<string, Ecran> = { '/accueil': { nom: 'offres' }, '/offres': { nom: 'offres' }, '/recrutements': { nom: 'recrutements' }, '/parametres': { nom: 'parametres' } }

function chemin(e: Ecran): string {
  if ('id' in e) {
    return `/${e.nom}/${e.id}`
  }
  return e.nom === 'creation' ? `/creation-${Date.now()}` : `/${e.nom}`
}
// Le routeur de Storybook est partagé entre les stories : on l'aligne sur l'écran de départ.
void router.replace(chemin(ecran.value))

function aller(e: Ecran) {
  // « Créer une offre » ouvre directement le formulaire vide (retour Alice du 25/11/2026) : plus d'écran de choix.
  if (e.nom === 'creation') {
    e = { nom: 'rediger', id: nouvelleOffre(undefined, 'manuel').id }
  }
  ecran.value = e
  void router.replace(chemin(e))
  document.querySelector('.csp-page-container')?.scrollTo({ top: 0 })
}

const DETAILS = /^\/(offre|rediger|publier|recrutement)\/(.+)$/
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
  <OffresListe
    v-if="ecran.nom === 'offres'"
    :key="ecran.filtre ?? 'toutes'"
    :filtre="ecran.filtre"
  />
  <RedactionOffre
    v-else-if="ecran.nom === 'rediger'"
    :id="ecran.id"
    :key="`r-${ecran.id}`"
    :etape="ecran.etape"
  />
  <OffreEspace
    v-else-if="ecran.nom === 'offre'"
    :id="ecran.id"
    :key="`o-${ecran.id}`"
    :section="ecran.section"
  />
  <PublierOffre
    v-else-if="ecran.nom === 'publier'"
    :id="ecran.id"
    :key="`p-${ecran.id}`"
  />
  <RecrutementOffre
    v-else-if="ecran.nom === 'recrutement'"
    :id="ecran.id"
    :key="`rec-${ecran.id}`"
  />
  <RecrutementsListe
    v-else-if="ecran.nom === 'recrutements'"
    :onglet-depart="ecran.onglet"
  />
  <Parametres v-else-if="ecran.nom === 'parametres'" />
</template>
