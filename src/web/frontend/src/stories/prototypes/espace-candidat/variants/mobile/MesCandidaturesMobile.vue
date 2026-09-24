<script setup lang="ts">
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useEspace } from '../../data/useEspace'
import CandidatureListCard from '../../shared/mobile/CandidatureListCard.vue'

defineProps<{
  confirmation?: string | null
}>()

defineEmits<{
  ouvrir: [id: string]
}>()

const espace = useEspace()
</script>

<template>
  <div class="liste">
    <h1 class="liste__titre">
      Mes candidatures
    </h1>

    <CspCallout
      v-if="confirmation"
      variant="success"
      :description="confirmation"
    />

    <CspEmptyState
      v-if="espace.candidatures.length === 0"
      icon="ri:briefcase-line"
      title="Vous n'avez pas encore de candidature"
      description="Les offres auxquelles vous postulez apparaîtront ici."
    />

    <template v-else>
      <section class="liste__section">
        <h2 class="liste__sous-titre">
          En cours ({{ espace.enCours.value.length }})
        </h2>
        <p
          v-if="espace.enCours.value.length === 0"
          class="liste__vide"
        >
          Aucune candidature en cours.
        </p>
        <div
          v-else
          class="liste__cartes"
        >
          <CandidatureListCard
            v-for="candidature in espace.enCours.value"
            :key="candidature.id"
            :candidature="candidature"
            :non-lus="espace.nonLusCandidature(candidature)"
            @ouvrir="$emit('ouvrir', $event)"
          />
        </div>
      </section>

      <details class="liste__terminees">
        <summary>
          <span>Terminées ({{ espace.terminees.value.length }})</span>
          <CspIcon
            name="ri:arrow-down-s-line"
            :size="20"
            class="liste__terminees-icone"
          />
        </summary>
        <p
          v-if="espace.terminees.value.length === 0"
          class="liste__vide"
        >
          Aucune candidature terminée
        </p>
        <div
          v-else
          class="liste__cartes"
        >
          <CandidatureListCard
            v-for="candidature in espace.terminees.value"
            :key="candidature.id"
            :candidature="candidature"
            :non-lus="espace.nonLusCandidature(candidature)"
            @ouvrir="$emit('ouvrir', $event)"
          />
        </div>
      </details>
    </template>
  </div>
</template>

<style scoped lang="scss">
.liste {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  padding: var(--csp-space-4) var(--csp-space-4) var(--csp-space-8);
}

.liste__titre {
  margin: 0;
  font-size: 1.375rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.liste__sous-titre {
  margin: 0 0 var(--csp-space-3);
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.liste__cartes {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.liste__vide {
  margin: var(--csp-space-3) 0 0;
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.liste__terminees {
  summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 2.75rem;
    padding: 0 var(--csp-space-3);
    margin-bottom: var(--csp-space-3);
    border-radius: 0.5rem;
    background-color: var(--background-alt-grey);
    cursor: pointer;
    list-style: none;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-title-grey);

    &::-webkit-details-marker {
      display: none;
    }
  }

  &[open] .liste__terminees-icone {
    transform: rotate(180deg);
  }
}

.liste__terminees-icone {
  transition: transform 0.15s ease;
  color: var(--text-mention-grey);
}
</style>
