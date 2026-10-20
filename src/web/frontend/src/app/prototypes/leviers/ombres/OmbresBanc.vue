<script setup lang="ts">
import type { LevierOption } from '../options'
import { computed, ref, watch } from 'vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import { storyFrameSrc } from '../../storyFrame'
import { valeursOf } from '../options'

const props = defineProps<{
  options: LevierOption[]
  // Id of the screen story, rendered without option
  ecran: string
}>()

// The story writes its color mode on the root element before it renders
const theme = document.documentElement.getAttribute('data-fr-theme') ?? 'light'
const ecranSrc = storyFrameSrc(props.ecran)

const choix = ref(props.options[0]!.id)
const option = computed(() => props.options.find(({ id }) => id === choix.value)!)
const segments = computed(() => props.options.map(({ id, nom }) => ({ value: id, label: nom })))

// The screen keeps its open menu, panel or dialog when the option changes: its variables change in place, on its
// root element, without reloading it
const ecran = ref<HTMLIFrameElement | null>(null)
let ecrites: string[] = []

function appliquer(): void {
  const racine = ecran.value?.contentDocument?.documentElement
  if (!racine) {
    return
  }
  for (const name of ecrites) {
    racine.style.removeProperty(name)
  }
  const valeurs = valeursOf(option.value, theme)
  for (const [name, value] of Object.entries(valeurs)) {
    racine.style.setProperty(name, value)
  }
  ecrites = Object.keys(valeurs)
}

watch(option, appliquer)
</script>

<template>
  <div class="ombres-banc">
    <div class="ombres-banc__barre">
      <CspSegmentedControl
        v-model="choix"
        :options="segments"
        legend="Ombres"
        inline-legend
        size="sm"
      />
    </div>
    <iframe
      ref="ecran"
      class="ombres-banc__ecran"
      :src="ecranSrc"
      title="Écran de l'application"
      @load="appliquer"
    />
  </div>
</template>

<style scoped lang="scss">
.ombres-banc {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  height: 100vh;
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
}

.ombres-banc__barre {
  display: flex;
  justify-content: center;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-bottom: 1px solid var(--border-default-grey);
}

.ombres-banc__ecran {
  width: 100%;
  height: 100%;
  border: 0;
}
</style>
