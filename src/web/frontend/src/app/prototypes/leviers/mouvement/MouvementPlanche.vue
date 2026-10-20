<script setup lang="ts">
import type { Geste } from './boucle'
import type { Recadrage } from './MouvementCadre.vue'
import type { PisteMouvement } from './pistes'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { boucle, MESSAGE_ORIGINE, MESSAGE_PRET } from './boucle'
import { lignesDuGeste, lignesDuRole } from './frise'
import MouvementCadre from './MouvementCadre.vue'
import MouvementFrise from './MouvementFrise.vue'
import { PISTES, reduite } from './pistes'

const props = withDefaults(defineProps<{
  // A track plays the whole demo with its rule; a gesture compares the tracks
  piste?: string
  geste?: Geste
  ralenti?: number
  // Rule and screen of a theme, in place of a track: the story that plays the demo and the theme it renders
  regle?: PisteMouvement
  ecran?: string
  interfaceTheme?: string
}>(), {
  piste: undefined,
  geste: undefined,
  ralenti: 1,
  regle: undefined,
  ecran: undefined,
  interfaceTheme: undefined,
})

// Part of the screen that each gesture needs, wider than high so that the four screens stay large; the menu of the job
// offer under its button
const RECADRAGES: Record<Geste, Recadrage> = {
  menu: { x: 1200, y: 36, width: 384, height: 136 },
  panneau: { x: 256, y: 0, width: 1344, height: 560 },
  dialogue: { x: 450, y: 250, width: 700, height: 400 },
  depot: { x: 925, y: 330, width: 636, height: 440 },
}

const mouvementReduit = window.matchMedia('(prefers-reduced-motion: reduce)').matches
const pistes = mouvementReduit ? PISTES.map(reduite) : PISTES

const demo = computed(() => props.geste ?? 'parcours')
const loop = computed(() => boucle(demo.value, props.ralenti))

const lignes = computed(() => {
  if (props.geste) {
    return lignesDuGeste(pistes, props.geste)
  }
  return lignesDuRole(props.regle ?? pistes.find(({ id }) => id === props.piste)!)
})

// The screens start their loop together, a moment after the last of them is ready; a screen ready later takes the same
// origin and waits for the next start of the loop
const origine = ref<number | null>(null)
const ecransPrets = new Set<Window>()

function recevoir(event: MessageEvent): void {
  if (event.origin !== window.location.origin || event.data?.type !== MESSAGE_PRET || !event.source) {
    return
  }
  ecransPrets.add(event.source as Window)
  if (origine.value === null && ecransPrets.size < (props.geste ? lignes.value.length : 1)) {
    return
  }
  origine.value ??= Date.now() + 100
  for (const ecran of ecransPrets) {
    ecran.postMessage({ type: MESSAGE_ORIGINE, origine: origine.value }, window.location.origin)
  }
}

onMounted(() => window.addEventListener('message', recevoir))
onBeforeUnmount(() => window.removeEventListener('message', recevoir))
</script>

<template>
  <div
    class="mouvement-planche"
    :class="{ 'mouvement-planche--comparaison': geste }"
  >
    <template v-if="geste">
      <figure
        v-for="ligne in lignes"
        :key="ligne.id"
        class="mouvement-planche__ecran"
      >
        <figcaption class="mouvement-planche__nom">
          {{ ligne.libelle }}
        </figcaption>
        <MouvementCadre
          class="mouvement-planche__cadre"
          :style="{ '--mouvement-planche-ratio': RECADRAGES[geste].width / RECADRAGES[geste].height }"
          :piste="ligne.id"
          :demo="geste"
          :ralenti="ralenti"
          :recadrage="RECADRAGES[geste]"
        />
      </figure>
    </template>

    <div
      v-else
      class="mouvement-planche__ecran"
    >
      <MouvementCadre
        class="mouvement-planche__cadre"
        :piste="piste ?? regle!.id"
        :ecran="ecran"
        :interface-theme="interfaceTheme"
        demo="parcours"
        :ralenti="ralenti"
      />
    </div>

    <MouvementFrise
      class="mouvement-planche__frise"
      :lignes="lignes"
      :loop="loop"
      :origine="origine"
      :ralenti="ralenti"
    />

    <p
      v-if="ralenti > 1 || mouvementReduit"
      class="mouvement-planche__note"
    >
      <template v-if="ralenti > 1">
        Ralenti {{ ralenti }} fois ; la frise donne les durées réelles.
      </template>
      <template v-if="mouvementReduit">
        Le système demande un mouvement réduit : les écrans jouent la version sans déplacement, en fondu.
      </template>
    </p>
  </div>
</template>

<style scoped lang="scss">
/* The screens above the timeline: the whole application for the rule of a track, four parts of it for a comparison */
.mouvement-planche {
  --mouvement-planche-ratio: 16 / 9;

  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
  gap: var(--csp-space-6);
  height: 100vh;
  padding: var(--csp-space-6);
  overflow: hidden;
  background-color: var(--background-default-grey);
}

.mouvement-planche--comparaison {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-template-rows: repeat(2, minmax(0, 1fr)) auto;
  gap: var(--csp-space-4) var(--csp-space-8);
}

.mouvement-planche__ecran {
  container-type: size;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-1);
  min-height: 0;
  margin: 0;
}

/* As large as the cell allows, with the proportions of its part of the screen */
.mouvement-planche__cadre {
  width: min(100cqw, (100cqh - 1.75rem) * var(--mouvement-planche-ratio));
}

.mouvement-planche:not(.mouvement-planche--comparaison) {
  .mouvement-planche__ecran {
    align-items: center;
  }

  .mouvement-planche__cadre {
    width: min(100cqw, 100cqh * var(--mouvement-planche-ratio));
  }
}

.mouvement-planche__nom {
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}

.mouvement-planche__frise {
  grid-column: 1 / -1;
}

.mouvement-planche__note {
  grid-column: 1 / -1;
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
