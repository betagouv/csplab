<script setup lang="ts">
import { useRouter } from 'vue-router'
import CspButton from '@/components/base/CspButton/CspButton.vue'

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

function switchTo(view: CandidaturesViewName) {
  if (view === props.current)
    return
  void router.push({
    name: ROUTE_BY_VIEW[view],
    params: { recrutementUuid: props.recrutementUuid },
  })
}
</script>

<template>
  <div
    class="candidatures-view-switch"
    role="group"
    aria-label="Affichage des candidatures"
  >
    <CspButton
      icon="ri:table-line"
      label="Kanban"
      is-icon-left
      size="sm"
      :variant="current === 'kanban' ? 'secondary' : 'tertiary'"
      :aria-pressed="current === 'kanban'"
      @click="switchTo('kanban')"
    />
    <CspButton
      icon="ri:list-unordered"
      label="Liste"
      is-icon-left
      size="sm"
      :variant="current === 'liste' ? 'secondary' : 'tertiary'"
      :aria-pressed="current === 'liste'"
      @click="switchTo('liste')"
    />
  </div>
</template>

<style scoped lang="scss">
.candidatures-view-switch {
  display: inline-flex;
  gap: 0.375rem;
}
</style>
