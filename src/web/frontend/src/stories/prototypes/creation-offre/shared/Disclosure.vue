<script setup lang="ts">
import { useId } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

// Section repliable : garde les informations conditionnelles ou facultatives
// à portée de main sans alourdir l'écran. Le résumé dit ce qu'elle contient, même fermée.
withDefaults(defineProps<{
  titre: string
  resume?: string
  facultatif?: boolean
  icon?: string
}>(), {
  resume: undefined,
  facultatif: false,
  icon: undefined,
})

const ouvert = defineModel<boolean>('ouvert', { default: false })
const id = useId()
</script>

<template>
  <section
    class="disclosure"
    :class="{ 'disclosure--open': ouvert }"
  >
    <h3 class="disclosure__heading">
      <button
        type="button"
        class="disclosure__toggle"
        :aria-expanded="ouvert"
        :aria-controls="id"
        @click="ouvert = !ouvert"
      >
        <CspIcon
          class="disclosure__chevron"
          name="ri:arrow-right-s-line"
          :size="20"
        />
        <CspIcon
          v-if="icon"
          :name="icon"
          :size="16"
          class="disclosure__icon"
        />
        <span class="disclosure__text">
          <span class="disclosure__title">
            {{ titre }}
            <span
              v-if="facultatif"
              class="disclosure__opt"
            >facultatif</span>
          </span>
          <span
            v-if="resume"
            class="disclosure__resume"
          >{{ resume }}</span>
        </span>
      </button>
    </h3>
    <div
      v-show="ouvert"
      :id="id"
      class="disclosure__body"
    >
      <slot />
    </div>
  </section>
</template>

<style scoped lang="scss">
.disclosure {
  border-top: 1px solid var(--border-default-grey);
}

.disclosure__heading {
  margin: 0;
  font-size: inherit;
}

.disclosure__toggle {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-2);
  width: 100%;
  padding: var(--csp-space-3) 0;
  border: 0;
  background: none;
  font: inherit;
  text-align: left;
  color: var(--text-default-grey);
  cursor: pointer;

  &:hover .disclosure__title {
    color: var(--text-action-high-blue-france);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
    outline-offset: 2px;
  }
}

.disclosure__chevron {
  flex-shrink: 0;
  margin-top: 1px;
  color: var(--text-action-high-blue-france);
  transition: transform 0.15s;

  .disclosure--open & {
    transform: rotate(90deg);
  }
}

.disclosure__icon {
  flex-shrink: 0;
  margin-top: 3px;
  color: var(--text-mention-grey);
}

.disclosure__text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.disclosure__title {
  font-weight: var(--csp-font-weight-bold);
}

.disclosure__opt {
  margin-left: var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}

.disclosure__resume {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.disclosure__body {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  padding: var(--csp-space-1) 0 var(--csp-space-5) calc(20px + var(--csp-space-2));
}
</style>
