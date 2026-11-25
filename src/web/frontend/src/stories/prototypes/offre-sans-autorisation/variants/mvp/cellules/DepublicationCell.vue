<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { joursRestants } from '../store'
import { dateCourte } from '../suivi'

// Fin de publication (= date limite de candidature), uniquement quand une échéance existe (Alice, 25/11/2026) :
// en ligne, ou en pause avant la date de fin. Pour une offre en ligne, le nombre de jours restants est
// écrit sous la date, pas seulement signalé par la couleur (retour PO, L5 : accessibilité).
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const j = computed(() => joursRestants(props.row.dateFin))
const enLigne = computed(() => Boolean(props.row.dateFin) && (props.row.etat === 'publiee' || (props.row.etat === 'retiree' && j.value >= 0)))
const proche = computed(() => props.row.etat === 'publiee' && j.value < 7)
const restant = computed(() => (j.value <= 0 ? 'aujourd\'hui' : j.value === 1 ? 'demain' : `dans ${j.value} jours`))
</script>

<template>
  <div
    v-if="enLigne"
    class="fin"
  >
    <span>{{ dateCourte(row.dateFin) }}</span>
    <span
      v-if="row.etat === 'publiee'"
      class="fin__restant"
      :class="{ 'fin__restant--proche': proche }"
    >
      <CspIcon
        v-if="proche"
        name="ri:error-warning-line"
        :size="14"
      />
      {{ restant }}
    </span>
  </div>
  <span
    v-else
    class="vide"
  >—</span>
</template>

<style scoped lang="scss">
.fin {
  display: flex;
  flex-direction: column;
  white-space: nowrap;
}

.fin__restant {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.fin__restant--proche {
  font-weight: 600;
  color: var(--text-default-error);
}

.vide {
  color: var(--text-mention-grey);
}
</style>
