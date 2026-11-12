<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import { statutListe, STATUTS } from '../suivi'

// Statut unique de la liste : publication et validation réunies dans un seul badge.
defineOptions({ inheritAttrs: false })

const props = defineProps<{ row: Offre }>()
const s = computed(() => STATUTS[statutListe(props.row)])
</script>

<template>
  <CspBadge
    :label="s.label"
    :type="s.type"
    :variant="s.contour ? 'outline' : 'soft'"
    size="sm"
  />
</template>
