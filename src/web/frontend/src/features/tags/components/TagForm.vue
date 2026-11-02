<script setup lang="ts">
import type { CreateTagPayload, Tag, TagCategory, TagColor } from '../types'
import { computed, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawerFooter from '@/components/base/CspDrawer/CspDrawerFooter.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { DEFAULT_TAG_COLOR, TAG_CATEGORY_OPTIONS_ORDER, TAG_CATEGORY_TEXTS, TAG_COLOR_LABELS, TAG_COLOR_PALETTE, TAG_NAME_MAX_LENGTH } from '../constants/tag'

const props = defineProps<{
  category: TagCategory
  tag?: Tag | null
  saving?: boolean
  duplicate?: CreateTagPayload | null
}>()

const emit = defineEmits<{
  save: [payload: CreateTagPayload]
  cancel: []
}>()

const FORBIDDEN_CHARACTERS = /[<>\p{Extended_Pictographic}]/u

const CATEGORY_OPTIONS = TAG_CATEGORY_OPTIONS_ORDER.map(value => ({ value, label: TAG_CATEGORY_TEXTS[value].option }))

const COLOR_OPTIONS = Object.entries(TAG_COLOR_LABELS).map(([value, label]) => ({ value, label }))

const name = ref(props.tag?.name ?? '')
const category = ref<string>(props.tag?.category ?? props.category)
const color = ref<string>(props.tag?.color ?? DEFAULT_TAG_COLOR)

const trimmedName = computed(() => name.value.trim())

const nameError = computed(() => {
  if (FORBIDDEN_CHARACTERS.test(name.value)) {
    return 'Les émojis et les caractères < > ne sont pas autorisés.'
  }
  if (props.duplicate?.name.toLocaleLowerCase() === trimmedName.value.toLocaleLowerCase() && props.duplicate.category === category.value) {
    return 'Une étiquette de ce type porte déjà ce libellé.'
  }
  return null
})

const canSubmit = computed(() => trimmedName.value.length > 0 && !nameError.value)

function handleSubmit(): void {
  if (!canSubmit.value || props.saving) {
    return
  }
  emit('save', {
    name: trimmedName.value,
    category: category.value as TagCategory,
    color: color.value as TagColor,
  })
}

const formId = useId()
</script>

<template>
  <form
    :id="formId"
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

    <div
      v-if="tag"
      class="tag-form__field"
    >
      <p class="tag-form__field-label">
        Type d'étiquette
      </p>
      <p class="tag-form__field-value">
        {{ TAG_CATEGORY_TEXTS[tag.category].option }}
      </p>
    </div>
    <CspRadioGroup
      v-else
      v-model="category"
      label="Type d'étiquette"
      name="category"
      :options="CATEGORY_OPTIONS"
    />

    <CspRadioGroup
      v-model="color"
      label="Couleur"
      name="color"
      :options="COLOR_OPTIONS"
      :columns="2"
    >
      <template #option="{ option }">
        <CspLabel
          :label="option.label"
          :color="TAG_COLOR_PALETTE[option.value as TagColor]"
          size="md"
        />
      </template>
    </CspRadioGroup>

    <div class="tag-form__field">
      <p class="tag-form__field-label">
        Aperçu
      </p>
      <CspLabel
        :label="trimmedName || 'Libellé'"
        :color="TAG_COLOR_PALETTE[color as TagColor]"
      />
    </div>
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
      label="Enregistrer"
      :disabled="!canSubmit || saving"
    />
  </CspDrawerFooter>
</template>

<style scoped lang="scss">
.tag-form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
}

.tag-form__field {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-field-label-gap);
}

.tag-form__field-label,
.tag-form__field-value {
  margin: 0;
  font-size: var(--csp-font-size-base);
}

.tag-form__field-label {
  font-weight: 600;
}
</style>
