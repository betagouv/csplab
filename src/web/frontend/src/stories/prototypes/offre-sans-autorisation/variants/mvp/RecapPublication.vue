<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { champsObligatoires } from './aide'
import { ETAPES_OFFRE } from './etapes'

// Récapitulatif avant publication (retour PO, F4) : ce qui est fait (coché) et ce qui reste, étape par étape,
// avec « Plus que N champs obligatoires à remplir avant de publier ». Un clic mène à l'étape concernée.
const props = defineProps<{ offre: Offre }>()
const emit = defineEmits<{ aller: [etape: number] }>()

const champs = computed(() => champsObligatoires(props.offre))
const reste = computed(() => champs.value.filter(c => !c.ok).length)
const parEtape = computed(() => ETAPES_OFFRE
  .map((e, i) => ({ ...e, n: i + 1, champs: champs.value.filter(c => c.partie === e.id) }))
  .filter(e => e.champs.length))
</script>

<template>
  <div class="recap">
    <p
      class="recap__titre"
      :class="{ 'recap__titre--ok': !reste }"
    >
      {{ reste
        ? `Plus que ${reste} champ${reste > 1 ? 's' : ''} obligatoire${reste > 1 ? 's' : ''} à remplir avant de publier`
        : 'Tous les champs obligatoires sont remplis' }}
    </p>
    <p class="recap__compte">
      {{ champs.length - reste }} / {{ champs.length }} remplis
    </p>
    <div
      v-for="e in parEtape"
      :key="e.id"
      class="recap__etape"
    >
      <button
        type="button"
        class="recap__lien"
        @click="emit('aller', e.n)"
      >
        {{ e.n }}. {{ e.titre }}
      </button>
      <ul>
        <li
          v-for="c in e.champs"
          :key="c.label"
          :class="{ fait: c.ok }"
        >
          <CspIcon
            :name="c.ok ? 'ri:checkbox-circle-fill' : 'ri:checkbox-blank-circle-line'"
            :size="16"
            :class="c.ok ? 'icone--ok' : 'icone--reste'"
          />
          <span>{{ c.label }}<span class="sr-only">{{ c.ok ? ' : rempli' : ' : à remplir' }}</span></span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped lang="scss">
.recap {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.recap__titre {
  margin: 0;
  font-weight: 700;
  color: var(--text-title-grey);
}

.recap__titre--ok {
  color: var(--text-default-success);
}

.recap__compte {
  margin: calc(-1 * var(--csp-space-2)) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.recap__lien {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-size: var(--csp-font-size-sm);
  font-weight: 700;
  color: var(--text-action-high-blue-france);
  text-align: left;
  text-decoration: underline;
  text-underline-offset: 3px;
  cursor: pointer;
}

ul {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin: var(--csp-space-1) 0 0;
  padding: 0;
  list-style: none;
}

li {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
}

li.fait {
  color: var(--text-mention-grey);
}

.icone--ok {
  flex-shrink: 0;
  color: var(--text-default-success);
}

.icone--reste {
  flex-shrink: 0;
  color: var(--text-mention-grey);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
