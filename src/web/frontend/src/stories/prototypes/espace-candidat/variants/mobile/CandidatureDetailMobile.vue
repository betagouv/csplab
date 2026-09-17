<script setup lang="ts">
import { computed } from 'vue'
import { candidatureParId, conversationParCandidature, documentsParCandidature, nombreMessagesNonLus } from '../../data/candidatMock'
import EtapesTimeline from '../../shared/EtapesTimeline.vue'
import MobileTopBar from '../../shared/mobile/MobileTopBar.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

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
    <MobileTopBar
      title="Détail de la candidature"
      show-back
      @back="emit('retour')"
    />

    <div class="detail__content">
      <div class="detail__intro">
        <h1 class="detail__poste">
          {{ candidature.poste }}
        </h1>
        <p class="detail__organisme">
          {{ candidature.organisme }}
        </p>
        <p class="detail__meta">
          Candidature envoyée le {{ candidature.dateEnvoi }}
        </p>
      </div>

      <section class="detail__section">
        <h2>Avancée de ma candidature</h2>
        <EtapesTimeline :etapes="candidature.etapes" />
      </section>

      <section
        v-if="conversation"
        class="detail__section"
      >
        <h2>Conversation</h2>
        <button
          type="button"
          class="detail__card"
          @click="emit('voirConversation', conversation.id)"
        >
          <span class="detail__card-icon">
            <CspIcon
              name="ri:message-3-line"
              :size="18"
            />
          </span>
          <span class="detail__card-body">
            <span class="detail__card-titre">
              Conversation avec le recruteur
              <span
                v-if="messagesNonLus > 0"
                class="detail__unread-dot"
                aria-label="Message non lu"
              />
            </span>
            <span class="detail__card-texte">
              {{ conversation.messages.at(-1)?.texte }}
            </span>
          </span>
          <CspIcon
            name="ri:arrow-right-s-line"
            :size="20"
            class="detail__card-chevron"
          />
        </button>
      </section>

      <section
        v-if="documents.length > 0"
        class="detail__section"
      >
        <h2>Documents</h2>
        <button
          type="button"
          class="detail__card"
          @click="emit('voirDocuments', candidature.id)"
        >
          <span class="detail__card-icon">
            <CspIcon
              name="ri:folder-line"
              :size="18"
            />
          </span>
          <span class="detail__card-body">
            <span class="detail__card-titre">
              {{ documentsAFournir > 0 ? `${documentsAFournir} document à fournir` : 'Documents à jour' }}
            </span>
            <span class="detail__card-texte">
              {{ documents.length }} document{{ documents.length > 1 ? 's' : '' }} au total
            </span>
          </span>
          <CspIcon
            name="ri:arrow-right-s-line"
            :size="20"
            class="detail__card-chevron"
          />
        </button>
      </section>
    </div>
  </div>
</template>

<style scoped lang="scss">
.detail {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}

.detail__content {
  padding: var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.detail__intro {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.detail__poste {
  margin: 0;
  font-size: 1.1875rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.detail__organisme {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-default-grey);
}

.detail__meta {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.detail__section {
  h2 {
    margin: 0 0 var(--csp-space-3);
    font-size: 0.9375rem;
    font-weight: 700;
    color: var(--text-title-grey);
  }
}

.detail__card {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  width: 100%;
  text-align: left;
  padding: var(--csp-space-3) var(--csp-space-10) var(--csp-space-3) var(--csp-space-3);
  border: none;
  border-radius: 0.5rem;
  background-color: var(--background-alt-grey);
  cursor: pointer;
  font: inherit;
  min-height: 3.5rem;
}

.detail__card-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 50%;
  background-color: var(--background-default-grey);
  color: var(--text-action-high-blue-france);
}

.detail__card-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.detail__card-titre {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.detail__unread-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background-color: var(--background-action-high-blue-france);
}

.detail__card-texte {
  margin-top: 0.125rem;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detail__card-chevron {
  position: absolute;
  right: var(--csp-space-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-mention-grey);
}
</style>
