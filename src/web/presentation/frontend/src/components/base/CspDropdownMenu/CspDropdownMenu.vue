<script setup lang="ts">
import {
  DropdownMenuContent,
  DropdownMenuPortal,
  DropdownMenuRoot,
  DropdownMenuTrigger,
} from 'reka-ui'

export interface CspDropdownMenuProps {
  align?: 'start' | 'center' | 'end'
  side?: 'top' | 'right' | 'bottom' | 'left'
  sideOffset?: number
  sideFlip?: boolean
}

withDefaults(defineProps<CspDropdownMenuProps>(), {
  align: 'start',
  side: 'top',
  sideOffset: 8,
  sideFlip: true,
})
</script>

<template>
  <DropdownMenuRoot>
    <DropdownMenuTrigger as-child>
      <slot name="trigger" />
    </DropdownMenuTrigger>

    <DropdownMenuPortal>
      <DropdownMenuContent
        :align="align"
        :side="side"
        :side-offset="sideOffset"
        :side-flip="sideFlip"
      >
        <div class="csp-dropdown-menu">
          <slot />
        </div>
      </DropdownMenuContent>
    </DropdownMenuPortal>
  </DropdownMenuRoot>
</template>

<style lang="scss">
.csp-dropdown-menu {
  z-index: var(--csp-z-dropdown);
  min-width: 8rem;
  overflow: hidden;
  padding: 0.25rem;
  border-radius: 0.375rem;
  border: 1px solid var(--border-default-grey);
  background-color: var(--background-default-grey);
  box-shadow:
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -4px rgba(0, 0, 0, 0.1);
  animation: csp-dropdown-fade-in 0.12s ease-out;

  [role='menuitem'] {
    position: relative;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.375rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.875rem;
    line-height: 1.25rem;
    color: var(--text-default-grey);
    cursor: default;
    outline: none;
    user-select: none;
    transition: background-color 0.1s ease;

    svg,
    .csp-icon {
      width: 1rem;
      height: 1rem;
      flex-shrink: 0;
      color: var(--text-mention-grey);
    }

    &[data-highlighted] {
      background-color: var(--background-contrast-grey);
      color: var(--text-title-grey);

      svg,
      .csp-icon {
        color: var(--text-default-grey);
      }
    }

    &:focus-visible {
      outline: var(--focus-ring);
      outline-offset: -2px;
    }

    &[data-disabled] {
      opacity: 0.5;
      pointer-events: none;
    }
  }

  [role='group'] > span:first-child {
    display: block;
    padding: 0.375rem 0.5rem;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-mention-grey);
  }

  [role='separator'] {
    height: 1px;
    margin: 0.25rem -0.25rem;
    background-color: var(--border-default-grey);
  }
}

@keyframes csp-dropdown-fade-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
