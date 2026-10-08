<script setup lang="ts">
import { AccordionContent, AccordionHeader, AccordionItem, AccordionTrigger } from 'reka-ui'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

export interface CspAccordionItemProps {
  value: string
  title: string
  headingLevel?: 2 | 3 | 4 | 5 | 6
}

withDefaults(defineProps<CspAccordionItemProps>(), {
  headingLevel: 3,
})
</script>

<template>
  <AccordionItem
    :value="value"
    class="csp-accordion__item"
  >
    <AccordionHeader
      :as="`h${headingLevel}`"
      class="csp-accordion__header"
    >
      <AccordionTrigger class="csp-accordion__trigger">
        <span class="csp-accordion__title">{{ title }}</span>
        <CspIcon
          name="ri:arrow-down-s-line"
          :size="20"
          class="csp-accordion__chevron"
        />
      </AccordionTrigger>
    </AccordionHeader>
    <AccordionContent class="csp-accordion__content">
      <slot />
    </AccordionContent>
  </AccordionItem>
</template>

<style scoped lang="scss">
.csp-accordion__item {
  border-bottom: 1px solid var(--border-default-grey);
}

.csp-accordion__header {
  margin: 0;
  font-size: 1rem;
}

.csp-accordion__trigger {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.75rem 1rem;
  font: inherit;
  font-weight: 500;
  line-height: 1.5;
  text-align: left;
  color: var(--text-action-high-grey);
  background: transparent;
  border: none;
  cursor: pointer;

  &:hover {
    background-color: var(--background-default-grey-hover);
  }

  &:active {
    background-color: var(--background-default-grey-active);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: -2px;
  }

  &[data-state='open'] {
    color: var(--text-action-high-blue-france);
  }
}

.csp-accordion__chevron {
  flex-shrink: 0;
  transition: transform 0.15s ease;

  [data-state='open'] > & {
    transform: rotate(180deg);
  }
}

.csp-accordion__content {
  padding: 0 1rem 1rem;
}

@media (prefers-reduced-motion: reduce) {
  .csp-accordion__chevron {
    transition: none;
  }
}
</style>
