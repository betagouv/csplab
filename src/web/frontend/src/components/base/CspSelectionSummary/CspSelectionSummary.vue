<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'

withDefaults(defineProps<{
  summary: string
  editable?: boolean
}>(), {
  editable: true,
})

const emit = defineEmits<{
  edit: []
}>()
</script>

<template>
  <div class="csp-selection-summary">
    <p class="csp-selection-summary__text">
      {{ summary }}
    </p>
    <CspButton
      v-if="editable"
      variant="link"
      label="Modifier la sélection"
      @click="emit('edit')"
    />
  </div>
</template>

<style scoped lang="scss">
.csp-selection-summary {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-1);
}

.csp-selection-summary__text {
  margin: 0;
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}
</style>
