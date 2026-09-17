<script setup lang="ts">
import type { ActionRequise } from '../../data/candidatMock'
import type { OngletCandidat } from '../../shared/mobile/MobileTabBar.vue'
import { computed, ref } from 'vue'
import { conversationParCandidature, conversations, nombreMessagesNonLus } from '../../data/candidatMock'
import AccueilCandidaturesMobile from './AccueilCandidaturesMobile.vue'
import CandidatureDetailMobile from './CandidatureDetailMobile.vue'
import ConversationsMobile from './ConversationsMobile.vue'
import DocumentsMobile from './DocumentsMobile.vue'
import MobileTabBar from '../../shared/mobile/MobileTabBar.vue'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'

const onglet = ref<OngletCandidat>('candidatures')
const candidatureOuverteId = ref<string | null>(null)
const conversationCibleeId = ref<string | null>(null)
const candidatureDocumentsCibleeId = ref<string | null>(null)

const messagesNonLus = computed(() =>
  conversations.reduce((total, conv) => total + nombreMessagesNonLus(conv), 0),
)

function changerOnglet(cible: OngletCandidat) {
  onglet.value = cible
  candidatureOuverteId.value = null
  conversationCibleeId.value = null
  candidatureDocumentsCibleeId.value = null
}

function ouvrirCandidature(id: string) {
  candidatureOuverteId.value = id
}

function voirConversation(id: string) {
  conversationCibleeId.value = id
  onglet.value = 'messages'
}

function voirDocuments(candidatureId: string) {
  candidatureDocumentsCibleeId.value = candidatureId
  onglet.value = 'documents'
}

function agirSurAction(action: ActionRequise) {
  if (action.type === 'message') {
    const conversation = conversationParCandidature(action.candidatureId)
    if (conversation) {
      voirConversation(conversation.id)
      return
    }
  }
  if (action.type === 'document') {
    voirDocuments(action.candidatureId)
    return
  }
  ouvrirCandidature(action.candidatureId)
}

const montrerTabBar = computed(() => !(onglet.value === 'candidatures' && candidatureOuverteId.value))
</script>

<template>
  <div class="espace">
    <div class="espace__ecran">
      <CandidatureDetailMobile
        v-if="onglet === 'candidatures' && candidatureOuverteId"
        :candidature-id="candidatureOuverteId"
        @retour="candidatureOuverteId = null"
        @voir-conversation="voirConversation"
        @voir-documents="voirDocuments"
      />
      <AccueilCandidaturesMobile
        v-else-if="onglet === 'candidatures'"
        @ouvrir-candidature="ouvrirCandidature"
        @agir="agirSurAction"
      />
      <ConversationsMobile
        v-else-if="onglet === 'messages'"
        :initial-conversation-id="conversationCibleeId"
      />
      <DocumentsMobile
        v-else-if="onglet === 'documents'"
        :initial-candidature-id="candidatureDocumentsCibleeId"
      />
      <div
        v-else-if="onglet === 'profil'"
        class="profil"
      >
        <CspAvatar
          name="Camille Rousseau"
          size="lg"
        />
        <p class="profil__nom">
          Camille Rousseau
        </p>
        <p class="profil__email">
          camille.rousseau@example.com
        </p>
        <CspButton
          variant="secondary"
          label="Se déconnecter"
          icon="ri:logout-box-line"
        />
      </div>
    </div>

    <MobileTabBar
      v-if="montrerTabBar"
      :actif="onglet"
      :messages-non-lus="messagesNonLus"
      @changer="changerOnglet"
    />
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

.profil {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-8) var(--csp-space-4);
  text-align: center;
}

.profil__nom {
  margin: var(--csp-space-2) 0 0;
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.profil__email {
  margin: 0 0 var(--csp-space-4);
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

@media (min-width: 40rem) {
  .espace {
    max-width: 28rem;
    margin: 0 auto;
    box-shadow: inset 0 0 0 1px var(--border-default-grey);
  }
}
</style>
