<script setup lang="ts">
import type { Offre } from '../store'

// Origine de l'offre, en texte seul (Alice, 27/11/2026) : téléversée, ou créée manuellement dans l'ATS (formulaire ou duplication).
defineOptions({ inheritAttrs: false })
defineProps<{ row: Offre }>()
</script>

<template>
  <span
    class="origine"
    :class="{ 'origine--televersee': row.origineContenu === 'televersement' }"
  >
    {{ row.origineContenu === 'televersement' ? 'Téléversée' : 'Créée manuellement' }}
  </span>
</template>

<style scoped lang="scss">
.origine {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.origine--televersee {
  color: var(--text-default-grey);
}
</style>
