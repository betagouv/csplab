<script setup lang="ts">
import type { Role } from '../types'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { ROLE_LABELS } from '../constants/organisme'

defineProps<{
  submitting?: boolean
}>()

const emit = defineEmits<{
  attach: [payload: { agent_id: string, role: Role }]
}>()

const open = defineModel<boolean>('open', { required: true })

const AGENT_ID_PATTERN = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

const ROLE_OPTIONS: CspRadioGroupOption[] = [
  { value: 'membre', label: ROLE_LABELS.membre },
  { value: 'responsable', label: ROLE_LABELS.responsable },
]

const agentId = ref('')
const role = ref<Role>('membre')
const error = ref('')

watch(open, (isOpen) => {
  if (!isOpen) {
    agentId.value = ''
    role.value = 'membre'
    error.value = ''
  }
})

watch(agentId, () => {
  error.value = ''
})

function handleSubmit() {
  const value = agentId.value.trim()
  if (!AGENT_ID_PATTERN.test(value)) {
    error.value = 'Renseignez l\'identifiant de l\'agent, au format 8-4-4-4-12 caractères.'
    return
  }
  error.value = ''
  emit('attach', { agent_id: value, role: role.value })
}

function setAgentIdError(message: string): void {
  error.value = message
}

defineExpose({ setAgentIdError })
</script>

<template>
  <CspDrawer
    v-model:open="open"
    title="Ajouter un membre"
    size="md"
  >
    <form
      class="attach-agent-drawer"
      @submit.prevent="handleSubmit"
    >
      <CspInput
        v-model="agentId"
        label="Identifiant de l'agent"
        name="agent-id"
        placeholder="00000000-0000-0000-0000-000000000000"
        autocomplete="off"
        :error="Boolean(error)"
        :error-message="error"
      />

      <CspRadioGroup
        v-model="role"
        label="Rôle dans l'organisme"
        name="role"
        :options="ROLE_OPTIONS"
      />

      <div class="attach-agent-drawer__actions">
        <CspButton
          variant="secondary"
          label="Annuler"
          @click="open = false"
        />
        <CspButton
          type="submit"
          label="Ajouter le membre"
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
