<script setup lang="ts">
import type { RecrutementRole } from '../types'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import type { AgentSearchStatus } from '@/features/organismes/composables/useAgentParEmail'
import type { AgentRecherche } from '@/features/organismes/types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import AgentRechercheForm from '@/features/organismes/components/AgentRechercheForm.vue'
import { RECRUTEMENT_ROLE_LABELS } from '../constants/equipe-recrutement'

const props = defineProps<{
  status: AgentSearchStatus
  agent?: AgentRecherche | null
  searching?: boolean
  submitting?: boolean
}>()

const emit = defineEmits<{
  search: [email: string]
  add: [role: RecrutementRole]
  reset: []
}>()

const open = defineModel<boolean>('open', { required: true })

const DEFAULT_ROLE: RecrutementRole = 'contributeur'

const ROLE_OPTIONS: CspRadioGroupOption[] = (
  Object.keys(RECRUTEMENT_ROLE_LABELS) as RecrutementRole[]
).map(role => ({ value: role, label: RECRUTEMENT_ROLE_LABELS[role] }))

const email = ref('')
const role = ref<RecrutementRole>(DEFAULT_ROLE)
const error = ref('')

const isFound = computed(() => props.status === 'found')

const isSearched = computed(() => props.status !== 'idle')

const submitLabel = computed(() => isFound.value ? 'Ajouter le membre' : 'Créer et ajouter')

watch(open, (isOpen) => {
  if (!isOpen) {
    email.value = ''
    role.value = DEFAULT_ROLE
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
      class="ajout-membre-equipe-drawer"
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
        label="Rôle dans le recrutement"
        name="recrutement_role"
        :options="ROLE_OPTIONS"
      />

      <div class="ajout-membre-equipe-drawer__actions">
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
.ajout-membre-equipe-drawer {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.ajout-membre-equipe-drawer__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
