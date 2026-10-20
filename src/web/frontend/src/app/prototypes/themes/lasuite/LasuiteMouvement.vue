<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { boucle, MESSAGE_ORIGINE, MESSAGE_PRET } from '../../leviers/mouvement/boucle'
import { lignesDuRole } from '../../leviers/mouvement/frise'
import MouvementFrise from '../../leviers/mouvement/MouvementFrise.vue'
import { mouvementDuTheme } from './mouvementDuTheme'

const props = defineProps<{
  // Id of the story that plays the demo in a loop in the theme
  scene: string
}>()

const ECRAN = { width: 1600, height: 900 }
const loop = boucle('parcours')
const lignes = lignesDuRole(mouvementDuTheme('theme', 'Thème'))

// The screen takes the theme, the colour mode and the density of this story
const root = document.documentElement
const globals = [
  `interfaceTheme:${root.getAttribute('data-csp-theme') ?? 'kit'}`,
  `theme:${root.getAttribute('data-fr-theme') ?? 'light'}`,
  `density:${root.getAttribute('data-csp-density') ?? 'compact'}`,
].join(';')
const src = `${window.location.pathname}?id=${encodeURIComponent(props.scene)}&viewMode=story&globals=${globals}`

const cadre = ref<HTMLElement | null>(null)
const echelle = ref(0)
let observer: ResizeObserver | null = null

// The screen tells when its application is ready, and the plate gives it the origin of the loop the timeline follows
const origine = ref<number | null>(null)

function recevoir(event: MessageEvent): void {
  if (event.origin !== window.location.origin || event.data?.type !== MESSAGE_PRET || !event.source) {
    return
  }
  origine.value ??= Date.now() + 100
  ;(event.source as Window).postMessage({ type: MESSAGE_ORIGINE, origine: origine.value }, window.location.origin)
}

onMounted(() => {
  window.addEventListener('message', recevoir)
  observer = new ResizeObserver(([entry]) => {
    echelle.value = entry!.contentRect.width / ECRAN.width
  })
  observer.observe(cadre.value!)
})

onBeforeUnmount(() => {
  window.removeEventListener('message', recevoir)
  observer?.disconnect()
})
</script>

<template>
  <div class="lasuite-mouvement">
    <div class="lasuite-mouvement__ecran">
      <div
        ref="cadre"
        class="lasuite-mouvement__cadre"
      >
        <iframe
          v-if="echelle"
          class="mouvement-cadre__ecran lasuite-mouvement__iframe"
          :src="src"
          :style="{ width: `${ECRAN.width}px`, height: `${ECRAN.height}px`, transform: `scale(${echelle})` }"
          title="Démonstration"
          tabindex="-1"
        />
      </div>
    </div>
    <MouvementFrise
      :lignes="lignes"
      :loop="loop"
      :origine="origine"
    />
  </div>
</template>

<style scoped lang="scss">
/* The screen that plays the demo above the timeline of the theme */
.lasuite-mouvement {
  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
  gap: var(--csp-space-5);
  box-sizing: border-box;
  height: 100vh;
  padding: var(--csp-space-6);
  overflow: hidden;
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
}

.lasuite-mouvement__ecran {
  container-type: size;
  display: flex;
  justify-content: center;
  min-height: 0;
}

/* As large as the cell allows, with the proportions of the screen; clip: a focus moved inside the screen cannot scroll
   the frame */
.lasuite-mouvement__cadre {
  position: relative;
  width: min(100cqw, 100cqh * 16 / 9);
  aspect-ratio: 16 / 9;
  overflow: clip;
  box-shadow: 0 0 0 1px var(--border-default-grey);
}

.lasuite-mouvement__iframe {
  position: absolute;
  top: 0;
  left: 0;
  border: 0;
  transform-origin: top left;
  pointer-events: none;
}
</style>
