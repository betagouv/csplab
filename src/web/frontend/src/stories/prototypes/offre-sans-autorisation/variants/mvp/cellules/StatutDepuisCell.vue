<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import { categorieOffre, CATEGORIES_OFFRE, depuis } from '../suivi'

// Statut (badge) et temps passé dans ce statut : « depuis 6 jours ».
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
    <span class="statut__depuis">{{ depuis(row) }}</span>
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
