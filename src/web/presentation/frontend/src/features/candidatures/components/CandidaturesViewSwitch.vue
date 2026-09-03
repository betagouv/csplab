<script setup lang="ts">
import type { CspSegmentedControlOption } from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'

export type CandidaturesViewName = 'liste' | 'kanban'

const props = defineProps<{
  recrutementUuid: string
  current: CandidaturesViewName
}>()

const router = useRouter()

const ROUTE_BY_VIEW: Record<CandidaturesViewName, string> = {
  kanban: 'recrutement-candidatures-kanban',
  liste: 'recrutement-candidatures',
}

const OPTIONS: CspSegmentedControlOption<CandidaturesViewName>[] = [
  { value: 'kanban', label: 'Kanban', icon: 'ri:table-line' },
  { value: 'liste', label: 'Liste', icon: 'ri:list-unordered' },
]

const view = computed({
  get: () => props.current,
  set: (value) => {
    if (value === props.current)
      return
    void router.push({
      name: ROUTE_BY_VIEW[value],
      params: { recrutementUuid: props.recrutementUuid },
    })
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
