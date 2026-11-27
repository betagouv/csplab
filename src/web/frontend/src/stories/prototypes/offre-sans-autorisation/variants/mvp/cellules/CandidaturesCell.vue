<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import { useNav } from '../nav'
import { candidatures } from '../recrutement'
import { horsAts } from '../suivi'

// Candidatures (retour PO, 27/11/2026) : gérées dans l'ATS, le nombre avec un lien vers le recrutement ; hors ATS
// (offre téléversée), « Hors ATS » sans lien.
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const { aller } = useNav()
// Rien avant la mise en ligne (brouillon).
const n = computed(() => props.row.etat !== 'brouillon' ? candidatures(props.row).total : null)
const hors = computed(() => horsAts(props.row))
</script>

<template>
  <span
    v-if="hors"
    class="vide"
  >Hors ATS</span>
  <button
    v-else-if="n !== null"
    type="button"
    class="lien"
    :aria-label="`${n} candidature${n > 1 ? 's' : ''}, voir le recrutement`"
    @click="aller({ nom: 'recrutements' })"
  >
    {{ n }} candidature{{ n > 1 ? 's' : '' }}
  </button>
  <span
    v-else
    class="vide"
  >—</span>
</template>

<style scoped lang="scss">
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
