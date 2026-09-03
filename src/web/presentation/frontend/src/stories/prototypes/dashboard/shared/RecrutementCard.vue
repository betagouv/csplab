<script setup lang="ts">
import type { RecrutementDashboard } from '../data/dashboardMock'
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'

const props = defineProps<{
  recrutement: RecrutementDashboard
}>()

const emit = defineEmits<{
  open: [id: string]
}>()

const metaItems = computed(() => [
  { icon: 'ri:hashtag', srLabel: 'Référence RenoiRH', label: `Réf. RenoiRH ${props.recrutement.referenceRenoiRH}` },
  { icon: 'ri:building-line', srLabel: 'Service', label: props.recrutement.service },
  { icon: 'ri:file-list-3-line', srLabel: 'Type de contrat', label: props.recrutement.typeContrat },
])

function open() {
  emit('open', props.recrutement.id)
}
</script>

<template>
  <CspCard
    class="recrutement-card"
    size="sm"
    role="button"
    tabindex="0"
    :aria-label="`Voir le recrutement ${recrutement.intitule}, ${recrutement.referenceRenoiRH}`"
    @click="open"
    @keydown.enter="open"
    @keydown.space.prevent="open"
  >
    <template #title>
      {{ recrutement.intitule }}
    </template>

    <template #description>
      <CspMetaList
        :items="metaItems"
        size="sm"
      />
    </template>

    <div class="recrutement-card__candidatures">
      <CspBadge
        v-if="recrutement.nouveauxCV > 0"
        type="new"
        :label="`${recrutement.nouveauxCV} nouveau${recrutement.nouveauxCV > 1 ? 'x' : ''} CV`"
      />
      <span class="recrutement-card__total">
        {{ recrutement.candidaturesTotal }} candidature{{ recrutement.candidaturesTotal > 1 ? 's' : '' }} au total
      </span>
    </div>

    <template #footer>
      <span class="recrutement-card__date">{{ recrutement.datePublicationLabel }}</span>
      <CspButton
        variant="tertiary-no-outline"
        size="sm"
        label="Voir le recrutement"
        icon="ri:arrow-right-line"
        tabindex="-1"
      />
    </template>
  </CspCard>
</template>

<style scoped lang="scss">
.recrutement-card {
  cursor: pointer;

  &:hover {
    background: var(--background-alt-grey-hover);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.recrutement-card__candidatures {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem;
}

.recrutement-card__total {
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.recrutement-card__date {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
  margin-right: auto;
}
</style>
