<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

// Section repliable de la page de l'offre. L'ancre (`id`) sert aux raccourcis « Accéder à ».
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
          {{ titre }}
          <CspIcon
            :name="ouvert ? 'ri:arrow-up-s-line' : 'ri:arrow-down-s-line'"
            :size="20"
          />
        </button>
      </h2>
      <div
        v-if="$slots.actions && ouvert"
        class="section__actions"
      >
        <slot name="actions" />
      </div>
    </header>
    <p
      v-if="description && ouvert"
      class="section__desc"
    >
      {{ description }}
    </p>
    <div
      v-show="ouvert"
      :id="`${id}-corps`"
      class="section__corps"
    >
      <slot />
    </div>
  </section>
</template>

<style scoped lang="scss">
.section {
  scroll-margin-top: var(--csp-space-6);
  padding: var(--csp-space-5) var(--csp-space-6);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.section__tete {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
}

.section__titre {
  flex: 1;
  margin: 0;
  font-size: 1.25rem;
}

.section__bouton {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
  text-align: left;
  cursor: pointer;

  :deep(svg) {
    color: var(--text-action-high-blue-france);
  }
}

.section__actions {
  display: flex;
  gap: var(--csp-space-2);
  order: -1;
  margin-left: auto;
}

.section__tete .section__actions {
  order: 0;
}

.section__desc {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.section__corps {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  margin-top: var(--csp-space-5);
}
</style>
