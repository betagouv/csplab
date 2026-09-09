<script setup lang="ts">
import type { AgentSearchStatus } from '../composables/useAjoutMembre'
import type { AgentRecherche, Role } from '../types'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { ROLE_LABELS } from '../constants/organisme'
import { formatAgentName } from '../format'

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

const EMAIL_PATTERN = /^[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+$/

const ROLE_OPTIONS: CspRadioGroupOption[] = [
  { value: 'membre', label: ROLE_LABELS.membre },
  { value: 'responsable', label: ROLE_LABELS.responsable },
]

const email = ref('')
const role = ref<Role>('membre')
const error = ref('')

const isFound = computed(() => props.status === 'found')

const isSearched = computed(() => props.status !== 'idle')

const submitLabel = computed(() => {
  if (isFound.value)
    return 'Ajouter le membre'
  return isSearched.value ? 'Créer et ajouter' : 'Rechercher'
})

const submitIcon = computed(() =>
  isSearched.value ? 'ri:user-add-line' : 'ri:search-line',
)

const submitDisabled = computed(() => props.searching || props.submitting)

watch(open, (isOpen) => {
  if (!isOpen) {
    email.value = ''
    role.value = 'membre'
    error.value = ''
  }
})

watch(email, () => {
  error.value = ''
  if (props.status !== 'idle')
    emit('reset')
})

function handleSubmit(): void {
  if (isSearched.value) {
    emit('add', role.value)
    return
  }
  const value = email.value.trim()
  if (!EMAIL_PATTERN.test(value)) {
    error.value = 'Renseignez une adresse électronique valide.'
    return
  }
  error.value = ''
  emit('search', value)
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
      <CspInput
        v-model="email"
        label="Adresse électronique de l'agent"
        name="email"
        type="email"
        placeholder="prenom.nom@exemple.gouv.fr"
        autocomplete="off"
        :error="Boolean(error)"
        :error-message="error"
      />

      <div
        v-if="isFound && agent"
        class="attach-agent-drawer__agent"
      >
        <p class="attach-agent-drawer__agent-name">
          {{ formatAgentName(agent) }}
        </p>
        <p class="attach-agent-drawer__agent-detail">
          {{ agent.intitule_poste }}
        </p>
        <p class="attach-agent-drawer__agent-detail">
          {{ agent.email }}
        </p>
      </div>

      <p
        v-else-if="status === 'not-found'"
        class="attach-agent-drawer__hint"
      >
        Aucun compte ne correspond à cette adresse. Un compte sera créé, la personne
        complétera son profil à sa première connexion.
      </p>

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
          type="submit"
          :label="submitLabel"
          :icon="submitIcon"
          is-icon-left
          :disabled="submitDisabled"
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

.attach-agent-drawer__agent {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  border-radius: 0.25rem;
}

.attach-agent-drawer__agent-name {
  margin: 0;
  font-weight: 600;
}

.attach-agent-drawer__agent-detail {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
}

.attach-agent-drawer__hint {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
}

.attach-agent-drawer__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
