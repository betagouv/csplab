<script setup lang="ts">
import type { ActionRequise } from '../../data/candidatMock'
import { computed, ref } from 'vue'
import AccueilCandidaturesMobile from './AccueilCandidaturesMobile.vue'
import CandidatureDetailMobile from './CandidatureDetailMobile.vue'
import ConversationsMobile from './ConversationsMobile.vue'
import DocumentsMobile from './DocumentsMobile.vue'
import ProfilMobile from './ProfilMobile.vue'

// Mes candidatures est l'unique point d'entrée : messages et documents ne sont accessibles
// qu'en contexte, depuis une candidature précise. Navigation en pile (retour = dépiler) plutôt
// qu'un jeu d'onglets, pour refléter cette hiérarchie à un seul niveau d'entrée.
type Ecran =
  | { nom: 'accueil' }
  | { nom: 'detail', candidatureId: string }
  | { nom: 'conversation', candidatureId: string }
  | { nom: 'documents', candidatureId: string }
  | { nom: 'profil' }

const pile = ref<Ecran[]>([{ nom: 'accueil' }])
const ecran = computed(() => pile.value[pile.value.length - 1])

function naviguer(cible: Ecran) {
  pile.value.push(cible)
}

function retour() {
  if (pile.value.length > 1) {
    pile.value.pop()
  }
}

function agirSurAction(action: ActionRequise) {
  if (action.type === 'message') {
    naviguer({ nom: 'conversation', candidatureId: action.candidatureId })
    return
  }
  if (action.type === 'document') {
    naviguer({ nom: 'documents', candidatureId: action.candidatureId })
    return
  }
  naviguer({ nom: 'detail', candidatureId: action.candidatureId })
}
</script>

<template>
  <div class="espace">
    <div class="espace__ecran">
      <AccueilCandidaturesMobile
        v-if="ecran.nom === 'accueil'"
        @ouvrir-candidature="(id) => naviguer({ nom: 'detail', candidatureId: id })"
        @ouvrir-profil="naviguer({ nom: 'profil' })"
        @agir="agirSurAction"
      />
      <CandidatureDetailMobile
        v-else-if="ecran.nom === 'detail'"
        :candidature-id="ecran.candidatureId"
        @retour="retour"
        @voir-conversation="(id) => naviguer({ nom: 'conversation', candidatureId: id })"
        @voir-documents="(id) => naviguer({ nom: 'documents', candidatureId: id })"
      />
      <ConversationsMobile
        v-else-if="ecran.nom === 'conversation'"
        :candidature-id="ecran.candidatureId"
        @retour="retour"
      />
      <DocumentsMobile
        v-else-if="ecran.nom === 'documents'"
        :candidature-id="ecran.candidatureId"
        @retour="retour"
      />
      <ProfilMobile
        v-else-if="ecran.nom === 'profil'"
        @retour="retour"
      />
    </div>
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
  overflow-y: auto;
}

@media (min-width: 40rem) {
  .espace {
    max-width: 28rem;
    margin: 0 auto;
    box-shadow: inset 0 0 0 1px var(--border-default-grey);
  }
}
</style>
