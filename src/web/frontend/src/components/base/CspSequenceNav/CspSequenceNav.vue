<script setup lang="ts">
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'

const props = withDefaults(defineProps<{
  position: number | null
  total: number
  itemLabel?: string
  label?: string
  previousDisabled?: boolean
  nextDisabled?: boolean
}>(), {
  itemLabel: 'Élément',
  label: 'Navigation entre les éléments',
  previousDisabled: false,
  nextDisabled: false,
})

const emit = defineEmits<{
  previous: []
  next: []
}>()

const counter = computed(() =>
  props.position === null ? null : `${props.itemLabel} ${props.position} sur ${props.total}`,
)
</script>

<template>
  <nav
    class="csp-sequence-nav"
    :aria-label="label"
  >
    <CspButton
      label="Précédent"
      variant="secondary"
      size="sm"
      icon="ri:arrow-left-line"
      is-icon-left
      :disabled="previousDisabled"
      @click="emit('previous')"
    />
    <div class="csp-sequence-nav__status">
      <slot />
      <p
        class="csp-sequence-nav__counter"
        aria-live="polite"
      >
        {{ counter }}
      </p>
    </div>
    <CspButton
      label="Suivant"
      variant="secondary"
      size="sm"
      icon="ri:arrow-right-line"
      :disabled="nextDisabled"
      @click="emit('next')"
    />
  </nav>
</template>

<style scoped lang="scss">
@use '@/styles/breakpoints' as bp;

.csp-sequence-nav {
  container-type: inline-size;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-3) var(--csp-space-4);
  width: 100%;
}

.csp-sequence-nav__status {
  flex: 1 1 0;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 0.875rem;
  line-height: 1.4;
  color: var(--text-default-grey);
  text-align: center;

  @container (width < #{bp.$sm}) {
    flex-basis: 100%;
    order: -1;
  }
}

.csp-sequence-nav__counter {
  min-height: 1.4em;
  margin: 0;
  font-weight: 700;
  color: var(--text-title-grey);
}
</style>
