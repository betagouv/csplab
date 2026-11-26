<script setup lang="ts">
import type { CspSegmentedControlOption } from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import type { CandidaturesLayoutName } from '@/router/names'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import { CANDIDATURES_LAYOUT_ROUTE_NAMES } from '@/router/names'

const props = defineProps<{
  organismeUuid: string
  recrutementUuid: string
  current: CandidaturesLayoutName
}>()

const router = useRouter()

const OPTIONS: CspSegmentedControlOption<CandidaturesLayoutName>[] = [
  { value: 'kanban', label: 'Kanban', icon: 'ri:table-line' },
  { value: 'liste', label: 'Liste', icon: 'ri:list-unordered' },
]

const layout = computed({
  get: () => props.current,
  set: (value) => {
    if (value === props.current) {
      return
    }
    void router.push({
      name: CANDIDATURES_LAYOUT_ROUTE_NAMES[value],
      params: { organismeUuid: props.organismeUuid, recrutementUuid: props.recrutementUuid },
    })
  },
})
</script>

<template>
  <CspSegmentedControl
    v-model="layout"
    :options="OPTIONS"
    legend="Affichage des candidatures"
    hide-legend
    size="sm"
  />
</template>
