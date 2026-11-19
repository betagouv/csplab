<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import CspTooltip from '@/components/base/CspTooltip/CspTooltip.vue'
import { responsables } from '../suivi'

// Plusieurs responsables : « Camille Moreau +1 », la liste complète au survol (retour PO, L7).
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const noms = computed(() => responsables(props.row))
</script>

<template>
  <CspTooltip
    v-if="noms.length > 1"
    :content="noms.join(', ')"
    side="top"
  >
    <span
      class="resp"
      tabindex="0"
      :aria-label="`Responsables : ${noms.join(', ')}`"
    >{{ noms[0] }} <span class="resp__plus">+{{ noms.length - 1 }}</span></span>
  </CspTooltip>
  <span
    v-else
    class="resp"
  >{{ noms[0] ?? '—' }}</span>
</template>

<style scoped lang="scss">
.resp {
  white-space: nowrap;
}

.resp__plus {
  padding: 0 var(--csp-space-1);
  border-radius: 4px;
  background: var(--background-contrast-grey);
  font-size: var(--csp-font-size-xs);
  font-weight: 600;
}
</style>
