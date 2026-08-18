<script setup lang="ts">
import type { OrganismeAdmin } from '../../types'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: OrganismeAdmin
}>()
</script>

<template>
  <RouterLink
    class="organisme-nom-cell"
    :to="{ name: 'parametres-organisme', params: { organismeUuid: row.uuid } }"
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
