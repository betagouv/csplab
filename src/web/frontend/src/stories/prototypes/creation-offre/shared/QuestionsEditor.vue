<script setup lang="ts">
import type { Question } from '../data/types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import { nouvelId, useOffre } from '../data/useOffre'

// Questions posées au candidat lors du dépôt. Raccourci : créer une question depuis un critère indispensable.
const { state, verrouille } = useOffre()
const c = state.conditions

const FORMATS = [
  { value: 'oui_non', label: 'Oui / Non' },
  { value: 'choix', label: 'Choix dans une liste' },
  { value: 'texte', label: 'Réponse courte' },
]
const criteresSansQuestion = computed(() => c.indispensables.filter(x => !c.questions.some(q => q.critereId === x.id)))

function ajouter(depuis?: { id: string, libelle: string }) {
  c.questions.push({
    id: nouvelId('q'),
    libelle: depuis ? `Remplissez-vous ce critère : ${depuis.libelle.toLowerCase()} ?` : '',
    format: 'oui_non',
    choix: [],
    bloquante: Boolean(depuis),
    critereId: depuis?.id ?? null,
  })
}
function maj(q: Question, patch: Partial<Question>) {
  Object.assign(q, patch)
}
</script>

<template>
  <ol
    v-if="c.questions.length"
    class="qs"
  >
    <li
      v-for="(q, i) in c.questions"
      :key="q.id"
      class="q"
    >
      <div class="q__row">
        <CspInput
          :model-value="q.libelle"
          :label="`Question ${i + 1}`"
          size="sm"
          :disabled="verrouille"
          @update:model-value="v => maj(q, { libelle: v })"
        />
        <CspSelect
          :model-value="q.format"
          label="Réponse"
          size="sm"
          :options="FORMATS"
          :disabled="verrouille"
          @update:model-value="v => maj(q, { format: v as Question['format'] })"
        />
        <CspButton
          v-if="!verrouille"
          icon="ri:delete-bin-line"
          variant="tertiary-no-outline"
          size="sm"
          :aria-label="`Supprimer la question ${i + 1}`"
          @click="c.questions.splice(i, 1)"
        />
      </div>
      <CspInput
        v-if="q.format === 'choix'"
        :model-value="q.choix.join(', ')"
        label="Choix proposés, séparés par des virgules"
        size="sm"
        :disabled="verrouille"
        @update:model-value="v => maj(q, { choix: v.split(',').map(x => x.trim()).filter(Boolean) })"
      />
      <CspSwitch
        v-if="q.format === 'oui_non'"
        :model-value="q.bloquante"
        label="Signaler au premier tri les réponses « non »"
        size="sm"
        :disabled="verrouille"
        @update:model-value="v => maj(q, { bloquante: v })"
      />
    </li>
  </ol>
  <div
    v-if="!verrouille"
    class="qs__add"
  >
    <CspButton
      label="Ajouter une question"
      variant="secondary"
      size="sm"
      icon="ri:add-line"
      is-icon-left
      @click="ajouter()"
    />
    <CspButton
      v-for="x in criteresSansQuestion"
      :key="x.id"
      :label="`Vérifier « ${x.libelle} »`"
      variant="tertiary-no-outline"
      size="sm"
      @click="ajouter(x)"
    />
  </div>
</template>

<style scoped lang="scss">
.qs {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  margin: 0;
  padding: 0;
  list-style: none;
}

.q {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.q__row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 12rem auto;
  align-items: end;
  gap: var(--csp-space-2);
}

.qs__add {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}
</style>
