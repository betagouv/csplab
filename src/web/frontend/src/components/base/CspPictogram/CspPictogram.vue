<script setup lang="ts">
import type { CspPictogramName } from './pictograms'
import { computed } from 'vue'
import { pictogramUrl } from './pictograms'

const props = defineProps<{
  name: CspPictogramName
}>()

const url = computed(() => pictogramUrl(props.name))
</script>

<template>
  <svg
    class="csp-pictogram"
    viewBox="0 0 80 80"
    aria-hidden="true"
    focusable="false"
  >
    <use
      class="csp-pictogram__decorative"
      :href="`${url}#artwork-decorative`"
    />
    <use
      class="csp-pictogram__minor"
      :href="`${url}#artwork-minor`"
    />
    <use
      class="csp-pictogram__major"
      :href="`${url}#artwork-major`"
    />
  </svg>
</template>

<style scoped lang="scss">
.csp-pictogram {
  display: block;
  flex-shrink: 0;
}

.csp-pictogram__decorative {
  fill: var(--csp-pictogram-decorative-color);
}

.csp-pictogram__minor {
  fill: var(--csp-pictogram-minor-color);
}

.csp-pictogram__major {
  fill: var(--csp-pictogram-major-color);
}

@media (forced-colors: active) {
  .csp-pictogram__decorative {
    fill: none;
  }

  .csp-pictogram__minor,
  .csp-pictogram__major {
    fill: CanvasText;
  }
}
</style>
