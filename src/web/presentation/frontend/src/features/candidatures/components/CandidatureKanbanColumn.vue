<script setup lang="ts">
import type { EtapeRecrutementDetailedCandidatures } from '../types'
import { computed, ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import { CATEGORIE_CONFIG } from '@/features/etapes-recrutement/constants/etape-recrutement'
import CandidatureKanbanCard from './CandidatureKanbanCard.vue'

const props = defineProps<{
  etape: EtapeRecrutementDetailedCandidatures
}>()

const categorieConfig = computed(() => CATEGORIE_CONFIG[props.etape.categorie])
const isSelected = ref(false)
</script>

<template>
  <section
    class="candidature-kanban-column"
    :class="`candidature-kanban-column--${categorieConfig.cssModifier}`"
  >
    <header class="candidature-kanban-column__header">
      <h2 class="candidature-kanban-column__title">
        <CspCheckbox
          v-model="isSelected"
          class="candidature-kanban-column__select"
          variant="checkbox-only"
          size="sm"
          :label="`Sélectionner la colonne ${etape.nom}`"
        />
        <span class="candidature-kanban-column__title-text">{{ etape.nom }}</span>
        <CspBadge
          class="candidature-kanban-column__count"
          size="md"
          variant="default"
          :label="String(etape.candidatures.length)"
        />
      </h2>
    </header>
    <ul class="candidature-kanban-column__cards">
      <li
        v-for="candidature in etape.candidatures"
        :key="candidature.uuid"
        class="candidature-kanban-column__card-item"
      >
        <CandidatureKanbanCard :candidature="candidature" />
      </li>
    </ul>
    <footer class="candidature-kanban-column__hint">
      <p class="candidature-kanban-column__hint-label">
        Statut visible par le candidat
      </p>
      <CspBadge
        class="candidature-kanban-column__hint-badge"
        size="sm"
        :icon="categorieConfig.icon"
        :type="categorieConfig.type"
        :label="categorieConfig.label"
      />
    </footer>
  </section>
</template>

<style scoped lang="scss">
.candidature-kanban-column {
  display: flex;
  flex-direction: column;
  flex: 0 0 18.75rem;
  min-width: 18.75rem;
  gap: var(--csp-space-3);
  min-height: 12rem;
  padding: var(--csp-space-3);
  background-color: var(--background-alt-grey);
  border-radius: 0.25rem;
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  border-top: 3px solid var(--border-default-grey);
}

.candidature-kanban-column--en-cours {
  border-top-color: var(--border-plain-info);
}

.candidature-kanban-column--refus {
  border-top-color: var(--border-plain-error);
}

.candidature-kanban-column--accepte {
  border-top-color: var(--border-plain-success);
}

.candidature-kanban-column__header {
  padding: 0 var(--csp-space-1);
}

.candidature-kanban-column__title {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 700;
  line-height: 1.3;
  color: var(--text-title-grey);
}

.candidature-kanban-column__title-text {
  min-width: 0;
}

.candidature-kanban-column__select {
  flex-shrink: 0;
}

.candidature-kanban-column__count {
  flex-shrink: 0;
  margin: 0;
}

.candidature-kanban-column__title :deep(.candidature-kanban-column__count) {
  align-self: center;
}

.candidature-kanban-column__cards {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.candidature-kanban-column__card-item {
  margin: 0;
}

.candidature-kanban-column__hint {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin-top: auto;
  padding: var(--csp-space-3) var(--csp-space-1) 0;
  border-top: 1px solid var(--border-default-grey);
}

.candidature-kanban-column__hint-label {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.candidature-kanban-column__hint-badge {
  margin: 0;
}

.candidature-kanban-column__hint :deep(.candidature-kanban-column__hint-badge) {
  align-self: flex-start;
}
</style>
