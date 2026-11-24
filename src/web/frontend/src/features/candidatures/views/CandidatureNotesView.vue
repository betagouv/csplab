<script setup lang="ts">
import { computed } from 'vue'
import CandidatureNotes from '../components/CandidatureNotes.vue'
import { useCandidaturePanelRoutes } from '../composables/useCandidaturePanelRoutes'

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
const { names } = useCandidaturePanelRoutes()
</script>

<template>
  <CandidatureNotes
    :candidature="candidatureParams"
    :routes="names.notes"
  />
</template>
