<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useNav } from '../nav'
import { candidatures } from '../recrutement'
import { horsAts } from '../suivi'

// Candidatures (Alice, 27/11/2026) : gérées dans l'ATS (nombre, lien vers le recrutement) ou hors ATS (lien ou courriel).
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const { aller } = useNav()
// Rien avant la mise en ligne (brouillon).
const n = computed(() => props.row.etat !== 'brouillon' ? candidatures(props.row).total : null)
// Offre gérée hors de l'ATS (téléversée, ou « Diffuser uniquement ») : pas de candidatures à compter.
const hors = computed(() => horsAts(props.row))
</script>

<template>
  <span
    v-if="hors"
    class="cand"
  >
    <span class="cand__hors">
      <CspIcon
        name="ri:external-link-line"
        :size="14"
      />
      Hors ATS
    </span>
    <span class="cand__sous">{{ row.modeCandidature === 'courriel' ? 'par courriel' : 'sur un autre site' }}</span>
  </span>
  <span
    v-else-if="n !== null"
    class="cand"
  >
    <button
      type="button"
      class="lien"
      :aria-label="`${n} candidatures dans l'ATS, voir le recrutement`"
      @click="aller({ nom: 'recrutements' })"
    >
      {{ n }} candidature{{ n > 1 ? 's' : '' }}
    </button>
    <span class="cand__sous">dans l'ATS</span>
  </span>
  <span
    v-else
    class="vide"
  >—</span>
</template>

<style scoped lang="scss">
.cand {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.cand__hors {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 700;
}

.cand__sous {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.lien {
  text-align: left;
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  text-underline-offset: 3px;
  cursor: pointer;
}

.vide {
  color: var(--text-mention-grey);
}
</style>
