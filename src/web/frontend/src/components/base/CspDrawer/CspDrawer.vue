<script setup lang="ts">
import {
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogOverlay,
  DialogPortal,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
} from 'reka-ui'
import { computed, useAttrs, useSlots } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'

export interface CspDrawerProps {
  open?: boolean
  defaultOpen?: boolean
  modal?: boolean
  overlay?: boolean
  title?: string | null
  description?: string | null
  ariaLabel?: string

  side?: 'left' | 'right'
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'full'
  showClose?: boolean
  closeLabel?: string
}

defineOptions({
  inheritAttrs: false,
})

const props = withDefaults(defineProps<CspDrawerProps>(), {
  open: undefined,
  defaultOpen: false,
  modal: true,
  overlay: true,
  title: null,
  description: null,
  ariaLabel: undefined,
  side: 'right',
  size: 'md',
  showClose: true,
  closeLabel: 'Fermer',
})

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

const attrs = useAttrs()
const slots = useSlots()

const hasTrigger = computed(() => Boolean(slots.trigger))
const hasStart = computed(() => Boolean(slots.start))
const hasTitle = computed(() => Boolean(slots.title) || Boolean(props.title))
const hasDescription = computed(() => Boolean(slots.description) || Boolean(props.description))
const hasFooter = computed(() => Boolean(slots.footer))
</script>

<template>
  <DialogRoot
    :open="open"
    :default-open="defaultOpen"
    :modal="modal"
    @update:open="value => emit('update:open', value)"
  >
    <DialogTrigger
      v-if="hasTrigger"
      as-child
    >
      <slot name="trigger" />
    </DialogTrigger>

    <DialogPortal>
      <DialogOverlay
        v-if="overlay"
        class="csp-drawer__overlay"
      />
      <DialogContent
        v-bind="attrs"
        :aria-label="ariaLabel"
        class="csp-drawer"
        :class="[
          `csp-drawer--${side}`,
          `csp-drawer--${size}`,
          {
            'csp-drawer--has-footer': hasFooter,
            'csp-drawer--modal-no-overlay': modal && !overlay,
          },
        ]"
      >
        <header class="csp-drawer__header">
          <div
            v-if="hasStart"
            class="csp-drawer__start"
          >
            <slot name="start" />
          </div>

          <div class="csp-drawer__heading">
            <div
              v-if="hasTitle"
              class="csp-drawer__title-row"
            >
              <DialogTitle class="csp-drawer__title">
                <slot name="title">
                  {{ title }}
                </slot>
              </DialogTitle>
              <slot name="title-end" />
            </div>

            <DialogDescription
              v-if="hasDescription"
              class="csp-drawer__description"
            >
              <slot name="description">
                {{ description }}
              </slot>
            </DialogDescription>

            <div
              v-if="$slots.meta"
              class="csp-drawer__meta"
            >
              <slot name="meta" />
            </div>
          </div>

          <div
            v-if="$slots.end"
            class="csp-drawer__end"
          >
            <slot name="end" />
          </div>

          <DialogClose
            v-if="showClose"
            as-child
          >
            <CspButton
              class="csp-drawer__close"
              variant="tertiary-no-outline"
              size="sm"
              icon="ri:close-line"
              :aria-label="closeLabel"
            />
          </DialogClose>
        </header>

        <div class="csp-drawer__body">
          <slot />
        </div>

        <footer
          v-if="hasFooter"
          class="csp-drawer__footer"
        >
          <slot name="footer" />
        </footer>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>

<style lang="scss">
:root:has(.csp-drawer--modal-no-overlay[data-state='open']) {
  overflow: hidden;
}
</style>

<style scoped lang="scss">
@use '@/styles/breakpoints' as bp;

.csp-drawer__overlay {
  position: fixed;
  inset: 0;
  background-color: var(--csp-overlay-scrim);
  z-index: var(--csp-z-overlay);

  &[data-state='open'] {
    animation: var(--csp-motion-scrim-enter);
  }

  &[data-state='closed'] {
    animation: var(--csp-motion-scrim-exit);
  }
}

.csp-drawer {
  --csp-drawer-body-gap: var(--csp-space-5);

  position: fixed;
  top: 0;
  bottom: 0;

  width: min(calc(100vw - var(--csp-space-4)), var(--base-drawer-width));

  outline: none;
  background-color: var(--background-overlap-grey);
  color: var(--text-default-grey);
  box-shadow: var(--csp-shadow-lg);
  z-index: var(--csp-z-modal);

  display: flex;
  flex-direction: column;
}

.csp-drawer--right {
  right: 0;
  border-left: 1px solid var(--border-default-grey);
  border-radius: var(--csp-radius-edge) 0 0 var(--csp-radius-edge);

  &[data-state='open'] {
    animation: var(--csp-motion-panel-enter-right);
  }

  &[data-state='closed'] {
    animation: var(--csp-motion-panel-exit-right);
  }
}

.csp-drawer--left {
  left: 0;
  border-right: 1px solid var(--border-default-grey);
  border-radius: 0 var(--csp-radius-edge) var(--csp-radius-edge) 0;

  &[data-state='open'] {
    animation: var(--csp-motion-panel-enter-left);
  }

  &[data-state='closed'] {
    animation: var(--csp-motion-panel-exit-left);
  }
}

.csp-drawer--xs {
  --base-drawer-width: 16rem;
}

.csp-drawer--sm {
  --base-drawer-width: 20rem;
}

.csp-drawer--md {
  --base-drawer-width: 26rem;
}

.csp-drawer--lg {
  --base-drawer-width: 34rem;
}

.csp-drawer--xl {
  --base-drawer-width: 42rem;
}

.csp-drawer--full {
  --base-drawer-width: 100vw;
}

@include bp.below(bp.$sm) {
  .csp-drawer {
    --base-drawer-width: 100vw;
  }
}

@include bp.from(bp.$sm) {
  @include bp.below(bp.$md) {
    .csp-drawer--lg,
    .csp-drawer--xl,
    .csp-drawer--full {
      --base-drawer-width: 80vw;
    }
  }
}

.csp-drawer__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding-block: var(--csp-space-6);
  padding-inline: var(--csp-drawer-padding-inline, var(--csp-space-6));
  border-bottom: 1px solid var(--border-default-grey);
  background-image: var(--csp-drawer-header-backdrop, none);
  background-repeat: var(--csp-drawer-header-backdrop-repeat, no-repeat);
  background-position: var(--csp-drawer-header-backdrop-position, right bottom);
  background-size: var(--csp-drawer-header-backdrop-size, cover);
}

.csp-drawer__start {
  display: flex;
  flex-shrink: 0;
  margin-block: calc(-1 * var(--csp-space-1));
}

.csp-drawer__start :slotted(.csp-btn--icon-only) {
  margin-inline-start: calc(-1 * var(--csp-btn-icon-inset));
}

.csp-drawer__end {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  gap: var(--csp-space-2);
  margin-block: calc(-1 * var(--csp-space-1));
}

.csp-drawer__close {
  margin-block: calc(-1 * var(--csp-space-1));
  margin-inline-end: calc(-1 * var(--csp-btn-icon-inset));
}

.csp-drawer__heading {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.csp-drawer__title-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-1) var(--csp-space-3);
  min-width: 0;
}

.csp-drawer__meta {
  margin-top: var(--csp-space-2);
}

.csp-drawer__title {
  color: var(--text-title-grey);
  font-size: var(--csp-text-section-title-size, 1.125rem);
  font-weight: var(--csp-text-section-title-weight, 700);
  line-height: var(--csp-text-section-title-line-height, 1.25);
}

.csp-drawer__description {
  color: var(--text-mention-grey);
  font-size: 0.875rem;
  line-height: 1.4;
}

.csp-drawer__body {
  flex: 1 1 auto;
  overflow: auto;
  overscroll-behavior: contain;
  padding-block: var(--csp-space-6);
  padding-inline: var(--csp-drawer-padding-inline, var(--csp-space-6));
  font-size: 0.875rem;
  line-height: 1.5;
}

.csp-drawer__footer {
  padding-block: var(--csp-space-6);
  padding-inline: var(--csp-drawer-padding-inline, var(--csp-space-6));
  border-top: 1px solid var(--border-default-grey);
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: var(--csp-space-3);
}
</style>
