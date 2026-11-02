<script setup lang="ts">
import { nextTick, useTemplateRef } from 'vue'
import CspTag from './CspTag.vue'

export interface CspDismissibleTagItem {
  value: string
  label: string
}

const props = defineProps<{
  items: CspDismissibleTagItem[]
  dismissLabel: (label: string) => string
}>()

const emit = defineEmits<{
  dismiss: [value: string]
}>()

const list = useTemplateRef<HTMLUListElement>('list')

async function handleDismiss(index: number): Promise<void> {
  const item = props.items[index]
  if (!item) {
    return
  }
  emit('dismiss', item.value)
  await nextTick()
  const buttons = list.value?.querySelectorAll<HTMLButtonElement>('button') ?? []
  buttons[Math.min(index, buttons.length - 1)]?.focus()
}
</script>

<template>
  <ul
    ref="list"
    class="csp-dismissible-tag-list"
  >
    <li
      v-for="(item, index) in items"
      :key="item.value"
    >
      <CspTag
        variant="dismissible"
        :label="item.label"
        :dismiss-label="dismissLabel(item.label)"
        @dismiss="handleDismiss(index)"
      />
    </li>
  </ul>
</template>

<style scoped lang="scss">
.csp-dismissible-tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}
</style>
