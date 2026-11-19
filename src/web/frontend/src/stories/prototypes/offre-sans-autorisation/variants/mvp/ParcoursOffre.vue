<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { champsObligatoires } from './aide'
import EquipeRecrutementOffre from './EquipeRecrutementOffre.vue'
import { ETAPES_OFFRE } from './etapes'
import EtapesRecrutementOffre from './EtapesRecrutementOffre.vue'
import FormAnnonce from './FormAnnonce.vue'
import FormCandidature from './FormCandidature.vue'
import FormInterne from './FormInterne.vue'

// Formulaire de l'offre en étapes successives (retour PO, F1), le même à la création et sur la page de l'offre.
// Les étapes restent cliquables : on n'est jamais bloqué, rien n'est contrôlé avant la publication.
// Une étape est cochée quand tous ses champs obligatoires sont remplis.
const props = defineProps<{ offre: Offre, lectureSeule?: boolean, verrouilleCandidature?: boolean }>()
const etape = defineModel<number>('etape', { default: 1 })

const courante = computed(() => ETAPES_OFFRE[etape.value - 1]!)
const derniere = computed(() => etape.value === ETAPES_OFFRE.length)
const restants = computed(() => {
  const m = new Map<string, number>()
  for (const c of champsObligatoires(props.offre).filter(x => !x.ok)) {
    m.set(c.partie, (m.get(c.partie) ?? 0) + 1)
  }
  return m
})

function aller(n: number) {
  etape.value = n
  document.querySelector('.csp-page-container')?.scrollTo({ top: 0 })
}
defineExpose({ aller })
</script>

<template>
  <div class="parcours">
    <nav
      class="etapes"
      aria-label="Étapes du formulaire"
    >
      <ol>
        <li
          v-for="(e, i) in ETAPES_OFFRE"
          :key="e.id"
        >
          <button
            type="button"
            class="etape"
            :class="{ 'etape--active': etape === i + 1 }"
            :aria-current="etape === i + 1 ? 'step' : undefined"
            @click="aller(i + 1)"
          >
            <span class="etape__num">{{ i + 1 }}</span>
            <span class="etape__titre">{{ e.titre }}</span>
            <CspIcon
              v-if="!restants.get(e.id)"
              name="ri:checkbox-circle-fill"
              :size="16"
              class="etape__ok"
              aria-label="complète"
            />
          </button>
        </li>
      </ol>
    </nav>

    <div class="tete">
      <p class="tete__etat">
        Étape {{ etape }} sur {{ ETAPES_OFFRE.length }}
      </p>
      <h2 class="tete__titre">
        {{ courante.titre }}{{ courante.facultatif ? ' (facultatif)' : '' }}
      </h2>
      <p class="tete__aide">
        {{ courante.aide }}
      </p>
    </div>

    <div class="corps">
      <FormInterne
        v-if="courante.id === 'interne'"
        :offre="offre"
        :lecture-seule="lectureSeule"
      />
      <FormCandidature
        v-else-if="courante.id === 'candidature'"
        :offre="offre"
        :verrouille="verrouilleCandidature"
      />
      <EtapesRecrutementOffre
        v-else-if="courante.id === 'processus'"
        :offre="offre"
      />
      <EquipeRecrutementOffre
        v-else-if="courante.id === 'equipe'"
        :offre="offre"
      />
      <FormAnnonce
        v-else
        :offre="offre"
        :partie="courante.id"
        :lecture-seule="lectureSeule"
      />
    </div>

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
        v-if="!derniere && courante.facultatif"
        label="Passer cette étape"
        variant="tertiary-no-outline"
        @click="aller(etape + 1)"
      />
      <CspButton
        v-if="!derniere"
        :label="`Suivant : ${ETAPES_OFFRE[etape]!.titre}`"
        icon="ri:arrow-right-line"
        @click="aller(etape + 1)"
      />
      <slot
        v-else
        name="fin"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.parcours {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  min-width: 0;
}

.etapes ol {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.etape {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-1) var(--csp-space-3) var(--csp-space-1) var(--csp-space-1);
  border: 1px solid var(--border-default-grey);
  border-radius: 999px;
  background: var(--background-default-grey);
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
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
  border-color: var(--border-action-high-blue-france);
  box-shadow: inset 0 0 0 1px var(--border-action-high-blue-france);
  font-weight: 700;
  color: var(--text-action-high-blue-france);
}

.etape__num {
  display: inline-grid;
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

.etape__ok {
  color: var(--text-default-success);
}

.tete__etat {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.tete__titre {
  margin: 0;
  font-size: 1.375rem;
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
