<script setup lang="ts">
import type { CspDropdownMenuProps } from '@/components/base/CspDropdownMenu/CspDropdownMenu.types'
import { computed } from 'vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useSidebar } from '@/composables/ui/useSidebar'

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

const { showLabels } = useSidebar()
</script>

<template>
  <CspDropdownMenu v-bind="menuProps">
    <template #trigger>
      <button
        type="button"
        class="csp-sidebar-dropdown-button"
        :aria-label="title"
        v-bind="$attrs"
      >
        <span class="csp-sidebar-dropdown-button__leading">
          <slot name="leading" />
        </span>
        <template v-if="showLabels">
          <span class="csp-sidebar-dropdown-button__text">
            <span class="csp-sidebar-dropdown-button__title">{{ title }}</span>
            <span
              v-if="description"
              class="csp-sidebar-dropdown-button__description"
            >{{ description }}</span>
          </span>
          <CspIcon
            name="ri:expand-up-down-line"
            :size="16"
            class="csp-sidebar-dropdown-button__chevron"
          />
        </template>
      </button>
    </template>
  </CspDropdownMenu>
</template>

<style scoped lang="scss">
.csp-sidebar-dropdown-button {
  display: flex;
  align-items: center;
  padding-block: 0.5rem;
  padding-inline: 0.5rem;
  gap: 0.625rem;
  min-width: 0;
  cursor: pointer;
  background-color: var(--background-alt-grey);

  &:hover {
    background-color: var(--background-alt-grey-hover);
  }

  &:active {
    background-color: var(--background-alt-grey-active);
  }

  &:focus-visible {
    outline: var(--focus-ring);
    outline-offset: var(--csp-focus-ring-offset);
  }
}

.csp-sidebar-dropdown-button__leading {
  display: flex;
  flex-shrink: 0;
}

.csp-sidebar-dropdown-button__text {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  text-align: left;
  line-height: 1.2;
}

.csp-sidebar-dropdown-button__title,
.csp-sidebar-dropdown-button__description {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.csp-sidebar-dropdown-button__title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-title-grey);
}

.csp-sidebar-dropdown-button__description {
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.csp-sidebar-dropdown-button__chevron {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}
</style>
