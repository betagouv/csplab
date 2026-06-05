<script setup lang="ts">
import { computed, provide, ref } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

interface CspSidebarProps {
  defaultExpanded?: boolean
}

const props = withDefaults(defineProps<CspSidebarProps>(), {
  defaultExpanded: false,
})

const isExpanded = ref(props.defaultExpanded)
const isExpandedComputed = computed(() => isExpanded.value)

function toggle() {
  isExpanded.value = !isExpanded.value
}

provide('sidebar-expanded', isExpandedComputed)
provide('sidebar-toggle', toggle)
</script>

<template>
  <nav
    class="csp-sidebar"
    :class="{ 'csp-sidebar--expanded': isExpanded }"
    :aria-expanded="isExpanded"
  >
    <div class="csp-sidebar__header">
      <div
        v-show="isExpanded"
        class="csp-sidebar__brand"
      >
        <slot name="logo" />
      </div>
      <button
        type="button"
        class="csp-sidebar__toggle"
        :aria-label="isExpanded ? 'Réduire le menu' : 'Ouvrir le menu'"
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

    <div class="csp-sidebar__footer">
      <slot name="footer" />
    </div>
  </nav>
</template>

<style scoped lang="scss">
.csp-sidebar {
  --sidebar-inset-x: 0.5rem;
  --sidebar-item-size: 2.5rem;
  --sidebar-padding-x: 0.5rem;

  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  width: 4rem;
  height: 100vh;
  padding: 0.75rem var(--sidebar-padding-x);
  background: var(--background-alt-grey);
  overflow: hidden;
  transition: width 0.2s cubic-bezier(0.4, 0, 0.2, 1);

  &--expanded {
    width: 15rem;
    --sidebar-padding-x: 0.75rem;
  }
}

.csp-sidebar__header {
  position: relative;
  flex-shrink: 0;
  min-height: 2rem;
  margin-bottom: 1rem;
}

.csp-sidebar__brand {
  padding-left: var(--sidebar-inset-x);
  padding-right: 2.25rem;
  min-width: 0;
  overflow: hidden;
}

.csp-sidebar__toggle {
  position: absolute;
  top: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  padding: 0;
  border: none;
  border-radius: 0.375rem;
  background: transparent;
  color: var(--text-mention-grey);
  cursor: pointer;

  .csp-sidebar:not(.csp-sidebar--expanded) & {
    left: 50%;
    right: auto;
    transform: translateX(-50%);
  }

  .csp-sidebar--expanded & {
    right: 0;
    left: auto;
    transform: none;
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

  .csp-sidebar--expanded & {
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

  .csp-sidebar--expanded & {
    align-items: stretch;
  }
}
</style>
