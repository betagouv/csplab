<script setup lang="ts">
import type { Phase, PhaseId } from '../../data/processus'
import type { OffreState } from '../../data/types'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { phases } from '../../data/processus'

// Fil du processus : besoin → validation (DAR ou non) → offre → publication.
// Version normale (tête de dossier, phases cliquables) ou compacte (cellule de tableau).
const props = withDefaults(defineProps<{
  state: OffreState
  compact?: boolean
  actif?: PhaseId
  cliquables?: PhaseId[]
}>(), { compact: false, actif: undefined, cliquables: () => [] })

const emit = defineEmits<{ aller: [phase: PhaseId] }>()

const liste = computed(() => phases(props.state))

const ICONES: Record<Phase['etat'], string> = {
  fait: 'ri:checkbox-circle-fill',
  en_cours: 'ri:edit-circle-line',
  a_venir: 'ri:checkbox-blank-circle-line',
  sans_objet: 'ri:indeterminate-circle-line',
}
</script>

<template>
  <ol
    class="proc"
    :class="{ 'proc--compact': compact }"
    :aria-label="compact ? undefined : 'Avancement du recrutement'"
  >
    <li
      v-for="(p, i) in liste"
      :key="p.id"
      class="proc__item"
      :class="[`proc__item--${p.etat}`, { 'proc__item--actif': actif === p.id }]"
    >
      <span
        v-if="i > 0"
        class="proc__sep"
        aria-hidden="true"
      />
      <component
        :is="!compact && cliquables.includes(p.id) ? 'button' : 'span'"
        :type="!compact && cliquables.includes(p.id) ? 'button' : undefined"
        class="proc__step"
        :aria-current="actif === p.id ? 'step' : undefined"
        @click="!compact && cliquables.includes(p.id) && emit('aller', p.id)"
      >
        <CspIcon
          :name="ICONES[p.etat]"
          :size="compact ? 14 : 16"
          class="proc__icon"
        />
        <span
          v-if="!compact"
          class="proc__text"
        >
          <span class="proc__label">{{ p.libelle }}</span>
          <span class="proc__detail">{{ p.detail }}</span>
        </span>
        <span
          v-else
          class="sr-only"
        >{{ p.libelle }} : {{ p.detail }}</span>
      </component>
    </li>
  </ol>
</template>

<style scoped lang="scss">
.proc {
  display: flex;
  align-items: center;
  margin: 0;
  padding: 0;
  list-style: none;
}

.proc__item {
  display: flex;
  align-items: center;
}

.proc__sep {
  width: 2rem;
  height: 1px;
  margin: 0 var(--csp-space-2);
  background: var(--border-default-grey);

  .proc--compact & {
    width: 0.5rem;
    margin: 0 2px;
  }
}

.proc__step {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  padding: var(--csp-space-2) var(--csp-space-2);
  border: 0;
  border-bottom: 2px solid transparent;
  background: none;
  font: inherit;
  text-align: left;
  color: var(--text-default-grey);

  .proc--compact & {
    padding: 0;
  }

  &:is(button) {
    cursor: pointer;

    &:hover .proc__label {
      color: var(--text-action-high-blue-france);
      text-decoration: underline;
    }

    &:focus-visible {
      outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
    }
  }

  .proc__item--actif & {
    border-bottom-color: var(--border-active-blue-france);
  }
}

.proc__icon {
  flex-shrink: 0;
  color: var(--text-mention-grey);

  .proc__item--fait & {
    color: var(--text-default-success);
  }

  .proc__item--en_cours & {
    color: var(--text-action-high-blue-france);
  }

  .proc__item--sans_objet & {
    color: var(--text-disabled-grey, var(--text-mention-grey));
  }
}

.proc__text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.proc__label {
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);

  .proc__item--actif & {
    color: var(--text-action-high-blue-france);
  }
}

.proc__detail {
  font-size: var(--csp-font-size-xs);
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
