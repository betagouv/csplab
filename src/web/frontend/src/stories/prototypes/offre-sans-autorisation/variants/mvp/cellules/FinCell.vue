<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import { ilYa } from '../recrutement'
import { joursRestants } from '../store'

// Colonne « Publication » : depuis quand l'offre est en ligne ; la fin n'apparaît que lorsqu'elle approche
// (c'est le moment de penser à prolonger) ou quand l'offre est retirée.
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const j = computed(() => joursRestants(props.row.dateFin))
</script>

<template>
  <span class="publication">
    {{ ilYa(row.dateDebut) }}
    <small
      v-if="row.etat === 'retiree'"
      class="retiree"
    >Retirée</small>
    <small
      v-else-if="row.etat === 'publiee' && j <= 7"
      class="bientot"
    >{{ j <= 0 ? 'Fin aujourd\'hui' : `Fin dans ${j} jour${j > 1 ? 's' : ''}` }}</small>
  </span>
</template>

<style scoped lang="scss">
.publication {
  display: flex;
  flex-direction: column;
  white-space: nowrap;
}

small {
  font-size: var(--csp-font-size-xs);
}

.bientot {
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-default-warning);
}

.retiree {
  color: var(--text-mention-grey);
}
</style>
