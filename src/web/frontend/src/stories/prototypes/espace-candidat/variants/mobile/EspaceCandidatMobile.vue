<script setup lang="ts">
import type { JeuDonnees, Utilisateur } from '../../data/espaceMock'
import { computed, ref } from 'vue'
import { creerEspace, provideEspace } from '../../data/useEspace'
import EspaceHeader from '../../shared/mobile/EspaceHeader.vue'
import CandidatureDetailMobile from './CandidatureDetailMobile.vue'
import CompteMobile from './CompteMobile.vue'
import ConversationMobile from './ConversationMobile.vue'
import MesCandidaturesMobile from './MesCandidaturesMobile.vue'

// Écran d'arrivée optionnel : sert aux stories isolées et au lien « nouveau message » d'un courriel.
export interface CibleEspace {
  ecran: 'liste' | 'detail' | 'conversation' | 'compte'
  candidatureId?: string
  conversationId?: string
}

const props = withDefaults(defineProps<{
  jeu?: JeuDonnees
  methode?: Utilisateur['methode']
  simulerEchecEnvoi?: boolean
  cible?: CibleEspace
}>(), {
  jeu: 'complet',
  methode: 'formulaire',
  simulerEchecEnvoi: false,
  cible: undefined,
})

defineEmits<{
  deconnexion: []
}>()

const espace = creerEspace({
  jeu: props.jeu,
  methode: props.methode,
  simulerEchecEnvoi: props.simulerEchecEnvoi,
})
provideEspace(espace)

// Navigation en pile : « Mes candidatures » est l'unique point d'entrée ; détail, conversation et
// compte s'empilent dessus, retour = dépiler.
type Ecran
  = | { nom: 'liste' }
    | { nom: 'detail', candidatureId: string }
    | { nom: 'conversation', candidatureId: string, conversationId: string }
    | { nom: 'compte' }

function pileInitiale(): Ecran[] {
  const pile: Ecran[] = [{ nom: 'liste' }]
  const { cible } = props
  if (!cible || cible.ecran === 'liste') {
    return pile
  }
  if (cible.ecran === 'compte') {
    return [...pile, { nom: 'compte' }]
  }
  if (cible.candidatureId) {
    pile.push({ nom: 'detail', candidatureId: cible.candidatureId })
    if (cible.ecran === 'conversation' && cible.conversationId) {
      pile.push({ nom: 'conversation', candidatureId: cible.candidatureId, conversationId: cible.conversationId })
    }
  }
  return pile
}

const pile = ref<Ecran[]>(pileInitiale())
const ecran = computed(() => pile.value[pile.value.length - 1])
const confirmation = ref<string | null>(null)

function naviguer(cibleEcran: Ecran) {
  confirmation.value = null
  pile.value.push(cibleEcran)
}

function retour() {
  if (pile.value.length > 1) {
    pile.value.pop()
  }
}

function versLaListe() {
  confirmation.value = null
  pile.value = [{ nom: 'liste' }]
}

function surRetrait() {
  pile.value = [{ nom: 'liste' }]
  confirmation.value = 'Votre candidature a été retirée. Elle figure désormais dans « Terminées ».'
}

function ouvrirConversation(conversationId: string) {
  const courant = ecran.value
  if (courant.nom === 'detail') {
    naviguer({ nom: 'conversation', candidatureId: courant.candidatureId, conversationId })
  }
}

function ouvrirCompte() {
  if (ecran.value.nom !== 'compte') {
    naviguer({ nom: 'compte' })
  }
}
</script>

<template>
  <div class="espace">
    <EspaceHeader
      :non-lus="espace.nonLusTotal.value"
      :nom-complet="`${espace.utilisateur.prenom} ${espace.utilisateur.nom}`"
      @accueil="versLaListe"
      @non-lus="versLaListe"
      @compte="ouvrirCompte"
    />

    <main class="espace__ecran">
      <MesCandidaturesMobile
        v-if="ecran.nom === 'liste'"
        :confirmation="confirmation"
        @ouvrir="(id) => naviguer({ nom: 'detail', candidatureId: id })"
      />
      <CandidatureDetailMobile
        v-else-if="ecran.nom === 'detail'"
        :key="ecran.candidatureId"
        :candidature-id="ecran.candidatureId"
        @retour="retour"
        @ouvrir-conversation="ouvrirConversation"
        @retiree="surRetrait"
      />
      <ConversationMobile
        v-else-if="ecran.nom === 'conversation'"
        :key="ecran.conversationId"
        :candidature-id="ecran.candidatureId"
        :conversation-id="ecran.conversationId"
        @retour="retour"
      />
      <CompteMobile
        v-else-if="ecran.nom === 'compte'"
        @retour="retour"
        @deconnexion="$emit('deconnexion')"
      />
    </main>
  </div>
</template>

<style scoped lang="scss">
.espace {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--background-default-grey);
}

.espace__ecran {
  flex: 1;
  display: flex;
  flex-direction: column;
}

@media (min-width: 40rem) {
  .espace {
    max-width: 26rem;
    margin: 0 auto;
    box-shadow: inset 0 0 0 1px var(--border-default-grey);
  }
}
</style>
