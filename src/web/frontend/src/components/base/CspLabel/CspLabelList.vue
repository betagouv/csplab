<script setup lang="ts">
import type { CspLabelItem } from './types'
import { computed, nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch } from 'vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'
import CspTooltip from '@/components/base/CspTooltip/CspTooltip.vue'
import { paletteVar } from '@/styles/palette'
import { pluralize } from '@/utils/format'
import CspLabel from './CspLabel.vue'

const props = withDefaults(defineProps<{
  labels: CspLabelItem[]
  maxLines?: number
  size?: 'sm' | 'md'
  removable?: boolean
}>(), {
  maxLines: undefined,
  size: 'sm',
  removable: false,
})

const emit = defineEmits<{
  remove: [label: CspLabelItem]
}>()

const measure = useTemplateRef<HTMLElement>('measure')
const visibleCount = ref(props.labels.length)
const isPopoverOpen = ref(false)
const isTooltipOpen = ref(false)

const visibleLabels = computed(() => props.labels.slice(0, visibleCount.value))
const hiddenLabels = computed(() => props.labels.slice(visibleCount.value))
const hiddenNames = computed(() => hiddenLabels.value.map(({ label }) => label).join(', '))
const stripColors = computed(() => [...new Set(props.labels.map(({ color }) => color))])
const moreLabel = computed(() => {
  const count = hiddenLabels.value.length
  return `${count} ${pluralize(count, 'autre étiquette', 'autres étiquettes')} : ${hiddenNames.value}`
})

// The open popover already shows the hidden labels: the tooltip stays closed meanwhile
function updateTooltipOpen(open: boolean | undefined): void {
  isTooltipOpen.value = Boolean(open) && !isPopoverOpen.value
}

// Every visible label fits whole: when the first one does not fit next to « +N », « +N » alone gives every label
function computeVisibleCount(): void {
  const container = measure.value
  if (!container || !props.maxLines) {
    visibleCount.value = props.labels.length
    return
  }
  const box = container.getBoundingClientRect()
  const items = [...container.querySelectorAll<HTMLElement>('[data-label-item]')].map(item => item.getBoundingClientRect())
  const lineTops = [...new Set(items.map(item => Math.round(item.top)))].sort((a, b) => a - b)
  if (lineTops.length <= props.maxLines && items.every(item => item.right - box.left <= box.width)) {
    visibleCount.value = items.length
    return
  }
  const lastLineTop = lineTops[Math.min(props.maxLines, lineTops.length) - 1]!
  const moreWidth = container.querySelector<HTMLElement>('[data-label-more]')?.getBoundingClientRect().width ?? 0
  const gap = Number.parseFloat(getComputedStyle(container).columnGap) || 0
  let count = items.filter(item => Math.round(item.top) <= lastLineTop).length
  while (count > 0) {
    const last = items[count - 1]!
    const fitsMore = last.right - box.left + gap + moreWidth <= box.width
    if (Math.round(last.top) < lastLineTop || fitsMore) {
      break
    }
    count -= 1
  }
  visibleCount.value = count
}

let observer: ResizeObserver | undefined

onMounted(() => {
  computeVisibleCount()
  void document.fonts.ready.then(computeVisibleCount)
  observer = new ResizeObserver(() => computeVisibleCount())
  if (measure.value) {
    observer.observe(measure.value)
  }
})

onBeforeUnmount(() => observer?.disconnect())

watch(() => [props.labels, props.maxLines], () => nextTick(computeVisibleCount), { deep: true })
</script>

<template>
  <div
    class="csp-label-list"
    :class="`csp-label-list--${size}`"
  >
    <span
      class="csp-label-list__strip"
      aria-hidden="true"
    >
      <span
        v-for="color in stripColors"
        :key="color"
        :style="{ '--csp-label-list-strip-color': paletteVar(color, 'dot') }"
      />
    </span>
    <ul
      ref="measure"
      class="csp-label-list__items csp-label-list__items--measure"
      aria-hidden="true"
      inert
    >
      <li
        v-for="item in labels"
        :key="item.label"
        data-label-item
      >
        <CspLabel
          :label="item.label"
          :color="item.color"
          :size="size"
          :removable="removable"
        />
      </li>
      <li data-label-more>
        <button
          type="button"
          class="csp-label-list__more"
          :class="`csp-label-list__more--${size}`"
        >
          +{{ labels.length }}
        </button>
      </li>
    </ul>
    <ul
      class="csp-label-list__items"
      :class="{ 'csp-label-list__items--single-line': maxLines === 1 }"
    >
      <li
        v-for="item in visibleLabels"
        :key="item.label"
      >
        <CspLabel
          :label="item.label"
          :color="item.color"
          :size="size"
          :removable="removable"
          @remove="emit('remove', item)"
        />
      </li>
      <li
        v-if="hiddenLabels.length"
        class="csp-label-list__more-item"
      >
        <CspTooltip
          :open="isTooltipOpen"
          :content="hiddenNames"
          side="top"
          @update:open="updateTooltipOpen"
        >
          <CspPopover
            v-model:open="isPopoverOpen"
            side="top"
            align="center"
          >
            <template #trigger>
              <button
                type="button"
                class="csp-label-list__more"
                :class="`csp-label-list__more--${size}`"
                :aria-label="moreLabel"
              >
                +{{ hiddenLabels.length }}
              </button>
            </template>
            <ul class="csp-label-list__items">
              <li
                v-for="item in hiddenLabels"
                :key="item.label"
              >
                <CspLabel
                  :label="item.label"
                  :color="item.color"
                  :size="size"
                />
              </li>
            </ul>
          </CspPopover>
          <template #content>
            <span class="csp-label-list__hidden-names">{{ hiddenNames }}</span>
            <span
              class="csp-label-list__hidden-labels"
              aria-hidden="true"
            >
              <CspLabel
                v-for="item in hiddenLabels"
                :key="item.label"
                :label="item.label"
                :color="item.color"
                :size="size"
              />
            </span>
          </template>
        </CspTooltip>
      </li>
    </ul>
  </div>
</template>

<style scoped lang="scss">
/* The hidden copy shares the grid cell of the list: no positioning, so a parent link overlay stays above the labels */
.csp-label-list {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  align-content: start;
  min-width: 0;
}

.csp-label-list__items {
  display: flex;
  flex-wrap: wrap;
  grid-area: 1 / 1;
  align-content: flex-start;
  align-items: center;
  gap: var(--csp-space-1);
  min-width: 0;
  margin: 0;
  padding: 0;
  list-style: none;

  > li {
    display: flex;
    align-items: center;
    min-width: 0;
  }
}

.csp-label-list--md .csp-label-list__items {
  gap: var(--csp-space-2);
}

.csp-label-list__items--single-line {
  flex-wrap: nowrap;
}

.csp-label-list__more-item {
  flex-shrink: 0;
}

/* The hidden copy keeps each label at its whole width, which tells whether it fits */
.csp-label-list__items--measure {
  align-self: start;
  height: 0;
  overflow: hidden;
  visibility: hidden;

  > li {
    flex-shrink: 0;
  }
}

.csp-label-list__more {
  display: inline-flex;
  align-items: center;
  padding: 0.125rem 0.375rem;
  border: none;
  border-radius: var(--csp-label-radius, var(--csp-badge-radius));
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  background: transparent;
  color: var(--text-mention-grey);
  font-size: 0.75rem;
  font-weight: var(--csp-font-weight-medium);
  line-height: var(--csp-line-height-tight);
  cursor: pointer;

  &:hover {
    background-color: var(--background-default-grey-hover);
  }

  &:active {
    background-color: var(--background-default-grey-active);
  }

  &:focus-visible {
    outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
    outline-offset: var(--csp-focus-ring-offset);
  }
}

/* A theme may show the hidden labels themselves in the tooltip, in place of their names */
.csp-label-list__hidden-labels {
  display: none;
}

/* A theme may draw one band per colour of the labels along the edge of the card that holds the list */
.csp-label-list__strip {
  display: none;
}

.csp-label-list__more--md {
  padding: 0.1875rem 0.5rem;
  font-size: 0.875rem;
}
</style>
