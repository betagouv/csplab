<script setup lang="ts">
import type { ProtoRecrutement } from '../../data/mock'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: ProtoRecrutement
}>()
</script>

<template>
  <span class="intitule-cell">{{ row.intitule }}</span>
</template>

<style scoped lang="scss">
.intitule-cell {
  font-weight: 600;
  color: var(--text-title-grey);
}
</style>
