<script setup lang="ts">
import type { AgentSearchStatus } from '../composables/useFindOrCreateAgent'
import type { AgentRecherche } from '../types'
import { computed, ref } from 'vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import { formatAgentLabel } from '../format'

const props = withDefaults(defineProps<{
  status: AgentSearchStatus
  agent?: AgentRecherche | null
  searching?: boolean
  errorMessage?: string
  label?: string
  hint?: string
}>(), {
  agent: null,
  errorMessage: '',
  label: 'Courriel de l\'agent',
  hint: undefined,
})

const emit = defineEmits<{
  search: [email: string]
  reset: []
}>()

const email = defineModel<string>({ default: '' })

const EMAIL_PATTERN = /^[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+$/

const formatError = ref('')

const error = computed(() => props.errorMessage || formatError.value)

function handleInput(value: string): void {
  email.value = value
  formatError.value = ''
  if (props.status !== 'idle') {
    emit('reset')
  }
}

function handleSearch(value: string): void {
  if (!EMAIL_PATTERN.test(value)) {
    formatError.value = 'Renseignez un courriel valide.'
    return
  }
  formatError.value = ''
  emit('search', value)
}
</script>

<template>
  <CspSearchBar
    :model-value="email"
    :label="label"
    :hint="hint"
    name="email"
    placeholder="prenom.nom@exemple.gouv.fr"
    :disabled="searching"
    :error="Boolean(error)"
    :error-message="error"
    @update:model-value="handleInput"
    @search="handleSearch"
  />

  <div
    v-if="status === 'found' && agent"
    class="agent-recherche-form__agent"
  >
    <p class="agent-recherche-form__agent-name">
      {{ formatAgentLabel(agent) }}
    </p>
    <p class="agent-recherche-form__agent-detail">
      {{ agent.intitule_poste }}
    </p>
    <p class="agent-recherche-form__agent-detail">
      {{ agent.email }}
    </p>
  </div>

  <p
    v-else-if="status === 'not-found'"
    class="agent-recherche-form__hint"
  >
    Aucun compte ne correspond à ce courriel. Un compte sera créé, la personne
    complétera son profil à sa première connexion.
  </p>
</template>

<style scoped lang="scss">
.agent-recherche-form__agent {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  border-radius: 0.25rem;
}

.agent-recherche-form__agent-name {
  margin: 0;
  font-weight: 600;
}

.agent-recherche-form__agent-detail {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
}

.agent-recherche-form__hint {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: 0.875rem;
}
</style>
