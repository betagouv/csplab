<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

// Section repliable de la page de l'offre. L'ancre (`id`) sert aux raccourcis « Accéder à ».
// Chevron à gauche du titre, actions éventuelles à droite.
defineProps<{ id: string, titre: string, description?: string }>()
const ouvert = defineModel<boolean>('ouvert', { default: true })
</script>

<template>
  <section
    :id="id"
    class="section"
  >
    <header class="section__tete">
      <h2 class="section__titre">
        <button
          type="button"
          class="section__bouton"
          :aria-expanded="ouvert"
          :aria-controls="`${id}-corps`"
          @click="ouvert = !ouvert"
        >
          <CspIcon
            :name="ouvert ? 'ri:arrow-down-s-line' : 'ri:arrow-right-s-line'"
            :size="24"
          />
          {{ titre }}
        </button>
      </h2>
      <div
        v-if="$slots.actions && ouvert"
        class="section__actions"
      >
        <slot name="actions" />
      </div>
    </header>
    <div
      v-if="$slots.intro && ouvert"
      class="section__intro"
    >
      <slot name="intro" />
    </div>
    <div
      v-show="ouvert"
      :id="`${id}-corps`"
      class="section__corps"
    >
      <p
        v-if="description"
        class="section__desc"
      >
        {{ description }}
      </p>
      <slot />
    </div>
  </section>
</template>

<style scoped lang="scss">
.section {
  scroll-margin-top: 4.5rem;
  padding: var(--csp-space-6) var(--csp-space-8);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.section__tete {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
}

.section__titre {
  margin: 0;
  font-size: 1.375rem;
  line-height: 1.3;
}

.section__bouton {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin-left: calc(-1 * var(--csp-space-1));
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
  cursor: pointer;

  :deep(svg) {
    color: var(--text-action-high-blue-france);
  }
}

.section__actions {
  display: flex;
  gap: var(--csp-space-2);
}

.section__intro {
  margin-top: var(--csp-space-1);
  padding-left: calc(24px + var(--csp-space-2) - var(--csp-space-1));
}

.section__corps {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  margin-top: var(--csp-space-6);
  padding-left: calc(24px + var(--csp-space-2) - var(--csp-space-1));
}

.section__desc {
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-contrast-info);
  font-size: var(--csp-font-size-sm);
}
</style>
