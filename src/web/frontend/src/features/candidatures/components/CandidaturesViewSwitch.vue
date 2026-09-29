<script setup lang="ts">
import type { CandidaturesViewName } from '../composables/useCandidaturesView'
import type { CspSegmentedControlOption } from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import { candidaturesViewQuery } from '../composables/useCandidaturesView'

const props = defineProps<{
  current: CandidaturesViewName
}>()

const router = useRouter()

const OPTIONS: CspSegmentedControlOption<CandidaturesViewName>[] = [
  { value: 'kanban', label: 'Kanban', icon: 'ri:table-line' },
  { value: 'liste', label: 'Liste', icon: 'ri:list-unordered' },
]

const view = computed({
  get: () => props.current,
  set: (value) => {
    if (value === props.current)
      return
    void router.push({ query: candidaturesViewQuery(value) })
  },
})
</script>

<template>
  <CspSegmentedControl
    v-model="view"
    :options="OPTIONS"
    legend="Affichage des candidatures"
    hide-legend
    size="sm"
  />
</template>
