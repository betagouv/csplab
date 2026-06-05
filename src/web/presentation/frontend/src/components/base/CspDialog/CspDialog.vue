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

export interface CspDialogProps {
  open?: boolean
  defaultOpen?: boolean
  modal?: boolean
  title?: string | null
  description?: string | null
  ariaLabel?: string

  size?: 'sm' | 'md' | 'lg'
  showClose?: boolean
  closeLabel?: string
}

defineOptions({
  inheritAttrs: false,
})

const props = withDefaults(defineProps<CspDialogProps>(), {
  open: undefined,
  defaultOpen: false,
  modal: true,
  title: null,
  description: null,
  ariaLabel: undefined,
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
      <DialogOverlay class="csp-dialog__overlay" />
      <DialogContent
        v-bind="attrs"
        :aria-label="ariaLabel"
        class="csp-dialog"
        :class="[
          `csp-dialog--${size}`,
          {
            'csp-dialog--has-footer': hasFooter,
          },
        ]"
      >
        <header class="csp-dialog__header">
          <div class="csp-dialog__heading">
            <DialogTitle
              v-if="hasTitle"
              class="csp-dialog__title"
            >
              <slot name="title">
                {{ title }}
              </slot>
            </DialogTitle>

            <DialogDescription
              v-if="hasDescription"
              class="csp-dialog__description"
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

        <div class="csp-dialog__body">
          <slot />
        </div>

        <footer
          v-if="hasFooter"
          class="csp-dialog__footer"
        >
          <slot name="footer" />
        </footer>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>

<style scoped lang="scss">
.csp-dialog__overlay {
  position: fixed;
  inset: 0;
  background-color: var(--csp-overlay-scrim);
  z-index: var(--csp-z-overlay);
}

.csp-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  width: min(calc(100vw - (var(--csp-space-4) * 2)), var(--csp-dialog-max-width));
  max-height: calc(100vh - (var(--csp-space-6) * 2));

  overflow: auto;
  outline: none;
  background-color: var(--background-overlap-grey);
  color: var(--text-default-grey);
  border-radius: 0.25rem;
  box-shadow:
    inset 0 0 0 1px var(--border-default-grey),
    var(--csp-shadow-lg);

  z-index: var(--csp-z-modal);
  padding: var(--csp-space-6);

  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.csp-dialog--sm {
  --csp-dialog-max-width: 24rem;
}

.csp-dialog--md {
  --csp-dialog-max-width: 32rem;
}

.csp-dialog--lg {
  --csp-dialog-max-width: 44rem;
}

.csp-dialog__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--csp-space-4);
}

.csp-dialog__heading {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.csp-dialog__title {
  color: var(--text-title-grey);
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1.25;
}

.csp-dialog__description {
  color: var(--text-mention-grey);
  font-size: 0.875rem;
  line-height: 1.4;
}

.csp-dialog__body {
  font-size: 0.875rem;
  line-height: 1.5;
}

.csp-dialog__footer {
  display: flex;
  justify-content: flex-end;
}
</style>
