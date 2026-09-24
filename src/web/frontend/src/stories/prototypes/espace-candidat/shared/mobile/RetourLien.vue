<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

defineProps<{
  label: string
}>()

defineEmits<{
  retour: []
}>()
</script>

<template>
  <button
    type="button"
    class="retour"
    @click="$emit('retour')"
  >
    <CspIcon
      name="ri:arrow-left-line"
      :size="18"
    />
    {{ label }}
  </button>
</template>

<style scoped lang="scss">
.retour {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
  align-self: flex-start;
  min-height: 2.75rem;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-action-high-blue-france);
}
</style>
