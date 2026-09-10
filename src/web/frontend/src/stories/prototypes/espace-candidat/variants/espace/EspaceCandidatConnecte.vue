<script setup lang="ts">
import type { ActionRequise } from '../../data/candidatMock'
import type { CandidatePage } from '../../shared/CandidateHeader.vue'
import { computed, ref } from 'vue'
import { conversationParCandidature, conversations, nombreMessagesNonLus } from '../../data/candidatMock'
import CandidateHeader from '../../shared/CandidateHeader.vue'
import AccueilCandidatures from './AccueilCandidatures.vue'
import CandidatureDetail from './CandidatureDetail.vue'
import ConversationsView from './ConversationsView.vue'
import DocumentsView from './DocumentsView.vue'

const page = ref<CandidatePage>('accueil')
const candidatureOuverteId = ref<string | null>(null)
const conversationCibleeId = ref<string | null>(null)
const candidatureDocumentsCibleeId = ref<string | null>(null)

const unreadCount = computed(() =>
  conversations.reduce((total, conv) => total + nombreMessagesNonLus(conv), 0),
)

function allerA(cible: CandidatePage) {
  page.value = cible
  candidatureOuverteId.value = null
}

function ouvrirCandidature(id: string) {
  page.value = 'accueil'
  candidatureOuverteId.value = id
}

function retourAccueil() {
  candidatureOuverteId.value = null
}

function voirConversation(id: string) {
  conversationCibleeId.value = id
  page.value = 'conversations'
}

function voirDocuments(candidatureId: string) {
  candidatureDocumentsCibleeId.value = candidatureId
  page.value = 'documents'
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
</script>

<template>
  <div class="espace">
    <CandidateHeader
      variant="connected"
      :current-page="page"
      :unread-count="unreadCount"
      @navigate="allerA"
    />

    <main class="espace__main">
      <div class="espace__container">
        <CandidatureDetail
          v-if="page === 'accueil' && candidatureOuverteId"
          :candidature-id="candidatureOuverteId"
          @retour="retourAccueil"
          @voir-conversation="voirConversation"
          @voir-documents="voirDocuments"
        />
        <AccueilCandidatures
          v-else-if="page === 'accueil'"
          @ouvrir-candidature="ouvrirCandidature"
          @agir="agirSurAction"
        />
        <ConversationsView
          v-else-if="page === 'conversations'"
          :initial-conversation-id="conversationCibleeId"
        />
        <DocumentsView
          v-else-if="page === 'documents'"
          :initial-candidature-id="candidatureDocumentsCibleeId"
        />
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss">
.espace {
  min-height: 100vh;
  background-color: var(--background-alt-grey);
}

.espace__main {
  display: flex;
  justify-content: center;
  padding: var(--csp-space-6);
}

.espace__container {
  width: 100%;
  max-width: 56rem;
}
</style>
