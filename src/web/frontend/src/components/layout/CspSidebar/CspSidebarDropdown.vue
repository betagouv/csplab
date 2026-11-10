<script setup lang="ts">
import type { CspDropdownMenuProps } from '@/components/base/CspDropdownMenu/CspDropdownMenu.types'
import { computed } from 'vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspSidebarButton from '@/components/layout/CspSidebar/CspSidebarButton.vue'

defineOptions({
  inheritAttrs: false,
})

const props = defineProps<CspDropdownMenuProps & {
  title: string
  description?: string
}>()

const menuProps = computed(() => {
  const { title: _title, description: _description, ...rest } = props
  return rest
})
</script>

<template>
  <CspDropdownMenu v-bind="menuProps">
    <template #trigger>
      <CspSidebarButton
        :title="title"
        :description="description"
        :aria-label="title"
        v-bind="$attrs"
      >
        <template #leading>
          <slot name="leading" />
        </template>
      </CspSidebarButton>
    </template>
  </CspDropdownMenu>
</template>
