<script setup lang="ts">
import type { AgentSearchStatus } from '../composables/useAgentParEmail'
import type { AgentRecherche, Role } from '../types'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { ROLE_LABELS } from '../constants/organisme'
import AgentRechercheForm from './AgentRechercheForm.vue'

const props = defineProps<{
  status: AgentSearchStatus
  agent?: AgentRecherche | null
  searching?: boolean
  submitting?: boolean
}>()

const emit = defineEmits<{
  search: [email: string]
  add: [role: Role]
  reset: []
}>()

const open = defineModel<boolean>('open', { required: true })

const ROLE_OPTIONS: CspRadioGroupOption[] = [
  { value: 'agent', label: ROLE_LABELS.agent },
  { value: 'superviseur', label: ROLE_LABELS.superviseur },
]

const email = ref('')
const role = ref<Role>('agent')
const error = ref('')

const isFound = computed(() => props.status === 'found')

const isSearched = computed(() => props.status !== 'idle')

const submitLabel = computed(() => isFound.value ? 'Ajouter le membre' : 'Créer et ajouter')

watch(open, (isOpen) => {
  if (!isOpen) {
    email.value = ''
    role.value = 'agent'
    error.value = ''
  }
})

function handleReset(): void {
  error.value = ''
  emit('reset')
}

function handleSubmit(): void {
  if (isSearched.value)
    emit('add', role.value)
}

function setEmailError(message: string): void {
  error.value = message
}

defineExpose({ setEmailError })
</script>

<template>
  <CspDrawer
    v-model:open="open"
    title="Ajouter un membre"
    size="md"
  >
    <form
      class="attach-agent-drawer"
      novalidate
      @submit.prevent="handleSubmit"
    >
      <AgentRechercheForm
        v-model="email"
        :status="status"
        :agent="agent"
        :searching="searching"
        :error-message="error"
        @search="emit('search', $event)"
        @reset="handleReset"
      />

      <CspRadioGroup
        v-if="isSearched"
        v-model="role"
        label="Rôle dans l'organisme"
        name="role"
        :options="ROLE_OPTIONS"
      />

      <div class="attach-agent-drawer__actions">
        <CspButton
          variant="secondary"
          type="button"
          label="Annuler"
          @click="open = false"
        />
        <CspButton
          v-if="isSearched"
          type="submit"
          :label="submitLabel"
          icon="ri:user-add-line"
          is-icon-left
          :disabled="submitting"
        />
      </div>
    </form>
  </CspDrawer>
</template>

<style scoped lang="scss">
.attach-agent-drawer {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.attach-agent-drawer__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
