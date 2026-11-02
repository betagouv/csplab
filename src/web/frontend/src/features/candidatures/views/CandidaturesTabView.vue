<script setup lang="ts">
import { computed } from 'vue'
import CspEmptyState from '@/components/base/CspEmptyState/CspEmptyState.vue'
import CspErrorState from '@/components/base/CspErrorState/CspErrorState.vue'
import { useRecrutementDetail } from '@/features/recrutements/composables/useRecrutementDetail'
import CandidaturesToolbar from '../components/CandidaturesToolbar.vue'
import { provideCandidaturesFilters } from '../composables/useCandidaturesFilters'
import { provideCandidaturesToolbar } from '../composables/useCandidaturesToolbar'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
}>()

const { recrutementDetail, etapes, pending: pendingDetail, error } = useRecrutementDetail(() => props)

provideCandidaturesFilters(etapes)
provideCandidaturesToolbar()

const loadFailed = computed(() => !pendingDetail.value && Boolean(error.value))

const isNotFound = computed(() =>
  !pendingDetail.value && !error.value && !recrutementDetail.value,
)
</script>

<template>
  <CspErrorState
    v-if="loadFailed"
    title="Une erreur est survenue lors du chargement du recrutement."
  />

  <CspEmptyState
    v-else-if="isNotFound"
    icon="ri:search-line"
    title="Recrutement introuvable"
    description="Ce recrutement n'existe pas ou n'est plus accessible."
  />

  <template v-else>
    <CandidaturesToolbar
      :organisme-uuid="organismeUuid"
      :recrutement-uuid="recrutementUuid"
    />
    <router-view />
  </template>
</template>
