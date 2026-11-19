<script setup lang="ts" generic="R extends string">
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawerFooter from '@/components/base/CspDrawer/CspDrawerFooter.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import AgentEmail from './AgentEmail.vue'

const props = defineProps<{
  email: string
  role: R
  roleLabel: string
  options: CspRadioGroupOption<R>[]
  submitting?: boolean
}>()

const emit = defineEmits<{
  submit: [role: R]
  cancel: []
}>()

const formId = useId()
const selectedRole = ref<R>(props.role)

function handleSubmit(): void {
  emit('submit', selectedRole.value)
}
</script>

<template>
  <form
    :id="formId"
    class="agent-role-form"
    novalidate
    @submit.prevent="handleSubmit"
  >
    <AgentEmail :email="email" />

    <CspRadioGroup
      v-model="selectedRole"
      :label="roleLabel"
      name="role"
      :options="options"
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
      label="Enregistrer les modifications"
      icon="ri:save-3-line"
      is-icon-left
      :disabled="selectedRole === role || submitting"
    />
  </CspDrawerFooter>
</template>

<style scoped lang="scss">
.agent-role-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
}
</style>
