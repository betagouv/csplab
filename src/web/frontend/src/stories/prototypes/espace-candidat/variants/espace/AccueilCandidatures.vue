<script setup lang="ts">
import type { ActionRequise } from '../../data/candidatMock'
import { actionsRequises, candidatures } from '../../data/candidatMock'
import ActionRequiseCard from '../../shared/ActionRequiseCard.vue'
import CandidatureCard from '../../shared/CandidatureCard.vue'

defineEmits<{
  ouvrirCandidature: [id: string]
  agir: [action: ActionRequise]
}>()
</script>

<template>
  <div class="accueil">
    <section
      v-if="actionsRequises.length > 0"
      class="accueil__section"
    >
      <h2 class="accueil__title">
        {{ actionsRequises.length }} action{{ actionsRequises.length > 1 ? 's' : '' }} à effectuer
      </h2>
      <div class="accueil__actions">
        <ActionRequiseCard
          v-for="action in actionsRequises"
          :key="action.id"
          :action="action"
          @agir="$emit('agir', action)"
        />
      </div>
    </section>

    <section class="accueil__section">
      <h2 class="accueil__title">
        Mes candidatures
      </h2>
      <div class="accueil__candidatures">
        <CandidatureCard
          v-for="candidature in candidatures"
          :key="candidature.id"
          :candidature="candidature"
          @ouvrir="$emit('ouvrirCandidature', $event)"
        />
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
.accueil {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-8);
}

.accueil__title {
  margin: 0 0 var(--csp-space-3);
  font-size: 1.0625rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.accueil__actions {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.accueil__candidatures {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}
</style>
