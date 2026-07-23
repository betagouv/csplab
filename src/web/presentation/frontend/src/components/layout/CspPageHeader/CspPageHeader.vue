<script setup lang="ts">
import type { RouteLocationRaw } from 'vue-router'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import { computed } from 'vue'
import CspBreadcrumb from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'

const props = defineProps<{
  title?: string
  breadcrumb?: CspBreadcrumbItem[]
  backLink?: { to: RouteLocationRaw, label: string }
  showTitleSkeleton?: boolean
  showSubtitleSkeleton?: boolean
}>()

const hasBreadcrumb = computed(() => Boolean(props.breadcrumb?.length))
</script>

<template>
  <header
    class="csp-page-header"
    :class="{ 'csp-page-header--has-back-link': Boolean(backLink) }"
  >
    <div class="csp-page-header__top-row">
      <div
        class="csp-page-header__breadcrumb-wrapper"
      >
        <CspBreadcrumb
          v-if="hasBreadcrumb"
          :items="breadcrumb!"
        />
      </div>
    </div>
    <div class="csp-page-header__main-row">
      <div class="csp-page-header__hgroup-wrapper">
        <div
          v-if="backLink"
          class="csp-page-header__back-link"
        >
          <RouterLink
            as-child
            :to="backLink.to"
            :aria-label="backLink.label"
          >
            <CspButton
              variant="tertiary-no-outline"
              is-icon-left
              icon="ri:arrow-left-line"
              size="sm"
            />
          </RouterLink>
        </div>
        <div
          class="csp-page-header__hgroup"
        >
          <div class="csp-page-header__title">
            <CspSkeleton
              v-if="showTitleSkeleton"
              class="csp-page-header__title-skeleton"
              width="25rem"
            />
            <h1 v-else>
              {{ title }}
            </h1>
          </div>
          <div class="csp-page-header__subtitle">
            <CspSkeleton
              v-if="showSubtitleSkeleton"
              width="28rem"
              height="1.375rem"
            />
            <slot
              v-else
              name="subtitle"
            />
          </div>
        </div>
      </div>
      <div
        v-if="$slots.actions"
        class="csp-page-header__actions"
      >
        <slot name="actions" />
      </div>
    </div>
  </header>
</template>

<style scoped lang="scss">
.csp-page-header {
  background: var(--background-default-grey);

  --csp-page-header-back-link-size: 0;
  --csp-page-header-back-link-gap: 0;

  &.csp-page-header--has-back-link {
    --csp-page-header-back-link-size: 2rem;
    --csp-page-header-back-link-gap: 0.5rem;
  }
}

.csp-page-header__top-row {
  padding-top: 0.75rem;
  padding-bottom: 1.25rem;
  padding-inline: var(--csp-page-container-padding-inline);
}

.csp-page-header__breadcrumb-wrapper {
  min-height: 1.5rem;
}

.csp-page-header__main-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid var(--border-default-grey);
  padding-inline: var(--csp-page-container-padding-inline);
}

.csp-page-header__hgroup-wrapper {
  display: flex;
  gap: var(--csp-page-header-back-link-gap);
  margin-left: calc(calc(var(--csp-page-header-back-link-size) + var(--csp-page-header-back-link-gap)) * -1);
}

.csp-page-header__hgroup {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.csp-page-header__back-link {
  margin-top: 0.25rem;
  width: var(--csp-page-header-back-link-size);
}

.csp-page-header__title {
  font-weight: 600;
  font-size: 1.5rem;
  min-height: 2.5rem;
}

.csp-page-header__title-skeleton {
  height: 4rem;
}

.csp-page-header__subtitle {
  min-height: 1.5rem;
}

.csp-page-header__actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}
</style>
