<script setup lang="ts">
// Bloc de contenu sobre d'une étape. `nature="candidat"` signale le contenu publié (liseré bleu).
withDefaults(defineProps<{
  titre?: string
  description?: string
  nature?: 'interne' | 'candidat'
}>(), { titre: undefined, description: undefined, nature: 'interne' })
</script>

<template>
  <section
    class="panel"
    :class="`panel--${nature}`"
  >
    <header
      v-if="titre || $slots.actions"
      class="panel__head"
    >
      <div>
        <h3
          v-if="titre"
          class="panel__title"
        >
          {{ titre }}
        </h3>
        <p
          v-if="description"
          class="panel__desc"
        >
          {{ description }}
        </p>
      </div>
      <slot name="actions" />
    </header>
    <div class="panel__body">
      <slot />
    </div>
  </section>
</template>

<style scoped lang="scss">
.panel {
  padding: var(--csp-space-5) var(--csp-space-6);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);

  &--candidat {
    box-shadow: inset 3px 0 0 var(--border-plain-blue-france);
  }
}

.panel__head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--csp-space-4);
  margin-bottom: var(--csp-space-4);
}

.panel__title {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  line-height: var(--csp-line-height-tight);
}

.panel__desc {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.panel__body {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}
</style>
