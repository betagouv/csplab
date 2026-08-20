<script setup lang="ts">
import type { OrganismesList } from '../../types'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: OrganismesList
}>()
</script>

<template>
  <span class="organisme-nom-cell">
    {{ row.nom }}
  </span>
</template>

<style scoped lang="scss">
.organisme-nom-cell {
  font-weight: 600;
  color: var(--text-title-grey);
}
</style>
