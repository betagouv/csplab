<script setup lang="ts">
import type { LevierOption } from './options'
import { onBeforeUnmount, onMounted, ref } from 'vue'

const props = withDefaults(defineProps<{
  options: LevierOption[]
  // Story id without the export name, for instance prototypes-leviers-ombres
  storyPrefix: string
  // Viewport of the screen in each frame
  largeur: number
  hauteur: number
  colonnes?: number
}>(), {
  colonnes: 2,
})

// Each frame takes the color mode and the density of this story, that the preview decorator writes on the root element
function currentGlobals(): string {
  const root = document.documentElement
  return [
    `theme:${root.getAttribute('data-fr-theme') ?? 'light'}`,
    `density:${root.getAttribute('data-csp-density') ?? 'compact'}`,
    `etiquettes:${root.getAttribute('data-csp-etiquettes') ?? 'repli'}`,
  ].join(';')
}

const globals = currentGlobals()

function srcOf(option: LevierOption): string {
  return `${window.location.pathname}?id=${props.storyPrefix}--${option.id}&viewMode=story&globals=${globals}`
}

const grille = ref<HTMLElement | null>(null)
const echelle = ref(0)
let observer: ResizeObserver | null = null

onMounted(() => {
  const cellule = grille.value?.querySelector('.leviers-planche__cadre')
  if (!cellule) {
    return
  }
  observer = new ResizeObserver(([entry]) => {
    echelle.value = entry!.contentRect.width / props.largeur
  })
  observer.observe(cellule)
})

onBeforeUnmount(() => observer?.disconnect())
</script>

<template>
  <div
    ref="grille"
    class="leviers-planche"
    :style="{ '--leviers-planche-colonnes': colonnes }"
  >
    <figure
      v-for="option in options"
      :key="option.id"
      class="leviers-planche__option"
      :data-option="option.id"
    >
      <figcaption class="leviers-planche__nom">
        {{ option.nom }}
      </figcaption>
      <div
        class="leviers-planche__cadre"
        :style="{ aspectRatio: `${largeur} / ${hauteur}` }"
      >
        <iframe
          v-if="echelle"
          class="leviers-planche__ecran"
          :src="srcOf(option)"
          :style="{ width: `${largeur}px`, height: `${hauteur}px`, transform: `scale(${echelle})` }"
          :title="option.nom"
          tabindex="-1"
        />
      </div>
    </figure>
  </div>
</template>

<style scoped lang="scss">
.leviers-planche {
  display: grid;
  grid-template-columns: repeat(var(--leviers-planche-colonnes), minmax(0, 1fr));
  align-content: start;
  gap: var(--csp-space-6) var(--csp-space-8);
  min-height: 100vh;
  box-sizing: border-box;
  padding: var(--csp-space-6) var(--csp-space-8);
  background-color: var(--background-alt-grey);
  color: var(--text-default-grey);
}

.leviers-planche__option {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
}

.leviers-planche__nom {
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-medium);
  color: var(--text-mention-grey);
}

.leviers-planche__cadre {
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 0 1px var(--border-default-grey);
}

.leviers-planche__ecran {
  position: absolute;
  top: 0;
  left: 0;
  border: 0;
  transform-origin: top left;
  pointer-events: none;
}
</style>
