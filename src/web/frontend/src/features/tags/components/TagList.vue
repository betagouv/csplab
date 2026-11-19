<script setup lang="ts" generic="T extends TagSummary">
import type { TagSummary } from '../types'
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'
import { tagPaletteColor } from '../format'

const props = defineProps<{
  tags: T[]
  editLabel?: (tag: T) => string
  dismissLabel?: (tag: T) => string
}>()

const emit = defineEmits<{
  edit: [tag: T]
  dismiss: [tag: T]
}>()
</script>

<template>
  <ul class="tag-list">
    <li
      v-for="tag in tags"
      :key="tag.uuid"
    >
      <CspLabel
        :label="tag.name"
        :color="tagPaletteColor(tag)"
        :clickable="props.editLabel !== undefined"
        :aria-label="props.editLabel?.(tag)"
        :dismiss-label="props.dismissLabel?.(tag)"
        @click="props.editLabel && emit('edit', tag)"
        @dismiss="emit('dismiss', tag)"
      />
    </li>
  </ul>
</template>

<style scoped lang="scss">
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}
</style>
