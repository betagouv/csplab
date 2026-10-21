<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import { PROFILS, STATUTS } from '../../data/referentiels'
import { nouvelId, useOffre } from '../../data/useOffre'
import CritereList from '../../shared/CritereList.vue'
import Disclosure from '../../shared/Disclosure.vue'
import EvaluationEditor from '../../shared/EvaluationEditor.vue'
import FieldRow from '../../shared/FieldRow.vue'
import ListEditor from '../../shared/ListEditor.vue'
import Panel from '../../shared/Panel.vue'
import QuestionsEditor from '../../shared/QuestionsEditor.vue'
import EtapeFooter from './EtapeFooter.vue'
import RemarquesSection from './RemarquesSection.vue'
import { useEtapes } from './useEtapes'

// Étape 3 — qui peut candidater et sur quoi les candidatures seront comparées.
// Les profils sont déduits des statuts déjà saisis ; questions et grille d'évaluation sont repliées.
const { state, verrouille, notifier, afficherErreurs, canaux } = useOffre()
const c = state.conditions
const b = state.besoin

// --- Informations propres à l'offre ---
const postesDar = computed(() => state.darContenu?.nbPostes)
const ISO = /^\d{4}-\d{2}-\d{2}$/
const erreurLimite = computed(() => {
  if (state.dateLimite && !ISO.test(state.dateLimite)) {
    return 'Format attendu : AAAA-MM-JJ'
  }
  return undefined
})
const lignesCanaux = computed(() => canaux.map(c => ({ ...c, etat: state.canaux.find(x => x.id === c.id)! })))
const autresCanaux = ref(state.canaux.some(c => c.selectionne && c.id !== 'csp'))
const criteresOuverts = ref(c.indispensables.length + c.souhaites.length > 0)
const resumeCriteres = computed(() => (c.indispensables.length + c.souhaites.length
  ? `${c.indispensables.length} indispensable(s), ${c.souhaites.length} souhaité(s)`
  : 'Préciser ce qui est indispensable et ce qui départage les candidatures'))
const { aller } = useEtapes()

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
      Configurer le recrutement
    </h2>
    <p class="desc">
      Les informations propres à ce recrutement. Ce qui vient de la fiche de poste{{ state.besoin.darApplicable === 'oui' ? ' et de la DAR' : '' }} n'est pas redemandé.
    </p>
  </header>

  <RemarquesSection :step-ids="['conditions', 'evaluation']" />

  <fieldset
    class="fields"
    :disabled="verrouille"
  >
    <section
      class="repris"
      aria-label="Informations reprises"
    >
      <p class="repris__title">
        <CspIcon
          name="ri:file-copy-2-line"
          :size="14"
        />
        Repris de la fiche {{ state.ficheId }} (version du {{ state.ficheVersion }}){{ state.besoin.darApplicable === 'oui' ? ` et de la DAR ${b.darRef}` : '' }}
      </p>
      <p class="repris__body">
        {{ [b.service, b.localisation, b.categories.length ? `Catégorie ${b.categories.join(', ')}` : '', b.statuts.length === 2 ? 'Fonctionnaires et contractuels' : b.statuts[0] === 'contractuel' ? 'Contractuels' : 'Fonctionnaires'].filter(Boolean).join(' · ') }}
      </p>
      <p class="repris__body">
        Missions, activités et compétences : reprises pour la rédaction de l'offre (étape suivante).
      </p>
    </section>

    <Panel titre="Informations de l'offre">
      <FieldRow :cols="2">
        <CspInput
          v-model="b.nbPostes"
          type="number"
          label="Nombre de postes à pourvoir"
          :hint="postesDar ? `Une seule offre publiée pour ${b.nbPostes} poste(s). DAR : ${postesDar}.` : `Une seule offre publiée pour ${b.nbPostes} poste(s).`"
          :disabled="verrouille"
          :error="Number(b.nbPostes) < 1"
          :error-message="Number(b.nbPostes) < 1 ? 'Indiquez au moins 1 poste.' : undefined"
        />
        <ListEditor
          v-model="b.codesPostes"
          :label="Number(b.nbPostes) > 1 ? 'Codes des postes (facultatif)' : 'Code poste (facultatif)'"
          :hint="Number(b.nbPostes) > 1 ? `${b.codesPostes.length} sur ${b.nbPostes} renseigné(s)` : undefined"
          placeholder="Ex. : SG-PAIE-012"
          :disabled="verrouille"
        />
      </FieldRow>
      <FieldRow
        id="fin-dates"
        :cols="2"
      >
        <CspInput
          v-model="state.dateLimite"
          label="Date limite de candidature"
          hint="Nécessaire pour activer la publication."
          placeholder="AAAA-MM-JJ"
          :disabled="verrouille"
          :error="Boolean(erreurLimite) || (afficherErreurs && !state.dateLimite && state.statut === 'creee')"
          :error-message="erreurLimite ?? (afficherErreurs && !state.dateLimite && state.statut === 'creee' ? 'Indiquez une date limite pour publier.' : undefined)"
        />
        <CspInput
          v-model="b.datePriseDePoste"
          label="Prise de poste souhaitée (facultatif)"
          placeholder="AAAA-MM-JJ"
          :disabled="verrouille"
        />
      </FieldRow>
      <CspInput
        v-model="state.contactCandidats"
        label="Contact pour les candidats (facultatif)"
        placeholder="Ex. : Isabelle Fournier, cheffe du bureau RH — 05 00 00 00 00"
        :disabled="verrouille"
      />
      <fieldset
        id="fin-canaux"
        class="canaux"
      >
        <legend class="canaux__legend">
          Publication
        </legend>
        <label
          v-for="l in lignesCanaux.filter(x => x.id === 'csp' || autresCanaux)"
          :key="l.id"
          class="canal"
        >
          <input
            v-model="l.etat.selectionne"
            type="checkbox"
            :disabled="verrouille"
          >
          <span>
            {{ l.nom }}
            <small>{{ l.mode === 'connecteur' ? 'Transmission automatique (simulée)' : `Ensuite : ${l.actionsManuelles.join(', ').toLowerCase()}` }}</small>
          </span>
        </label>
        <button
          v-if="!autresCanaux"
          type="button"
          class="link link--block"
          @click="autresCanaux = true"
        >
          Diffuser aussi ailleurs (site, intranet, LinkedIn…)
        </button>
      </fieldset>
    </Panel>

    <Panel titre="Modalités et conditions de candidature">
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

    <Panel>
      <Disclosure
        v-model:ouvert="criteresOuverts"
        titre="Critères de sélection"
        :resume="resumeCriteres"
        icon="ri:filter-3-line"
        facultatif
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
      </Disclosure>
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

.repris {
  padding: var(--csp-space-3) var(--csp-space-4);
  border: 1px dashed var(--border-default-grey);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);

  p {
    margin: 0;
  }
}

.repris__title {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin-bottom: var(--csp-space-1) !important;
  font-weight: var(--csp-font-weight-bold);
}

.repris__body {
  color: var(--text-mention-grey);
}

.canaux {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  border: 0;
  scroll-margin-top: var(--csp-space-6);
}

.canaux__legend {
  margin-bottom: var(--csp-space-2);
  color: var(--text-label-grey);
}

.canal {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
  cursor: pointer;

  input {
    margin-top: 3px;
    accent-color: var(--background-action-high-blue-france);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.link--block {
  align-self: flex-start;
  margin-left: 0;
  font-size: var(--csp-font-size-sm);
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
