<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'

defineProps<{
  selectedCount: number
}>()

const emit = defineEmits<{
  changerEtape: []
}>()

function handleChangerEtape(): void {
  emit('changerEtape')
}
</script>

<template>
  <div class="selection-action-bar">
    <p class="selection-action-bar__count">
      {{ selectedCount }} candidat{{ selectedCount > 1 ? 's' : '' }} sélectionné{{ selectedCount > 1 ? 's' : '' }}
    </p>

    <div class="selection-action-bar__actions">
      <CspButton
        label="Changer d'étape"
        icon="ri:arrow-left-right-line"
        variant="secondary"
        size="sm"
        @click="handleChangerEtape"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.selection-action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding: var(--csp-space-3) var(--csp-space-4);
  margin-bottom: var(--csp-space-4);
  background-color: var(--background-default-grey);
  border: 1px solid var(--border-default-grey);
}

.selection-action-bar__count {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.selection-action-bar__actions {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
}
</style>
