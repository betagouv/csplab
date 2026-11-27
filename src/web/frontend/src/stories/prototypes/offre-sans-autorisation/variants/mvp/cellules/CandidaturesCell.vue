<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import { useNav } from '../nav'
import { candidatures } from '../recrutement'
import { horsAts } from '../suivi'

// Nombre de candidatures : lien vers le recrutement (offres en ligne seulement).
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
    class="vide"
    title="Candidatures gérées hors de l'ATS"
  >Hors ATS</span>
  <button
    v-else-if="n !== null"
    type="button"
    class="lien"
    :aria-label="`${n} candidatures, voir le recrutement`"
    @click="aller({ nom: 'recrutements' })"
  >
    {{ n }}
  </button>
  <span
    v-else
    class="vide"
  >—</span>
</template>

<style scoped lang="scss">
.lien {
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
