<script setup lang="ts">
import type { Demo } from './boucle'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

export interface Recadrage {
  x: number
  y: number
  width: number
  height: number
}

const props = withDefaults(defineProps<{
  piste: string
  demo: Demo
  ralenti?: number
  // Part of the screen that the frame shows, in screen pixels; the whole screen by default
  recadrage?: Recadrage
  // Story of the screen, and the interface theme it renders, when the screen is not the scene of a track
  ecran?: string
  interfaceTheme?: string
}>(), {
  ralenti: 1,
  recadrage: undefined,
  ecran: undefined,
  interfaceTheme: 'kit',
})

const ECRAN = { width: 1600, height: 900 }
const zone = computed(() => props.recadrage ?? { x: 0, y: 0, ...ECRAN })

// The screen takes the colour mode and the density of this story, that the preview decorator writes on the root element
const root = document.documentElement
const globals = [
  `interfaceTheme:${props.interfaceTheme}`,
  `theme:${root.getAttribute('data-fr-theme') ?? 'light'}`,
  `density:${root.getAttribute('data-csp-density') ?? 'compact'}`,
  `etiquettes:${root.getAttribute('data-csp-etiquettes') ?? 'repli'}`,
].join(';')

const src = computed(() => `${window.location.pathname}?id=${props.ecran ?? `prototypes-leviers-mouvement--scene-${props.piste}`}&viewMode=story`
  + `&args=demo:${props.demo};ralenti:${props.ralenti}&globals=${globals}`)

const cadre = ref<HTMLElement | null>(null)
const echelle = ref(0)
let observer: ResizeObserver | null = null

onMounted(() => {
  observer = new ResizeObserver(([entry]) => {
    echelle.value = entry!.contentRect.width / zone.value.width
  })
  observer.observe(cadre.value!)
})
onBeforeUnmount(() => observer?.disconnect())
</script>

<template>
  <div
    ref="cadre"
    class="mouvement-cadre"
    :style="{ aspectRatio: `${zone.width} / ${zone.height}` }"
  >
    <iframe
      v-if="echelle"
      class="mouvement-cadre__ecran"
      :src="src"
      :style="{
        width: `${ECRAN.width}px`,
        height: `${ECRAN.height}px`,
        transform: `scale(${echelle}) translate(${-zone.x}px, ${-zone.y}px)`,
      }"
      title="Démonstration"
      tabindex="-1"
    />
  </div>
</template>

<style scoped lang="scss">
/* clip: a focus moved inside the screen cannot scroll the frame */
.mouvement-cadre {
  position: relative;
  overflow: clip;

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    border: 1px solid var(--border-default-grey);
    pointer-events: none;
  }
}

.mouvement-cadre__ecran {
  position: absolute;
  top: 0;
  left: 0;
  border: 0;
  transform-origin: top left;
  pointer-events: none;
}
</style>
