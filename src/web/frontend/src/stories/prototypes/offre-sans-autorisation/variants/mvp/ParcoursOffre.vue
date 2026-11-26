<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { avancementEtape, champsObligatoires } from './aide'
import { ETAPES_OFFRE, GROUPES } from './etapes'
import FormEtape from './FormEtape.vue'
import TexteEtoile from './TexteEtoile.vue'

// Formulaire de création, une page par étape (retour Alice du 25/11/2026). À gauche, les étapes regroupées dans les
// deux grandes parties : « Annonce visible du candidat » et « Paramétrage des candidatures ». Les étapes restent
// cliquables : on n'est jamais bloqué. Une étape est cochée quand ses champs obligatoires sont remplis.
const props = defineProps<{ offre: Offre }>()
const etape = defineModel<number>('etape', { default: 1 })

const courante = computed(() => ETAPES_OFFRE[etape.value - 1]!)
const derniere = computed(() => etape.value === ETAPES_OFFRE.length)
const champs = computed(() => champsObligatoires(props.offre))
function etat(id: string) {
  const c = champs.value.filter(x => x.partie === id)
  return { total: c.length, reste: c.filter(x => !x.ok).length }
}
const groupes = computed(() => GROUPES.map((g, gi) => ({
  ...g,
  n: gi + 1,
  etapes: ETAPES_OFFRE.map((e, i) => ({ ...e, n: i + 1, ...etat(e.id) })).filter(e => e.groupe === g.id),
})))
const suivante = computed(() => ETAPES_OFFRE[etape.value])
const changeDePartie = computed(() => suivante.value && suivante.value.groupe !== courante.value.groupe)

function aller(n: number) {
  etape.value = n
  document.querySelectorAll('.ats__main, .csp-page-container').forEach(e => e.scrollTo({ top: 0 }))
}
defineExpose({ aller })
</script>

<template>
  <div class="parcours">
    <nav
      class="etapes"
      aria-label="Étapes du formulaire"
    >
      <div
        v-for="g in groupes"
        :key="g.id"
        class="partie"
        :class="{ 'partie--active': g.id === courante.groupe }"
      >
        <p class="partie__titre">
          <span class="partie__num">Partie {{ g.n }}</span>
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
              :class="{ 'etape--active': etape === e.n }"
              :aria-current="etape === e.n ? 'step' : undefined"
              @click="aller(e.n)"
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

    <div class="principal">
      <div class="tete">
        <h2 class="tete__titre">
          {{ courante.titre }}
        </h2>
        <p class="tete__aide">
          Étape {{ etape }} sur {{ ETAPES_OFFRE.length }} · {{ courante.aide }}
        </p>
      </div>

      <div class="corps">
        <FormEtape
          :offre="offre"
          :partie="courante.id"
        />
      </div>

      <p
        v-if="changeDePartie"
        class="transition"
      >
        <CspIcon
          name="ri:information-line"
          :size="16"
        />
        L'annonce est terminée. Partie suivante : {{ GROUPES.find(g => g.id === suivante!.groupe)!.titre.toLowerCase() }}.
      </p>

      <div class="nav">
        <CspButton
          v-if="etape > 1"
          label="Précédent"
          variant="secondary"
          icon="ri:arrow-left-line"
          is-icon-left
          @click="aller(etape - 1)"
        />
        <span class="nav__espace" />
        <CspButton
          v-if="!derniere"
          :label="`Suivant : ${suivante!.titre}`"
          icon="ri:arrow-right-line"
          @click="aller(etape + 1)"
        />
        <slot
          v-else
          name="fin"
        />
      </div>
      <slot
        v-if="derniere"
        name="sous-fin"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.parcours {
  display: grid;
  grid-template-columns: 17rem minmax(0, 1fr);
  gap: var(--csp-space-8);
  align-items: start;
  max-width: 80rem;

  @media (width <= 64rem) {
    grid-template-columns: minmax(0, 1fr);
  }
}

.etapes {
  position: sticky;
  top: var(--csp-space-4);
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);

  // Écran étroit (retour Alice) : les deux parties côte à côte, au-dessus du formulaire, sans rester collées en haut.
  @media (width <= 64rem) {
    position: static;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
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

.principal {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  min-width: 0;
}

.tete__titre {
  margin: 0;
  font-size: 1.5rem;
  line-height: 1.3;
}

.tete__aide {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.corps {
  padding: var(--csp-space-6) var(--csp-space-8);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.transition {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.nav {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-3);
}

.nav__espace {
  flex: 1;
}
</style>
