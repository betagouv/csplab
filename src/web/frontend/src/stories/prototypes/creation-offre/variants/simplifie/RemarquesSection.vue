<script setup lang="ts">
import type { StepId } from '../../data/types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { personne } from '../../data/referentiels'
import { useOffre } from '../../data/useOffre'

// Remarque d'un valideur affichée là où elle doit être traitée, sur un ton neutre.
const props = defineProps<{ stepIds: StepId[] }>()
const { state } = useOffre()
const remarques = computed(() => state.remarques.filter(r => !r.resolue && props.stepIds.includes(r.stepId)))
</script>

<template>
  <div
    v-for="r in remarques"
    :key="r.id"
    class="remarque"
  >
    <CspIcon
      name="ri:chat-1-line"
      :size="16"
      class="remarque__icon"
    />
    <div class="remarque__body">
      <p class="remarque__meta">
        {{ personne(r.auteurId).nom }} · {{ r.date }}
      </p>
      <p class="remarque__text">
        {{ r.texte }}
      </p>
    </div>
    <CspButton
      label="C'est corrigé"
      size="sm"
      variant="secondary"
      @click="r.resolue = true"
    />
  </div>
</template>

<style scoped lang="scss">
.remarque {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-alt-blue-france);
}

.remarque__icon {
  flex-shrink: 0;
  margin-top: 2px;
  color: var(--text-action-high-blue-france);
}

.remarque__body {
  flex: 1;

  p {
    margin: 0;
  }
}

.remarque__meta {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.remarque__text {
  font-size: var(--csp-font-size-sm);
}
</style>
