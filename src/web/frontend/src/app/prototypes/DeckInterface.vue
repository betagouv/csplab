<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

export type DeckInterfacePlanche = 'ecran'

export interface DeckInterfaceCadre {
  x: number
  y: number
  width: number
  height: number
}

const props = withDefaults(defineProps<{
  planche: DeckInterfacePlanche
  // Id of the screen story that the « ecran » plate frames
  ecran?: string
  // Width of the framed screen; without a frame, its height follows the proportions of the plate
  largeur?: number
  // Height of the framed screen, with a frame
  hauteur?: number
  // Part of the screen that the plate shows, in screen pixels
  cadre?: DeckInterfaceCadre
}>(), {
  ecran: 'prototypes-deck-interface--ecran-kanban',
  largeur: 1280,
  hauteur: 900,
  cadre: undefined,
})

// The framed screen takes the globals of this story, which the preview decorator writes on the root element
function currentGlobals(): string {
  const root = document.documentElement
  return [
    `interfaceTheme:${root.getAttribute('data-csp-theme') ?? 'kit'}`,
    `theme:${root.getAttribute('data-fr-theme') ?? 'light'}`,
    `density:${root.getAttribute('data-csp-density') ?? 'compact'}`,
    `etiquettes:${root.getAttribute('data-csp-etiquettes') ?? 'repli'}`,
  ].join(';')
}

const ecranSrc = `${window.location.pathname}?id=${encodeURIComponent(props.ecran)}&viewMode=story&globals=${currentGlobals()}`

const racine = ref<HTMLElement | null>(null)
const taille = ref({ width: 0, height: 0 })
let observer: ResizeObserver | null = null

onMounted(() => {
  if (props.planche !== 'ecran' || !racine.value) {
    return
  }
  observer = new ResizeObserver(([entry]) => {
    taille.value = { width: entry!.contentRect.width, height: entry!.contentRect.height }
  })
  observer.observe(racine.value)
})

onBeforeUnmount(() => observer?.disconnect())

// A part of a screen leaves out the scrollbars, which the browser draws over the edges of the window and of the lists
function sansBarres(event: Event): void {
  const ecran = (event.target as HTMLIFrameElement).contentDocument
  if (!props.cadre || !ecran) {
    return
  }
  const style = ecran.createElement('style')
  style.textContent = '* { scrollbar-width: none !important; }'
  ecran.head.append(style)
}

const ecranStyle = computed(() => {
  const { width, height } = taille.value
  if (!width || !height) {
    return null
  }
  const viewport = props.cadre
    ? { width: props.largeur, height: props.hauteur }
    : { width: props.largeur, height: Math.round(props.largeur * height / width) }
  const cadre = props.cadre ?? { x: 0, y: 0, ...viewport }
  const scale = Math.min(width / cadre.width, height / cadre.height)
  const x = width / 2 - (cadre.x + cadre.width / 2) * scale
  const y = height / 2 - (cadre.y + cadre.height / 2) * scale
  return {
    width: `${viewport.width}px`,
    height: `${viewport.height}px`,
    transform: `translate(${x}px, ${y}px) scale(${scale})`,
  }
})
</script>

<template>
  <div
    ref="racine"
    class="deck-interface"
    :class="`deck-interface--${planche}`"
  >
    <iframe
      v-if="planche === 'ecran' && ecranStyle"
      class="deck-interface__ecran"
      :src="ecranSrc"
      :style="ecranStyle"
      title="Écran de l'application"
      tabindex="-1"
      @load="sansBarres"
    />
  </div>
</template>

<style scoped lang="scss">
.deck-interface {
  position: relative;
  display: grid;
  place-items: center;
  height: 100vh;
  overflow: hidden;
  background-color: var(--csp-canvas-background);
  color: var(--text-default-grey);
}

.deck-interface__ecran {
  position: absolute;
  top: 0;
  left: 0;
  border: 0;
  transform-origin: top left;
  pointer-events: none;
}
</style>
