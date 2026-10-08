<script setup lang="ts">
import type { CandidatureListe } from '../../types'
import type { CspTableCellValue } from '@/components/base/CspDataTable/table'
import { RouterLink } from 'vue-router'
import { CANDIDATURE_PANEL_ROUTE_NAMES } from '../../routes'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: CandidatureListe
  value?: CspTableCellValue
}>()
</script>

<template>
  <RouterLink
    :to="{ name: CANDIDATURE_PANEL_ROUTE_NAMES.liste.tabs.candidature, params: { candidatureUuid: row.uuid } }"
    class="candidat-nom-cell"
    :data-candidature-uuid="row.uuid"
  >
    {{ value }}
  </RouterLink>
</template>

<style scoped lang="scss">
.candidat-nom-cell {
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
