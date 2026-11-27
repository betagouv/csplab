<script setup lang="ts">
import type { Offre } from '../store'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

// Origine de l'offre (Alice, 27/11/2026) : téléversée, ou créée manuellement dans l'ATS (formulaire ou duplication).
defineOptions({ inheritAttrs: false })
defineProps<{ row: Offre }>()
</script>

<template>
  <span
    class="origine"
    :class="{ 'origine--televersee': row.origineContenu === 'televersement' }"
  >
    <CspIcon
      :name="row.origineContenu === 'televersement' ? 'ri:upload-2-line' : 'ri:edit-line'"
      :size="16"
    />
    {{ row.origineContenu === 'televersement' ? 'Téléversée' : 'Créée manuellement' }}
  </span>
</template>

<style scoped lang="scss">
.origine {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.origine--televersee {
  color: var(--text-default-grey);
}
</style>
