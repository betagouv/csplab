<script setup lang="ts">
import {
  DialogContent,
  DialogOverlay,
  DialogPortal,
  DialogRoot,
} from 'reka-ui'
import { computed, useSlots } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { SIDEBAR_WIDTH, SIDEBAR_WIDTH_COLLAPSED, useSidebar } from '@/composables/useSidebar'

const slots = useSlots()
const hasLogo = computed(() => Boolean(slots.logo))
const hasFooter = computed(() => Boolean(slots.footer))

const { state, isExpanded, isMobile, isMobileOpen, setMobileOpen, toggle } = useSidebar()
</script>

<template>
  <DialogRoot
    v-if="isMobile"
    :open="isMobileOpen"
    @update:open="setMobileOpen"
  >
    <DialogPortal>
      <DialogOverlay class="csp-sidebar-overlay" />
      <DialogContent
        class="csp-sidebar csp-sidebar--mobile"
        :aria-label="$attrs['aria-label'] ?? 'Menu de navigation'"
        :style="{
          '--sidebar-width': SIDEBAR_WIDTH,
        }"
      >
        <header class="csp-sidebar__header">
          <div
            v-if="hasLogo"
            class="csp-sidebar__brand"
          >
            <slot name="logo" />
          </div>
          <CspButton
            class="csp-sidebar__close"
            variant="tertiary-no-outline"
            size="sm"
            icon="ri:close-line"
            aria-label="Fermer le menu"
            @click="setMobileOpen(false)"
          />
        </header>

        <nav class="csp-sidebar__nav">
          <slot />
        </nav>

        <div
          v-if="hasFooter"
          class="csp-sidebar__footer"
        >
          <slot name="footer" />
        </div>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>

  <nav
    v-else
    class="csp-sidebar"
    :class="{ 'csp-sidebar--expanded': isExpanded }"
    :data-state="state"
    :aria-expanded="isExpanded"
    :style="{
      '--sidebar-width': SIDEBAR_WIDTH,
      '--sidebar-width-collapsed': SIDEBAR_WIDTH_COLLAPSED,
    }"
  >
    <div class="csp-sidebar__header">
      <div
        v-if="hasLogo && isExpanded"
        class="csp-sidebar__brand"
      >
        <slot name="logo" />
      </div>
      <button
        type="button"
        class="csp-sidebar__toggle"
        :aria-label="isExpanded ? 'Réduire le menu' : 'Ouvrir le menu'"
        :title="`${isExpanded ? 'Réduire' : 'Ouvrir'} (Ctrl+B)`"
        @click="toggle"
      >
        <CspIcon
          :name="isExpanded ? 'ri:sidebar-fold-line' : 'ri:sidebar-unfold-line'"
          :size="18"
        />
      </button>
    </div>

    <div class="csp-sidebar__nav">
      <slot />
    </div>

    <div
      v-if="hasFooter"
      class="csp-sidebar__footer"
    >
      <slot name="footer" />
    </div>
  </nav>
</template>

<style scoped lang="scss">
.csp-sidebar-overlay {
  position: fixed;
  inset: 0;
  background-color: var(--csp-overlay-scrim);
  z-index: var(--csp-z-overlay);
}

.csp-sidebar {
  --sidebar-inset-x: 0.5rem;
  --sidebar-item-size: 2.5rem;
  --sidebar-padding-x: 0.5rem;

  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  width: var(--sidebar-width-collapsed);
  height: 100%;
  padding: 0.75rem var(--sidebar-padding-x);
  background: var(--background-alt-grey);
  overflow: hidden;
  transition:
    width 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    padding 0.2s cubic-bezier(0.4, 0, 0.2, 1);

  &--expanded {
    width: var(--sidebar-width);
    --sidebar-padding-x: 0.75rem;
  }

  &--mobile {
    position: fixed;
    inset-block: 0;
    left: 0;
    width: var(--sidebar-width);
    max-width: calc(100vw - 3rem);
    z-index: var(--csp-z-modal);
    box-shadow: var(--csp-shadow-lg);
    --sidebar-padding-x: 0.75rem;
  }
}

.csp-sidebar__header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
  min-height: 2rem;
  padding-bottom: 2rem;
}

.csp-sidebar__brand {
  flex: 1;
  min-width: 0;
  padding-left: var(--sidebar-inset-x);
  padding-right: 0.5rem;
  overflow: hidden;
}

.csp-sidebar__toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  flex-shrink: 0;
  padding: 0;
  border: none;
  border-radius: 0.375rem;
  background: transparent;
  color: var(--text-mention-grey);
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    color 0.15s ease;

  .csp-sidebar:not(.csp-sidebar--expanded) & {
    margin-inline: auto;
  }

  &:hover {
    background: var(--background-default-grey-hover);
    color: var(--text-default-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.csp-sidebar__close {
  flex-shrink: 0;
}

.csp-sidebar__nav {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  flex: 1;
  min-width: 0;
  min-height: 0;
  overflow-x: hidden;
  overflow-y: auto;

  .csp-sidebar--expanded &,
  .csp-sidebar--mobile & {
    align-items: stretch;
  }
}

.csp-sidebar__footer {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  width: calc(100% + 2 * var(--sidebar-padding-x));
  margin-top: 0.75rem;
  margin-inline: calc(-1 * var(--sidebar-padding-x));
  padding: 0.75rem var(--sidebar-padding-x) 0;
  border-top: 1px solid var(--border-default-grey);

  .csp-sidebar--expanded &,
  .csp-sidebar--mobile & {
    align-items: stretch;
  }
}
</style>
