<script setup lang="ts">
import type { OffreState } from '../../data/types'
import { computed } from 'vue'
import { phases } from '../../data/processus'
import ProcessusBar from './ProcessusBar.vue'

// Cellule « Avancement » du tableau des besoins : 4 pastilles + l'étape en cours en clair.
const props = defineProps<{ row: OffreState }>()
const enCours = computed(() => {
  const p = phases(props.row)
  const courant = [...p].reverse().find(x => x.etat === 'fait' || x.etat === 'en_cours')
  const suivant = p.find(x => x.etat === 'en_cours') ?? p.find(x => x.etat === 'a_venir' && x.detail !== '—')
  return (suivant ?? courant)?.detail ?? ''
})
</script>

<template>
  <span class="cell">
    <ProcessusBar
      :state="row"
      compact
    />
    <span class="cell__txt">{{ enCours }}</span>
  </span>
</template>

<style scoped lang="scss">
.cell {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
}

.cell__txt {
  font-size: var(--csp-font-size-sm);
}
</style>
