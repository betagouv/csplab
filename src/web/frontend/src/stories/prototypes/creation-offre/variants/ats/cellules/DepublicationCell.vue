<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import { joursRestants } from '../store'
import { dateCourte } from '../suivi'

// Date de dépublication : en rouge à moins de 7 jours.
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const enLigne = computed(() => props.row.etat === 'publiee' && Boolean(props.row.dateFin))
const proche = computed(() => enLigne.value && joursRestants(props.row.dateFin) < 7)
</script>

<template>
  <span
    v-if="enLigne"
    :class="{ proche }"
  >{{ dateCourte(row.dateFin) }}</span>
  <span
    v-else
    class="vide"
  >—</span>
</template>

<style scoped lang="scss">
.proche {
  font-weight: 600;
  color: var(--text-default-error);
}

.vide {
  color: var(--text-mention-grey);
}
</style>
