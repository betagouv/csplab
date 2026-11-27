<script setup lang="ts">
import type { GroupeOffre, PartieOffre } from './etapes'
import type { Offre } from './store'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { avancementEtape, champsObligatoires } from './aide'
import { ETAPES_OFFRE, GROUPES } from './etapes'
import TexteEtoile from './TexteEtoile.vue'

// Les étapes de l'offre, regroupées par partie, avec ce qui reste à remplir dans chacune. Sert au formulaire de création
// et à la page d'une offre en préparation (retour PO, 27/11/2026 : le même avancement que dans le formulaire).
// `seule` : n'afficher qu'une partie, sans « Partie N » (page de l'offre, Alice, 27/11/2026).
const props = defineProps<{ offre: Offre, active?: PartieOffre, groupe?: GroupeOffre, seule?: GroupeOffre }>()
const emit = defineEmits<{ choisir: [id: PartieOffre, n: number] }>()

const champs = computed(() => champsObligatoires(props.offre))
function etat(id: string) {
  const c = champs.value.filter(x => x.partie === id)
  return { total: c.length, reste: c.filter(x => !x.ok).length }
}
const groupes = computed(() => GROUPES.map((g, gi) => ({
  ...g,
  n: gi + 1,
  etapes: ETAPES_OFFRE.map((e, i) => ({ ...e, n: i + 1, ...etat(e.id) })).filter(e => e.groupe === g.id),
})).filter(g => !props.seule || g.id === props.seule))
</script>

<template>
  <nav
    class="etapes"
    aria-label="Étapes du formulaire"
  >
    <div
      v-for="g in groupes"
      :key="g.id"
      class="partie"
      :class="{ 'partie--active': g.id === groupe }"
    >
      <p class="partie__titre">
        <span
          v-if="!seule"
          class="partie__num"
        >Partie {{ g.n }}</span>
        {{ g.titre }}
      </p>
      <ol>
        <li
          v-for="e in g.etapes"
          :key="e.id"
        >
          <button
            type="button"
            class="etape"
            :class="{ 'etape--active': active === e.id }"
            :aria-current="active === e.id ? 'step' : undefined"
            @click="emit('choisir', e.id, e.n)"
          >
            <span class="etape__num">{{ e.n }}</span>
            <span class="etape__corps">
              <span class="etape__titre">{{ e.titre }}</span>
              <span
                class="etape__reste"
                :class="{ 'etape__reste--ok': e.total && !e.reste }"
              >
                <CspIcon
                  v-if="e.total && !e.reste"
                  name="ri:checkbox-circle-fill"
                  :size="14"
                />
                <TexteEtoile :texte="avancementEtape(e.total, e.reste)" />
              </span>
            </span>
          </button>
        </li>
      </ol>
    </div>
  </nav>
</template>

<style scoped lang="scss">
.etapes {
  position: sticky;
  top: var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);

  // Écran étroit (retour Alice) : les parties côte à côte, au-dessus du formulaire, sans rester collées en haut.
  @media (width <= 64rem) {
    position: static;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: var(--csp-space-6);
  }
}

.partie {
  ol {
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin: var(--csp-space-2) 0 0;
    padding: 0 0 0 var(--csp-space-3);
    border-left: 2px solid var(--border-default-grey);
    list-style: none;
  }

  &--active ol {
    border-left-color: var(--border-plain-blue-france);
  }
}

.partie__titre {
  margin: 0;
  font-weight: 700;
  font-size: var(--csp-font-size-sm);
  line-height: 1.3;
  color: var(--text-title-grey);
}

.partie__num {
  display: block;
  font-weight: 400;
  font-size: var(--csp-font-size-xs);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-mention-grey);
}

.etape {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  width: 100%;
  padding: var(--csp-space-2);
  border: 0;
  background: none;
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

.etape--active {
  background: var(--background-alt-blue-france);
  font-weight: 700;
  color: var(--text-action-high-blue-france);
}

.etape__num {
  display: inline-grid;
  flex-shrink: 0;
  place-items: center;
  width: 1.5rem;
  height: 1.5rem;
  border-radius: 50%;
  background: var(--background-contrast-grey);
  font-size: var(--csp-font-size-xs);
  font-weight: 700;
}

.etape--active .etape__num {
  background: var(--background-action-high-blue-france);
  color: var(--text-inverted-blue-france);
}

.etape__corps {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.etape__reste {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-weight: 400;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);

  &--ok {
    color: var(--text-default-success);
  }
}
</style>
