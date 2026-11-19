<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import { useNav } from '../nav'
import { db, UTILISATEUR } from '../store'
import { prochaineEtape } from '../suivi'

// Prochaine étape : lien s'il y a quelque chose à faire, texte sinon. Jamais vide.
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const { aller } = useNav()
const e = computed(() => prochaineEtape(props.row, Boolean(db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)))
</script>

<template>
  <div class="etape">
    <button
      v-if="e.ecran"
      type="button"
      class="lien"
      @click="aller(e.ecran)"
    >
      {{ e.label }}
    </button>
    <span
      v-else
      class="texte"
    >{{ e.label }}</span>
    <span
      v-if="e.detail"
      class="detail"
    >{{ e.detail }}</span>
  </div>
</template>

<style scoped lang="scss">
.lien {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-align: left;
  text-decoration: underline;
  text-underline-offset: 3px;
  cursor: pointer;

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.texte {
  color: var(--text-mention-grey);
}

.etape {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.detail {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
