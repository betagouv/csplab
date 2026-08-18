<script setup lang="ts">
import type { CreateCompteUtilisateurPayload, OrganismeAdmin, UtilisateurSearchResult } from '../types'
import { computed, nextTick, ref, useTemplateRef, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import { useDebounce } from '@/composables/async/useDebounce'
import { searchUtilisateurs } from '../api'
import CompteUtilisateurForm from './CompteUtilisateurForm.vue'

defineProps<{
  organisme: OrganismeAdmin | null
  saving?: boolean
}>()

const emit = defineEmits<{
  assign: [utilisateur: UtilisateurSearchResult]
  create: [payload: CreateCompteUtilisateurPayload]
}>()

const open = defineModel<boolean>('open', { required: true })

const step = ref<'search' | 'creation'>('search')
const searchTerm = ref('')
const selected = ref<string | null>(null)
const results = ref<UtilisateurSearchResult[]>([])
const searching = ref(false)

const stepTitle = useTemplateRef('stepTitle')

watch(open, (isOpen) => {
  if (!isOpen)
    return
  step.value = 'search'
  searchTerm.value = ''
  selected.value = null
  results.value = []
})

const debouncedTerm = useDebounce(searchTerm, 300)

watch(debouncedTerm, async (term) => {
  if (term.trim().length < 2) {
    results.value = []
    return
  }
  searching.value = true
  try {
    results.value = await searchUtilisateurs(term)
  }
  finally {
    searching.value = false
  }
})

const options = computed(() => results.value.map(u => ({
  value: u.uuid,
  label: `${u.prenom} ${u.nom}`,
  description: u.email,
})))

const emailValid = computed(() => /^[^\s@]+@[^\s@][^\s.@]*\.[^\s@]+$/.test(searchTerm.value.trim()))

const actionLabel = computed(() => {
  const term = searchTerm.value.trim()
  if (!emailValid.value)
    return null
  if (results.value.some(u => u.email.toLowerCase() === term.toLowerCase()))
    return null
  return `Créer un compte pour ${term}`
})

const emptyLabel = computed(() =>
  searchTerm.value.trim().length < 2
    ? 'Saisissez au moins 2 caractères'
    : 'Aucun résultat. Saisissez une adresse e-mail complète pour inviter.',
)

watch(selected, (uuid) => {
  if (!uuid)
    return
  const utilisateur = results.value.find(u => u.uuid === uuid)
  if (utilisateur)
    emit('assign', utilisateur)
})

async function goToCreation(): Promise<void> {
  step.value = 'creation'
  await nextTick()
  stepTitle.value?.focus()
}

function backToSearch(): void {
  step.value = 'search'
  selected.value = null
}
</script>

<template>
  <CspDrawer
    v-model:open="open"
    title="Assigner un gestionnaire"
    :description="organisme ? `Le gestionnaire administre les comptes et les paramètres de ${organisme.nom}.` : undefined"
    size="md"
  >
    <div
      v-if="step === 'search'"
      class="gestionnaire-assign"
    >
      <CspCombobox
        v-model="selected"
        v-model:search-term="searchTerm"
        :options="options"
        label="Rechercher une personne"
        hint="Recherchez par nom ou saisissez un e-mail pour créer un compte"
        placeholder="Nom ou adresse e-mail"
        :pending="searching"
        :empty-label="emptyLabel"
        :action-label="actionLabel"
        action-icon="ri:user-add-line"
        @action="goToCreation"
      />
    </div>

    <div
      v-else
      class="gestionnaire-assign"
    >
      <div class="gestionnaire-assign__step-header">
        <CspButton
          variant="tertiary-no-outline"
          size="sm"
          icon="ri:arrow-left-line"
          aria-label="Retour à la recherche"
          @click="backToSearch"
        />
        <h3
          ref="stepTitle"
          class="gestionnaire-assign__step-title"
          tabindex="-1"
        >
          Créer un compte
        </h3>
      </div>

      <CompteUtilisateurForm
        :initial-email="searchTerm.trim()"
        locked-type="gestionnaire"
        submit-label="Créer le compte et l'assigner"
        :saving="saving"
        @submit="payload => emit('create', payload)"
        @cancel="backToSearch"
      />
    </div>
  </CspDrawer>
</template>

<style scoped lang="scss">
.gestionnaire-assign {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  height: 100%;
}

.gestionnaire-assign__step-header {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
}

.gestionnaire-assign__step-title {
  margin: 0;
  font-size: 1rem;

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}
</style>
