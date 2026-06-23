<script setup lang="ts">
import type { RouteLocationRaw } from 'vue-router'
import { Primitive } from 'reka-ui'
import { RouterLink } from 'vue-router'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export interface CspBreadcrumbItem {
  label: string
  to?: RouteLocationRaw
}

export interface CspBreadcrumbProps {
  items: CspBreadcrumbItem[]
  ariaLabel?: string
}

withDefaults(defineProps<CspBreadcrumbProps>(), {
  ariaLabel: 'Fil d’Ariane',
})
</script>

<template>
  <nav
    :aria-label="ariaLabel"
    class="csp-breadcrumb"
  >
    <ol class="csp-breadcrumb__list">
      <li
        v-for="(item, index) in items"
        :key="`${index}-${item.label}`"
        class="csp-breadcrumb__item"
      >
        <Primitive
          :as="item.to ? RouterLink : 'span'"
          :to="item.to"
          class="csp-breadcrumb__link"
          :class="{ 'csp-breadcrumb__link--current': !item.to }"
          :aria-current="!item.to && index === items.length - 1 ? 'page' : undefined"
        >
          {{ item.label }}
        </Primitive>
        <span
          v-if="index < items.length - 1"
          aria-hidden="true"
          class="csp-breadcrumb__separator"
        >
          <CspIcon
            name="ri:arrow-right-s-line"
            size="16"
          />
        </span>
      </li>
    </ol>
  </nav>
</template>

<style scoped lang="scss">
.csp-breadcrumb {
  font-size: 0.875rem;
  color: var(--text-mention-grey);
}

.csp-breadcrumb__list {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.25rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.csp-breadcrumb__item {
  display: inline-flex;
  align-items: center;
}

.csp-breadcrumb__link {
  text-decoration: underline;
  text-underline-offset: 0.25rem;

  &:hover {
    text-decoration-thickness: 2px;
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.csp-breadcrumb__link--current {
  text-decoration: none;
  color: var(--text-default-grey);
}

.csp-breadcrumb__separator {
  margin-left: 0.375rem;
  color: var(--text-mention-grey);
}
</style>
