<script setup lang="ts">
import { DEMO_RECRUTEMENT_UUID } from '@/api/__mocks__/demo'
import { demoKanban } from '@/features/candidatures/__mocks__/demo'
import CandidatureKanbanCard from '@/features/candidatures/components/CandidatureKanbanCard.vue'
import UnreadVariantProvider from './UnreadVariantProvider.vue'
import { UNREAD_VARIANTS } from './variants'

const NOMS = ['Fontaine', 'Moreau', 'Benali', 'Leroy']

const candidatures = demoKanban().etapes.flatMap(({ candidatures }) => candidatures).filter(({ candidat }) => NOMS.includes(candidat.nom)).sort((a, b) => NOMS.indexOf(a.candidat.nom) - NOMS.indexOf(b.candidat.nom))
</script>

<template>
  <div class="messages-non-lus-comparaison">
    <UnreadVariantProvider
      v-for="variant in UNREAD_VARIANTS"
      :key="variant.id"
      :variant="variant.id"
    >
      <section class="messages-non-lus-comparaison__colonne">
        <h2 class="messages-non-lus-comparaison__titre">
          {{ variant.name }}
        </h2>
        <CandidatureKanbanCard
          v-for="candidature in candidatures"
          :key="candidature.uuid"
          :candidature="candidature"
          :board-id="`${DEMO_RECRUTEMENT_UUID}-${variant.id}`"
          column-id="a-traiter"
        />
      </section>
    </UnreadVariantProvider>
  </div>
</template>

<style scoped lang="scss">
.messages-non-lus-comparaison {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: var(--csp-space-6);
  max-width: calc(4 * var(--csp-kanban-column-width) + 5 * var(--csp-space-6));
  padding: var(--csp-space-6);
  background-color: var(--background-default-grey);
}

.messages-non-lus-comparaison__colonne {
  display: flex;
  flex-direction: column;
  gap: var(--csp-kanban-column-gap);
  width: var(--csp-kanban-column-width);
  padding: var(--csp-kanban-column-padding);
  background-color: var(--csp-region-background);
  box-shadow: inset 0 0 0 1px var(--csp-region-border-color);
}

.messages-non-lus-comparaison__titre {
  margin: 0 0 var(--csp-space-1);
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-medium);
  line-height: 1.5;
  color: var(--text-mention-grey);
}
</style>
