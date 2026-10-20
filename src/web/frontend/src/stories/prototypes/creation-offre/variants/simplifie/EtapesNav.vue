<script setup lang="ts">
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { ETAPES, useEtapes } from './useEtapes'

// 4 étapes cliquables dans n'importe quel ordre. Progression discrète : une coche quand
// l'étape a été vue et ne manque de rien ; aucun compteur d'erreurs.
const { etape, aller, faite, index } = useEtapes()
</script>

<template>
  <nav
    class="etapes"
    aria-label="Étapes de création de l'offre"
  >
    <ol class="etapes__list">
      <li
        v-for="(e, i) in ETAPES"
        :key="e.id"
      >
        <button
          type="button"
          class="etapes__item"
          :class="{ 'etapes__item--active': etape === e.id, 'etapes__item--done': faite(e.id) }"
          :aria-current="etape === e.id ? 'step' : undefined"
          @click="aller(e.id)"
        >
          <span
            class="etapes__marker"
            aria-hidden="true"
          >
            <CspIcon
              v-if="faite(e.id) && etape !== e.id"
              name="ri:check-line"
              :size="14"
            />
            <template v-else>{{ i + 1 }}</template>
          </span>
          <span class="etapes__label">{{ e.libelle }}</span>
          <span
            v-if="faite(e.id)"
            class="sr-only"
          > — complète</span>
        </button>
      </li>
    </ol>
    <p
      class="etapes__count"
      aria-hidden="true"
    >
      Étape {{ index + 1 }} sur {{ ETAPES.length }}
    </p>
  </nav>
</template>

<style scoped lang="scss">
.etapes {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding: 0 var(--csp-space-6);
  border-bottom: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.etapes__list {
  display: flex;
  gap: var(--csp-space-1);
  margin: 0;
  padding: 0;
  list-style: none;
}

.etapes__item {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-3) var(--csp-space-3);
  border: 0;
  border-bottom: 2px solid transparent;
  background: none;
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
  cursor: pointer;

  &:hover {
    color: var(--text-default-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
    outline-offset: -2px;
  }

  &--active {
    border-bottom-color: var(--border-active-blue-france);
    color: var(--text-action-high-blue-france);
    font-weight: var(--csp-font-weight-bold);
  }
}

.etapes__marker {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.375rem;
  height: 1.375rem;
  border: 1px solid var(--border-default-grey);
  border-radius: 50%;
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);

  .etapes__item--active & {
    border-color: var(--background-action-high-blue-france);
    background: var(--background-action-high-blue-france);
    color: var(--text-inverted-blue-france);
  }

  .etapes__item--done:not(.etapes__item--active) & {
    border-color: var(--border-default-grey);
    color: var(--text-default-grey);
  }
}

.etapes__count {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
