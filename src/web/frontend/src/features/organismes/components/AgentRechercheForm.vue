<script setup lang="ts">
import type { AgentSearchStatus } from '../composables/useAgentParEmail'
import type { AgentRecherche } from '../types'
import { computed, ref, watch } from 'vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import { formatAgentName } from '../format'

const props = withDefaults(defineProps<{
  status: AgentSearchStatus
  agent?: AgentRecherche | null
  searching?: boolean
  errorMessage?: string
  label?: string
}>(), {
  agent: null,
  errorMessage: '',
  label: 'Adresse électronique de l\'agent',
})

const emit = defineEmits<{
  search: [email: string]
  reset: []
}>()

const email = defineModel<string>({ default: '' })

const EMAIL_PATTERN = /^[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+$/

const formatError = ref('')

const error = computed(() => props.errorMessage || formatError.value)

watch(email, () => {
  formatError.value = ''
  if (props.status !== 'idle') {
    emit('reset')
  }
})

function handleSearch(value: string): void {
  if (!EMAIL_PATTERN.test(value)) {
    formatError.value = 'Renseignez une adresse électronique valide.'
    return
  }
  formatError.value = ''
  emit('search', value)
}
</script>

<template>
  <CspSearchBar
    v-model="email"
    :label="label"
    hint="Saisissez l'adresse complète du compte de l'agent."
    name="email"
    placeholder="prenom.nom@exemple.gouv.fr"
    :disabled="searching"
    :error="Boolean(error)"
    :error-message="error"
    @search="handleSearch"
  />

  <div
    v-if="status === 'found' && agent"
    class="agent-recherche-form__agent"
  >
    <p class="agent-recherche-form__agent-name">
      {{ formatAgentName(agent) || agent.email }}
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
    Aucun compte ne correspond à cette adresse. Un compte sera créé, la personne
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
