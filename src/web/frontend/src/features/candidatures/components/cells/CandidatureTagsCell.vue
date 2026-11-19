<script setup lang="ts">
import type { CandidatureListe } from '../../types'
import { EMPTY_CELL_TEXT } from '@/components/base/CspDataTable/table'
import TagList from '@/features/tags/components/TagList.vue'
import { formatCandidatTagsLabel } from '../../format'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: CandidatureListe
}>()
</script>

<template>
  <TagList
    v-if="row.tags.length > 0"
    :tags="row.tags"
    :max-lines="1"
    :aria-label="formatCandidatTagsLabel(row.candidat)"
  />
  <span v-else>{{ EMPTY_CELL_TEXT }}</span>
</template>
