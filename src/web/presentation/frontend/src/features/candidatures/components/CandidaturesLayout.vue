<script setup lang="ts">
import type { RecrutementDetailKanban } from '../types'
import type { CandidaturesViewName } from './CandidaturesViewSwitch.vue'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import CspMetaList from '@/components/base/CspMeta/CspMetaList.vue'
import CspPageHeader from '@/components/layout/CspPageHeader/CspPageHeader.vue'
import { formatRecrutementMeta } from '../format'
import CandidaturesViewSwitch from './CandidaturesViewSwitch.vue'

const props = defineProps<{
  recrutementUuid: string
  recrutementDetail: RecrutementDetailKanban | null | undefined
  currentView: CandidaturesViewName
  pending: boolean
  error: unknown
}>()

const title = computed(() => props.recrutementDetail?.intitule ?? 'Candidatures')

const breadcrumb = computed<CspBreadcrumbItem[]>(() => [
  { label: 'Accueil', to: { name: 'home' } },
  { label: 'Mes recrutements', to: { name: 'mes-recrutements' } },
  { label: title.value },
])

const metaItems = computed(() =>
  props.recrutementDetail ? formatRecrutementMeta(props.recrutementDetail) : [],
)

const isNotFound = computed(() =>
  !props.pending && (Boolean(props.error) || !props.recrutementDetail),
)
</script>

<template>
  <div class="candidatures-layout">
    <CspPageHeader
      :title="title"
      :breadcrumb="breadcrumb"
      class="candidatures-layout__header"
    >
      <template #actions>
        <CandidaturesViewSwitch
          :recrutement-uuid="recrutementUuid"
          :current="currentView"
        />
      </template>
    </CspPageHeader>

    <CspMetaList
      v-if="recrutementDetail"
      :items="metaItems"
      class="candidatures-layout__meta"
    />

    <div
      v-if="pending"
      class="candidatures-layout__status"
    >
      Chargement des candidatures...
    </div>

    <div
      v-else-if="isNotFound"
      class="candidatures-layout__status candidatures-layout__status--error"
    >
      Recrutement introuvable.
    </div>

    <template v-else>
      <slot />
    </template>
  </div>
</template>

<style scoped lang="scss">
.candidatures-layout {
  padding: 2rem;
}

.candidatures-layout__header {
  margin-bottom: var(--csp-space-4);
}

.candidatures-layout__meta {
  margin-bottom: var(--csp-space-4);
}

.candidatures-layout__status {
  color: var(--text-mention-grey);
}

.candidatures-layout__status--error {
  color: var(--text-default-error);
}
</style>
