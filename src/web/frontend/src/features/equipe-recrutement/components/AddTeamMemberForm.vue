<script setup lang="ts">
import type { RecrutementRole } from '../types'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import type { AgentSearchStatus } from '@/features/agents/composables/useFindOrCreateAgent'
import type { AgentRecherche } from '@/features/agents/types'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import AgentRechercheForm from '@/features/agents/components/AgentRechercheForm.vue'
import { RECRUTEMENT_ROLE_LABELS } from '../constants/equipe-recrutement'

const props = defineProps<{
  status: AgentSearchStatus
  agent?: AgentRecherche | null
  searching?: boolean
  submitting?: boolean
  emailError?: string
}>()

const emit = defineEmits<{
  search: [email: string]
  add: [role: RecrutementRole]
  reset: []
  cancel: []
}>()

const DEFAULT_ROLE: RecrutementRole = 'contributeur'

const ROLE_OPTIONS: CspRadioGroupOption[] = (
  Object.keys(RECRUTEMENT_ROLE_LABELS) as RecrutementRole[]
).map(role => ({ value: role, label: RECRUTEMENT_ROLE_LABELS[role] }))

const email = ref('')
const role = ref<RecrutementRole>(DEFAULT_ROLE)

const isSearched = computed(() => props.status !== 'idle')

const submitLabel = computed(() => props.status === 'not-found' ? 'Créer et ajouter' : 'Ajouter le membre')

function handleSubmit(): void {
  if (isSearched.value) {
    emit('add', role.value)
  }
}
</script>

<template>
  <form
    class="add-team-member-form"
    novalidate
    @submit.prevent="handleSubmit"
  >
    <AgentRechercheForm
      v-model="email"
      :status="status"
      :agent="agent"
      :searching="searching"
      :error-message="emailError"
      @search="emit('search', $event)"
      @reset="emit('reset')"
    />

    <CspRadioGroup
      v-if="isSearched"
      v-model="role"
      label="Rôle dans le recrutement"
      name="recrutement_role"
      :options="ROLE_OPTIONS"
    />

    <div class="add-team-member-form__actions">
      <CspButton
        variant="secondary"
        type="button"
        label="Annuler"
        @click="emit('cancel')"
      />
      <CspButton
        type="submit"
        :label="submitLabel"
        icon="ri:user-add-line"
        is-icon-left
        :disabled="!isSearched || submitting"
      />
    </div>
  </form>
</template>

<style scoped lang="scss">
.add-team-member-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
}

.add-team-member-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
