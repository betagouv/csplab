<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'

defineProps<{
  canReset: boolean
}>()

const emit = defineEmits<{
  apply: []
  reset: []
}>()

const open = defineModel<boolean>('open', { required: true })
</script>

<template>
  <CspDrawer
    v-model:open="open"
    title="Filtres"
  >
    <div class="csp-filters-drawer">
      <slot />

      <div class="csp-filters-drawer__actions">
        <CspButton
          label="Appliquer les filtres"
          variant="primary"
          @click="emit('apply')"
        />
        <CspButton
          label="Réinitialiser"
          variant="tertiary"
          icon="ri:refresh-line"
          is-icon-left
          :disabled="!canReset"
          @click="emit('reset')"
        />
      </div>
    </div>
  </CspDrawer>
</template>

<style scoped lang="scss">
.csp-filters-drawer {
  display: flex;
  flex-direction: column;
  gap: var(--csp-drawer-body-gap);
}

.csp-filters-drawer__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-3);

  &:deep(button) {
    /* @todo We should not do this but have a CspButtonGroup component instead */
    flex: 1;
  }
}
</style>
