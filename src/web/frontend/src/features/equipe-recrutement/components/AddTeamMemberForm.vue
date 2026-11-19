<script setup lang="ts">
import type { RecrutementRole } from '../types'
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import type { AgentSearchStatus } from '@/features/agents/composables/useFindOrCreateAgent'
import type { AgentRecherche } from '@/features/agents/types'
import { computed, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawerFooter from '@/components/base/CspDrawer/CspDrawerFooter.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import AgentRechercheForm from '@/features/agents/components/AgentRechercheForm.vue'
import TagSelect from '@/features/tags/components/TagSelect.vue'

const props = defineProps<{
  options: CspRadioGroupOption<RecrutementRole>[]
  status: AgentSearchStatus
  agent?: AgentRecherche | null
  searching?: boolean
  submitting?: boolean
  emailError?: string
  organismeUuid: string
  tagsEditable: boolean
}>()

const emit = defineEmits<{
  search: [email: string]
  add: [role: RecrutementRole, tagUuid: string | null]
  reset: []
  cancel: []
}>()

const DEFAULT_ROLE: RecrutementRole = 'contributeur'

const email = ref('')
const role = ref<RecrutementRole>(DEFAULT_ROLE)
const tagUuid = ref<string | null>(null)

const isSearched = computed(() => props.status !== 'idle')

const submitLabel = computed(() => props.status === 'not-found' ? 'Créer et ajouter' : 'Ajouter le membre')

function handleSubmit(): void {
  if (isSearched.value) {
    emit('add', role.value, tagUuid.value)
  }
}

const formId = useId()
</script>

<template>
  <form
    :id="formId"
    class="add-team-member-form"
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
      label="Rôle dans le recrutement"
      name="recrutement_role"
      :options="options"
    />

    <TagSelect
      v-if="isSearched && tagsEditable"
      v-model="tagUuid"
      :organisme-uuid="organismeUuid"
      category="recrutement_agent"
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
      type="submit"
      :form="formId"
      :label="submitLabel"
      icon="ri:user-add-line"
      is-icon-left
      :disabled="!isSearched || submitting"
    />
  </CspDrawerFooter>
</template>

<style scoped lang="scss">
.add-team-member-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
}
</style>
