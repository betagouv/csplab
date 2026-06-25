<script setup lang="ts">
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed, useSlots } from 'vue'
import CspBreadcrumb from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'

const props = defineProps<{
  title?: string
  breadcrumb?: CspBreadcrumbItem[]
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

        <h1 class="csp-page-header__title">
          <slot name="title">
            {{ title }}
          </slot>
        </h1>

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
