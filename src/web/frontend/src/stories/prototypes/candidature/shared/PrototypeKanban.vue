<script setup lang="ts">
import type { ProtoCandidature, ProtoEtape } from '../data/mock'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { CATEGORIE_CONFIG } from '@/features/etapes-recrutement/constants/etape-recrutement'
import { formatElapsedDays } from '@/utils/date'
import { formatCandidatNom } from './format'

defineProps<{
  etapes: ProtoEtape[]
  candidatureOf: (uuid: string) => ProtoCandidature | null
  openUuid: string | null
}>()

const emit = defineEmits<{
  open: [uuid: string]
}>()
</script>

<template>
  <div class="proto-kanban">
    <section
      v-for="etape in etapes"
      :key="etape.uuid"
      class="proto-kanban__column"
      :class="`proto-kanban__column--${CATEGORIE_CONFIG[etape.categorie].cssModifier}`"
    >
      <header class="proto-kanban__header">
        <h2 class="proto-kanban__title">
          <span>{{ etape.nom }}</span>
          <CspBadge
            size="md"
            :label="String(etape.candidatureUuids.length)"
          />
        </h2>
      </header>
      <ul class="proto-kanban__cards">
        <li
          v-for="uuid in etape.candidatureUuids"
          :key="uuid"
        >
          <CspCard
            v-if="candidatureOf(uuid)"
            as="div"
            size="sm"
            role="button"
            tabindex="0"
            class="proto-kanban__card"
            :class="{ 'proto-kanban__card--open': uuid === openUuid }"
            :title="formatCandidatNom(candidatureOf(uuid)!.candidat)"
            @click="emit('open', uuid)"
            @keydown.enter.prevent="emit('open', uuid)"
            @keydown.space.prevent="emit('open', uuid)"
          >
            <p class="proto-kanban__date">
              <CspIcon
                name="ri:calendar-line"
                :size="14"
                aria-hidden="true"
              />
              {{ formatElapsedDays(candidatureOf(uuid)!.dateSoumission) }}
            </p>
          </CspCard>
        </li>
      </ul>
      <footer class="proto-kanban__hint">
        <p class="proto-kanban__hint-label">
          Statut visible par le candidat
        </p>
        <CspBadge
          size="sm"
          :icon="CATEGORIE_CONFIG[etape.categorie].icon"
          :type="CATEGORIE_CONFIG[etape.categorie].type"
          :label="CATEGORIE_CONFIG[etape.categorie].label"
        />
      </footer>
    </section>
  </div>
</template>

<style scoped lang="scss">
.proto-kanban {
  display: flex;
  flex: 1;
  gap: var(--csp-space-3);
  overflow-x: auto;
  padding-bottom: var(--csp-space-2);
  min-height: 0;
}

.proto-kanban__column {
  display: flex;
  flex-direction: column;
  flex: 0 0 18.75rem;
  gap: var(--csp-space-3);
  min-height: 12rem;
  max-height: 100%;
  padding: var(--csp-space-3);
  background-color: var(--background-alt-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  border-top: 3px solid var(--border-default-grey);
}

.proto-kanban__column--en-cours {
  border-top-color: var(--border-plain-info);
}

.proto-kanban__column--refus {
  border-top-color: var(--border-plain-error);
}

.proto-kanban__column--accepte {
  border-top-color: var(--border-plain-success);
}

.proto-kanban__header {
  padding: 0 var(--csp-space-1);
}

.proto-kanban__title {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.proto-kanban__cards {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
  overflow-y: auto;
  min-height: 0;
}

.proto-kanban__card {
  box-shadow:
    0 1px 2px rgb(0 0 0 / 6%),
    inset 0 0 0 1px var(--border-default-grey);
  cursor: pointer;

  &:hover {
    background-color: var(--background-default-grey-hover);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.proto-kanban__card--open {
  box-shadow: inset 0 0 0 2px var(--border-action-high-blue-france);
}

.proto-kanban__date {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: var(--csp-space-2) 0 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.proto-kanban__hint {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-2);
  margin-top: auto;
  padding: var(--csp-space-3) var(--csp-space-1) 0;
  border-top: 1px solid var(--border-default-grey);
}

.proto-kanban__hint-label {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}
</style>
