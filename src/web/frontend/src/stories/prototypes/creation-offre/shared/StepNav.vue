<script setup lang="ts">
import type { StepStatut } from '../data/useOffre'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { STEPS, useOffre } from '../data/useOffre'

// Navigation libre entre les étapes, groupées par phase. Chaque étape affiche son état
// de complétude : l'ordre est suggéré, pas imposé.
const { step, aller, statutStep, manquesDe, progression, state } = useOffre()

const phases = computed(() => {
  const groupes: { phase: string, steps: typeof STEPS }[] = []
  for (const s of STEPS) {
    const g = groupes.find(x => x.phase === s.phase)
    if (g) {
      g.steps.push(s)
    }
    else {
      groupes.push({ phase: s.phase, steps: [s] })
    }
  }
  return groupes
})

const ICONES: Record<StepStatut, { icon: string, label: string }> = {
  complet: { icon: 'ri:checkbox-circle-fill', label: 'complet' },
  incomplet: { icon: 'ri:error-warning-line', label: 'à compléter' },
  facultatif: { icon: 'ri:checkbox-blank-circle-line', label: 'facultatif' },
  a_faire: { icon: 'ri:checkbox-blank-circle-line', label: 'à faire' },
  en_cours: { icon: 'ri:time-line', label: 'en cours' },
}

function remarquesDe(id: string) {
  return state.remarques.filter(r => r.stepId === id && !r.resolue).length
}

const pourcent = computed(() => Math.round((progression.value.faits / progression.value.total) * 100))
</script>

<template>
  <nav
    class="step-nav"
    aria-label="Étapes de création de l'offre"
  >
    <button
      type="button"
      class="step-nav__start"
      :class="{ 'step-nav__start--active': step === 'demarrer' }"
      :aria-current="step === 'demarrer' ? 'step' : undefined"
      @click="aller('demarrer')"
    >
      <CspIcon
        name="ri:play-circle-line"
        :size="16"
      />
      <span>
        Point de départ
        <small v-if="state.sourceLibelle">{{ state.sourceLibelle.split(' — ')[0] }}</small>
        <small v-else-if="state.startMode === 'vierge'">Offre vierge</small>
      </span>
    </button>

    <div
      class="step-nav__progress"
      role="group"
      aria-label="Progression"
    >
      <div class="step-nav__progress-label">
        <span>Informations requises</span>
        <strong>{{ progression.faits }}/{{ progression.total }} étapes</strong>
      </div>
      <div
        class="step-nav__bar"
        role="progressbar"
        :aria-valuenow="pourcent"
        aria-valuemin="0"
        aria-valuemax="100"
        :aria-label="`${pourcent} % des étapes requises complètes`"
      >
        <span :style="{ width: `${pourcent}%` }" />
      </div>
    </div>

    <div
      v-for="g in phases"
      :key="g.phase"
      class="step-nav__phase"
    >
      <p class="step-nav__phase-title">
        {{ g.phase }}
      </p>
      <ol class="step-nav__list">
        <li
          v-for="s in g.steps"
          :key="s.id"
        >
          <button
            type="button"
            class="step-nav__item"
            :class="[`step-nav__item--${statutStep(s.id)}`, { 'step-nav__item--active': step === s.id }]"
            :aria-current="step === s.id ? 'step' : undefined"
            @click="aller(s.id)"
          >
            <CspIcon
              class="step-nav__icon"
              :name="ICONES[statutStep(s.id)].icon"
              :size="16"
            />
            <span class="step-nav__label">
              {{ s.libelle }}
              <span class="sr-only">— {{ ICONES[statutStep(s.id)].label }}</span>
            </span>
            <span
              v-if="remarquesDe(s.id)"
              class="step-nav__remark"
              :title="`${remarquesDe(s.id)} remarque(s) à traiter`"
            ><CspIcon
              name="ri:chat-1-line"
              :size="12"
            />{{ remarquesDe(s.id) }}<span class="sr-only"> remarque(s) à traiter</span></span>
            <span
              v-if="manquesDe(s.id).length"
              class="step-nav__count"
              :title="`${manquesDe(s.id).length} information(s) requise(s) manquante(s)`"
            >{{ manquesDe(s.id).length }}</span>
            <span
              v-else-if="s.facultatif && !remarquesDe(s.id)"
              class="step-nav__opt"
            >facultatif</span>
          </button>
        </li>
      </ol>
    </div>
  </nav>
</template>

<style scoped lang="scss">
.step-nav {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding: var(--csp-space-4) var(--csp-space-3);
}

.step-nav__start {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-2);
  width: 100%;
  padding: var(--csp-space-2);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  text-align: left;
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
  cursor: pointer;

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  &:hover {
    background: var(--background-default-grey-hover);
  }

  &--active {
    border-color: var(--border-active-blue-france);
  }
}

.step-nav__progress-label {
  display: flex;
  justify-content: space-between;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
  margin-bottom: var(--csp-space-1);

  strong {
    color: var(--text-default-grey);
  }
}

.step-nav__bar {
  height: 4px;
  background: var(--background-contrast-grey);

  span {
    display: block;
    height: 100%;
    background: var(--background-action-high-blue-france);
    transition: width 0.3s;
  }
}

.step-nav__phase-title {
  margin: 0 0 var(--csp-space-1);
  padding-inline: var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--text-mention-grey);
}

.step-nav__list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.step-nav__item {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  width: 100%;
  padding: var(--csp-space-2);
  border: 0;
  border-left: 2px solid transparent;
  background: none;
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
  text-align: left;
  cursor: pointer;

  &:hover {
    background: var(--background-default-grey-hover);
  }

  &--active {
    border-left-color: var(--border-active-blue-france);
    background: var(--background-default-grey);
    color: var(--text-action-high-blue-france);
    font-weight: var(--csp-font-weight-bold);
  }
}

.step-nav__icon {
  flex-shrink: 0;
  color: var(--text-mention-grey);

  .step-nav__item--complet & {
    color: var(--text-default-success);
  }

  .step-nav__item--incomplet & {
    color: var(--text-default-warning);
  }

  .step-nav__item--en_cours & {
    color: var(--text-action-high-blue-france);
  }
}

.step-nav__label {
  flex: 1;
  min-width: 0;
}

.step-nav__count {
  flex-shrink: 0;
  min-width: 1.25rem;
  padding: 0 var(--csp-space-1);
  border-radius: 1rem;
  background: var(--background-contrast-warning);
  color: var(--text-default-warning);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-align: center;
}

.step-nav__remark {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  flex-shrink: 0;
  padding: 0 var(--csp-space-1);
  border-radius: 1rem;
  background: var(--background-contrast-error);
  color: var(--text-default-error);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
}

.step-nav__opt {
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-regular);
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
