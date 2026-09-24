<script setup lang="ts">
import type { MessageDocument } from '../shared/types'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { formatFileSize } from '../shared/format'

defineProps<{
  documents: MessageDocument[]
}>()
</script>

<template>
  <ul
    class="message-documents"
    aria-label="Pièces jointes"
  >
    <li
      v-for="document in documents"
      :key="document.nom"
      class="message-documents__item"
    >
      <CspIcon
        name="ri:file-pdf-2-line"
        :size="24"
        class="message-documents__icon"
      />
      <span class="message-documents__text">
        <span class="message-documents__name">{{ document.nom }}</span>
        <span class="message-documents__size">PDF, {{ formatFileSize(document.taille) }}</span>
      </span>
      <a
        href="#"
        class="message-documents__open"
        @click.prevent
      >
        Ouvrir<span class="sr-only"> {{ document.nom }}</span>
      </a>
    </li>
  </ul>
</template>

<style scoped>
.message-documents {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  max-width: 26rem;
}

.message-documents__item {
  display: flex;
  gap: var(--csp-space-3);
  align-items: center;
  padding: var(--csp-space-2) var(--csp-space-3);
  background: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
}

.message-documents__icon {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}

.message-documents__text {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.message-documents__name {
  overflow: hidden;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.message-documents__size {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.message-documents__open {
  flex-shrink: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  text-underline-offset: 0.2em;
}

.message-documents__open:hover {
  text-decoration-thickness: 2px;
}

.message-documents__open:focus-visible {
  outline: var(--csp-focus-ring-width) solid var(--csp-focus-ring-color);
  outline-offset: var(--csp-focus-ring-offset);
}
</style>
