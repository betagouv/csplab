<script setup lang="ts">
import MobileStepProgress from './MobileStepProgress.vue'
import MobileTopBar from './MobileTopBar.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'

withDefaults(defineProps<{
  title?: string
  steps: string[]
  currentIndex: number
  isLastContentStep?: boolean
  nextDisabled?: boolean
  nextLabel?: string
}>(), {
  title: '',
  isLastContentStep: false,
  nextDisabled: false,
  nextLabel: undefined,
})

defineEmits<{
  back: []
  next: []
}>()
</script>

<template>
  <div class="mobile-flow">
    <MobileTopBar
      :title="title"
      show-back
      @back="$emit('back')"
    />
    <MobileStepProgress
      :steps="steps"
      :current-index="currentIndex"
    />

    <div class="mobile-flow__content">
      <slot />
    </div>

    <div class="mobile-flow__cta">
      <CspButton
        variant="primary"
        size="lg"
        :label="nextLabel ?? (isLastContentStep ? 'Envoyer ma candidature' : 'Continuer')"
        :disabled="nextDisabled"
        class="mobile-flow__cta-button"
        @click="$emit('next')"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.mobile-flow {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--background-default-grey);
}

.mobile-flow__content {
  flex: 1;
  padding: var(--csp-space-4) var(--csp-space-4) calc(var(--csp-space-8) * 2);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.mobile-flow__cta {
  position: sticky;
  bottom: 0;
  padding: var(--csp-space-3) var(--csp-space-4) max(var(--csp-space-3), env(safe-area-inset-bottom));
  background-color: var(--background-default-grey);
  box-shadow: inset 0 1px 0 var(--border-default-grey), 0 -2px 8px rgb(0 0 0 / 6%);
}

.mobile-flow__cta-button {
  width: 100%;
  justify-content: center;
  min-height: 3rem;
}

@media (min-width: 40rem) {
  .mobile-flow {
    max-width: 32rem;
    margin: 0 auto;
    box-shadow: inset 0 0 0 1px var(--border-default-grey);
    min-height: auto;
    margin-top: var(--csp-space-6);
    margin-bottom: var(--csp-space-6);
    border-radius: 0.5rem;
    overflow: hidden;
  }
}
</style>
