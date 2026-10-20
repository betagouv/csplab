<script setup lang="ts">
import type { CritereEvaluation } from '../data/types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import { PERSONNES } from '../data/referentiels'
import { nouvelId, useOffre } from '../data/useOffre'
import ListEditor from './ListEditor.vue'

// Grille d'évaluation légère (importance, pas de note), premier tri et entretiens.
const { state, verrouille } = useOffre()
const e = state.evaluation

const IMPORTANCES = [
  { value: 'essentiel', label: 'Essentiel' },
  { value: 'important', label: 'Important' },
  { value: 'complementaire', label: 'Complémentaire' },
]
const aImporter = computed(() => [...state.conditions.indispensables, ...state.conditions.souhaites].filter(c => !e.criteres.some(x => x.depuisCritereId === c.id)))
function importer() {
  for (const c of aImporter.value) {
    e.criteres.push({ id: nouvelId('e'), libelle: c.libelle, importance: state.conditions.indispensables.includes(c) ? 'essentiel' : 'important', depuisCritereId: c.id })
  }
  e.active = true
}
function maj(c: CritereEvaluation, patch: Partial<CritereEvaluation>) {
  Object.assign(c, patch)
}
const premierTri = computed({
  get: () => e.premierTri.map(t => t.libelle),
  set: (l: string[]) => {
    e.premierTri = l.map((libelle, i) => ({ id: e.premierTri[i]?.id ?? nouvelId('t'), libelle }))
    e.active = true
  },
})
const juryOptions = PERSONNES.map(p => ({ value: p.id, label: p.nom }))
</script>

<template>
  <div class="ev">
    <p class="ev__label">
      Critères d'évaluation
    </p>
    <ul
      v-if="e.criteres.length"
      class="ev__list"
    >
      <li
        v-for="c in e.criteres"
        :key="c.id"
      >
        <input
          class="ev__input"
          :value="c.libelle"
          :aria-label="`Critère ${c.libelle}`"
          :disabled="verrouille"
          @change="maj(c, { libelle: ($event.target as HTMLInputElement).value })"
        >
        <select
          class="ev__input ev__imp"
          :value="c.importance"
          :aria-label="`Importance de ${c.libelle}`"
          :disabled="verrouille"
          @change="maj(c, { importance: ($event.target as HTMLSelectElement).value as CritereEvaluation['importance'] })"
        >
          <option
            v-for="i in IMPORTANCES"
            :key="i.value"
            :value="i.value"
          >
            {{ i.label }}
          </option>
        </select>
        <CspButton
          v-if="!verrouille"
          icon="ri:delete-bin-line"
          variant="tertiary-no-outline"
          size="sm"
          :aria-label="`Supprimer ${c.libelle}`"
          @click="e.criteres = e.criteres.filter(x => x.id !== c.id)"
        />
      </li>
    </ul>
    <div
      v-if="!verrouille"
      class="ev__actions"
    >
      <CspButton
        v-if="aImporter.length"
        :label="`Reprendre les ${aImporter.length} critère(s) de sélection`"
        variant="secondary"
        size="sm"
        @click="importer"
      />
      <CspButton
        label="Ajouter un critère"
        variant="tertiary-no-outline"
        size="sm"
        icon="ri:add-line"
        is-icon-left
        @click="e.criteres.push({ id: nouvelId('e'), libelle: '', importance: 'important', depuisCritereId: null }); e.active = true"
      />
    </div>
  </div>
  <ListEditor
    v-model="premierTri"
    label="Points à vérifier au premier tri"
    placeholder="Ex. : CV et lettre de motivation présents"
    :disabled="verrouille"
  />
  <div class="ev__cols">
    <CspRadioGroup
      v-model="e.tours"
      label="Entretiens"
      :options="[{ value: '1', label: 'Un entretien' }, { value: '2', label: 'Deux entretiens' }]"
      :disabled="verrouille"
    />
    <CspCheckboxGroup
      v-model="e.jury"
      label="Jury pressenti"
      :options="juryOptions"
      :disabled="verrouille"
    />
  </div>
</template>

<style scoped lang="scss">
.ev {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.ev__label {
  margin: 0;
  color: var(--text-label-grey);
}

.ev__list {
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid var(--border-default-grey);

  li {
    display: flex;
    align-items: center;
    gap: var(--csp-space-2);
    padding: var(--csp-space-1) var(--csp-space-2);
  }

  li + li {
    border-top: 1px solid var(--border-default-grey);
  }
}

.ev__input {
  flex: 1;
  min-width: 0;
  padding: var(--csp-space-1) var(--csp-space-2);
  border: 1px solid transparent;
  background: transparent;
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);

  &:hover:not(:disabled) {
    border-color: var(--border-default-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
  }
}

.ev__imp {
  flex: 0 0 10rem;
}

.ev__actions {
  display: flex;
  gap: var(--csp-space-2);
}

.ev__cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--csp-space-5);
}
</style>
