<script setup lang="ts">
import type { StatutCandidat } from '../../data/espaceMock'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import { statutMeta } from '../../data/espaceMock'

defineProps<{
  statut: StatutCandidat
}>()
</script>

<template>
  <CspBadge
    :label="statutMeta[statut].label"
    :type="statutMeta[statut].ton"
    :icon="statutMeta[statut].icon"
    variant="soft"
  />
</template>
