<script setup lang="ts">
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { candidatureParId, conversationParCandidature, documentsParCandidature, nombreMessagesNonLus } from '../../data/candidatMock'
import EtapesTimeline from '../../shared/EtapesTimeline.vue'

const props = defineProps<{
  candidatureId: string
}>()

const emit = defineEmits<{
  retour: []
  voirConversation: [id: string]
  voirDocuments: [candidatureId: string]
}>()

const candidature = computed(() => candidatureParId(props.candidatureId))
const conversation = computed(() => conversationParCandidature(props.candidatureId))
const documents = computed(() => documentsParCandidature(props.candidatureId))
const messagesNonLus = computed(() => conversation.value ? nombreMessagesNonLus(conversation.value) : 0)
const documentsAFournir = computed(() => documents.value.filter(d => d.statut === 'a_fournir').length)
</script>

<template>
  <div
    v-if="candidature"
    class="detail"
  >
    <button
      type="button"
      class="detail__retour"
      @click="emit('retour')"
    >
      <CspIcon
        name="ri:arrow-left-line"
        :size="16"
      />
      Mes candidatures
    </button>

    <header class="detail__header">
      <h1 class="detail__poste">
        {{ candidature.poste }}
      </h1>
      <p class="detail__organisme">
        {{ candidature.organisme }}
      </p>
      <p class="detail__meta">
        Candidature envoyée le {{ candidature.dateEnvoi }}
      </p>
    </header>

    <div class="detail__layout">
      <CspCard title="Avancement de votre candidature">
        <EtapesTimeline :etapes="candidature.etapes" />
      </CspCard>

      <div class="detail__side">
        <CspCard
          v-if="conversation"
          size="sm"
        >
          <template #title>
            Messages
          </template>
          <p class="detail__side-text">
            {{ messagesNonLus > 0 ? `${messagesNonLus} nouveau message du recruteur` : 'Aucun nouveau message' }}
          </p>
          <template #footer>
            <CspButton
              variant="secondary"
              size="sm"
              label="Voir la conversation"
              @click="emit('voirConversation', conversation.id)"
            />
          </template>
        </CspCard>

        <CspCard
          v-if="documents.length > 0"
          size="sm"
        >
          <template #title>
            Documents
          </template>
          <p class="detail__side-text">
            {{ documentsAFournir > 0 ? `${documentsAFournir} document à fournir` : 'Tous les documents sont à jour' }}
          </p>
          <template #footer>
            <CspButton
              variant="secondary"
              size="sm"
              label="Voir les documents"
              @click="emit('voirDocuments', candidature.id)"
            />
          </template>
        </CspCard>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.detail {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.detail__retour {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  align-self: flex-start;
  border: none;
  background: none;
  cursor: pointer;
  padding: 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);

  &:hover {
    color: var(--text-action-high-blue-france);
  }
}

.detail__poste {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.detail__organisme {
  margin: 0.125rem 0 0;
  font-size: 0.9375rem;
  color: var(--text-default-grey);
}

.detail__meta {
  margin: 0.25rem 0 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.detail__layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 16rem;
  gap: var(--csp-space-5);
  align-items: start;
}

.detail__side {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.detail__side-text {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

@media (max-width: 48rem) {
  .detail__layout {
    grid-template-columns: 1fr;
  }
}
</style>
