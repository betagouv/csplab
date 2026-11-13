<script setup lang="ts">
import type { Offre } from '../store'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { useNav } from '../nav'

defineOptions({ inheritAttrs: false })
defineProps<{ row: Offre }>()
const { notifier } = useNav()
</script>

<template>
  <span v-if="row.responsables?.length">{{ row.responsables.join(' ; ') }}</span>
  <CspButton
    v-else
    label="Assigner un responsable"
    size="sm"
    variant="secondary"
    @click.stop="notifier('Simulation : assignation d\'un responsable non prototypée.')"
  />
</template>
