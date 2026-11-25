<script setup lang="ts">
import type { Champ } from './aide'
import type { Offre } from './store'
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { alerte, tentatives } from './aide'

// Un champ de l'annonce avec son aide légère : un conseil 💡 qui réagit à la saisie (un seul format d'aide,
// retour Alice du 25/11/2026 : plus de « ? » à côté du libellé), une alerte au besoin, et l'indication « repris de la fiche » tant que le texte n'a pas été adapté.
// « Requis pour la validation » signale les champs déterminants pour la DAR.
const props = defineProps<{
  offre: Offre
  champ: Champ
  label?: string
  /** Texte d'aide gris sous le libellé (DSFR). */
  hint?: string
  /** Champ obligatoire pour publier : astérisque après le libellé (retour PO, F5). */
  obligatoire?: boolean
  forId?: string
  repris?: boolean
  modifie?: boolean
  /** Champ déterminant pour la demande de validation (organisme avec DAR). */
  requis?: boolean
  /** Champ validé par la DAR : verrouillé. */
  valide?: boolean
  /** Message affiché après une tentative d'envoi ou de création. */
  erreur?: string
}>()
const emit = defineEmits<{ restaurer: [] }>()

// Les alertes « à corriger » n'apparaissent qu'après une tentative de publication (retour PO, F6).
const a = computed(() => {
  const x = alerte(props.offre, props.champ)
  return x?.niveau === 'attention' && !tentatives.has(props.offre.id) ? null : x
})
</script>

<template>
  <div class="champ">
    <div
      v-if="label"
      class="champ__tete"
    >
      <span>
        <label
          :for="forId"
          class="champ__label"
        >{{ label }}<abbr
          v-if="obligatoire"
          class="champ__etoile"
          title="obligatoire"
        > *</abbr></label>
        <span
          v-if="requis"
          class="champ__requis"
        >Requis pour la validation</span>
        <span
          v-if="valide"
          class="champ__valide"
        ><CspIcon
          name="ri:lock-line"
          :size="12"
        /> Validé · non modifiable</span>
      </span>
      <span
        v-if="repris"
        class="champ__tag"
      >Repris de la fiche</span>
      <button
        v-else-if="modifie"
        type="button"
        class="champ__lien"
        @click="emit('restaurer')"
      >
        Reprendre le texte de la fiche
      </button>
    </div>
    <p
      v-if="label && hint"
      class="champ__hint"
    >
      {{ hint }}
    </p>
    <slot />
    <p
      v-if="erreur"
      class="champ__erreur"
      role="alert"
    >
      {{ erreur }}
    </p>
    <p
      v-else-if="a"
      class="champ__alerte"
      :class="`champ__alerte--${a.niveau}`"
    >
      <CspIcon
        :name="a.niveau === 'attention' ? 'ri:error-warning-line' : 'ri:lightbulb-line'"
        :size="14"
      />
      {{ a.texte }}
    </p>
  </div>
</template>

<style scoped lang="scss">
.champ {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
}

.champ__tete {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-3);
}

.champ__hint {
  margin: var(--csp-space-1) 0 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.champ__label {
  font-weight: var(--csp-font-weight-bold);
}

.champ__requis {
  margin-left: var(--csp-space-2);
  padding: 0 var(--csp-space-1);
  background: var(--background-alt-blue-france);
  font-size: var(--csp-font-size-xs);
  color: var(--text-action-high-blue-france);
  white-space: nowrap;
}

.champ__valide {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  margin-left: var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
  white-space: nowrap;
}

.champ__erreur {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-default-error);
}

.champ__tag {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.champ__alerte {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.champ__alerte {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);

  &--attention {
    color: var(--text-default-warning);
  }
}

.champ__lien {
  margin-left: var(--csp-space-1);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-size: var(--csp-font-size-xs);
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}
.champ__etoile {
  color: var(--text-default-error);
  text-decoration: none;
}
</style>
