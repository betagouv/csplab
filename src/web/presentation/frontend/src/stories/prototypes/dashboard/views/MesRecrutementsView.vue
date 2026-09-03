<script setup lang="ts">
import type { RecrutementDashboard } from '../data/dashboardMock'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import CspPageContainer from '@/components/layout/CspPageContainer/CspPageContainer.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import RecrutementCard from '../shared/RecrutementCard.vue'

const props = defineProps<{
  recrutements: RecrutementDashboard[]
  focusRecrutementId: string | null
}>()

const emit = defineEmits<{
  open: [id: string]
}>()

const BREADCRUMB: CspBreadcrumbItem[] = [
  { label: 'Accueil' },
  { label: 'Mes recrutements' },
]

const recrutementsTries = computed(() => {
  return [...props.recrutements].sort((a, b) => b.nouveauxCV - a.nouveauxCV)
})

const nouveauxCVTotal = computed(() => props.recrutements.reduce((acc, r) => acc + r.nouveauxCV, 0))
</script>

<template>
  <CspPageHeader
    title="Mes recrutements"
    :breadcrumb="BREADCRUMB"
  >
    <template #subtitle>
      <p class="mrv__subtitle">
        {{ recrutements.length }} recrutements, {{ nouveauxCVTotal }} nouveaux CV à traiter au total.
      </p>
    </template>
  </CspPageHeader>

  <CspPageContainer width="wide">
    <ul class="mrv__list">
      <li
        v-for="recrutement in recrutementsTries"
        :key="recrutement.id"
        :class="{ 'mrv__item--focus': recrutement.id === focusRecrutementId }"
      >
        <RecrutementCard
          :recrutement="recrutement"
          @open="emit('open', $event)"
        />
      </li>
    </ul>
  </CspPageContainer>
</template>

<style scoped lang="scss">
.mrv__subtitle {
  margin: 0;
  color: var(--text-mention-grey);
}

.mrv__list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.mrv__item--focus {
  animation: mrv-focus-flash 2s ease-out;
  border-radius: 0.5rem;
}

@keyframes mrv-focus-flash {
  0%,
  40% {
    box-shadow: 0 0 0 2px var(--border-active-blue-france);
  }
  100% {
    box-shadow: 0 0 0 2px transparent;
  }
}
</style>
