<script setup lang="ts">
import {
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuPortal,
  DropdownMenuRoot,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from 'reka-ui'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

withDefaults(defineProps<{
  sections: {
    items: {
      label: string
      icon?: string
      disabled?: boolean
      destructive?: boolean
      onSelect?: () => void
    }[]
  }[]
  align?: 'start' | 'center' | 'end'
  side?: 'top' | 'right' | 'bottom' | 'left'
  sideOffset?: number
  sideFlip?: boolean
}>(), {
  align: 'start',
  side: 'top',
})

const open = defineModel<boolean | undefined>('open')
</script>

<template>
  <DropdownMenuRoot
    :open="open"
    @update:open="value => open = value"
  >
    <DropdownMenuTrigger as-child>
      <slot name="trigger" />
    </DropdownMenuTrigger>

    <DropdownMenuPortal>
      <DropdownMenuContent
        class="csp-dropdown"
        :align="align"
        :side="side"
        :side-offset="sideOffset"
        :side-flip="sideFlip"
      >
        <template
          v-for="(section, sectionIndex) in sections"
          :key="sectionIndex"
        >
          <DropdownMenuSeparator
            v-if="sectionIndex > 0"
            class="csp-dropdown__separator"
          />

          <DropdownMenuItem
            v-for="item in section.items"
            :key="item.label"
            class="csp-dropdown__item"
            :class="{ 'csp-dropdown__item--destructive': item.destructive }"
            :disabled="item.disabled"
            @select="item.onSelect"
          >
            <CspIcon
              v-if="item.icon"
              class="csp-dropdown__item-icon"
              :name="item.icon"
            />
            {{ item.label }}
          </DropdownMenuItem>
        </template>
      </DropdownMenuContent>
    </DropdownMenuPortal>
  </DropdownMenuRoot>
</template>

<style lang="scss">
.csp-dropdown {
  min-width: 10rem;
  background-color: var(--background-overlap-grey);
  box-shadow:
    inset 0 0 0 1px var(--border-default-grey),
    var(--csp-shadow-lg);
  padding: 0.25rem;
  z-index: var(--csp-z-dropdown);
  outline: none;
}

.csp-dropdown__separator {
  height: 1px;
  background-color: var(--border-default-grey);
  margin: 0.25rem 0;
}

.csp-dropdown__item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  outline: none;
  color: var(--text-default-grey);
  user-select: none;

  &[data-highlighted] {
    background-color: var(--background-default-grey-hover);
  }

  &[data-disabled] {
    cursor: not-allowed;
    color: var(--text-disabled-grey);

    .csp-dropdown__item-icon {
      color: var(--text-disabled-grey);
    }
  }
}

.csp-dropdown__item--destructive {
  color: var(--text-default-error);

  .csp-dropdown__item-icon {
    color: var(--text-default-error);
  }

  &[data-highlighted] {
    background-color: var(--background-default-grey-hover);
    color: var(--text-default-error);

    .csp-dropdown__item-icon {
      color: var(--text-default-error);
    }
  }
}

.csp-dropdown__item-icon {
  flex: 0 0 auto;
  width: 1rem;
  height: 1rem;
  color: var(--text-mention-grey);
}
</style>
