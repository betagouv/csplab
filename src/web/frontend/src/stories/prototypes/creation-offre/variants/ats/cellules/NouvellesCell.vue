<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import { candidatures } from '../recrutement'

defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const n = computed(() => candidatures(props.row).nouvelles)
</script>

<template>
  <span class="pastille">{{ n }}</span>
</template>

<style scoped lang="scss">
.pastille {
  display: inline-block;
  min-width: 2rem;
  padding: var(--csp-space-1) var(--csp-space-2);
  background: var(--background-alt-grey);
  text-align: center;
}
</style>
