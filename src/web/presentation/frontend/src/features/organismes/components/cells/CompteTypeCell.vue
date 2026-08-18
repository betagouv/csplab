<script setup lang="ts">
import type { CompteUtilisateur } from '../../types'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: CompteUtilisateur
}>()
</script>

<template>
  <CspBadge
    variant="soft"
    size="sm"
    :label="row.type === 'gestionnaire' ? 'Gestionnaire' : 'Agent'"
  />
</template>
