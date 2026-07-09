<script setup lang="ts">
import { provideSidebar } from '@/composables/ui/useSidebar'

interface CspSidebarProviderProps {
  defaultExpanded?: boolean
  persistState?: boolean
}

const props = withDefaults(defineProps<CspSidebarProviderProps>(), {
  defaultExpanded: true,
  persistState: true,
})

provideSidebar({
  defaultExpanded: props.defaultExpanded,
  persistState: props.persistState,
})
</script>

<template>
  <slot />
</template>
