<script setup lang="ts">
import type { TypeAction } from './suivi'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'

// Encart « À faire » en tête de « Mes offres d'emploi » (Alice, 25/11/2026) : une carte par type d'action,
// avec le nombre d'offres concernées. Une carte disparaît quand il n'y a rien à faire, l'encart aussi.
const props = defineProps<{ compte: Record<TypeAction, number>, actif: TypeAction | null }>()
const emit = defineEmits<{ choisir: [TypeAction] }>()

const pluriel = (n: number, un: string, plusieurs: string) => (n > 1 ? plusieurs : un)
const cartes = computed(() => ([
  { id: 'continuer' as const, icone: 'ri:edit-line', texte: (n: number) => pluriel(n, 'offre en préparation à continuer', 'offres en préparation à continuer') },
  { id: 'publier' as const, icone: 'ri:send-plane-line', texte: (n: number) => pluriel(n, 'offre prête à publier', 'offres prêtes à publier') },
  { id: 'prolonger' as const, icone: 'ri:time-line', texte: (n: number) => `${pluriel(n, 'offre se termine', 'offres se terminent')} dans moins de 7 jours` },
]).filter(c => props.compte[c.id] > 0))
</script>

<template>
  <section
    v-if="cartes.length"
    class="a-faire"
    aria-labelledby="a-faire-titre"
  >
    <h2
      id="a-faire-titre"
      class="a-faire__titre"
    >
      À faire
    </h2>
    <ul class="a-faire__cartes">
      <li
        v-for="c in cartes"
        :key="c.id"
      >
        <button
          type="button"
          class="carte"
          :class="[`carte--${c.id}`, { 'carte--active': actif === c.id }]"
          :aria-pressed="actif === c.id"
          @click="emit('choisir', c.id)"
        >
          <CspIcon
            :name="c.icone"
            :size="20"
            class="carte__icone"
          />
          <span class="carte__texte">
            <strong class="carte__nombre">{{ compte[c.id] }}</strong>
            {{ c.texte(compte[c.id]) }}
          </span>
          <CspIcon
            name="ri:arrow-right-line"
            :size="16"
            class="carte__fleche"
          />
        </button>
      </li>
    </ul>
  </section>
</template>

<style scoped lang="scss">
.a-faire__titre {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
  font-weight: 700;
  color: var(--text-title-grey);
}

.a-faire__cartes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.carte {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  width: 100%;
  height: 100%;
  padding: var(--csp-space-3) var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  border-left: 4px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
  text-align: left;
  cursor: pointer;

  &:hover {
    background: var(--background-default-grey-hover);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.carte--prolonger {
  border-left-color: var(--border-plain-warning);
}

.carte--active {
  border-color: var(--border-action-high-blue-france);
  background: var(--background-alt-blue-france);
}

.carte__icone {
  flex-shrink: 0;
  color: var(--text-action-high-blue-france);
}

.carte--prolonger .carte__icone {
  color: var(--text-default-warning);
}

.carte__texte {
  flex: 1;
}

.carte__nombre {
  margin-right: 0.25em;
  font-size: 1.25rem;
  color: var(--text-title-grey);
}

.carte__fleche {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}
</style>
