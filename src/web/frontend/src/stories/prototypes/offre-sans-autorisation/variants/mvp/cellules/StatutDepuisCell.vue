<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import { categorieOffre, CATEGORIES_OFFRE } from '../suivi'

// Statut (badge), dans l'onglet « Toutes » seulement. Plus de « depuis 6 jours » : la date de mise en ligne suffit (retour PO, L2).
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const c = computed(() => CATEGORIES_OFFRE.find(x => x.id === categorieOffre(props.row))!)
</script>

<template>
  <div class="statut">
    <CspBadge
      :label="c.label"
      :type="c.badge"
      size="sm"
    />
  </div>
</template>

<style scoped lang="scss">
.statut {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-1);
}

.statut__depuis {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
