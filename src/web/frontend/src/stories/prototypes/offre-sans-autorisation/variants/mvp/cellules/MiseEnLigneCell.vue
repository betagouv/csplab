<script setup lang="ts">
import type { Offre } from '../store'
import { dateCourte } from '../suivi'

// Date de mise en ligne : la seule information de durée pour une offre publiée (retour PO, L2).
defineOptions({ inheritAttrs: false })
defineProps<{ row: Offre }>()
</script>

<template>
  <span
    v-if="row.etat !== 'brouillon' && row.dateDebut"
    class="date"
  >{{ dateCourte(row.dateDebut) }}</span>
  <span
    v-else
    class="vide"
  >—</span>
</template>

<style scoped lang="scss">
.date {
  white-space: nowrap;
}

.vide {
  color: var(--text-mention-grey);
}
</style>
