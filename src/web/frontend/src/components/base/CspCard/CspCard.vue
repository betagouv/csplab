<script setup lang="ts">
import { computed, useSlots } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export interface CspCardProps {
  as?: string
  variant?: 'default' | 'alt'
  size?: 'sm' | 'md' | 'lg'
  title?: string | null
  titleAs?: 'h2' | 'h3' | 'h4' | 'h5' | 'h6'
  description?: string | null
  href?: string
}

const props = withDefaults(defineProps<CspCardProps>(), {
  as: 'article',
  variant: 'default',
  size: 'md',
  title: null,
  titleAs: 'h3',
  description: null,
})

const slots = useSlots()

const hasTitle = computed(() => Boolean(slots.title) || Boolean(props.title))
const hasDescription = computed(() => Boolean(slots.description) || Boolean(props.description))
const hasHeader = computed(() => hasTitle.value || hasDescription.value)
const hasStart = computed(() => Boolean(slots.start))
const hasBody = computed(() => Boolean(slots.default))
const hasEnd = computed(() => Boolean(slots.end))
const hasFooter = computed(() => Boolean(slots.footer))
const isLink = computed(() => Boolean(props.href))
</script>

<template>
  <component
    :is="as"
    class="csp-card"
    :class="[
      `csp-card--${variant}`,
      `csp-card--${size}`,
      {
        'csp-card--link': isLink,
      },
    ]"
  >
    <div
      v-if="hasStart"
      class="csp-card__start"
    >
      <slot name="start" />
    </div>

    <header
      v-if="hasHeader"
      class="csp-card__header"
    >
      <component
        :is="titleAs"
        v-if="hasTitle"
        class="csp-card__title"
      >
        <a
          v-if="isLink"
          :href="href"
          class="csp-card__link"
        >
          <slot name="title">{{ title }}</slot>
        </a>
        <slot
          v-else
          name="title"
        >
          {{ title }}
        </slot>
      </component>

      <p
        v-if="hasDescription"
        class="csp-card__description"
      >
        <slot name="description">
          {{ description }}
        </slot>
      </p>
    </header>

    <div
      v-if="hasBody"
      class="csp-card__body"
    >
      <slot />
    </div>

    <div
      v-if="hasEnd"
      class="csp-card__end"
    >
      <slot name="end" />
    </div>

    <footer
      v-if="hasFooter"
      class="csp-card__footer"
    >
      <slot name="footer" />
    </footer>

    <CspIcon
      v-if="isLink"
      name="ri:arrow-right-line"
      class="csp-card__arrow"
      :size="20"
    />
  </component>
</template>

<style scoped lang="scss">
.csp-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--csp-card-gap);

  background-color: var(--csp-card-bg);
  color: var(--csp-card-text);
  border-radius: var(--csp-card-radius);
  padding: var(--csp-card-padding);
  box-shadow: inset 0 0 0 1px var(--csp-card-border);

  --csp-card-bg: var(--background-default-grey);
  --csp-card-text: var(--text-default-grey);
  --csp-card-border: var(--border-default-grey);
  --csp-card-radius: 0.25rem;
  --csp-card-gap: var(--csp-space-4);
  --csp-card-padding: var(--csp-space-4);
  --csp-card-title-size: 1.125rem;
  --csp-card-text-size: 0.875rem;
}

.csp-card--alt {
  --csp-card-bg: var(--background-alt-grey);
}

.csp-card--sm {
  --csp-card-gap: var(--csp-space-3);
  --csp-card-padding: var(--csp-space-3);
  --csp-card-title-size: 1rem;
  --csp-card-text-size: 0.875rem;
}

.csp-card--md {
  --csp-card-gap: var(--csp-space-4);
  --csp-card-padding: var(--csp-space-5);
  --csp-card-title-size: 1.125rem;
  --csp-card-text-size: 0.875rem;
}

.csp-card--lg {
  --csp-card-gap: var(--csp-space-5);
  --csp-card-padding: var(--csp-space-6);
  --csp-card-title-size: 1.25rem;
  --csp-card-text-size: 1rem;
}

.csp-card__header {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.csp-card__title {
  margin: 0;
  color: var(--text-title-grey);
  font-size: var(--csp-card-title-size);
  font-weight: 700;
  line-height: 1.25;
}

.csp-card__description {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: var(--csp-card-text-size);
  line-height: 1.4;
}

.csp-card__start,
.csp-card__end {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2);
}

.csp-card__end {
  color: var(--text-mention-grey);
  font-size: 0.75rem;
}

.csp-card__body {
  font-size: var(--csp-card-text-size);
  line-height: 1.5;
}

.csp-card__footer {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-3);
}

.csp-card__arrow {
  align-self: flex-end;
  color: var(--text-action-high-blue-france);
}

.csp-card__link {
  color: inherit;
  text-decoration: none;
  background-image: none;

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: inherit;
  }
}

.csp-card--link {
  .csp-card__title {
    color: var(--text-action-high-blue-france);
  }

  &:hover {
    --csp-card-bg: var(--background-alt-grey);

    .csp-card__link {
      text-decoration: underline;
    }
  }

  &:focus-within {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }

  :where(a:not(.csp-card__link), button) {
    position: relative;
    z-index: 1;
  }
}
</style>
