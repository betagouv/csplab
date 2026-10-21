<script setup lang="ts">
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspPopover from '@/components/base/CspPopover/CspPopover.vue'

// Choix des colonnes d'un tableau (dont le code poste). La configuration est gardée pendant la session.
const props = defineProps<{ colonnes: { id: string, header: string, verrouillee?: boolean }[], defaut: string[], cle: string }>()
const visibles = defineModel<string[]>({ required: true })

try {
  const brut = sessionStorage.getItem(props.cle)
  if (brut) {
    visibles.value = JSON.parse(brut)
  }
}
catch {
  // sans persistance
}

function enregistrer(v: string[]) {
  visibles.value = v
  try {
    sessionStorage.setItem(props.cle, JSON.stringify(v))
  }
  catch {
    // sans persistance
  }
}
</script>

<template>
  <CspPopover align="end">
    <template #trigger>
      <CspButton
        label="Colonnes"
        variant="tertiary"
        size="sm"
        icon="ri:layout-column-line"
        is-icon-left
      />
    </template>
    <div class="cols">
      <p class="cols__titre">
        Colonnes affichées
      </p>
      <CspCheckbox
        v-for="c in colonnes"
        :key="c.id"
        :label="c.header"
        size="sm"
        :model-value="c.verrouillee || visibles.includes(c.id)"
        :disabled="c.verrouillee"
        @update:model-value="on => enregistrer(on ? [...visibles, c.id] : visibles.filter(x => x !== c.id))"
      />
      <CspButton
        label="Revenir aux colonnes par défaut"
        variant="tertiary-no-outline"
        size="sm"
        @click="enregistrer([...defaut])"
      />
    </div>
  </CspPopover>
</template>

<style scoped lang="scss">
.cols {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  min-width: 15rem;
  padding: var(--csp-space-3);
}

.cols__titre {
  margin: 0 0 var(--csp-space-1);
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}
</style>
