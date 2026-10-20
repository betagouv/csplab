<script setup lang="ts">
import type { LevierOption } from '../options'
import type { OmbresEtat } from './OmbresCarte.vue'
import { demoKanban } from '@/features/candidatures/__mocks__/demo'
import { valeursOf } from '../options'
import OmbresCarte from './OmbresCarte.vue'

defineProps<{
  options: LevierOption[]
}>()

const CANDIDATURE = demoKanban().etapes[0]!.candidatures[0]!

const ETATS: { etat: OmbresEtat, legende: string }[] = [
  { etat: 'repos', legende: 'Au repos' },
  { etat: 'survol', legende: 'Au survol' },
  { etat: 'glisser', legende: 'Pendant le glisser' },
]

// The story writes its color mode on the root element before it renders
const theme = document.documentElement.getAttribute('data-fr-theme') ?? 'light'
</script>

<template>
  <div class="ombres-comparaison">
    <span />
    <span
      v-for="{ etat, legende } in ETATS"
      :key="etat"
      class="ombres-comparaison__legende"
    >{{ legende }}</span>
    <span class="ombres-comparaison__legende">Coin au repos, agrandi quatre fois</span>
    <template
      v-for="option in options"
      :key="option.id"
    >
      <span class="ombres-comparaison__option">{{ option.nom }}</span>
      <div
        class="ombres-comparaison__rangee"
        :style="valeursOf(option, theme)"
      >
        <OmbresCarte
          v-for="({ etat }, index) in ETATS"
          :key="etat"
          :etat="etat"
          :candidature="CANDIDATURE"
          :card-index="index"
        />
        <div
          class="ombres-comparaison__loupe"
          aria-hidden="true"
        >
          <OmbresCarte
            class="ombres-comparaison__carte-agrandie"
            etat="repos"
            :candidature="CANDIDATURE"
            :card-index="ETATS.length"
          />
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
.ombres-comparaison {
  display: grid;
  grid-template-columns: auto repeat(3, 14rem) minmax(6rem, 14rem);
  place-content: center;
  align-items: center;
  gap: var(--csp-space-6) var(--csp-space-4);
  box-sizing: border-box;
  height: 100vh;
  padding: var(--csp-space-6) var(--csp-space-4);
  background-color: var(--csp-region-background);
  color: var(--text-default-grey);
}

/* The cards of a row share its grid columns, and the row carries the variables of its option */
.ombres-comparaison__rangee {
  display: grid;
  grid-template-columns: subgrid;
  grid-column: span 4;
  align-items: center;
}

/* The bottom right corner of the card at rest, four times larger, on the background of the column with room for the
   shadow: the card keeps its width, and its content stays hidden */
.ombres-comparaison__loupe {
  position: relative;
  height: 7rem;
  overflow: hidden;
  box-shadow: 0 0 0 1px var(--border-default-grey);
}

.ombres-comparaison__carte-agrandie {
  position: absolute;
  right: var(--csp-space-8);
  bottom: var(--csp-space-8);
  width: 14rem;
  transform: scale(4);
  transform-origin: bottom right;
}

.ombres-comparaison__carte-agrandie :deep(.candidature-kanban-card > *) {
  visibility: hidden;
}

.ombres-comparaison__legende {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.ombres-comparaison__option {
  font-weight: var(--csp-font-weight-medium);
}
</style>
