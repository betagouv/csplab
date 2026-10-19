<script setup lang="ts">
import type { CandidatureListe } from '../../types'
import { computed } from 'vue'
import CspLabelList from '@/components/base/CspLabel/CspLabelList.vue'
import { etiquettesOf } from '../../etiquettes'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: CandidatureListe
}>()

const etiquettes = computed(() => etiquettesOf(props.row))
</script>

<template>
  <CspLabelList
    v-if="etiquettes.length"
    :labels="etiquettes"
    :max-lines="1"
  />
</template>
