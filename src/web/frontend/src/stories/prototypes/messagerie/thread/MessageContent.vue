<script setup lang="ts">
import type { Block } from '../shared/types'

defineProps<{
  content: Block[]
}>()
</script>

<template>
  <div class="message-content">
    <template
      v-for="(block, index) in content"
      :key="index"
    >
      <p v-if="block.type === 'p'">
        {{ block.text }}
      </p>
      <ul v-else>
        <li
          v-for="item in block.items"
          :key="item"
        >
          {{ item }}
        </li>
      </ul>
    </template>
  </div>
</template>

<style scoped>
.message-content {
  font-size: var(--csp-font-size-base);
  line-height: var(--csp-line-height-base);
  color: var(--text-default-grey);
  overflow-wrap: anywhere;
}

.message-content p {
  white-space: pre-line;
}

.message-content > * + * {
  margin-top: var(--csp-space-3);
}

.message-content ul {
  padding-left: var(--csp-space-5);
  list-style: disc;
}
</style>
