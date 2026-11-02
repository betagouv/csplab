<script setup lang="ts">
import type { AgentSearchStatus } from '@/features/agents/composables/useFindOrCreateAgent'
import type { AgentRecherche } from '@/features/agents/types'
import { computed, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawerFooter from '@/components/base/CspDrawer/CspDrawerFooter.vue'
import CspSelectionSummary from '@/components/base/CspSelectionSummary/CspSelectionSummary.vue'
import CspSeparator from '@/components/base/CspSeparator/CspSeparator.vue'
import AgentRechercheForm from '@/features/agents/components/AgentRechercheForm.vue'
import { pluralize } from '@/utils/format'

const props = defineProps<{
  count: number
  summary: string
  editable: boolean
  status: AgentSearchStatus
  agent?: AgentRecherche | null
  searching?: boolean
  submitting?: boolean
}>()

const emit = defineEmits<{
  editSelection: []
  search: [email: string]
  assign: []
  reset: []
  cancel: []
}>()

const email = ref('')

const isSearched = computed(() => props.status !== 'idle')

const submitLabel = computed(() => {
  const creates = props.status === 'not-found'
  if (props.count === 1) {
    return creates ? 'Créer et assigner' : 'Assigner un responsable'
  }
  return `${creates ? 'Créer et assigner' : 'Assigner'} à ${props.count} ${pluralize(props.count, 'recrutement')}`
})

function handleSubmit(): void {
  if (isSearched.value) {
    emit('assign')
  }
}

const formId = useId()
</script>

<template>
  <form
    :id="formId"
    class="assign-responsable-form"
    novalidate
    @submit.prevent="handleSubmit"
  >
    <CspSelectionSummary
      :summary="summary"
      :editable="editable"
      @edit="emit('editSelection')"
    />

    <CspSeparator />

    <AgentRechercheForm
      v-model="email"
      label="Responsable"
      :status="status"
      :agent="agent"
      :searching="searching"
      @search="emit('search', $event)"
      @reset="emit('reset')"
    />
  </form>

  <CspDrawerFooter>
    <CspButton
      variant="secondary"
      type="button"
      label="Annuler"
      @click="emit('cancel')"
    />
    <CspButton
      type="submit"
      :form="formId"
      :label="submitLabel"
      :disabled="!isSearched || submitting"
    />
  </CspDrawerFooter>
</template>

<style scoped lang="scss">
.assign-responsable-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
}
</style>
