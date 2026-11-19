<script setup lang="ts">
import { ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawerFooter from '@/components/base/CspDrawer/CspDrawerFooter.vue'
import AgentEmail from '@/features/agents/components/AgentEmail.vue'
import TagSelect from '@/features/tags/components/TagSelect.vue'

const props = defineProps<{
  organismeUuid: string
  email: string
  tagUuid: string | null
  submitting?: boolean
}>()

const emit = defineEmits<{
  submit: [tagUuid: string | null]
  cancel: []
}>()

const formId = useId()
const selectedTag = ref<string | null>(props.tagUuid)
</script>

<template>
  <form
    :id="formId"
    class="membre-tag-form"
    novalidate
    @submit.prevent="emit('submit', selectedTag)"
  >
    <AgentEmail :email="email" />

    <TagSelect
      v-model="selectedTag"
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
      label="Enregistrer les modifications"
      icon="ri:save-3-line"
      is-icon-left
      :disabled="selectedTag === tagUuid || submitting"
    />
  </CspDrawerFooter>
</template>

<style scoped lang="scss">
.membre-tag-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
}
</style>
