<script setup lang="ts">
import { computed } from 'vue'
import MessagesSection from '@/features/messages/components/MessagesSection.vue'
import { useCandidatureDetail } from '../composables/useCandidatureDetail'
import { useCandidaturePanelRoutes } from '../composables/useCandidaturePanelRoutes'
import { formatCandidatName } from '../format'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
  candidatureUuid: string
}>()

const candidatureParams = computed(() => ({
  organismeUuid: props.organismeUuid,
  recrutementUuid: props.recrutementUuid,
  candidatureUuid: props.candidatureUuid,
}))
const { candidature } = useCandidatureDetail(() => candidatureParams.value)
const { names } = useCandidaturePanelRoutes()
</script>

<template>
  <MessagesSection
    v-if="candidature"
    :candidature="candidatureParams"
    :candidat-nom="formatCandidatName(candidature.candidat)"
    :routes="names.conversations"
  />
</template>
