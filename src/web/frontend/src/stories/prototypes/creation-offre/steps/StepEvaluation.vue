<script setup lang="ts">
import type { CritereEvaluation } from '../data/types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import { personne, PERSONNES } from '../data/referentiels'
import { nouvelId, useOffre } from '../data/useOffre'
import FormSection from '../shared/FormSection.vue'
import ListEditor from '../shared/ListEditor.vue'
import StepFooter from '../shared/StepFooter.vue'
import StepHeader from '../shared/StepHeader.vue'

// Écran 6 — préparer l'évaluation (facultatif). Pas de notation chiffrée :
// une grille lisible, réutilisée au tri des candidatures.
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
    const indispensable = state.conditions.indispensables.includes(c)
    e.criteres.push({ id: nouvelId('e'), libelle: c.libelle, importance: indispensable ? 'essentiel' : 'important', depuisCritereId: c.id })
  }
}
function ajouterCritere() {
  e.criteres.push({ id: nouvelId('e'), libelle: '', importance: 'important', depuisCritereId: null })
}
function maj(c: CritereEvaluation, patch: Partial<CritereEvaluation>) {
  Object.assign(c, patch)
}

const premierTri = computed({
  get: () => e.premierTri.map(t => t.libelle),
  set: (libelles: string[]) => {
    e.premierTri = libelles.map((libelle, i) => ({ id: e.premierTri[i]?.id ?? nouvelId('t'), libelle }))
  },
})

const TOURS = [{ value: '1', label: 'Un entretien' }, { value: '2', label: 'Deux entretiens' }]
const FORMATS = [{ value: 'presentiel', label: 'Sur place' }, { value: 'visio', label: 'En visioconférence' }, { value: 'mixte', label: 'Au choix du candidat' }]
const juryOptions = PERSONNES.map(p => ({ value: p.id, label: `${p.nom} — ${p.role}` }))
</script>

<template>
  <StepHeader
    id="evaluation"
    description="Facultatif à ce stade. Définir dès maintenant comment les candidatures seront examinées fait gagner du temps au tri et aligne l'équipe. Tout reste modifiable après publication."
  />

  <CspSwitch
    v-model="e.active"
    label="Préparer l'évaluation des candidatures maintenant"
    :disabled="verrouille"
  />

  <div
    v-if="!e.active"
    class="empty"
  >
    <CspIcon
      name="ri:list-check-3"
      :size="24"
    />
    <p><strong>L'évaluation n'est pas encore préparée.</strong></p>
    <p>Vous pourrez la définir au moment du tri des candidatures. Les critères de sélection saisis à l'étape précédente seront proposés automatiquement.</p>
  </div>

  <fieldset
    v-else
    class="step-fields"
    :disabled="verrouille"
  >
    <FormSection
      titre="Critères d'évaluation"
      description="Sur quoi l'équipe appréciera chaque candidature. L'importance sert à ordonner, pas à calculer une note."
      nature="recrutement"
    >
      <table
        v-if="e.criteres.length"
        class="grid"
      >
        <thead>
          <tr>
            <th scope="col">
              Critère
            </th>
            <th scope="col">
              Importance
            </th>
            <th scope="col">
              <span class="sr-only">Actions</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="c in e.criteres"
            :key="c.id"
          >
            <td>
              <input
                class="grid__input"
                :value="c.libelle"
                placeholder="Décrire le critère"
                :aria-label="`Critère ${c.libelle}`"
                @change="maj(c, { libelle: ($event.target as HTMLInputElement).value })"
              >
              <small
                v-if="c.depuisCritereId"
                class="grid__src"
              >Issu des critères de sélection</small>
            </td>
            <td class="grid__imp">
              <select
                class="grid__input"
                :value="c.importance"
                :aria-label="`Importance de ${c.libelle}`"
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
            </td>
            <td class="grid__act">
              <CspButton
                v-if="!verrouille"
                icon="ri:delete-bin-line"
                variant="tertiary-no-outline"
                size="sm"
                :aria-label="`Supprimer ${c.libelle}`"
                @click="e.criteres = e.criteres.filter(x => x.id !== c.id)"
              />
            </td>
          </tr>
        </tbody>
      </table>
      <div
        v-if="!verrouille"
        class="actions"
      >
        <CspButton
          v-if="aImporter.length"
          :label="`Reprendre les ${aImporter.length} critère(s) de sélection`"
          variant="secondary"
          size="sm"
          icon="ri:download-2-line"
          is-icon-left
          @click="importer"
        />
        <CspButton
          label="Ajouter un critère"
          variant="tertiary"
          size="sm"
          icon="ri:add-line"
          is-icon-left
          @click="ajouterCritere"
        />
      </div>
    </FormSection>

    <FormSection
      titre="Premier tri"
      description="Points à vérifier rapidement sur chaque dossier avant un examen approfondi."
      nature="recrutement"
    >
      <ListEditor
        v-model="premierTri"
        label="Points de vérification"
        placeholder="Ex. : Diplôme bac+3 ou équivalent"
        :disabled="verrouille"
      />
      <p
        v-if="state.conditions.questions.length"
        class="note"
      >
        <CspIcon
          name="ri:information-line"
          :size="14"
        />
        Les réponses aux {{ state.conditions.questions.length }} question(s) de présélection seront affichées à côté de ces points.
      </p>
    </FormSection>

    <FormSection
      titre="Entretiens envisagés"
      nature="recrutement"
      facultatif
    >
      <div class="cols">
        <CspRadioGroup
          v-model="e.tours"
          label="Nombre d'entretiens"
          :options="TOURS"
          :disabled="verrouille"
        />
        <CspRadioGroup
          v-model="e.format"
          label="Format"
          :options="FORMATS"
          :disabled="verrouille"
        />
      </div>
      <CspCheckboxGroup
        v-model="e.jury"
        label="Membres du jury pressentis"
        :options="juryOptions"
        :disabled="verrouille"
      />
    </FormSection>
  </fieldset>

  <section
    class="next"
    aria-labelledby="next-title"
  >
    <h3
      id="next-title"
      class="next__title"
    >
      <CspIcon
        name="ri:arrow-right-circle-line"
        :size="16"
      />
      Après publication : ce que verra l'équipe sur chaque candidature
    </h3>
    <div class="next__mock">
      <div class="next__cand">
        <strong>Candidature n° 12</strong>
        <small>Reçue le 14 novembre · Premier tri</small>
      </div>
      <div class="next__cols">
        <div>
          <p class="next__label">
            Premier tri
          </p>
          <ul>
            <li
              v-for="t in e.premierTri"
              :key="t.id"
            >
              <span class="next__box" />{{ t.libelle }}
            </li>
            <li
              v-for="q in state.conditions.questions"
              :key="q.id"
            >
              <CspIcon
                name="ri:question-answer-line"
                :size="12"
              />{{ q.libelle || 'Question' }} <em>réponse du candidat</em>
            </li>
            <li
              v-if="!e.premierTri.length && !state.conditions.questions.length"
              class="next__empty"
            >
              Rien de préparé
            </li>
          </ul>
        </div>
        <div>
          <p class="next__label">
            Appréciation
          </p>
          <ul>
            <li
              v-for="c in e.criteres"
              :key="c.id"
            >
              <span class="next__imp">{{ IMPORTANCES.find(i => i.value === c.importance)?.label }}</span>{{ c.libelle || '—' }}
            </li>
            <li
              v-if="!e.criteres.length"
              class="next__empty"
            >
              Rien de préparé
            </li>
          </ul>
        </div>
        <div>
          <p class="next__label">
            Jury
          </p>
          <ul>
            <li
              v-for="j in e.jury"
              :key="j"
            >
              {{ personne(j).nom }}
            </li>
            <li
              v-if="!e.jury.length"
              class="next__empty"
            >
              Non défini
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <StepFooter id="evaluation" />
</template>

<style scoped lang="scss">
.step-fields {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  margin: 0;
  padding: 0;
  border: 0;
  min-width: 0;
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-1);
  padding: var(--csp-space-5);
  border: 1px dashed var(--border-default-grey);
  background: var(--background-default-grey);
  color: var(--text-mention-grey);

  p {
    margin: 0;
    max-width: 40rem;
  }

  strong {
    color: var(--text-default-grey);
  }
}

.grid {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--csp-font-size-sm);

  th {
    text-align: left;
    font-size: var(--csp-font-size-xs);
    font-weight: var(--csp-font-weight-medium);
    color: var(--text-mention-grey);
    padding: var(--csp-space-1) var(--csp-space-2);
    border-bottom: 1px solid var(--border-default-grey);
  }

  td {
    padding: var(--csp-space-1);
    border-bottom: 1px solid var(--border-default-grey);
    vertical-align: top;
  }
}

.grid__input {
  width: 100%;
  padding: var(--csp-space-1) var(--csp-space-2);
  border: 1px solid transparent;
  background: transparent;
  font: inherit;
  color: var(--text-default-grey);

  &:hover:not(:disabled) {
    border-color: var(--border-default-grey);
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
  }
}

.grid__src {
  display: block;
  padding-left: var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  color: var(--text-default-info);
}

.grid__imp {
  width: 11rem;
}

.grid__act {
  width: 2.5rem;
}

.actions {
  display: flex;
  gap: var(--csp-space-2);
}

.note {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--csp-space-5);
}

.next {
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.next__title {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0 0 var(--csp-space-3);
  font-size: var(--csp-font-size-base);
}

.next__mock {
  border: 1px solid var(--border-default-grey);
  background: var(--background-alt-grey);
  font-size: var(--csp-font-size-xs);
}

.next__cand {
  display: flex;
  justify-content: space-between;
  padding: var(--csp-space-2) var(--csp-space-3);
  border-bottom: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);

  small {
    color: var(--text-mention-grey);
  }
}

.next__cols {
  display: grid;
  grid-template-columns: 1.3fr 1.3fr 0.8fr;
  gap: var(--csp-space-4);
  padding: var(--csp-space-3);

  ul {
    display: flex;
    flex-direction: column;
    gap: var(--csp-space-1);
    margin: 0;
    padding: 0;
    list-style: none;
  }

  li {
    display: flex;
    align-items: center;
    gap: var(--csp-space-1);
    flex-wrap: wrap;
  }

  em {
    color: var(--text-mention-grey);
  }
}

.next__label {
  margin: 0 0 var(--csp-space-2);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.next__box {
  width: 0.75rem;
  height: 0.75rem;
  border: 1px solid var(--border-plain-grey);
}

.next__imp {
  padding: 0 var(--csp-space-1);
  background: var(--background-contrast-grey);
}

.next__empty {
  color: var(--text-mention-grey);
  font-style: italic;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
