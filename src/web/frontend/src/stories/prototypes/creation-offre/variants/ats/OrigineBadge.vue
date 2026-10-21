<script setup lang="ts">
import type { OrigineFiche } from './store'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { LIBELLES_ORIGINE } from './store'

// Origine d'une fiche de poste : ATS, SIRH (simulé) ou document ajouté.
defineProps<{ origine: OrigineFiche, court?: boolean }>()
const ICONES: Record<OrigineFiche, string> = { ats: 'ri:file-text-line', sirh: 'ri:refresh-line', document: 'ri:attachment-2' }
const COURT: Record<OrigineFiche, string> = { ats: 'ATS', sirh: 'SIRH', document: 'Document' }
</script>

<template>
  <span
    class="origine"
    :class="`origine--${origine}`"
  >
    <CspIcon
      :name="ICONES[origine]"
      :size="12"
    />
    {{ court ? COURT[origine] : LIBELLES_ORIGINE[origine] }}
  </span>
</template>

<style scoped lang="scss">
.origine {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  padding: 0 var(--csp-space-2);
  border: 1px solid var(--border-default-grey);
  border-radius: 1rem;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
  white-space: nowrap;

  &--sirh {
    border-color: var(--border-default-blue-france);
    color: var(--text-action-high-blue-france);
  }
}
</style>
