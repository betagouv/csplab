<script setup lang="ts">
import type { Candidature } from '../types'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useReturnTo } from '@/composables/navigation/useReturnTo'
import { formatElapsedDays } from '@/utils/date'
import { useCandidatures } from '../composables/useCandidatures'
import { formatCandidatNom } from '../utils/candidat'

const route = useRoute()

const { findCandidature, pendingKanban, error } = useCandidatures()

const candidature = computed<Candidature | null>(() => findCandidature(route.params.candidatureUuid as string))

const showSkeleton = useMinimumPending(computed(() => pendingKanban.value && !candidature.value))
const loadFailed = computed(() => !pendingKanban.value && Boolean(error.value))
const isNotFound = computed(() => !pendingKanban.value && !error.value && !candidature.value)

const title = computed(() => candidature.value ? formatCandidatNom(candidature.value.candidat) : 'Candidature')
const description = computed(() =>
  candidature.value ? `Candidature ${formatElapsedDays(candidature.value.date_soumission)}` : null,
)

const close = useReturnTo(() => ({
  name: 'recrutement-candidatures-kanban',
  params: { organismeUuid: route.params.organismeUuid, recrutementUuid: route.params.recrutementUuid },
}))

function handleUpdateOpen(open: boolean): void {
  if (!open)
    close()
}
</script>

<template>
  <CspDrawer
    :open="true"
    :modal="false"
    :show-close="false"
    aria-label="Candidature"
    class="candidature-panel"
    @update:open="handleUpdateOpen"
    @interact-outside="(event: Event) => event.preventDefault()"
  >
    <template #start>
      <CspButton
        variant="tertiary-no-outline"
        size="sm"
        icon="ri:arrow-left-line"
        aria-label="Fermer la candidature et revenir au kanban"
        @click="close"
      />
    </template>

    <template #title>
      <CspSkeleton
        v-if="showSkeleton"
        width="12rem"
        height="1.375rem"
      />
      <template v-else>
        {{ title }}
      </template>
    </template>

    <template
      v-if="showSkeleton || description"
      #description
    >
      <CspSkeleton
        v-if="showSkeleton"
        width="9rem"
        height="1.25rem"
      />
      <template v-else>
        {{ description }}
      </template>
    </template>

    <CspErrorState
      v-if="loadFailed"
      title="Une erreur est survenue lors du chargement de la candidature."
    />

    <CspEmptyState
      v-else-if="isNotFound"
      icon="ri:search-line"
      title="Candidature introuvable"
      description="Cette candidature n'existe pas ou n'est plus accessible."
    />
  </CspDrawer>
</template>

<style lang="scss">
@use '@/styles/breakpoints' as bp;

/* unscoped: the drawer content is portaled */
.csp-drawer.candidature-panel {
  --base-drawer-width: 100vw;

  @include bp.from(bp.$lg) {
    --base-drawer-width: calc(100vw - 15rem);
  }

  @include bp.from(bp.$xl) {
    --base-drawer-width: clamp(42rem, 100vw - 36rem, 90rem);
  }
}
</style>
