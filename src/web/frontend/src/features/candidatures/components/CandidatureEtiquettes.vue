<script setup lang="ts">
import type { CandidatureParams } from '@/api/params'
import type { TagSummary } from '@/features/tags/types'
import { computed, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'
import TagList from '@/features/tags/components/TagList.vue'
import TagPicker from '@/features/tags/components/TagPicker.vue'
import { useTagChanges } from '@/features/tags/composables/useTagChanges'
import { useCandidatureTags } from '../composables/useCandidatureTags'
import CandidatureAsideTitle from './CandidatureAsideTitle.vue'

const props = defineProps<{
  candidature: CandidatureParams
  tags: TagSummary[]
  editable: boolean
}>()

const titleId = useId()
const { addTag, removeTag } = useCandidatureTags(() => props.candidature)

const pickerOpen = ref(false)
const appliedTagUuids = computed(() => props.tags.map(({ uuid }) => uuid))
const { addingTagUuid, submitAdd, submitRemove } = useTagChanges({
  deletedTitle: 'L\'étiquette a été supprimée',
  onDeleted: () => {
    pickerOpen.value = false
  },
})

function handleAdd(tagUuid: string): void {
  void submitAdd(tagUuid, () => addTag(tagUuid))
}

function handleRemove(tag: TagSummary): void {
  void submitRemove(() => removeTag(tag.uuid))
}
</script>

<template>
  <section
    v-if="editable || tags.length > 0"
    :aria-labelledby="titleId"
    class="candidature-etiquettes"
  >
    <CandidatureAsideTitle :id="titleId">
      Étiquettes
    </CandidatureAsideTitle>
    <div class="candidature-etiquettes__tags">
      <TagList
        v-if="tags.length > 0"
        :tags="tags"
        :dismiss-label="editable ? tag => `Retirer l'étiquette ${tag.name}` : undefined"
        aria-label="Étiquettes de la candidature"
        class="candidature-etiquettes__list"
        @dismiss="handleRemove"
      />
      <CspPopover
        v-if="editable"
        v-model:open="pickerOpen"
        side="bottom"
        align="start"
      >
        <template #trigger>
          <CspButton
            label="Ajouter"
            icon="ri:add-line"
            is-icon-left
            variant="tertiary-no-outline"
            size="sm"
            aria-label="Ajouter une étiquette à la candidature"
          />
        </template>
        <TagPicker
          :organisme-uuid="candidature.organismeUuid"
          category="candidature"
          :applied-tag-uuids="appliedTagUuids"
          :adding-tag-uuid="addingTagUuid"
          @add="handleAdd"
        />
      </CspPopover>
    </div>
  </section>
</template>

<style scoped lang="scss">
.candidature-etiquettes {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.candidature-etiquettes__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  align-items: center;
}

.candidature-etiquettes__list {
  display: contents;
}
</style>
