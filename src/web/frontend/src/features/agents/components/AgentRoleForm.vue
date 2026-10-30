<script setup lang="ts" generic="R extends string">
import type { CspRadioGroupOption } from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawerFooter from '@/components/base/CspDrawer/CspDrawerFooter.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'

const props = defineProps<{
  email: string
  role: R
  roleLabel: string
  options: (CspRadioGroupOption & { value: R })[]
  submitting?: boolean
}>()

const emit = defineEmits<{
  submit: [role: R]
  cancel: []
}>()

const formId = useId()
const selectedRole = ref<string>(props.role)

function handleSubmit(): void {
  const option = props.options.find(({ value }) => value === selectedRole.value)
  if (option) {
    emit('submit', option.value)
  }
}
</script>

<template>
  <form
    :id="formId"
    class="agent-role-form"
    novalidate
    @submit.prevent="handleSubmit"
  >
    <div class="agent-role-form__member">
      <p class="agent-role-form__label">
        Courriel
      </p>
      <p class="agent-role-form__email">
        {{ email }}
      </p>
    </div>

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

.agent-role-form__member {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-field-legend-gap);
}

.agent-role-form__label {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: 600;
  color: var(--text-default-grey);
}

.agent-role-form__email {
  margin: 0;
  overflow-wrap: anywhere;
}
</style>
