<script setup lang="ts">
import { computed } from 'vue'

const COULEURS = [
  'var(--background-flat-blue-france)',
  'var(--background-flat-yellow-tournesol)',
  'var(--background-flat-green-emeraude)',
  'var(--background-flat-pink-tuile)',
]

interface Confetti {
  left: string
  delay: string
  duration: string
  rotate: string
  couleur: string
  forme: 'rond' | 'carre'
}

const confettis = computed<Confetti[]>(() => Array.from({ length: 24 }, (_, i) => ({
  left: `${(i * 41) % 100}%`,
  delay: `${(i % 8) * 0.06}s`,
  duration: `${1.1 + (i % 5) * 0.15}s`,
  rotate: `${(i * 53) % 360}deg`,
  couleur: COULEURS[i % COULEURS.length],
  forme: i % 2 === 0 ? 'rond' : 'carre',
})))
</script>

<template>
  <div
    class="confetti"
    aria-hidden="true"
  >
    <span
      v-for="(c, index) in confettis"
      :key="index"
      class="confetti__piece"
      :class="`confetti__piece--${c.forme}`"
      :style="{
        'left': c.left,
        'animationDelay': c.delay,
        'animationDuration': c.duration,
        'backgroundColor': c.couleur,
        '--rotate': c.rotate,
      }"
    />
  </div>
</template>

<style scoped lang="scss">
.confetti {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  border-radius: inherit;
}

.confetti__piece {
  position: absolute;
  top: -0.75rem;
  width: 0.5rem;
  height: 0.75rem;
  opacity: 0.9;
  animation-name: confetti-fall;
  animation-timing-function: ease-in;
  animation-fill-mode: forwards;
}

.confetti__piece--rond {
  border-radius: 50%;
}

.confetti__piece--carre {
  border-radius: 0.125rem;
}

@keyframes confetti-fall {
  from {
    transform: translateY(0) rotate(0deg);
    opacity: 0.9;
  }

  to {
    transform: translateY(14rem) rotate(var(--rotate));
    opacity: 0;
  }
}

@media (prefers-reduced-motion: reduce) {
  .confetti__piece {
    animation: none;
    opacity: 0;
  }
}
</style>
