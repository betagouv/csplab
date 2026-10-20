<script setup lang="ts">
import type { CspPictogramName } from '@/components/base/CspPictogram/pictograms'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspPictogram from '@/components/base/CspPictogram/CspPictogram.vue'

withDefaults(defineProps<{
  title: string
  description?: string
  icon?: string
  pictogram?: CspPictogramName
}>(), {
  description: undefined,
  icon: 'ri:inbox-2-line',
  pictogram: undefined,
})
</script>

<template>
  <div
    class="csp-empty-state"
    :class="{ 'csp-empty-state--has-pictogram': pictogram }"
  >
    <CspPictogram
      v-if="pictogram"
      class="csp-empty-state__pictogram"
      :name="pictogram"
    />
    <CspIcon
      :name="icon"
      :size="24"
      class="csp-empty-state__icon"
    />
    <p class="csp-empty-state__title">
      {{ title }}
    </p>
    <p
      v-if="description"
      class="csp-empty-state__description"
    >
      {{ description }}
    </p>
    <div
      v-if="$slots.action"
      class="csp-empty-state__action"
    >
      <slot name="action" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.csp-empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--csp-empty-state-gap);
  padding: var(--csp-empty-state-padding-block) var(--csp-space-4);
  background: var(--csp-empty-state-backdrop), var(--csp-empty-state-background);
  border-radius: var(--csp-frame-radius, 0);
  box-shadow: inset 0 0 0 var(--csp-empty-state-frame-width) var(--border-default-grey);
  text-align: center;
}

.csp-empty-state__icon {
  box-sizing: content-box;
  padding: var(--csp-empty-state-icon-padding);
  background-color: var(--csp-empty-state-icon-background);
  border-radius: var(--csp-empty-state-icon-radius);
  color: var(--csp-empty-state-icon-color);
}

/* the parent selector outweighs the display of the pictogram root, whatever the order of the stylesheets */
.csp-empty-state > .csp-empty-state__pictogram {
  display: var(--csp-empty-state-pictogram-display);
  width: var(--csp-empty-state-pictogram-size);
  height: var(--csp-empty-state-pictogram-size);
}

.csp-empty-state--has-pictogram .csp-empty-state__icon {
  display: var(--csp-empty-state-icon-display-with-pictogram);
}

.csp-empty-state__title {
  margin: 0;
  font-size: var(--csp-empty-state-title-size);
  font-weight: var(--csp-empty-state-title-weight);
  color: var(--text-title-grey);
}

.csp-empty-state__description {
  margin: 0;
  font-size: var(--csp-empty-state-description-size);
  color: var(--text-mention-grey);
}

.csp-empty-state__action {
  margin-top: var(--csp-space-2);
}
</style>
