<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import { PROFILS, STATUTS } from '../../data/referentiels'
import { nouvelId, useOffre } from '../../data/useOffre'
import CritereList from '../../shared/CritereList.vue'
import Disclosure from '../../shared/Disclosure.vue'
import EvaluationEditor from '../../shared/EvaluationEditor.vue'
import Panel from '../../shared/Panel.vue'
import QuestionsEditor from '../../shared/QuestionsEditor.vue'
import EtapeFooter from './EtapeFooter.vue'
import RemarquesSection from './RemarquesSection.vue'
import { useEtapes } from './useEtapes'

// Étape 3 — qui peut candidater et sur quoi les candidatures seront comparées.
// Les profils sont déduits des statuts déjà saisis ; questions et grille d'évaluation sont repliées.
const { state, verrouille, notifier } = useOffre()
const { aller } = useEtapes()
const c = state.conditions

/** Évite la double saisie : les profils autorisés sont proposés à partir des statuts ouverts à l'étape 1. */
const deduits = ref(false)
onMounted(() => {
  if (!c.profils.length && state.besoin.statuts.length && !verrouille.value) {
    const p: string[] = []
    if (state.besoin.statuts.includes('titulaire')) {
      p.push('fonct-meme-versant', 'fonct-autres-versants')
    }
    if (state.besoin.statuts.includes('contractuel')) {
      p.push('contractuels')
    }
    c.profils = p
    deduits.value = true
  }
})

const rappel = computed(() => {
  const b = state.besoin
  const statuts = b.statuts.map(s => STATUTS.find(x => x.value === s)?.label.toLowerCase()).join(' et ')
  return [b.categories.length ? `Catégorie ${b.categories.join(', ')}` : '', statuts ? `ouvert aux ${statuts.replace('fonctionnaire (titulaire)', 'fonctionnaires').replace('contractuel·le', 'contractuels')}` : ''].filter(Boolean).join(' · ')
})

const competences = computed(() => state.poste.competences.filter(x => ![...c.indispensables, ...c.souhaites].some(k => k.libelle === x)))
function ajouterCompetences() {
  const n = competences.value.length
  c.souhaites.push(...competences.value.map(l => ({ id: nouvelId('c'), libelle: l, type: 'competence' as const })))
  notifier(`${n} compétence(s) ajoutée(s) aux critères souhaités.`)
}

function critereSupprime(id: string) {
  c.questions.forEach((q) => {
    if (q.critereId === id) {
      q.critereId = null
    }
  })
}

const questionsOuvertes = ref(false)
const evaluationOuverte = ref(false)
const resumeQuestions = computed(() => (c.questions.length ? `${c.questions.length} question(s) posée(s) au dépôt` : 'Vérifier un critère dès le dépôt (permis, diplôme…)'))
const resumeEvaluation = computed(() => {
  const e = state.evaluation
  return e.criteres.length || e.premierTri.length
    ? `${e.criteres.length} critère(s), ${e.premierTri.length} point(s) de premier tri`
    : 'Préparer la grille de tri et les entretiens, ou le faire après publication'
})
</script>

<template>
  <header>
    <h2 class="title">
      Conditions de candidature
    </h2>
    <p class="desc">
      Ces éléments seront repris dans le traitement des candidatures après publication.
    </p>
  </header>

  <RemarquesSection :step-ids="['conditions', 'evaluation']" />

  <fieldset
    class="fields"
    :disabled="verrouille"
  >
    <Panel titre="Qui peut candidater ?">
      <p
        v-if="rappel"
        class="rappel"
      >
        {{ rappel }}
        <button
          type="button"
          class="link"
          @click="aller('poste', 'champ-statuts')"
        >
          Modifier
        </button>
      </p>
      <CspCheckboxGroup
        v-model="c.profils"
        label="Profils acceptés"
        :options="PROFILS"
        :disabled="verrouille"
      />
      <p
        v-if="deduits"
        class="hint"
      >
        Proposé à partir des statuts ouverts. Ajustez si besoin.
      </p>
    </Panel>

    <Panel
      titre="Critères de sélection"
      description="Les critères indispensables écartent une candidature s'ils ne sont pas remplis ; les critères souhaités départagent."
    >
      <CritereList
        v-model="c.indispensables"
        titre="Indispensables"
        aide="2 à 4 critères suffisent généralement."
        vide="Aucun critère indispensable."
        :disabled="verrouille"
        @supprime="critereSupprime"
      />
      <CritereList
        v-model="c.souhaites"
        titre="Souhaités"
        aide="Ils aident à comparer, sans écarter."
        vide="Aucun critère souhaité."
        :disabled="verrouille"
      />
      <p
        v-if="competences.length && !verrouille"
        class="hint"
      >
        {{ competences.length }} compétence(s) de la fiche de poste peuvent servir de critères.
        <button
          type="button"
          class="link"
          @click="ajouterCompetences"
        >
          Les ajouter aux critères souhaités
        </button>
      </p>
    </Panel>

    <Panel>
      <Disclosure
        v-model:ouvert="questionsOuvertes"
        titre="Questions de présélection"
        :resume="resumeQuestions"
        icon="ri:question-answer-line"
        facultatif
      >
        <QuestionsEditor />
      </Disclosure>
      <Disclosure
        v-model:ouvert="evaluationOuverte"
        titre="Évaluation et entretiens"
        :resume="resumeEvaluation"
        icon="ri:list-check-3"
        facultatif
      >
        <EvaluationEditor />
      </Disclosure>
    </Panel>
  </fieldset>

  <EtapeFooter />
</template>

<style scoped lang="scss">
.title {
  margin: 0;
  font-size: var(--csp-font-size-2xl);
}

.desc {
  margin: var(--csp-space-1) 0 0;
  color: var(--text-mention-grey);
}

.fields {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  margin: 0;
  padding: 0;
  border: 0;
  min-width: 0;
}

.rappel {
  margin: 0;
  padding: var(--csp-space-2) var(--csp-space-3);
  background: var(--background-alt-grey);
  font-size: var(--csp-font-size-sm);
}

.hint {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.link {
  margin-left: var(--csp-space-1);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}
</style>
