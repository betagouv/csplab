<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { RouteLocationRaw } from 'vue-router'
import { computed, useSlots } from 'vue'
import { RouterLink } from 'vue-router'
import CspBreadcrumb from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

const props = defineProps<{
  title?: string
  breadcrumb?: CspBreadcrumbItem[]
  backTo?: RouteLocationRaw
  backLabel?: string
}>()

const slots = useSlots()

const hasBreadcrumb = computed(() => (props.breadcrumb?.length ?? 0) > 0)
const hasTabs = computed(() => Boolean(slots.tabs))
</script>

<template>
  <header class="csp-page-header">
    <div class="csp-page-header__top">
      <div class="csp-page-header__main">
        <CspBreadcrumb
          v-if="hasBreadcrumb"
          :items="breadcrumb!"
        />

        <div class="csp-page-header__title-row">
          <RouterLink
            v-if="backTo"
            :to="backTo"
            :aria-label="backLabel ?? 'Retour'"
            class="csp-page-header__back"
          >
            <CspIcon
              name="ri:arrow-left-line"
              :size="20"
            />
          </RouterLink>
          <h1 class="csp-page-header__title">
            <slot name="title">
              {{ title }}
            </slot>
          </h1>
        </div>

        <div
          v-if="$slots.subtitle"
          class="csp-page-header__subtitle"
        >
          <slot name="subtitle" />
        </div>
      </div>

      <div
        v-if="$slots.actions"
        class="csp-page-header__actions"
      >
        <slot name="actions" />
      </div>
    </div>

    <div
      v-if="hasTabs"
      class="csp-page-header__tabs"
    >
      <slot name="tabs" />
    </div>
  </header>
</template>

<style scoped lang="scss">
.csp-page-header {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  background: var(--background-default-grey);
}

.csp-page-header__top {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
}

.csp-page-header__main {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.csp-page-header__title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.csp-page-header__back {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 2rem;
  height: 2rem;
  color: var(--text-action-high-blue-france);
  background-color: transparent;
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  text-decoration: none;

  &:hover {
    background-color: var(--background-default-grey-hover);
  }

  &:active {
    background-color: var(--background-default-grey-active);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.csp-page-header__title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  line-height: 1.3;
  color: var(--text-title-grey);
}

.csp-page-header__subtitle {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.csp-page-header__actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.csp-page-header__tabs {
  display: flex;
}
</style>
