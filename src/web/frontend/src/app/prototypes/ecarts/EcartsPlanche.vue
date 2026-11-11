<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'

export interface EcartsPlancheFrame {
  storyId: string
  label: string
}

const props = defineProps<{
  frames: EcartsPlancheFrame[]
  width: number
  height: number
}>()

function readTheme(): string {
  return document.documentElement.getAttribute('data-fr-theme') ?? 'light'
}

const theme = ref(readTheme())
let observer: MutationObserver | undefined

onMounted(() => {
  observer = new MutationObserver(() => {
    theme.value = readTheme()
  })
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-fr-theme'] })
})

onUnmounted(() => observer?.disconnect())

const globalsParam = computed(() => {
  const globals = new Map<string, string>()
  const current = new URLSearchParams(window.location.search).get('globals')
  for (const entry of current?.split(';') ?? []) {
    const [key, value] = entry.split(':')
    if (key && value) {
      globals.set(key, value)
    }
  }
  globals.set('theme', theme.value)
  return [...globals].map(([key, value]) => `${key}:${value}`).join(';')
})

function frameSrc(storyId: string): string {
  const params = new URLSearchParams({ id: storyId, viewMode: 'story', globals: globalsParam.value })
  return `iframe.html?${params.toString()}`
}

const gridStyle = computed(() => ({
  gridTemplateColumns: `repeat(${props.frames.length}, ${props.width}px)`,
}))
</script>

<template>
  <div
    class="ecarts-planche"
    :style="gridStyle"
  >
    <figure
      v-for="frame in frames"
      :key="frame.storyId"
      class="ecarts-planche__frame"
    >
      <figcaption class="ecarts-planche__label">
        {{ frame.label }}
      </figcaption>
      <iframe
        class="ecarts-planche__iframe"
        :src="frameSrc(frame.storyId)"
        :title="frame.label"
        :width="width"
        :height="height"
      />
    </figure>
  </div>
</template>

<style scoped lang="scss">
.ecarts-planche {
  display: grid;
  gap: var(--csp-space-6);
  padding: var(--csp-space-4);
  background: var(--background-alt-grey);
  min-height: 100vh;
  box-sizing: border-box;
  align-content: start;
}

.ecarts-planche__frame {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
}

.ecarts-planche__label {
  color: var(--text-title-grey);
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}

.ecarts-planche__iframe {
  display: block;
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}
</style>
