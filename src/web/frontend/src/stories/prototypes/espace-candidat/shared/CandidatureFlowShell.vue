<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CandidateHeader from './CandidateHeader.vue'
import CandidatureStepper from './CandidatureStepper.vue'

withDefaults(defineProps<{
  steps: string[]
  currentIndex: number
  isLastContentStep?: boolean
  nextDisabled?: boolean
  showAccountHint?: boolean
}>(), {
  isLastContentStep: false,
  nextDisabled: false,
  showAccountHint: true,
})

defineEmits<{
  back: []
  next: []
}>()
</script>

<template>
  <div class="flow-shell">
    <CandidateHeader
      variant="public"
      :show-account-hint="showAccountHint"
    />

    <main class="flow-shell__main">
      <div class="flow-shell__card">
        <CandidatureStepper
          :steps="steps"
          :current-index="currentIndex"
        />

        <div class="flow-shell__content">
          <slot />
        </div>

        <div class="flow-shell__footer">
          <CspButton
            v-if="currentIndex > 0"
            variant="secondary"
            label="Retour"
            @click="$emit('back')"
          />
          <span v-else />

          <CspButton
            variant="primary"
            :label="isLastContentStep ? 'Envoyer ma candidature' : 'Continuer'"
            :disabled="nextDisabled"
            @click="$emit('next')"
          />
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped lang="scss">
.flow-shell {
  min-height: 100vh;
  background-color: var(--background-alt-grey);
}

.flow-shell__main {
  display: flex;
  justify-content: center;
  padding: var(--csp-space-8) var(--csp-space-6);
}

.flow-shell__card {
  width: 100%;
  max-width: 36rem;
  background-color: var(--background-default-grey);
  border-radius: 0.5rem;
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  padding: var(--csp-space-6);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.flow-shell__content {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.flow-shell__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: var(--csp-space-4);
  border-top: 1px solid var(--border-default-grey);
}
</style>
