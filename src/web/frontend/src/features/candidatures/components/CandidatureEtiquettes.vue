<script setup lang="ts">
import type { CspLabelItem } from '@/components/base/CspLabel/types'
import { ref, useId, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspLabelList from '@/components/base/CspLabel/CspLabelList.vue'

const props = defineProps<{
  etiquettes: CspLabelItem[]
}>()

const titleId = useId()
const posees = ref([...props.etiquettes])

watch(() => props.etiquettes, (etiquettes) => {
  posees.value = [...etiquettes]
})

function retirer(etiquette: CspLabelItem): void {
  posees.value = posees.value.filter(({ label }) => label !== etiquette.label)
}
</script>

<template>
  <section
    class="candidature-etiquettes"
    :aria-labelledby="titleId"
  >
    <h3
      :id="titleId"
      class="candidature-etiquettes__title"
    >
      Étiquettes
    </h3>
    <CspLabelList
      v-if="posees.length"
      :labels="posees"
      size="md"
      removable
      @remove="retirer"
    />
    <CspButton
      class="candidature-etiquettes__add"
      variant="tertiary-no-outline"
      size="sm"
      icon="ri:add-line"
      is-icon-left
      label="Ajouter"
      aria-label="Ajouter une étiquette"
    />
  </section>
</template>

<style scoped lang="scss">
.candidature-etiquettes {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-3);
}

.candidature-etiquettes__title {
  margin: 0;
  font-size: var(--csp-text-group-title-size, var(--csp-font-size-base));
  font-weight: var(--csp-text-group-title-weight, var(--csp-font-weight-bold));
  color: var(--text-title-grey);
  line-height: var(--csp-text-group-title-line-height, inherit);
}

/* the content of the button lines up with the labels */
.candidature-etiquettes__add {
  margin-inline-start: calc(-1 * var(--csp-btn-padding-x-sm));
}
</style>
