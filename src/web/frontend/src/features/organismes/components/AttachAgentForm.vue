<script setup lang="ts">
import type { Role } from '../types'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import type { AgentSearchStatus } from '@/features/agents/composables/useFindOrCreateAgent'
import type { AgentRecherche } from '@/features/agents/types'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import AgentRechercheForm from '@/features/agents/components/AgentRechercheForm.vue'
import { ROLE_LABELS } from '../constants/organisme'

const props = defineProps<{
  status: AgentSearchStatus
  agent?: AgentRecherche | null
  searching?: boolean
  submitting?: boolean
  emailError?: string
}>()

const emit = defineEmits<{
  search: [email: string]
  add: [role: Role]
  reset: []
  cancel: []
}>()

const ROLE_OPTIONS: CspRadioGroupOption[] = [
  { value: 'agent', label: ROLE_LABELS.agent },
  { value: 'superviseur', label: ROLE_LABELS.superviseur },
]

const email = ref('')
const role = ref<Role>('agent')

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
    class="attach-agent-form"
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
      label="Rôle dans l'organisme"
      name="role"
      :options="ROLE_OPTIONS"
    />

    <div class="attach-agent-form__actions">
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
.attach-agent-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
}

.attach-agent-form__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
