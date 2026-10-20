<script setup lang="ts">
import type { RouteLocationRaw } from 'vue-router'
import type { CspBreadcrumbItem } from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import type { CspPictogramName } from '@/components/base/CspPictogram/pictograms'
import { computed, useSlots } from 'vue'
import CspBreadcrumb from '@/components/base/CspBreadcrumb/CspBreadcrumb.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspPictogram from '@/components/base/CspPictogram/CspPictogram.vue'
import CspSkeleton from '@/components/base/CspSkeleton/CspSkeleton.vue'

const props = defineProps<{
  title?: string
  subtitle?: string
  breadcrumb?: CspBreadcrumbItem[]
  backLink?: { to: RouteLocationRaw, label: string }
  showTitleSkeleton?: boolean
  showSubtitleSkeleton?: boolean
  pictogram?: CspPictogramName
  highlighted?: boolean
}>()

const slots = useSlots()

const hasBreadcrumb = computed(() => Boolean(props.breadcrumb?.length))
const hasSubtitle = computed(() => Boolean(props.subtitle || slots.subtitle || props.showSubtitleSkeleton))
</script>

<template>
  <header
    class="csp-page-header"
    :class="{ 'csp-page-header--has-back-link': Boolean(backLink), 'csp-page-header--highlighted': highlighted }"
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
              class="csp-page-header__back-button"
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
          <div
            class="csp-page-header__subtitle"
            :class="{ 'csp-page-header__subtitle--empty': !hasSubtitle }"
          >
            <CspSkeleton
              v-if="showSubtitleSkeleton"
              width="28rem"
              height="1.375rem"
            />
            <slot
              v-else
              name="subtitle"
            >
              <p
                v-if="subtitle"
                class="csp-page-header__subtitle-text"
              >
                {{ subtitle }}
              </p>
            </slot>
          </div>
        </div>
      </div>
      <div
        v-if="pictogram"
        class="csp-page-header__pictogram"
      >
        <CspPictogram :name="pictogram" />
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
@use '@/styles/breakpoints' as bp;

.csp-page-header {
  background: var(--csp-page-header-backdrop), var(--csp-chrome-background);

  --csp-page-header-back-link-size: 0;
  --csp-page-header-back-link-gap: 0;

  &.csp-page-header--has-back-link {
    --csp-page-header-back-link-size: 2rem;
    --csp-page-header-back-link-gap: var(--csp-space-2);
  }

  &.csp-page-header--highlighted {
    --csp-page-header-backdrop: var(--csp-page-header-backdrop-highlighted);
    --csp-chrome-background: var(--csp-page-header-background-highlighted);
    --csp-page-header-pictogram-major-color: var(--csp-page-header-pictogram-major-color-highlighted);
    --csp-page-header-pictogram-minor-color: var(--csp-page-header-pictogram-minor-color-highlighted);
    --csp-page-header-pictogram-decorative-color: var(--csp-page-header-pictogram-decorative-color-highlighted);

    color: var(--csp-page-header-color-highlighted);
  }
}

.csp-page-header__top-row {
  padding-top: var(--csp-page-header-padding-top);
  padding-bottom: var(--csp-page-header-breadcrumb-gap);
  padding-inline: var(--csp-page-container-padding-inline);
}

.csp-page-header__breadcrumb-wrapper {
  min-height: var(--csp-page-header-breadcrumb-height);
}

.csp-page-header__main-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding-bottom: var(--csp-page-header-padding-bottom);
  border-bottom: var(--csp-chrome-border-width) solid var(--csp-page-header-border-color);
  padding-inline: var(--csp-page-container-padding-inline);

  @include bp.from(bp.$md) {
    margin-inline: var(--csp-page-header-border-inset);
    padding-inline: calc(var(--csp-page-container-padding-inline) - var(--csp-page-header-border-inset));
  }
}

/* above tabs the line under the header takes its own width, and framed tabs draw it themselves */
.csp-page-header:has(+ .csp-page-container--tabs) .csp-page-header__main-row {
  border-bottom-width: calc((1 - var(--csp-tabs-framed)) * var(--csp-page-header-border-width-tabs));
}

.csp-page-header__hgroup-wrapper {
  display: flex;
  gap: var(--csp-page-header-back-link-gap);

  @include bp.from(bp.$lg) {
    margin-left: calc(calc(var(--csp-page-header-back-link-size) + var(--csp-page-header-back-link-gap)) * -1);
  }
}

.csp-page-header__hgroup {
  display: flex;
  flex-direction: column;
  gap: var(--csp-page-header-subtitle-gap);
}

.csp-page-header__back-link {
  margin-top: var(--csp-space-1);

  @include bp.from(bp.$lg) {
    width: var(--csp-page-header-back-link-size);
  }
}

.csp-page-header__back-button {
  @include bp.below(bp.$lg) {
    margin-inline-start: calc(-1 * var(--csp-btn-icon-inset));
  }
}

.csp-page-header__title {
  font-weight: var(--csp-text-page-title-weight, 600);
  font-size: var(--csp-text-page-title-size, 1.5rem);
  line-height: var(--csp-text-page-title-line-height, inherit);
  min-height: var(--csp-page-header-title-height);
}

.csp-page-header__title-skeleton {
  height: var(--csp-page-header-title-height);
}

.csp-page-header__subtitle {
  min-height: var(--csp-page-header-subtitle-height);
}

.csp-page-header__subtitle--empty {
  min-height: var(--csp-page-header-subtitle-height-empty);
}

.csp-page-header__subtitle-text {
  margin: 0;
  color: var(--text-mention-grey);

  .csp-page-header--highlighted & {
    color: var(--csp-page-header-subtitle-color-highlighted);
  }
}

.csp-page-header__pictogram {
  --csp-pictogram-major-color: var(--csp-page-header-pictogram-major-color);
  --csp-pictogram-minor-color: var(--csp-page-header-pictogram-minor-color);
  --csp-pictogram-decorative-color: var(--csp-page-header-pictogram-decorative-color);

  display: var(--csp-page-header-pictogram-display);
  flex-shrink: 0;
  height: var(--csp-page-header-pictogram-height);
  margin-block: var(--csp-page-header-pictogram-margin-block);
  margin-inline-start: auto;
  overflow: hidden;

  .csp-pictogram {
    width: var(--csp-page-header-pictogram-size);
    height: var(--csp-page-header-pictogram-size);
  }

  /* the title wraps over several lines on a phone, and the pictogram would take its width */
  @include bp.below(bp.$md) {
    display: none;
  }
}

.csp-page-header__actions {
  display: flex;
  align-items: center;
  align-self: flex-start;
  gap: var(--csp-space-2);
  flex-shrink: 0;
}
</style>
