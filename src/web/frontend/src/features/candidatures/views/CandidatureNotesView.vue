<script setup lang="ts">
import type { CandidatureParams } from '@/api/params'
import CandidatureNotes from '../components/CandidatureNotes.vue'
import { useCandidaturePanelRoutes } from '../composables/useCandidaturePanelRoutes'

defineProps<{
  candidature: CandidatureParams
}>()

const { names } = useCandidaturePanelRoutes()
</script>

<template>
  <CandidatureNotes
    :candidature="candidature"
    :routes="names.notes"
  />
</template>
