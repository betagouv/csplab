<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useNav } from './nav'
import { joursRestants } from './store'

export type CarteAFaire = 'prolonger' | 'publier'

// Encart « À faire » en tête de « Mes offres d'emploi » (Alice, 25/11/2026) : prolongations d'abord, puis offres
// prêtes à publier (en vert). Pas les offres en préparation à compléter : pas d'urgence. Une carte disparaît
// quand il n'y a rien à faire, l'encart aussi.
// Même modèle pour toutes les cartes : titre de la carte, titre de l'offre s'il n'y en a qu'une, et une flèche.
// Toute la carte est cliquable (Alice : on rouvre l'offre avant de publier ou prolonger). Une offre : sa page.
// Plusieurs : le tableau, filtré.
const props = defineProps<{ offres: Record<CarteAFaire, Offre[]> }>()
const emit = defineEmits<{ choisir: [CarteAFaire] }>()
const { aller } = useNav()

// Repère « J-4 » à côté du titre (Alice, 27/11/2026). Plusieurs offres : l'échéance la plus proche.
function echeance(offres: Offre[]) {
  const j = Math.max(0, Math.min(...offres.map(o => joursRestants(o.dateFin))))
  return { court: `J-${j}`, long: j === 0 ? 'aujourd\'hui' : j === 1 ? 'demain' : `dans ${j} jours` }
}
const cartes = computed(() => ([
  // Titre raccourci (Alice, 27/11/2026) : « 1 offre arrive en fin de publication » + repère J-x. Remplace « Une offre
  // sera dépubliée automatiquement dans N jours » (retour PO du 26/11/2026, à revalider avec elle).
  { id: 'prolonger' as const, icone: 'ri:time-line', titre: (n: number) => (n > 1 ? `${n} offres arrivent en fin de publication` : '1 offre arrive en fin de publication') },
  { id: 'publier' as const, icone: 'ri:send-plane-line', titre: (n: number) => (n > 1 ? `${n} offres prêtes à publier` : 'Une offre prête à publier') },
]).filter(c => props.offres[c.id].length > 0).map(c => ({
  ...c,
  n: props.offres[c.id].length,
  seule: props.offres[c.id].length === 1 ? props.offres[c.id][0]! : null,
  echeance: c.id === 'prolonger' ? echeance(props.offres[c.id]) : null,
})))
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
          :class="`carte--${c.id}`"
          @click="c.seule ? aller({ nom: 'offre', id: c.seule.id }) : emit('choisir', c.id)"
        >
          <span class="carte__corps">
            <span class="carte__tete">
              <CspIcon
                :name="c.icone"
                :size="20"
                class="carte__icone"
              />
              {{ c.titre(c.n) }}
              <span
                v-if="c.echeance"
                class="carte__jours"
              >
                <span aria-hidden="true">{{ c.echeance.court }}</span>
                <span class="sr-only">, fin {{ c.n > 1 ? 'de la première ' : '' }}{{ c.echeance.long }}</span>
              </span>
            </span>
            <span
              v-if="c.seule"
              class="carte__offre"
            >{{ c.seule.titre || 'Offre sans titre' }}</span>
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

.carte__corps {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: var(--csp-space-1);
  min-width: 0;
}

.carte__fleche {
  flex-shrink: 0;
  color: var(--text-mention-grey);
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

.carte__jours {
  flex-shrink: 0;
  padding: 0 var(--csp-space-2);
  border-radius: 0.25rem;
  background: var(--background-contrast-warning);
  font-size: var(--csp-font-size-xs);
  font-weight: 700;
  line-height: 1.5rem;
  color: var(--text-default-warning);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}

.carte__offre {
  color: var(--text-default-grey);
}
</style>
