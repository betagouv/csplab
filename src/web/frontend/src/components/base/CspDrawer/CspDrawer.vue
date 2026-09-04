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
  title: null,
  description: null,
  ariaLabel: undefined,
  side: 'right',
  size: 'md',
  showClose: true,
  closeLabel: 'Close',
})

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

const attrs = useAttrs()
const slots = useSlots()

const hasTrigger = computed(() => Boolean(slots.trigger))
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
      <DialogOverlay class="csp-drawer__overlay" />
      <DialogContent
        v-bind="attrs"
        :aria-label="ariaLabel"
        class="csp-drawer"
        :class="[
          `csp-drawer--${side}`,
          `csp-drawer--${size}`,
          {
            'csp-drawer--has-footer': hasFooter,
          },
        ]"
      >
        <header class="csp-drawer__header">
          <div class="csp-drawer__heading">
            <DialogTitle
              v-if="hasTitle"
              class="csp-drawer__title"
            >
              <slot name="title">
                {{ title }}
              </slot>
            </DialogTitle>

            <DialogDescription
              v-if="hasDescription"
              class="csp-drawer__description"
            >
              <slot name="description">
                {{ description }}
              </slot>
            </DialogDescription>
          </div>

          <DialogClose
            v-if="showClose"
            as-child
          >
            <CspButton
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

<style scoped lang="scss">
.csp-drawer__overlay {
  position: fixed;
  inset: 0;
  background-color: var(--csp-overlay-scrim);
  z-index: var(--csp-z-overlay);
}

.csp-drawer {
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
}

.csp-drawer--left {
  left: 0;
  border-right: 1px solid var(--border-default-grey);
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

@media (width <= 36em) {
  .csp-drawer {
    --base-drawer-width: 100vw;
  }
}

@media (36em < width <= 48em) {
  .csp-drawer--lg,
  .csp-drawer--xl,
  .csp-drawer--full {
    --base-drawer-width: 80vw;
  }
}

.csp-drawer__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding: var(--csp-space-6);
  border-bottom: 1px solid var(--border-default-grey);
}

.csp-drawer__heading {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.csp-drawer__title {
  color: var(--text-title-grey);
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1.25;
}

.csp-drawer__description {
  color: var(--text-mention-grey);
  font-size: 0.875rem;
  line-height: 1.4;
}

.csp-drawer__body {
  flex: 1 1 auto;
  overflow: auto;
  padding: var(--csp-space-6);
  font-size: 0.875rem;
  line-height: 1.5;
}

.csp-drawer__footer {
  padding: var(--csp-space-6);
  border-top: 1px solid var(--border-default-grey);
  display: flex;
  justify-content: flex-end;
}
</style>
