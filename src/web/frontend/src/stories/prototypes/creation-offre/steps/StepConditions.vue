<script setup lang="ts">
import type { Question } from '../data/types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import { PROFILS, STATUTS } from '../data/referentiels'
import { nouvelId, useOffre } from '../data/useOffre'
import CritereList from '../shared/CritereList.vue'
import Field from '../shared/Field.vue'
import FormSection from '../shared/FormSection.vue'
import StepFooter from '../shared/StepFooter.vue'
import StepHeader from '../shared/StepHeader.vue'

// Écran 5 — conditions de candidature. On sépare nettement l'éligibilité (qui peut candidater)
// des critères de sélection (ce qui permet de comparer les candidatures).
const { state, verrouille, afficherErreurs, aller, notifier } = useOffre()
const c = state.conditions

const statutsLibelle = computed(() => state.besoin.statuts.map(s => STATUTS.find(x => x.value === s)?.label).join(', ') || 'non renseigné')

const competencesNonReprises = computed(() =>
  state.poste.competences.filter(comp => ![...c.indispensables, ...c.souhaites].some(x => x.libelle === comp)),
)
function suggererDepuisFiche() {
  const n = competencesNonReprises.value.length
  c.souhaites.push(...competencesNonReprises.value.map(l => ({ id: nouvelId('c'), libelle: l, type: 'competence' as const })))
  notifier(`${n} compétence(s) de la fiche de poste ajoutée(s) aux critères souhaités. Déplacez-les si besoin.`)
}

const FORMATS = [
  { value: 'oui_non', label: 'Oui / Non' },
  { value: 'choix', label: 'Choix dans une liste' },
  { value: 'texte', label: 'Réponse courte' },
]
const optionsCriteres = computed(() => [{ value: 'aucun', label: 'Aucun' }, ...c.indispensables.map(x => ({ value: x.id, label: x.libelle }))])

function ajouterQuestion(depuis?: { id: string, libelle: string }) {
  c.questions.push({
    id: nouvelId('q'),
    libelle: depuis ? `Remplissez-vous ce critère : ${depuis.libelle.toLowerCase()} ?` : '',
    format: 'oui_non',
    choix: [],
    bloquante: Boolean(depuis),
    critereId: depuis?.id ?? null,
  })
}

function majQuestion(q: Question, patch: Partial<Question>) {
  Object.assign(q, patch)
}

function critereSupprime(id: string) {
  c.questions.forEach((q) => {
    if (q.critereId === id) {
      q.critereId = null
    }
  })
}

const criteresSansQuestion = computed(() => c.indispensables.filter(x => !c.questions.some(q => q.critereId === x.id)))
</script>

<template>
  <StepHeader
    id="conditions"
    description="Qui peut candidater, et sur quoi les candidatures seront comparées. Ces éléments sont repris tels quels dans le traitement des candidatures après publication. Rien n'est obligatoire en dehors des profils autorisés."
  />

  <fieldset
    class="step-fields"
    :disabled="verrouille"
  >
    <FormSection
      titre="Éligibilité — qui peut candidater ?"
      description="Conditions d'accès au poste. Elles déterminent qui peut déposer une candidature, pas qui sera retenu."
      nature="recrutement"
    >
      <dl class="recall">
        <div>
          <dt>Catégorie(s)</dt>
          <dd>{{ state.besoin.categories.join(', ') || 'non renseignée' }}</dd>
        </div>
        <div>
          <dt>Statuts ouverts</dt>
          <dd>{{ statutsLibelle }}</dd>
        </div>
        <CspButton
          label="Modifier dans « Besoin et poste »"
          variant="tertiary-no-outline"
          size="sm"
          @click="aller('besoin')"
        />
      </dl>
      <Field path="conditions.profils">
        <CspCheckboxGroup
          v-model="c.profils"
          label="Profils autorisés à candidater *"
          :options="PROFILS"
          :disabled="verrouille"
          :error="afficherErreurs && !c.profils.length"
          error-message="Cochez au moins un profil."
        />
      </Field>
      <p
        v-if="c.profils.includes('contractuels') && !state.besoin.statuts.includes('contractuel')"
        class="incoherence"
        role="status"
      >
        Les candidats contractuels sont autorisés ici, mais le statut « contractuel » n'est pas ouvert dans « Besoin et poste ».
      </p>
      <CspCallout
        variant="default"
        description="Hypothèse : les conditions réglementaires générales d'accès (statut, diplôme exigé par un corps…) ne sont pas modélisées ici. Elles pourraient être proposées automatiquement selon le versant et la catégorie."
      />
    </FormSection>

    <FormSection
      titre="Critères de sélection"
      description="Ce qui permet de comparer les candidatures éligibles. Définissez-les de préférence avec le manager."
      nature="recrutement"
    >
      <CritereList
        v-model="c.indispensables"
        titre="Critères indispensables"
        aide="Sans eux, la candidature ne peut pas être retenue. Restez sobre : 2 à 4 critères."
        vide="Aucun critère indispensable. C'est possible si le poste est ouvert à des profils variés."
        :disabled="verrouille"
        @supprime="critereSupprime"
      />
      <CritereList
        v-model="c.souhaites"
        titre="Critères souhaités"
        aide="Ils départagent les candidatures, sans en écarter aucune."
        vide="Aucun critère souhaité pour l'instant."
        :disabled="verrouille"
      />
      <div
        v-if="competencesNonReprises.length && !verrouille"
        class="suggest"
      >
        <span>{{ competencesNonReprises.length }} compétence(s) de la fiche de poste ne sont pas encore des critères.</span>
        <CspButton
          label="Les ajouter aux critères souhaités"
          variant="secondary"
          size="sm"
          icon="ri:add-line"
          is-icon-left
          @click="suggererDepuisFiche"
        />
      </div>
    </FormSection>

    <FormSection
      titre="Questions de présélection"
      description="Posées au candidat lors du dépôt. Elles aident au premier tri ; aucune candidature n'est écartée automatiquement (hypothèse)."
      nature="recrutement"
      facultatif
    >
      <div
        v-if="!c.questions.length"
        class="empty"
      >
        <p>Aucune question. Elles sont utiles pour vérifier rapidement un critère indispensable (permis, diplôme…).</p>
      </div>
      <ol
        v-else
        class="questions"
      >
        <li
          v-for="(q, i) in c.questions"
          :key="q.id"
          class="question"
        >
          <div class="question__head">
            <span class="question__num">Question {{ i + 1 }}</span>
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
            :model-value="q.libelle"
            label="Intitulé de la question"
            size="sm"
            :disabled="verrouille"
            :error="afficherErreurs && !q.libelle"
            error-message="Rédigez la question ou supprimez-la."
            @update:model-value="v => majQuestion(q, { libelle: v })"
          />
          <div class="question__row">
            <CspSelect
              :model-value="q.format"
              label="Format de réponse"
              size="sm"
              :options="FORMATS"
              :disabled="verrouille"
              @update:model-value="v => majQuestion(q, { format: v as Question['format'] })"
            />
            <CspSelect
              :model-value="q.critereId ?? 'aucun'"
              label="Vérifie le critère indispensable"
              size="sm"
              :options="optionsCriteres"
              :disabled="verrouille"
              @update:model-value="v => majQuestion(q, { critereId: v === 'aucun' ? null : (v ?? null) })"
            />
          </div>
          <CspInput
            v-if="q.format === 'choix'"
            :model-value="q.choix.join(', ')"
            label="Choix proposés"
            hint="Séparés par des virgules"
            size="sm"
            :disabled="verrouille"
            @update:model-value="v => majQuestion(q, { choix: v.split(',').map(x => x.trim()).filter(Boolean) })"
          />
          <CspSwitch
            v-if="q.format === 'oui_non'"
            :model-value="q.bloquante"
            label="Signaler au premier tri les candidatures qui répondent « non »"
            size="sm"
            :disabled="verrouille"
            @update:model-value="v => majQuestion(q, { bloquante: v })"
          />
        </li>
      </ol>
      <div
        v-if="!verrouille"
        class="questions__add"
      >
        <CspButton
          label="Ajouter une question"
          variant="secondary"
          size="sm"
          icon="ri:add-line"
          is-icon-left
          @click="ajouterQuestion()"
        />
        <CspButton
          v-for="x in criteresSansQuestion"
          :key="x.id"
          :label="`Question pour « ${x.libelle} »`"
          variant="tertiary-no-outline"
          size="sm"
          icon="ri:question-line"
          is-icon-left
          @click="ajouterQuestion(x)"
        />
      </div>
    </FormSection>
  </fieldset>

  <StepFooter id="conditions" />
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

.recall {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-6);
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-alt-grey);
  font-size: var(--csp-font-size-sm);

  dt {
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
    font-weight: var(--csp-font-weight-medium);
  }
}

.incoherence {
  margin: 0;
  padding: var(--csp-space-2) var(--csp-space-3);
  font-size: var(--csp-font-size-sm);
  background: var(--background-contrast-warning);
}

.suggest {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3);
  background: var(--background-alt-blue-france);
  font-size: var(--csp-font-size-sm);
}

.empty p {
  margin: 0;
  padding: var(--csp-space-3);
  background: var(--background-alt-grey);
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.questions {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  margin: 0;
  padding: 0;
  list-style: none;
}

.question {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4) var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
}

.question__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.question__num {
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.question__row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--csp-space-3);
}

.questions__add {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}
</style>
