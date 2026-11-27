<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { ETAPES_OFFRE, GROUPES } from './etapes'
import FormEtape from './FormEtape.vue'
import NavEtapes from './NavEtapes.vue'

// Formulaire de création, une page par étape (retour Alice du 25/11/2026). À gauche, les étapes regroupées dans les
// deux grandes parties : « Annonce visible du candidat » et « Formulaire de candidature » (et « Diffusion »). Les étapes restent
// cliquables : on n'est jamais bloqué. Une étape est cochée quand ses champs obligatoires sont remplis.
defineProps<{ offre: Offre }>()
const etape = defineModel<number>('etape', { default: 1 })

const courante = computed(() => ETAPES_OFFRE[etape.value - 1]!)
const derniere = computed(() => etape.value === ETAPES_OFFRE.length)
const suivante = computed(() => ETAPES_OFFRE[etape.value])
const changeDePartie = computed(() => suivante.value && suivante.value.groupe !== courante.value.groupe)

function aller(n: number) {
  etape.value = n
  document.querySelectorAll('.ats__main, .csp-page-container').forEach(e => e.scrollTo({ top: 0 }))
}
function choisir(_id: string, n: number) {
  aller(n)
}
defineExpose({ aller })
</script>

<template>
  <div class="parcours">
    <NavEtapes
      class="parcours__nav"
      :offre="offre"
      :active="courante.id"
      :groupe="courante.groupe"
      @choisir="choisir"
    />

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
        Partie {{ GROUPES.findIndex(g => g.id === courante.groupe) + 1 }} terminée. Partie suivante : {{ GROUPES.find(g => g.id === suivante!.groupe)!.titre.toLowerCase() }}.
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
