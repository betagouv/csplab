<script setup lang="ts" generic="T extends TagSummary">
import type { TagSummary } from '../types'
import { computed, useTemplateRef } from 'vue'
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'
import CspTooltip from '@/components/base/CspTooltip/CspTooltip.vue'
import { useFittingCount } from '@/composables/ui/useFittingCount'
import { pluralize } from '@/utils/format'
import { tagPaletteColor } from '../format'

const props = defineProps<{
  tags: T[]
  maxLines?: number
  editLabel?: (tag: T) => string
  dismissLabel?: (tag: T) => string
}>()

const emit = defineEmits<{
  edit: [tag: T]
  dismiss: [tag: T]
}>()

const measure = useTemplateRef<HTMLElement>('measure')
const visibleCount = useFittingCount(measure, () => props.tags, () => props.maxLines)

const visibleTags = computed(() => props.tags.slice(0, visibleCount.value))
const hiddenTags = computed(() => props.tags.slice(visibleCount.value))
const hiddenNames = computed(() => hiddenTags.value.map(({ name }) => name).join(', '))
const moreLabel = computed(() => {
  const count = hiddenTags.value.length
  return `${count} ${pluralize(count, 'autre étiquette', 'autres étiquettes')}`
})
</script>

<template>
  <ul
    class="tag-list"
    :class="{ 'tag-list--bounded': maxLines, 'tag-list--single-line': maxLines === 1 }"
  >
    <li
      v-if="maxLines"
      class="tag-list__measure"
      aria-hidden="true"
      inert
    >
      <div
        ref="measure"
        class="tag-list__measure-row"
      >
        <span
          v-for="tag in tags"
          :key="tag.uuid"
          data-fitting-item
        >
          <CspLabel
            :label="tag.name"
            :color="tagPaletteColor(tag)"
            :dismiss-label="props.dismissLabel?.(tag)"
          />
        </span>
        <CspLabel
          data-fitting-more
          :label="`+${tags.length}`"
          :dot="false"
          outlined
        />
      </div>
    </li>
    <li
      v-for="tag in visibleTags"
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
    <li
      v-if="hiddenTags.length > 0"
      class="tag-list__more-item"
    >
      <CspTooltip
        :content="hiddenNames"
        side="top"
      >
        <button
          type="button"
          class="tag-list__more"
          :aria-label="moreLabel"
        >
          <CspLabel
            :label="`+${hiddenTags.length}`"
            :dot="false"
            outlined
          />
        </button>
      </CspTooltip>
    </li>
  </ul>
</template>

<style scoped lang="scss">
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  align-items: center;
  margin: 0;
  padding: 0;
  list-style: none;

  > li {
    display: flex;
  }
}

// the measured width comes from the parent, whatever tags are visible
.tag-list--bounded {
  position: relative;
  contain: inline-size;
}

.tag-list--single-line {
  flex-wrap: nowrap;

  > li {
    min-width: 0;
  }

  > .tag-list__more-item {
    flex-shrink: 0;
  }
}

.tag-list__measure {
  position: absolute;
  inset: 0 0 auto;
  height: 0;
  overflow: hidden;
  visibility: hidden;
  pointer-events: none;
}

.tag-list__measure-row {
  display: flex;
  width: 100%;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}

.tag-list__more {
  display: inline-flex;
  padding: 0;
  border: 0;
  background: none;
  cursor: default;

  &:focus-visible {
    outline: var(--focus-ring);
    outline-offset: var(--csp-focus-ring-offset);
  }
}
</style>
