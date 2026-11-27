<script setup lang="ts">
import type { MembreEquipe } from '../../types'
import { EMPTY_CELL_TEXT } from '@/components/base/CspDataTable/table'
import TagList from '@/features/tags/components/TagList.vue'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: MembreEquipe
}>()
</script>

<template>
  <TagList
    v-if="row.tags.length > 0"
    :tags="row.tags"
  />
  <span v-else>{{ EMPTY_CELL_TEXT }}</span>
</template>
