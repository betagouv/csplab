<script setup lang="ts">
import type { PanelPosition } from '../shared/useCandidaturePrototype'
import CspButton from '@/components/base/CspButton/CspButton.vue'

defineProps<{
  etapeNom: string | null
  position: PanelPosition | null
}>()

const emit = defineEmits<{
  previous: []
  next: []
}>()
</script>

<template>
  <div class="panel-footer">
    <CspButton
      label="Précédent"
      variant="tertiary"
      size="sm"
      icon="ri:arrow-left-s-line"
      is-icon-left
      title="Candidature précédente (flèche gauche)"
      :disabled="!position?.previousUuid"
      @click="emit('previous')"
    />
    <div class="panel-footer__position">
      <p class="panel-footer__counter">
        <template v-if="position">
          Candidature {{ position.index + 1 }} sur {{ position.total }}
        </template>
        <template v-else>
          Position inconnue dans la colonne
        </template>
      </p>
      <p
        v-if="etapeNom"
        class="panel-footer__etape"
      >
        Étape {{ etapeNom }}
      </p>
    </div>
    <CspButton
      label="Suivant"
      variant="tertiary"
      size="sm"
      icon="ri:arrow-right-s-line"
      title="Candidature suivante (flèche droite)"
      :disabled="!position?.nextUuid"
      @click="emit('next')"
    />
  </div>
</template>

<style scoped lang="scss">
.panel-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
  width: 100%;
  min-height: 2.5rem;
}

.panel-footer__position {
  display: flex;
  align-items: baseline;
  gap: var(--csp-space-2);
  font-size: 0.875rem;
  line-height: 1.4;
}

.panel-footer__counter {
  margin: 0;
  font-weight: 700;
  color: var(--text-title-grey);
}

.panel-footer__etape {
  margin: 0;
  color: var(--text-mention-grey);

  &::before {
    margin-right: var(--csp-space-2);
    content: '·';
  }
}
</style>
