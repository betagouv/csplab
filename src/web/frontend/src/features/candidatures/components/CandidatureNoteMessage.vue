<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, useId, useTemplateRef } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'

defineProps<{
  message: string
}>()

const messageId = useId()
const text = useTemplateRef('text')
const expanded = ref(false)
const overflowing = ref(false)

function measure(): void {
  if (text.value && !expanded.value) {
    const halfLine = (Number.parseFloat(getComputedStyle(text.value).lineHeight) || 0) / 2
    overflowing.value = text.value.scrollHeight - text.value.clientHeight > halfLine
  }
}

let observer: ResizeObserver | undefined

onMounted(() => {
  measure()
  observer = new ResizeObserver(measure)
  observer.observe(text.value!)
})

onBeforeUnmount(() => observer?.disconnect())
</script>

<template>
  <div class="candidature-note-message">
    <p
      :id="messageId"
      ref="text"
      class="candidature-note-message__text"
      :class="{ 'candidature-note-message__text--clamped': !expanded }"
    >
      {{ message }}
    </p>
    <CspButton
      v-if="overflowing"
      variant="tertiary-no-outline"
      size="sm"
      :label="expanded ? 'Afficher moins' : 'Afficher plus'"
      :icon="expanded ? 'ri:arrow-up-s-line' : 'ri:arrow-down-s-line'"
      :aria-expanded="expanded"
      :aria-controls="messageId"
      @click="expanded = !expanded"
    />
  </div>
</template>

<style scoped lang="scss">
.candidature-note-message {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-2);
}

.candidature-note-message__text {
  margin: 0;
  white-space: pre-line;
}

.candidature-note-message__text--clamped {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 5;
  line-clamp: 5;
}
</style>
