<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import { joursRestants } from '../store'
import { dateCourte } from '../suivi'

// Fin de publication : mise en avant quand elle approche (c'est là qu'on pense à prolonger).
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const j = computed(() => joursRestants(props.row.dateFin))
</script>

<template>
  <span v-if="row.etat !== 'publiee'">Hors ligne</span>
  <span
    v-else-if="j <= 7"
    class="bientot"
  >{{ j <= 0 ? 'Aujourd\'hui' : `Dans ${j} jour${j > 1 ? 's' : ''}` }}</span>
  <span v-else>{{ dateCourte(row.dateFin) }}</span>
</template>

<style scoped lang="scss">
.bientot {
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-default-warning);
}
</style>
