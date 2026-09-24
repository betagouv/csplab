<script setup lang="ts">
import type { ScenarioKey } from '../data/scenario'
import type { PersonId, Settings } from '../shared/types'
import type { Messagerie } from '../shared/useMessagerie'
import { useMessagerie } from '../shared/useMessagerie'
import ThreadColumn from './ThreadColumn.vue'

export interface ColumnSpec {
  label: string
  scenario: ScenarioKey
  conversationId?: string
  viewerId: Extract<PersonId, 'jean-marc' | 'karim'>
  settings: Settings
}

const props = withDefaults(defineProps<{
  columns: ColumnSpec[]
  height?: string
}>(), {
  height: '46rem',
})

const messageries = new Map<ScenarioKey, Messagerie>()

function messagerieOf(scenario: ScenarioKey): Messagerie {
  let messagerie = messageries.get(scenario)
  if (!messagerie) {
    messagerie = useMessagerie(scenario)
    messageries.set(scenario, messagerie)
  }
  return messagerie
}

for (const column of props.columns) {
  const messagerie = messagerieOf(column.scenario)
  if (column.conversationId)
    messagerie.selectedId.value = column.conversationId
}
</script>

<template>
  <div
    class="side-by-side"
    :style="{ '--thread-column-height': height }"
  >
    <ThreadColumn
      v-for="column in columns"
      :key="column.label"
      :label="column.label"
      :messagerie="messagerieOf(column.scenario)"
      :viewer-id="column.viewerId"
      :settings="column.settings"
    />
  </div>
</template>

<style scoped>
.side-by-side {
  display: flex;
  gap: var(--csp-space-6);
  align-items: flex-start;
  padding: var(--csp-space-6);
  overflow-x: auto;
  background: var(--background-alt-grey);
}
</style>
