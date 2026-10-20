<script setup lang="ts">
import type { Boucle, Sens } from './boucle'
import type { Barre, Ligne } from './frise'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { instant, momentA } from './boucle'
import { progression } from './courbe'

const props = withDefaults(defineProps<{
  lignes: Ligne[]
  loop: Boucle
  // Time of the clock when the loop of the screens starts, once they are ready
  origine: number | null
  ralenti?: number
}>(), {
  ralenti: 1,
})

const SENS: { id: Sens, titre: string }[] = [
  { id: 'entree', titre: 'Entrée' },
  { id: 'sortie', titre: 'Sortie' },
]

// A column without any bar, the exit of a dropped card, is left out
const colonnes = computed(() => SENS.filter(({ id }) => props.lignes.some(ligne => ligne[id].length > 0)))

// One scale for every plate, which covers the longest animation of the tracks; a longer animation stretches it by steps
// of 200 ms
const PAS = 200
const ETENDUE = computed(() => Math.max(1000, ...props.lignes.flatMap(ligne => [...ligne.entree, ...ligne.sortie])
  .map(({ duree }) => Math.ceil(duree / PAS) * PAS)))
const GRADUATIONS = computed(() => Array.from({ length: ETENDUE.value / PAS + 1 }, (_, index) => index * PAS))

function graduation(ms: number): string {
  return ms < 1000 ? `${ms} ms` : `${(ms / 1000).toLocaleString('fr-FR')} s`
}

const moment = ref<ReturnType<typeof momentA>>(null)
let frame = 0

function tick(): void {
  const { origine } = props
  moment.value = origine !== null && Date.now() >= origine ? momentA(props.loop, instant(props.loop, origine), props.ralenti) : null
  frame = requestAnimationFrame(tick)
}

onMounted(() => {
  frame = requestAnimationFrame(tick)
})
onBeforeUnmount(() => cancelAnimationFrame(frame))

// Time spent in the animation of this cell, while the demo plays it
function ecoule(ligne: Ligne, sens: Sens): number | null {
  const current = moment.value
  if (!current || current.sens !== sens || !ligne.gestes.includes(current.geste) || current.ecoule > ETENDUE.value) {
    return null
  }
  return current.ecoule
}

function pourcent(ms: number): string {
  return `${(ms / ETENDUE.value) * 100}%`
}

function trace(barre: Barre): string {
  return Array.from({ length: 41 }, (_, index) => {
    const t = index / 40
    return `${t * barre.duree},${100 - progression(barre.courbe, t) * 100}`
  }).join(' ')
}

// The caption follows a short bar, and goes above a long one, out of the way of its curve
function legendeDessus(barre: Barre): boolean {
  return barre.duree > 0.55 * ETENDUE.value
}

// Height of the curve at this time: the dot rides the curve while the playhead crosses the bar
function hauteur(barre: Barre, ms: number): string {
  return `${(1 - progression(barre.courbe, Math.min(1, ms / barre.duree))) * 100}%`
}
</script>

<template>
  <div
    class="mouvement-frise"
    :style="{ gridTemplateColumns: `11rem repeat(${colonnes.length}, minmax(0, 1fr))` }"
  >
    <div class="mouvement-frise__coin" />
    <div
      v-for="{ id, titre } in colonnes"
      :key="id"
      class="mouvement-frise__entete"
    >
      <span class="mouvement-frise__titre">{{ titre }}</span>
      <div class="mouvement-frise__graduations">
        <span
          v-for="ms in GRADUATIONS"
          :key="ms"
          class="mouvement-frise__graduation"
          :style="{ left: pourcent(ms) }"
        >{{ graduation(ms) }}</span>
      </div>
    </div>

    <template
      v-for="ligne in lignes"
      :key="ligne.id"
    >
      <div class="mouvement-frise__libelle">
        {{ ligne.libelle }}
      </div>
      <div
        v-for="{ id } in colonnes"
        :key="id"
        class="mouvement-frise__cellule"
      >
        <div
          v-for="(barre, index) in ligne[id]"
          :key="index"
        >
          <span
            v-if="legendeDessus(barre)"
            class="mouvement-frise__legende mouvement-frise__legende--dessus"
          >{{ barre.legende }}</span>
          <div class="mouvement-frise__barre">
            <svg
              v-if="barre.duree"
              class="mouvement-frise__courbe"
              :style="{ width: pourcent(barre.duree) }"
              :viewBox="`0 0 ${barre.duree} 100`"
              preserveAspectRatio="none"
            >
              <rect
                :width="barre.duree"
                height="100"
              />
              <polyline :points="trace(barre)" />
            </svg>
            <span
              v-else
              class="mouvement-frise__instantane"
            />
            <span
              v-if="!legendeDessus(barre)"
              class="mouvement-frise__legende"
              :style="{ left: `calc(${pourcent(barre.duree)} + var(--csp-space-2))` }"
            >{{ barre.legende }}</span>
            <span
              v-if="ecoule(ligne, id) !== null && barre.duree && !barre.horsDemo"
              class="mouvement-frise__point"
              :style="{
                left: pourcent(Math.min(ecoule(ligne, id)!, barre.duree)),
                top: hauteur(barre, ecoule(ligne, id)!),
              }"
            />
          </div>
        </div>
        <span
          v-if="ecoule(ligne, id) !== null"
          class="mouvement-frise__tete"
          :style="{ left: pourcent(ecoule(ligne, id)!) }"
        />
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
.mouvement-frise {
  display: grid;
  column-gap: var(--csp-space-6);
  color: var(--text-default-grey);
  font-size: var(--csp-font-size-sm);
}

.mouvement-frise__entete {
  padding-bottom: var(--csp-space-1);
}

.mouvement-frise__titre {
  display: block;
  font-weight: var(--csp-font-weight-bold);
}

.mouvement-frise__graduations {
  position: relative;
  height: 1.25rem;
}

.mouvement-frise__graduation {
  position: absolute;
  bottom: 0;
  translate: -50% 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
  white-space: nowrap;

  &:first-child {
    translate: 0 0;
  }

  &:last-child {
    translate: -100% 0;
  }
}

.mouvement-frise__libelle,
.mouvement-frise__cellule {
  padding-block: var(--csp-space-2);
  border-top: 1px solid var(--border-default-grey);
}

.mouvement-frise__libelle {
  font-weight: var(--csp-font-weight-bold);
}

.mouvement-frise__cellule {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  background-image: linear-gradient(to right, var(--border-default-grey) 1px, transparent 1px);
  background-size: 20% 100%;
}

.mouvement-frise__barre {
  position: relative;
  height: 1.5rem;
}

.mouvement-frise__courbe {
  display: block;
  height: 100%;
  overflow: visible;

  rect {
    fill: var(--background-contrast-blue-france);
  }

  polyline {
    fill: none;
    stroke: var(--border-plain-blue-france);
    stroke-width: 2;
    vector-effect: non-scaling-stroke;
  }
}

.mouvement-frise__instantane {
  display: block;
  width: 3px;
  height: 100%;
  background-color: var(--border-plain-blue-france);
}

.mouvement-frise__legende {
  position: absolute;
  top: 50%;
  translate: 0 -50%;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
  white-space: nowrap;
}

/* Above a long bar, on a line of its own */
.mouvement-frise__legende--dessus {
  position: static;
  display: block;
  translate: none;
}

.mouvement-frise__point {
  position: absolute;
  width: 0.625rem;
  height: 0.625rem;
  translate: -50% -50%;
  border-radius: 50%;
  background-color: var(--border-plain-blue-france);
}

.mouvement-frise__tete {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  translate: -1px 0;
  background-color: var(--text-title-grey);
}
</style>
