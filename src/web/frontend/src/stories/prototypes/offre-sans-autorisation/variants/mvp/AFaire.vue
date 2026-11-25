<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useNav } from './nav'
import { actionOffre } from './suivi'

export type CarteAFaire = 'prolonger' | 'publier'

// Encart « À faire » en tête de « Mes offres d'emploi » (Alice, 25/11/2026) : prolongations d'abord, puis offres
// prêtes à publier (en vert). Pas les offres en préparation à compléter : pas d'urgence. Une carte disparaît
// quand il n'y a rien à faire, l'encart aussi.
// Même modèle pour toutes les cartes (Alice) : titre de la carte, titre de l'offre (lien) s'il n'y en a qu'une,
// puis bouton. Une offre : l'action (Prolonger, Publier). Plusieurs : « Voir les offres » filtre le tableau.
const props = defineProps<{ offres: Record<CarteAFaire, Offre[]> }>()
const emit = defineEmits<{ choisir: [CarteAFaire] }>()
const { aller } = useNav()

const cartes = computed(() => ([
  { id: 'prolonger' as const, icone: 'ri:time-line', titre: (n: number) => (n > 1 ? `${n} offres arrivent à échéance` : 'Une offre arrive à échéance') },
  { id: 'publier' as const, icone: 'ri:send-plane-line', titre: (n: number) => (n > 1 ? `${n} offres prêtes à publier` : 'Une offre prête à publier') },
]).filter(c => props.offres[c.id].length > 0).map(c => ({ ...c, n: props.offres[c.id].length, seule: props.offres[c.id].length === 1 ? props.offres[c.id][0]! : null })))
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
        <div
          class="carte"
          :class="`carte--${c.id}`"
        >
          <p class="carte__tete">
            <CspIcon
              :name="c.icone"
              :size="20"
              class="carte__icone"
            />
            {{ c.titre(c.n) }}
          </p>
          <template v-if="c.seule">
            <button
              type="button"
              class="carte__offre"
              @click="aller({ nom: 'offre', id: c.seule.id })"
            >
              {{ c.seule.titre || 'Offre sans titre' }}
            </button>
            <CspButton
              :label="actionOffre(c.seule)!.label"
              size="sm"
              class="carte__cta"
              @click="aller(actionOffre(c.seule)!.ecran)"
            />
          </template>
          <CspButton
            v-else
            label="Voir les offres"
            size="sm"
            variant="secondary"
            class="carte__cta"
            @click="emit('choisir', c.id)"
          />
        </div>
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
  grid-template-columns: repeat(auto-fill, minmax(22rem, 28rem));
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.carte {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-2);
  height: 100%;
  padding: var(--csp-space-3) var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  border-left: 4px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
}

.carte--prolonger {
  border-left-color: var(--border-plain-warning);
}

.carte--publier {
  border-left-color: var(--border-plain-success);
}

.carte--publier .carte__icone {
  color: var(--text-default-success);
}

.carte__icone {
  flex-shrink: 0;
  color: var(--text-action-high-blue-france);
}

.carte--prolonger .carte__icone {
  color: var(--text-default-warning);
}

.carte__tete {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-weight: 700;
  color: var(--text-title-grey);
}

.carte__cta {
  margin-top: auto;
}

.carte__offre {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-default-grey);
  text-align: left;
  text-decoration: underline;
  text-underline-offset: 3px;
  cursor: pointer;

  &:hover {
    text-decoration-thickness: 2px;
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}
</style>
