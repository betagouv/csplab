<script setup lang="ts">
import type { Candidature } from '../data/candidatMock'
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { etapeActuelle } from '../data/candidatMock'
import EtapesResume from './EtapesResume.vue'

const props = defineProps<{
  candidature: Candidature
}>()

defineEmits<{
  ouvrir: [id: string]
}>()

const phase = computed(() => etapeActuelle(props.candidature)?.label ?? 'Candidature reçue')
</script>

<template>
  <button
    type="button"
    class="cand-card"
    @click="$emit('ouvrir', candidature.id)"
  >
    <div class="cand-card__header">
      <div>
        <p class="cand-card__poste">
          {{ candidature.poste }}
        </p>
        <p class="cand-card__organisme">
          {{ candidature.organisme }}
        </p>
      </div>
      <CspBadge
        :label="phase"
        variant="soft"
        type="info"
      />
    </div>

    <EtapesResume :etapes="candidature.etapes" />

    <div class="cand-card__footer">
      <p class="cand-card__next">
        <strong>Prochaine étape :</strong> {{ candidature.prochaineEtapeLabel }}
      </p>
      <p
        v-if="candidature.prochaineDate"
        class="cand-card__date"
      >
        Prévu le {{ candidature.prochaineDate }}
      </p>
      <p
        v-else-if="candidature.delaiIndicatif"
        class="cand-card__date"
      >
        {{ candidature.delaiIndicatif }}
      </p>
    </div>

    <CspIcon
      name="ri:arrow-right-s-line"
      :size="20"
      class="cand-card__arrow"
    />
  </button>
</template>

<style scoped lang="scss">
.cand-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  width: 100%;
  text-align: left;
  padding: var(--csp-space-4) var(--csp-space-12) var(--csp-space-4) var(--csp-space-4);
  border: none;
  border-radius: 0.375rem;
  background-color: var(--background-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  cursor: pointer;
  font: inherit;

  &:hover {
    background-color: var(--background-alt-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.cand-card__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--csp-space-3);
}

.cand-card__poste {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-title-grey);
}

.cand-card__organisme {
  margin: 0.125rem 0 0;
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.cand-card__footer {
  padding-top: var(--csp-space-2);
  border-top: 1px solid var(--border-default-grey);
}

.cand-card__next {
  margin: 0;
  font-size: 0.8125rem;
  color: var(--text-default-grey);
}

.cand-card__date {
  margin: 0.125rem 0 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.cand-card__arrow {
  position: absolute;
  right: var(--csp-space-4);
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-mention-grey);
}
</style>
