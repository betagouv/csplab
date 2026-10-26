<script setup lang="ts">
import type { CreateTagPayload, TagCategory, TagColor } from '../types'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { DEFAULT_TAG_COLOR, TAG_CATEGORY_OPTIONS_ORDER, TAG_CATEGORY_TEXTS, TAG_COLOR_ACCENTS, TAG_COLOR_LABELS, TAG_NAME_MAX_LENGTH } from '../constants/tag'

const props = defineProps<{
  category: TagCategory
  saving?: boolean
}>()

const emit = defineEmits<{
  create: [payload: CreateTagPayload]
}>()

const open = defineModel<boolean>('open', { required: true })

const FORBIDDEN_CHARACTERS = /[<>\p{Extended_Pictographic}]/u

const name = ref('')
const category = ref<string>(props.category)
const color = ref<string>(DEFAULT_TAG_COLOR)
const nameError = ref<string | null>(null)

watch(open, (isOpen) => {
  if (!isOpen) {
    return
  }
  name.value = ''
  category.value = props.category
  color.value = DEFAULT_TAG_COLOR
  nameError.value = null
}, { immediate: true })

watch(name, (value) => {
  nameError.value = FORBIDDEN_CHARACTERS.test(value)
    ? 'Les émojis et les caractères < > ne sont pas autorisés.'
    : null
})

const CATEGORY_OPTIONS = TAG_CATEGORY_OPTIONS_ORDER.map(value => ({ value, label: TAG_CATEGORY_TEXTS[value].option }))

const COLOR_OPTIONS = Object.entries(TAG_COLOR_LABELS).map(([value, label]) => ({ value, label }))

const trimmedName = computed(() => name.value.trim())

const canSubmit = computed(() => trimmedName.value.length > 0 && !nameError.value)

function handleSubmit(): void {
  if (!canSubmit.value || props.saving) {
    return
  }
  emit('create', {
    name: trimmedName.value,
    category: category.value as TagCategory,
    color: color.value as TagColor,
  })
}

function setNameError(message: string): void {
  nameError.value = message
}

defineExpose({ setNameError })
</script>

<template>
  <CspDrawer
    v-model:open="open"
    title="Ajouter une étiquette"
    size="md"
  >
    <form
      class="tag-form"
      @submit.prevent="handleSubmit"
    >
      <CspInput
        v-model="name"
        label="Libellé"
        name="name"
        :hint="`${TAG_NAME_MAX_LENGTH} caractères maximum`"
        :maxlength="TAG_NAME_MAX_LENGTH"
        :error="Boolean(nameError)"
        :error-message="nameError ?? undefined"
      />

      <CspRadioGroup
        v-model="category"
        label="Type d'étiquette"
        name="category"
        :options="CATEGORY_OPTIONS"
      />

      <CspSelect
        v-model="color"
        label="Couleur"
        :options="COLOR_OPTIONS"
      />

      <div class="tag-form__preview">
        <p class="tag-form__preview-label">
          Aperçu
        </p>
        <CspTag
          :label="trimmedName || 'Libellé'"
          :accent="TAG_COLOR_ACCENTS[color as TagColor]"
        />
      </div>

      <div class="tag-form__actions">
        <CspButton
          type="submit"
          label="Enregistrer"
          :disabled="!canSubmit || saving"
        />
        <CspButton
          variant="secondary"
          type="button"
          label="Annuler"
          @click="open = false"
        />
      </div>
    </form>
  </CspDrawer>
</template>

<style scoped lang="scss">
.tag-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
  height: 100%;
}

.tag-form__preview {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-field-label-gap);
}

.tag-form__preview-label {
  margin: 0;
  font-size: var(--csp-font-size-base);
  font-weight: 600;
}

.tag-form__actions {
  margin-top: auto;
  display: flex;
  justify-content: flex-end;
  gap: var(--csp-space-3);
  padding-top: var(--csp-space-4);
  border-top: 1px solid var(--border-default-grey);
}
</style>
