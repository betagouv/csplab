<script setup lang="ts">
import {
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogOverlay,
  DialogPortal,
  DialogRoot,
  DialogTitle,
} from 'reka-ui'
import CspButton from '@/components/base/CspButton/CspButton.vue'

// Panneau modal qui monte du bas de l'écran. Même base (Reka Dialog) et mêmes tokens que
// CspDialog / CspDrawer, dont aucun ne propose une ancre « bas » — voir NOTES.md.
defineProps<{
  open: boolean
  title: string
  description?: string
}>()

defineEmits<{
  'update:open': [value: boolean]
}>()
</script>

<template>
  <DialogRoot
    :open="open"
    @update:open="value => $emit('update:open', value)"
  >
    <DialogPortal>
      <DialogOverlay class="sheet__overlay" />
      <DialogContent class="sheet">
        <span
          class="sheet__poignee"
          aria-hidden="true"
        />
        <header class="sheet__header">
          <div class="sheet__heading">
            <DialogTitle class="sheet__title">
              {{ title }}
            </DialogTitle>
            <DialogDescription
              class="sheet__description"
              :class="{ 'sheet__description--masquee': !description }"
            >
              {{ description ?? title }}
            </DialogDescription>
          </div>
          <DialogClose as-child>
            <CspButton
              variant="tertiary-no-outline"
              size="sm"
              icon="ri:close-line"
              aria-label="Fermer"
              class="sheet__close"
            />
          </DialogClose>
        </header>

        <div class="sheet__body">
          <slot />
        </div>

        <footer
          v-if="$slots.footer"
          class="sheet__footer"
        >
          <slot name="footer" />
        </footer>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>

<style scoped lang="scss">
.sheet__overlay {
  position: fixed;
  inset: 0;
  background-color: var(--csp-overlay-scrim);
  z-index: var(--csp-z-overlay);
}

.sheet {
  position: fixed;
  bottom: 0;
  left: 50%;
  width: min(100vw, 26rem);
  max-height: 90vh;
  overflow: auto;
  transform: translateX(-50%);
  z-index: var(--csp-z-modal);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding: var(--csp-space-2) var(--csp-space-4) max(var(--csp-space-4), env(safe-area-inset-bottom));
  border-radius: 1rem 1rem 0 0;
  background-color: var(--background-overlap-grey);
  box-shadow:
    inset 0 0 0 1px var(--border-default-grey),
    var(--csp-shadow-lg);
  outline: none;

  &[data-state='open'] {
    animation: sheet-monte 0.22s ease-out;
  }

  &[data-state='closed'] {
    animation: sheet-descend 0.16s ease-in;
  }
}

.sheet__poignee {
  align-self: center;
  width: 2.5rem;
  height: 0.25rem;
  border-radius: 999px;
  background-color: var(--border-default-grey);
}

.sheet__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--csp-space-3);
}

.sheet__heading {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.sheet__title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.sheet__description {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-mention-grey);

  &--masquee {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip-path: inset(50%);
  }
}

.sheet__close {
  flex-shrink: 0;
  min-width: 2.75rem;
  min-height: 2.75rem;
}

.sheet__body {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.sheet__footer {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

@keyframes sheet-monte {
  from {
    transform: translate(-50%, 100%);
  }

  to {
    transform: translate(-50%, 0);
  }
}

@keyframes sheet-descend {
  from {
    transform: translate(-50%, 0);
  }

  to {
    transform: translate(-50%, 100%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .sheet[data-state='open'],
  .sheet[data-state='closed'] {
    animation: none;
  }
}
</style>
