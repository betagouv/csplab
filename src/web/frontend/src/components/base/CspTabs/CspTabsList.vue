<script setup lang="ts">
import type { CspTabItem } from './CspTabs.vue'
import { injectTabsRootContext, TabsList, TabsTrigger } from 'reka-ui'
import { nextTick, onMounted, useTemplateRef, watch } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

defineProps<{
  tabs: CspTabItem[]
}>()

const root = injectTabsRootContext()
const list = useTemplateRef<InstanceType<typeof TabsList>>('list')

// Scrolls an overflowing list to the current trigger, as the script of the DSFR does, without scrolling the page
function revealCurrent() {
  const element: HTMLElement | undefined = list.value?.$el
  const current = element?.querySelector<HTMLElement>('[data-state="active"]')
  if (!element || !current) {
    return
  }
  const inset = Number.parseFloat(getComputedStyle(element).scrollPaddingInlineStart) || 0
  const start = current.offsetLeft - inset
  const end = current.offsetLeft + current.offsetWidth + inset - element.clientWidth
  if (start < element.scrollLeft) {
    element.scrollLeft = start
  }
  else if (end > element.scrollLeft) {
    element.scrollLeft = end
  }
}

onMounted(revealCurrent)
watch(root.modelValue, () => nextTick(revealCurrent))
</script>

<template>
  <TabsList
    ref="list"
    class="csp-tabs__list"
  >
    <TabsTrigger
      v-for="tab in tabs"
      :key="tab.value"
      :value="tab.value"
      :disabled="tab.disabled"
      class="csp-tabs__trigger"
    >
      <CspIcon
        v-if="tab.icon"
        :name="tab.icon"
        class="csp-tabs__icon"
      />
      {{ tab.label }}
    </TabsTrigger>
  </TabsList>
</template>

<style scoped lang="scss">
.csp-tabs__list {
  --csp-tabs-overflow-shadow-width: 2rem;
  --csp-tabs-frame: calc(var(--csp-tabs-framed) * var(--csp-tabs-frame-width));
  // The frame and the overline of the triggers belong to framed tabs. Unframed, their inset shadows of zero width keep a
  // transparent colour: Firefox draws a hairline for them on a high-density screen
  --csp-tabs-frame-color: color-mix(in srgb, var(--csp-divider-color) calc(var(--csp-tabs-framed) * 100%), transparent);
  --csp-tabs-overline-color: color-mix(
    in srgb,
    var(--border-active-blue-france) calc(var(--csp-tabs-framed) * 100%),
    transparent
  );
  --csp-tabs-divider: calc((1 - var(--csp-tabs-framed)) * var(--csp-tabs-list-border-width, 1px));
  // Room for a focus ring drawn outside the triggers, compensated below by the margin of the list; above, a scroll
  // container or a clipping parent, such as the page or the drawer, would cut the ring
  --csp-tabs-focus-space: max(0px, var(--csp-tabs-focus-offset) + var(--csp-focus-ring-width));
  // Aligns the trigger labels with content inset by --csp-tabs-content-padding-inline
  --csp-tabs-list-padding-inline: max(
    0px,
    var(--csp-tabs-content-padding-inline, 0px) - var(--csp-tabs-trigger-padding-inline)
  );

  position: relative;
  z-index: 1;
  display: flex;
  gap: var(--csp-tabs-gap);
  margin-block: 0 calc(-1 * var(--csp-tabs-focus-space));
  // The divider of an unframed list fills the last pixel row of the bottom padding
  padding: var(--csp-tabs-focus-space) var(--csp-tabs-list-padding-inline)
    calc(var(--csp-tabs-focus-space) + var(--csp-tabs-divider));
  overflow-x: auto;
  scrollbar-width: thin;
  scroll-padding-inline: var(--csp-tabs-overflow-shadow-width);
  // A framed list draws its line under the triggers, where the current trigger covers it; an unframed list draws its
  // divider over the box set by --csp-tabs-list-divider-box
  background:
    linear-gradient(var(--csp-divider-color), var(--csp-divider-color)) left 0 bottom var(--csp-tabs-focus-space) / 100%
      var(--csp-tabs-frame) no-repeat padding-box padding-box,
    linear-gradient(var(--csp-divider-color), var(--csp-divider-color)) left bottom / 100% var(--csp-tabs-divider)
      no-repeat var(--csp-tabs-list-divider-box) var(--csp-tabs-list-divider-box);

  // Shadows on the edges where triggers overflow, like the DSFR draws them, while the list scrolls; a sticky element
  // stops at the padding of its scroll container, which the negative offsets cross
  &::before,
  &::after {
    content: '';
    position: sticky;
    flex: 0 0 var(--csp-tabs-overflow-shadow-width);
    opacity: 0;
    pointer-events: none;
  }

  &::before {
    left: calc(-1 * var(--csp-tabs-list-padding-inline));
    margin-inline-end: calc(-1 * (var(--csp-tabs-overflow-shadow-width) + var(--csp-tabs-gap)));
    box-shadow: inset var(--csp-tabs-overflow-shadow-width) 0 1.5rem calc(-1 * var(--csp-tabs-overflow-shadow-width))
      var(--csp-tabs-overflow-shadow-color);
  }

  &::after {
    right: calc(-1 * var(--csp-tabs-list-padding-inline));
    margin-inline-start: calc(-1 * (var(--csp-tabs-overflow-shadow-width) + var(--csp-tabs-gap)));
    box-shadow: inset calc(-1 * var(--csp-tabs-overflow-shadow-width)) 0 1.5rem
      calc(-1 * var(--csp-tabs-overflow-shadow-width)) var(--csp-tabs-overflow-shadow-color);
  }

  // Without scroll-driven animations, the keyframes would run on the document timeline and leave the start shadow on
  // for good: such a browser draws no shadow
  @supports (animation-timeline: scroll()) {
    &::before,
    &::after {
      animation: linear both;
      animation-timeline: scroll(nearest inline);
    }

    &::before {
      animation-name: csp-tabs-overflow-start;
    }

    &::after {
      animation-name: csp-tabs-overflow-end;
    }
  }

  &[data-orientation='vertical'] {
    flex-direction: column;
    margin-block: 0;
    padding: 0;
    border-right: 1px solid var(--csp-divider-color);
    background: none;

    &::before,
    &::after {
      display: none;
    }
  }
}

@keyframes csp-tabs-overflow-start {
  from {
    opacity: 0;
  }

  2%,
  to {
    opacity: 1;
  }
}

@keyframes csp-tabs-overflow-end {
  from,
  98% {
    opacity: 1;
  }

  to {
    opacity: 0;
  }
}

.csp-tabs__trigger {
  display: inline-flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
  gap: 0.5rem;
  padding: var(--csp-tabs-trigger-padding-block) var(--csp-tabs-trigger-padding-inline);
  font-size: var(--csp-tabs-trigger-size);
  font-weight: var(--csp-tabs-trigger-weight);
  line-height: var(--csp-tabs-trigger-line-height);
  color: var(--csp-tabs-trigger-color);
  background-color: var(--csp-tabs-trigger-background);
  background-clip: var(--csp-tabs-trigger-background-clip, border-box);
  border: none;
  border-bottom: var(--csp-tabs-underline-width) solid transparent;
  border-radius: var(--csp-tabs-trigger-radius) var(--csp-tabs-trigger-radius) 0 0;
  box-shadow: inset 0 calc(-1 * var(--csp-tabs-frame)) 0 var(--csp-tabs-frame-color);
  cursor: pointer;

  &:hover:not([data-disabled]) {
    background-color: var(--csp-tabs-trigger-background-hover);
  }

  &:active:not([data-disabled]) {
    background-color: var(--csp-tabs-trigger-background-active);
  }

  // Without specificity, so that forced colours keep their underline
  &:where(:hover:not([data-disabled], [data-state='active'])) {
    border-bottom-color: var(--csp-tabs-trigger-border-color-hover);
  }

  &[data-state='active'] {
    color: var(--text-active-blue-france);
    // A shorthand: the background of the current trigger may draw its own lines in gradient layers
    background: var(--csp-tabs-trigger-background-current);
    border-bottom-color: var(--csp-tabs-trigger-border-color-current, var(--border-action-high-blue-france));
    box-shadow:
      inset 0 var(--csp-tabs-overline-width) 0 var(--csp-tabs-overline-color),
      inset var(--csp-tabs-frame) 0 0 var(--csp-tabs-frame-color),
      inset calc(-1 * var(--csp-tabs-frame)) 0 0 var(--csp-tabs-frame-color);

    &:hover:not([data-disabled]) {
      background-color: var(--csp-tabs-trigger-background-current-hover);
    }

    &:active:not([data-disabled]) {
      background-color: var(--background-default-grey-active);
    }
  }

  &[data-disabled] {
    color: var(--text-disabled-grey);
    background-color: var(--csp-tabs-trigger-background-disabled);
    cursor: not-allowed;
  }

  &:focus-visible {
    outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
    outline-offset: var(--csp-tabs-focus-offset);
  }

  // System colors would draw the reserved bottom border of every tab: only the active tab keeps it
  @media (forced-colors: active) {
    &:not([data-state='active']) {
      border-bottom-color: var(--csp-tabs-trigger-border-bottom-color-forced);
    }
  }

  &[data-orientation='vertical'] {
    justify-content: flex-start;
    border-bottom: none;
    border-right: 2px solid transparent;
    box-shadow: none;

    &[data-state='active'] {
      border-bottom-color: transparent;
      box-shadow: none;
      border-right-color: var(--border-action-high-blue-france);
    }
  }
}

// Forced colours remove box shadows and gradients: an unframed list draws its divider as a border, and framed triggers
// take the borders that the DSFR gives them in this mode, and overlap by 1px the top border that the panel below the
// list draws
@media (forced-colors: active) {
  .csp-tabs__list:not([data-orientation='vertical']) {
    margin-bottom: calc(-1 * (var(--csp-tabs-focus-space) + var(--csp-tabs-framed) * 1px));
    padding-bottom: var(--csp-tabs-focus-space);
    border-bottom: var(--csp-tabs-divider) solid var(--csp-divider-color);
  }

  .csp-tabs__trigger:not([data-orientation='vertical']) {
    border-top: calc(var(--csp-tabs-framed) * 1px) solid;
    border-inline: calc(var(--csp-tabs-framed) * 1px) solid;
    border-bottom-width: max(var(--csp-tabs-underline-width), calc(var(--csp-tabs-framed) * 1px));
  }

  .csp-tabs__trigger[data-state='active']:not([data-orientation='vertical']) {
    border-top-width: calc(var(--csp-tabs-framed) * 4px);
    border-top-color: Highlight;
    border-inline-color: Highlight;
    border-bottom-color: var(--csp-tabs-trigger-border-bottom-color-current-forced);
    color: var(--csp-tabs-trigger-color-current-forced);
  }
}

.csp-tabs__icon {
  width: 1.125em;
  height: 1.125em;
  flex-shrink: 0;
}
</style>
