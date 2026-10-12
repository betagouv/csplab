<script setup lang="ts">
import type { CspMetaItem } from './types'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspTooltip from '@/components/base/CspTooltip/CspTooltip.vue'
import { useToast } from '@/composables/ui/useToast'

const props = withDefaults(defineProps<CspMetaItem & {
  size?: 'sm' | 'md' | 'lg'
}>(), {
  icon: undefined,
  copy: undefined,
  size: 'md',
})

const { addToast } = useToast()

async function copyLabel(): Promise<void> {
  try {
    await navigator.clipboard.writeText(props.label)
    addToast({ variant: 'success', title: props.copy?.confirmation, duration: 2000 })
  }
  catch {
    addToast({ variant: 'error', title: 'La copie a échoué' })
  }
}
</script>

<template>
  <span
    v-if="label"
    class="csp-meta"
    :class="[
      `csp-meta--${size}`,
    ]"
  >
    <CspIcon
      v-if="icon"
      :name="icon"
      :size="12"
      class="csp-meta__icon"
    />
    <span class="sr-only csp-meta__sr-label">{{ srLabel }} :</span>
    <span class="csp-meta__label">{{ label }}</span>
    <CspTooltip
      v-if="copy"
      :content="copy.action"
      side="bottom"
    >
      <CspButton
        class="csp-meta__copy"
        variant="tertiary-no-outline"
        size="sm"
        icon="ri:file-copy-line"
        :aria-label="copy.action"
        @click="copyLabel"
      />
    </CspTooltip>
  </span>
</template>

<style scoped lang="scss">
.csp-meta {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-meta-gap);
  min-width: 0;
  color: var(--text-mention-grey);
  font-size: var(--csp-meta-font-size);
  line-height: 1.4;

  --csp-meta-font-size: 0.75rem;
  --csp-meta-gap: 0.25rem;
}

.csp-meta__icon {
  width: 1em;
  height: 1em;
}

.csp-meta--sm {
  --csp-meta-font-size: 0.625rem;
  --csp-meta-gap: 0.125rem;
}

.csp-meta--md {
  --csp-meta-font-size: 0.875rem;
  --csp-meta-gap: 0.25rem;
}

.csp-meta--lg {
  --csp-meta-font-size: 1rem;
  --csp-meta-gap: 0.375rem;
}

.csp-meta__icon {
  flex: none;
}

.csp-meta__sr-label {
  user-select: none;
}

.csp-meta__label {
  min-width: 0;
}

.csp-meta__copy {
  margin-block: calc(-1 * var(--csp-btn-icon-inset));
  color: inherit;
}
</style>
