<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'

withDefaults(defineProps<{
  title?: string
  showBack?: boolean
  backLabel?: string
}>(), {
  title: '',
  showBack: false,
  backLabel: 'Retour',
})

defineEmits<{
  back: []
}>()
</script>

<template>
  <header class="topbar">
    <CspButton
      v-if="showBack"
      variant="tertiary-no-outline"
      size="sm"
      icon="ri:arrow-left-line"
      :aria-label="backLabel"
      class="topbar__back"
      @click="$emit('back')"
    />
    <p
      v-if="title"
      class="topbar__title"
    >
      {{ title }}
    </p>
    <div class="topbar__end">
      <slot name="end" />
    </div>
  </header>
</template>

<style scoped lang="scss">
.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  min-height: 3.25rem;
  padding: var(--csp-space-2) var(--csp-space-3);
  background-color: var(--background-default-grey);
  box-shadow: inset 0 -1px 0 var(--border-default-grey);
}

.topbar__back {
  flex-shrink: 0;
  min-width: 2.75rem;
  min-height: 2.75rem;
}

.topbar__title {
  flex: 1;
  min-width: 0;
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 700;
  color: var(--text-title-grey);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.topbar__end {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}
</style>
