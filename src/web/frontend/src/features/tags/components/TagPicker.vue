<script setup lang="ts">
import type { TagCategory } from '../types'
import { computed, ref } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawerFooter from '@/components/base/CspDrawer/CspDrawerFooter.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import CspTagGroup from '@/components/base/CspTag/CspTagGroup.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTags } from '../composables/useTags'

const props = defineProps<{
  organismeUuid: string
  category: TagCategory
  excludedTagUuids: string[]
  saving?: boolean
}>()

const emit = defineEmits<{
  confirm: [tagUuids: string[]]
  cancel: []
}>()

const { tags, pending, error } = useTags(props.organismeUuid)
const showSkeleton = useMinimumPending(pending)

const availableTags = computed(() =>
  (tags.value ?? [])
    .filter(tag => tag.category === props.category && !props.excludedTagUuids.includes(tag.uuid))
    .sort((a, b) => a.name.localeCompare(b.name, 'fr')),
)

const selectedTagUuids = ref<string[]>([])
const selectedAvailableTagUuids = computed(() =>
  selectedTagUuids.value.filter(tagUuid => availableTags.value.some(({ uuid }) => uuid === tagUuid)),
)
</script>

<template>
  <CspAsyncSection
    :pending="showSkeleton"
    :error="error"
    loading-label="Chargement des étiquettes"
    error-title="Impossible de charger les étiquettes"
  >
    <CspTagGroup
      v-if="availableTags.length > 0"
      v-model="selectedTagUuids"
      type="multiple"
      size="md"
      aria-label="Étiquettes"
    >
      <CspTag
        v-for="tag in availableTags"
        :key="tag.uuid"
        :value="tag.uuid"
        :label="tag.name"
        variant="selectable"
      />
    </CspTagGroup>
    <p
      v-else
      class="tag-picker__empty"
    >
      Aucune étiquette à ajouter.
    </p>
  </CspAsyncSection>

  <CspDrawerFooter>
    <CspButton
      variant="secondary"
      label="Annuler"
      @click="emit('cancel')"
    />
    <CspButton
      label="Ajouter"
      :disabled="selectedAvailableTagUuids.length === 0 || saving"
      @click="emit('confirm', selectedAvailableTagUuids)"
    />
  </CspDrawerFooter>
</template>

<style scoped lang="scss">
.tag-picker__empty {
  margin: 0;
  color: var(--text-mention-grey);
}
</style>
