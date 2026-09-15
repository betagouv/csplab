<script setup lang="ts">
import type { MembreEquipePayload, RecrutementRole } from '../types'
import type { CspComboboxOption } from '@/components/base/CspCombobox/CspCombobox.vue'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import type { AgentOrganisme } from '@/features/organismes/types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspCombobox from '@/components/base/CspCombobox/CspCombobox.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { RECRUTEMENT_ROLE_LABELS } from '../constants/equipe-recrutement'

const props = defineProps<{
  agents: AgentOrganisme[]
  pendingAgents?: boolean
  submitting?: boolean
}>()

const emit = defineEmits<{
  add: [payload: MembreEquipePayload]
}>()

const open = defineModel<boolean>('open', { required: true })

const DEFAULT_ROLE: RecrutementRole = 'contributeur'

const ROLE_OPTIONS: CspRadioGroupOption[] = (
  Object.keys(RECRUTEMENT_ROLE_LABELS) as RecrutementRole[]
).map(role => ({ value: role, label: RECRUTEMENT_ROLE_LABELS[role] }))

const selectedAgentId = ref<string | null>(null)
const role = ref<RecrutementRole>(DEFAULT_ROLE)

const { search, filtered } = useTextSearch(() => props.agents, agent => [agent.email])

const options = computed<CspComboboxOption[]>(() => filtered.value.map(agent => ({
  value: agent.agent_id,
  label: agent.email,
})))

const aucunAgentDisponible = computed(
  () => !props.pendingAgents && props.agents.length === 0,
)

const submitDisabled = computed(() => !selectedAgentId.value || props.submitting)

watch(open, (isOpen) => {
  if (!isOpen) {
    selectedAgentId.value = null
    role.value = DEFAULT_ROLE
    search.value = ''
  }
})

function handleSubmit(): void {
  if (!selectedAgentId.value)
    return
  emit('add', {
    agent_id: selectedAgentId.value,
    recrutement_role: role.value,
  })
}
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
      <CspCombobox
        v-model="selectedAgentId"
        v-model:search-term="search"
        :options="options"
        label="Membre de l'organisme"
        hint="Seuls les membres de l'organisme peuvent rejoindre l'équipe de recrutement."
        placeholder="Rechercher un courriel"
        name="agent"
        :pending="pendingAgents"
        empty-label="Aucun courriel disponible ne correspond à votre recherche"
      />

      <CspCallout
        v-if="aucunAgentDisponible"
        variant="info"
        title="Aucun membre disponible"
        description="Tous les membres de l'organisme font déjà partie de cette équipe. Rattachez d'abord la personne à l'organisme pour pouvoir l'ajouter ici."
      />

      <CspRadioGroup
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
          type="submit"
          label="Ajouter le membre"
          icon="ri:user-add-line"
          is-icon-left
          :disabled="submitDisabled"
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
