<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { markKanbanCardMoved } from '@/composables/dnd/useKanbanDnd'
import { demoKanban } from '@/features/candidatures/__mocks__/demo'
import CandidatureKanbanCard from '@/features/candidatures/components/CandidatureKanbanCard.vue'

export type DeckInterfacePlanche = 'ecran' | 'etats'

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

const BOARD_ID = 'deck'

const ETAPE = demoKanban().etapes[0]!

const ETATS = [
  { id: 'repos', legende: 'Au repos', candidature: ETAPE.candidatures[0]! },
  { id: 'survol', legende: 'Au survol', candidature: ETAPE.candidatures[1]! },
  { id: 'depot', legende: 'Après un dépôt', candidature: ETAPE.candidatures[2]! },
] as const

if (props.planche === 'etats') {
  markKanbanCardMoved(BOARD_ID, ETATS[2].candidature.uuid)
}

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
    />

    <div
      v-else-if="planche === 'etats'"
      class="deck-interface__etats"
    >
      <template
        v-for="(etat, index) in ETATS"
        :key="etat.id"
      >
        <span class="deck-interface__legende">{{ etat.legende }}</span>
        <div :class="`deck-interface__etat--${etat.id}`">
          <CandidatureKanbanCard
            :candidature="etat.candidature"
            :board-id="BOARD_ID"
            :column-id="ETAPE.uuid"
            :card-index="index"
          />
        </div>
      </template>
    </div>
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

.deck-interface--etats {
  background-color: var(--csp-region-background);
}

.deck-interface__ecran {
  position: absolute;
  top: 0;
  left: 0;
  border: 0;
  transform-origin: top left;
  pointer-events: none;
}

.deck-interface__legende {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.deck-interface__etats {
  display: grid;
  grid-template-columns: auto var(--csp-kanban-column-width);
  align-items: center;
  gap: var(--csp-space-6) var(--csp-space-6);
}

/* Variables of the hover state, set on an ancestor of a card that the pointer does not reach */
.deck-interface__etat--survol {
  --csp-raised-shadow: var(--csp-raised-shadow-hover, 0 1px 2px rgb(0 0 0 / 6%));
  --csp-raised-background: var(--csp-raised-background-hover, var(--background-alt-grey));
  --csp-raised-border-color: var(--csp-raised-border-color-hover, var(--border-default-grey));
}

/* The highlight of a dropped card stays on its first frame */
.deck-interface__etat--depot :deep(.candidature-kanban-card--moved) {
  animation-play-state: paused;
}
</style>
