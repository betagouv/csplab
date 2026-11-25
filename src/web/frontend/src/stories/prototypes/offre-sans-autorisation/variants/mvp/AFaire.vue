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
// Une seule offre concernée : titre de la carte, titre de l'offre (lien), puis bouton d'action (Alice).
// Plusieurs : la carte filtre le tableau.
const props = defineProps<{ offres: Record<CarteAFaire, Offre[]>, actif: CarteAFaire | null }>()
const emit = defineEmits<{ choisir: [CarteAFaire] }>()
const { aller } = useNav()

const pluriel = (n: number, un: string, plusieurs: string) => (n > 1 ? plusieurs : un)
const cartes = computed(() => ([
  { id: 'prolonger' as const, icone: 'ri:time-line', texte: (n: number) => `${pluriel(n, 'offre se termine', 'offres se terminent')} dans moins de 7 jours`, titreSeule: 'Une offre arrive à échéance' },
  { id: 'publier' as const, icone: 'ri:send-plane-line', texte: (n: number) => pluriel(n, 'offre prête à publier', 'offres prêtes à publier'), titreSeule: 'Une offre prête à publier' },
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
          v-if="c.seule"
          class="carte carte--seule"
          :class="`carte--${c.id}`"
        >
          <p class="carte__tete">
            <CspIcon
              :name="c.icone"
              :size="20"
              class="carte__icone"
            />
            {{ c.titreSeule }}
          </p>
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
        </div>
        <button
          v-else
          type="button"
          class="carte"
          :class="`carte--${c.id}`"
          :aria-pressed="actif === c.id"
          @click="emit('choisir', c.id)"
        >
          <CspIcon
            :name="c.icone"
            :size="20"
            class="carte__icone"
          />
          <span class="carte__texte">
            <strong class="carte__nombre">{{ c.n }}</strong>
            {{ c.texte(c.n) }}
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
  grid-template-columns: repeat(auto-fill, minmax(22rem, 28rem));
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

.carte__texte {
  flex: 1;
  min-width: 0;
}

.carte--seule {
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-2);
  cursor: default;

  &:hover {
    background: var(--background-default-grey);
  }
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
