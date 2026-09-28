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
import { SIDEBAR_WIDTH, SIDEBAR_WIDTH_COLLAPSED, useSidebar } from '@/composables/ui/useSidebar'

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

        <div class="csp-sidebar__context">
          <slot name="context" />
        </div>

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

    <div class="csp-sidebar__context">
      <slot name="context" />
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
  --sidebar-item-size: 2.5rem;
  --sidebar-item-padding-inline: var(--csp-space-2);
  --sidebar-leading-size: 2rem;
  --sidebar-leading-gap: var(--csp-space-2);

  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  width: var(--sidebar-width-collapsed);
  height: 100%;
  background: var(--background-alt-grey);
  overflow: hidden;

  &--expanded {
    width: var(--sidebar-width);
  }

  &--mobile {
    position: fixed;
    inset-block: 0;
    left: 0;
    width: var(--sidebar-width);
    max-width: calc(100vw - 3rem);
    z-index: var(--csp-z-modal);
    box-shadow: var(--csp-shadow-lg);
  }
}

.csp-sidebar__header {
  position: relative;
  box-sizing: content-box;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--csp-page-header-breadcrumb-height);
  padding-top: var(--csp-page-header-padding-top);
  padding-bottom: var(--csp-page-header-breadcrumb-gap);
  padding-inline: var(--csp-sidebar-padding);
}

.csp-sidebar__context {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--csp-sidebar-padding);
  padding-bottom: 0;
  border-top: 1px solid var(--border-default-grey);

  .csp-sidebar--expanded &,
  .csp-sidebar--mobile & {
    align-items: stretch;
  }
}

.csp-sidebar__brand {
  flex: 1;
  min-width: 0;
  padding-inline: var(--sidebar-item-padding-inline);
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

  .csp-sidebar:not(.csp-sidebar--expanded) & {
    margin-inline: auto;
  }

  &:hover {
    background: var(--background-default-grey-hover);
    color: var(--text-default-grey);
  }

  &:focus-visible {
    outline: var(--focus-ring);
    outline-offset: var(--csp-focus-ring-offset);
  }
}

.csp-sidebar__close {
  flex-shrink: 0;
}

.csp-sidebar__nav {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  gap: var(--csp-space-2);
  min-height: 0;
  padding: var(--csp-space-2) var(--csp-sidebar-padding);
  overflow-x: hidden;
  overflow-y: auto;

  .csp-sidebar--expanded &,
  .csp-sidebar--mobile & {
    align-items: stretch;
  }
}

.csp-sidebar__footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  padding: var(--csp-sidebar-padding);
  border-top: 1px solid var(--border-default-grey);

  .csp-sidebar--expanded &,
  .csp-sidebar--mobile & {
    align-items: stretch;
  }
}
</style>
