<script setup lang="ts">
import type { OrganismesList } from '../../types'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: OrganismesList
}>()
</script>

<template>
  <RouterLink
    class="organisme-nom-cell"
    :to="{ name: 'organisme', params: { organismeUuid: row.organisme_uuid } }"
  >
    {{ row.nom }}
  </RouterLink>
</template>

<style scoped lang="scss">
.organisme-nom-cell {
  font-weight: 600;
  color: var(--text-title-grey);
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}
</style>
