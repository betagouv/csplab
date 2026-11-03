<script setup lang="ts">
import { nextTick, useTemplateRef } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { formatFileSize } from '@/utils/format'

export interface CspFileListItem {
  key: string
  name: string
  size: number
  error?: string
}

const props = withDefaults(defineProps<{
  items: CspFileListItem[]
  label: string
  disabled?: boolean
}>(), {
  disabled: false,
})

const emit = defineEmits<{
  remove: [key: string]
}>()

const list = useTemplateRef<HTMLUListElement>('list')

async function handleRemove(index: number): Promise<void> {
  const item = props.items[index]
  if (!item) {
    return
  }
  emit('remove', item.key)
  await nextTick()
  const buttons = list.value?.querySelectorAll<HTMLButtonElement>('button') ?? []
  buttons[Math.min(index, buttons.length - 1)]?.focus()
}
</script>

<template>
  <ul
    ref="list"
    class="csp-file-list"
    :aria-label="label"
    aria-live="polite"
  >
    <li
      v-for="(item, index) in items"
      :key="item.key"
      class="csp-file-list__item"
    >
      <div class="csp-file-list__row">
        <CspIcon
          class="csp-file-list__icon"
          name="ri:file-line"
        />
        <span class="csp-file-list__name">{{ item.name }}</span>
        <span class="csp-file-list__size">{{ formatFileSize(item.size) }}</span>
        <CspButton
          variant="tertiary-no-outline"
          size="sm"
          label="Retirer"
          :aria-label="`Retirer ${item.name}`"
          :disabled="disabled"
          @click="handleRemove(index)"
        />
      </div>
      <p
        v-if="item.error"
        class="csp-file-list__error"
      >
        <CspIcon
          name="ri:error-warning-fill"
          :size="14"
        />
        {{ item.error }}
      </p>
    </li>
  </ul>
</template>

<style scoped lang="scss">
.csp-file-list {
  --csp-file-list-icon-size: 1rem;

  margin: 0;
  padding: 0;
  list-style: none;
}

.csp-file-list__item + .csp-file-list__item {
  border-top: 1px solid var(--border-default-grey);
}

.csp-file-list__row {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  padding-block: var(--csp-space-1);
  font-size: var(--csp-font-size-base);
}

.csp-file-list__icon {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}

.csp-file-list__name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.csp-file-list__size {
  flex-shrink: 0;
  color: var(--text-mention-grey);
  font-size: var(--csp-font-size-xs);
}

.csp-file-list__error {
  display: flex;
  padding-inline-start: calc(var(--csp-file-list-icon-size) + var(--csp-space-2));
  gap: 0.375rem;
  align-items: center;
  margin: 0 0 var(--csp-space-1);
  color: var(--text-default-error);
  font-size: var(--csp-font-size-xs);
}
</style>
