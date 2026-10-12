<script setup lang="ts">
import type { ReponseAide } from '../types'
import { computed } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import { FAQ_ENTREES } from '../constants/faq'

const props = defineProps<{
  reponse?: ReponseAide
  pending: boolean
  error?: unknown
}>()

const entree = computed(() =>
  FAQ_ENTREES.find(candidate => candidate.id === props.reponse?.entreeId),
)
</script>

<template>
  <div
    class="assistant-aide"
    aria-live="polite"
  >
    <CspAsyncSection
      :pending="pending"
      :error="error"
      loading-label="L'assistant cherche une réponse"
      error-title="L'assistant n'a pas pu répondre. Réessayez."
    >
      <div class="assistant-aide__reponse">
        <template v-if="reponse">
          <template v-if="entree">
            <p class="assistant-aide__titre">
              Entrée la plus proche
            </p>
            <p>
              <strong>{{ entree.question }}</strong>
            </p>
          </template>
          <p class="assistant-aide__texte">
            {{ reponse.reponse }}
          </p>
          <p
            v-if="entree"
            class="assistant-aide__ou"
          >
            <strong>Où :</strong> {{ entree.ou }}
          </p>
        </template>
      </div>
    </CspAsyncSection>
    <p class="assistant-aide__mention">
      Assistant expérimental — réponses issues de la FAQ
    </p>
  </div>
</template>

<style scoped lang="scss">
.assistant-aide {
  padding: 1.5rem;
  border: 1px solid var(--border-default-grey);
  background-color: var(--background-alt-grey);
}

.assistant-aide__reponse {
  p {
    margin: 0 0 0.75rem;
  }
}

.assistant-aide__titre {
  font-size: 0.875rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.assistant-aide__texte {
  white-space: pre-line;
}

.assistant-aide__ou,
.assistant-aide__mention {
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.assistant-aide__mention {
  margin: 0;
}
</style>
