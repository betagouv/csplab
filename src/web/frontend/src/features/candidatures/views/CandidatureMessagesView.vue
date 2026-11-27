<script setup lang="ts">
import type { CandidatureParams } from '@/api/params'
import MessagesSection from '@/features/messages/components/MessagesSection.vue'
import { useCandidatureDetail } from '../composables/useCandidatureDetail'
import { useCandidaturePanelRoutes } from '../composables/useCandidaturePanelRoutes'
import { formatCandidatName } from '../format'

const props = defineProps<{
  candidature: CandidatureParams
}>()

const { candidature: detail } = useCandidatureDetail(() => props.candidature)
const { names } = useCandidaturePanelRoutes()
</script>

<template>
  <MessagesSection
    v-if="detail"
    :candidature="candidature"
    :candidat-nom="formatCandidatName(detail.candidat)"
    :routes="names.conversations"
  />
</template>
