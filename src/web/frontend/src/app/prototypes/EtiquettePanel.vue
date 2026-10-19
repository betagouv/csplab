<script setup lang="ts">
import type { PaletteColor } from '@/styles/palette'
import { computed, ref, useId } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import ColorField from './ColorField.vue'

const props = withDefaults(defineProps<{
  title: string
  libelle: string
  type: string
  couleur: PaletteColor
  proposerCouleur?: (type: string) => PaletteColor
}>(), {
  proposerCouleur: undefined,
})

const TYPES = [
  { value: 'candidature', label: 'Candidature' },
  { value: 'membre', label: 'Membre recrutement' },
  { value: 'note', label: 'Note' },
]

const titleId = useId()
const libelle = ref(props.libelle)
const type = ref(props.type)
const couleurChoisie = ref<PaletteColor>()
// Until the person picks a color, the panel shows the color proposed for the selected type
const couleur = computed<PaletteColor>({
  get: () => couleurChoisie.value ?? props.proposerCouleur?.(type.value) ?? props.couleur,
  set: (value) => {
    couleurChoisie.value = value
  },
})
</script>

<template>
  <section
    class="etiquette-panel"
    :aria-labelledby="titleId"
  >
    <header class="etiquette-panel__header">
      <h3
        :id="titleId"
        class="etiquette-panel__title"
      >
        {{ title }}
      </h3>
      <CspButton
        class="etiquette-panel__close"
        variant="tertiary-no-outline"
        size="sm"
        icon="ri:close-line"
        aria-label="Fermer"
      />
    </header>
    <div class="etiquette-panel__body">
      <CspInput
        v-model="libelle"
        label="Libellé"
        hint="25 caractères maximum"
        maxlength="25"
      />
      <CspRadioGroup
        v-model="type"
        label="Type d'étiquette"
        :options="TYPES"
      />
      <ColorField v-model="couleur" />
      <div class="etiquette-panel__preview">
        <p class="etiquette-panel__preview-title">
          Aperçu
        </p>
        <CspLabel
          :label="libelle.trim() || 'Libellé de l\'étiquette'"
          :color="couleur"
          size="md"
        />
      </div>
    </div>
    <footer class="etiquette-panel__footer">
      <CspButton
        variant="secondary"
        label="Annuler"
      />
      <CspButton
        label="Enregistrer"
        :disabled="!libelle.trim()"
      />
    </footer>
  </section>
</template>

<style scoped lang="scss">
/* Same frame as the side panel of the application (CspDrawer) */
.etiquette-panel {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-default-grey);
  background-color: var(--background-overlap-grey);
  color: var(--text-default-grey);
}

.etiquette-panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding: var(--csp-space-6);
  border-bottom: 1px solid var(--border-default-grey);
}

.etiquette-panel__title {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 700;
  line-height: 1.25;
  color: var(--text-title-grey);
}

.etiquette-panel__close {
  margin-block: calc(-1 * var(--csp-space-1));
  margin-inline-end: calc(-1 * var(--csp-btn-icon-inset));
}

.etiquette-panel__body {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  padding: var(--csp-space-6);
}

.etiquette-panel__preview {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-2);
}

.etiquette-panel__preview-title {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-default-grey);
}

.etiquette-panel__footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: var(--csp-space-3);
  padding: var(--csp-space-6);
  border-top: 1px solid var(--border-default-grey);
}
</style>
