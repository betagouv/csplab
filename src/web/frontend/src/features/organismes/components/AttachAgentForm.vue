<script setup lang="ts">
import type { Role } from '../types'
import type { AgentSearchStatus } from '@/features/agents/composables/useFindOrCreateAgent'
import type { AgentRecherche } from '@/features/agents/types'
import { computed, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawerFooter from '@/components/base/CspDrawer/CspDrawerFooter.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import AgentRechercheForm from '@/features/agents/components/AgentRechercheForm.vue'
import { ROLE_OPTIONS } from '../constants/organisme'

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

const email = ref('')
const role = ref<Role>('agent')

const isFound = computed(() => props.status === 'found')

const isSearched = computed(() => props.status !== 'idle')

const submitLabel = computed(() => isFound.value ? 'Ajouter le membre' : 'Créer et ajouter')

function handleSubmit(): void {
  if (isSearched.value) {
    emit('add', role.value)
  }
}

const formId = useId()
</script>

<template>
  <form
    :id="formId"
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
  </form>

  <CspDrawerFooter>
    <CspButton
      variant="secondary"
      type="button"
      label="Annuler"
      @click="emit('cancel')"
    />
    <CspButton
      v-if="isSearched"
      type="submit"
      :form="formId"
      :label="submitLabel"
      icon="ri:user-add-line"
      is-icon-left
      :disabled="submitting"
    />
  </CspDrawerFooter>
</template>

<style scoped lang="scss">
.attach-agent-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
}
</style>
