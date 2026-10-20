<script setup lang="ts">
import type { EtapeCircuit, StepId } from '../data/types'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import { ORGANISMES, personne, PERSONNES } from '../data/referentiels'
import { LIBELLES_STATUT, STEPS, useOffre } from '../data/useOffre'
import SimulationNote from '../shared/SimulationNote.vue'
import StepFooter from '../shared/StepFooter.vue'
import StepHeader from '../shared/StepHeader.vue'

// Écran 7 — validation et collaboration : état, circuit, remarques, contributions, équipe.
const {
  state,
  circuit,
  etapeEnCours,
  bloquantsSoumission,
  soumettre,
  repondre,
  retirerDeValidation,
  simulerContribution,
  aller,
  notifier,
} = useOffre()

const organisme = computed(() => ORGANISMES.find(o => o.value === state.besoin.organisme)?.label)
const modifiable = computed(() => state.statut === 'brouillon' || state.statut === 'a_corriger')
const echecSoumission = ref(false)

function onSoumettre() {
  echecSoumission.value = !soumettre()
}

const STATUT_ETAPE: Record<EtapeCircuit['statut'], { label: string, icon: string, cls: string }> = {
  a_venir: { label: 'À venir', icon: 'ri:checkbox-blank-circle-line', cls: 'todo' },
  en_attente: { label: 'En attente de réponse', icon: 'ri:time-line', cls: 'wait' },
  approuve: { label: 'Validé', icon: 'ri:checkbox-circle-fill', cls: 'ok' },
  corrections: { label: 'Corrections demandées', icon: 'ri:error-warning-fill', cls: 'ko' },
}

// --- Étapes facultatives ajoutables (hypothèse : dépend du paramétrage de l'organisation) ---
const ETAPES_OPTIONNELLES = [
  { id: 'budget', libelle: 'Visa budgétaire', personneId: 'thomas' },
  { id: 'com', libelle: 'Relecture par la communication', personneId: 'sophie' },
]
const ajoutables = computed(() => ETAPES_OPTIONNELLES.filter(o => !state.circuit.some(e => e.id === o.id)).map(o => ({ value: o.id, label: `${o.libelle} — ${personne(o.personneId).nom}` })))
const etapeAAjouter = ref<string>()
function ajouterEtape() {
  const o = ETAPES_OPTIONNELLES.find(x => x.id === etapeAAjouter.value)
  if (o) {
    state.circuit.push({ ...o, obligatoire: false, statut: 'a_venir', date: null })
    etapeAAjouter.value = undefined
  }
}

// --- Simulation de la réponse du valideur ---
const reponseOuverte = ref(false)
const texteCorrection = ref('')
const etapeCorrection = ref<StepId>('offre')
const erreurCorrection = ref('')
const stepsOptions = STEPS.filter(s => !['validation', 'recap'].includes(s.id)).map(s => ({ value: s.id, label: s.libelle }))

function valider() {
  repondre(etapeEnCours.value!.id, 'approuve')
  reponseOuverte.value = false
}
function demanderCorrections() {
  if (!texteCorrection.value.trim()) {
    erreurCorrection.value = 'Précisez ce qui doit être corrigé.'
    return
  }
  repondre(etapeEnCours.value!.id, 'corrections', { texte: texteCorrection.value, stepId: etapeCorrection.value })
  texteCorrection.value = ''
  erreurCorrection.value = ''
  reponseOuverte.value = false
}

const remarques = computed(() => [...state.remarques].reverse())
const stepLibelle = (id: StepId) => STEPS.find(s => s.id === id)?.libelle

// --- Équipe ---
const ACCES = [
  { value: 'gestion', label: 'Gère le recrutement' },
  { value: 'evaluation', label: 'Évalue les candidatures' },
  { value: 'lecture', label: 'Consulte uniquement' },
]
const ajoutablesEquipe = computed(() => PERSONNES.filter(p => !state.equipe.some(m => m.personneId === p.id)).map(p => ({ value: p.id, label: `${p.nom} — ${p.role}` })))
const membreAAjouter = ref<string>()
function ajouterMembre() {
  if (membreAAjouter.value) {
    state.equipe.push({ personneId: membreAAjouter.value, acces: 'lecture' })
    notifier(`${personne(membreAAjouter.value).nom} ajouté·e à l'équipe de recrutement`)
    membreAAjouter.value = undefined
  }
}
</script>

<template>
  <StepHeader
    id="validation"
    description="Qui intervient, ce qui reste à valider et ce qui est attendu de chacun. Le circuit présenté est un exemple : chaque organisation définit le sien."
  />

  <section
    class="state"
    :class="`state--${state.statut}`"
    aria-live="polite"
  >
    <div class="state__main">
      <p class="state__label">
        État de l'offre
      </p>
      <p class="state__value">
        {{ LIBELLES_STATUT[state.statut].label }}
      </p>
      <p class="state__detail">
        <template v-if="state.statut === 'brouillon'">
          Pas encore soumise.
          <template v-if="bloquantsSoumission.length">
            {{ bloquantsSoumission.length }} information(s) requise(s) avant de pouvoir la soumettre.
          </template>
          <template v-else>
            Tout est prêt pour la soumettre.
          </template>
        </template>
        <template v-else-if="state.statut === 'a_valider' && etapeEnCours">
          En attente de <strong>{{ personne(etapeEnCours.personneId).nom }}</strong> ({{ etapeEnCours.libelle.toLowerCase() }}).
        </template>
        <template v-else-if="state.statut === 'a_corriger'">
          {{ state.remarques.filter(r => !r.resolue).length }} remarque(s) à traiter avant de renvoyer l'offre.
        </template>
        <template v-else-if="state.statut === 'validee'">
          Toutes les validations obligatoires sont obtenues. L'offre peut être publiée.
        </template>
        <template v-else>
          L'offre est en ligne.
        </template>
      </p>
    </div>
    <div class="state__actions">
      <CspButton
        v-if="modifiable"
        :label="state.statut === 'a_corriger' ? 'Renvoyer en validation' : 'Soumettre à validation'"
        icon="ri:send-plane-line"
        is-icon-left
        @click="onSoumettre"
      />
      <CspButton
        v-if="state.statut === 'a_valider'"
        label="Retirer de la validation"
        variant="secondary"
        @click="retirerDeValidation"
      />
      <CspButton
        v-if="state.statut === 'validee'"
        label="Configurer la diffusion"
        icon="ri:arrow-right-line"
        @click="aller('diffusion')"
      />
    </div>
  </section>

  <CspCallout
    v-if="echecSoumission && bloquantsSoumission.length"
    variant="error"
    title="L'offre ne peut pas encore être soumise"
  >
    <p class="err-intro">
      Complétez les informations suivantes :
    </p>
    <ul class="err-list">
      <li
        v-for="m in bloquantsSoumission"
        :key="m.libelle"
      >
        <button
          type="button"
          class="link"
          @click="aller(m.stepId)"
        >
          {{ m.libelle }}
        </button>
        <span class="muted"> — {{ stepLibelle(m.stepId) }}</span>
      </li>
    </ul>
  </CspCallout>

  <section
    class="block"
    aria-labelledby="circuit-title"
  >
    <div class="block__head">
      <h3
        id="circuit-title"
        class="block__title"
      >
        Circuit de validation
      </h3>
      <span class="muted">Paramétrage : {{ organisme }} (exemple)</span>
    </div>
    <ol class="circuit">
      <li
        v-for="(e, i) in circuit"
        :key="e.id"
        class="circuit__step"
        :class="`circuit__step--${STATUT_ETAPE[e.statut].cls}`"
      >
        <span
          class="circuit__marker"
          aria-hidden="true"
        >
          <CspIcon
            :name="STATUT_ETAPE[e.statut].icon"
            :size="18"
          />
        </span>
        <div class="circuit__body">
          <p class="circuit__name">
            {{ i + 1 }}. {{ e.libelle }}
            <span class="circuit__tag">{{ e.obligatoire ? 'obligatoire' : 'facultative' }}</span>
          </p>
          <p class="circuit__who">
            {{ personne(e.personneId).nom }} · {{ personne(e.personneId).role }}
          </p>
          <p class="circuit__status">
            {{ STATUT_ETAPE[e.statut].label }}<template v-if="e.date">
              · {{ e.date }}
            </template>
            <template v-if="e.externe">
              · obtenue avant la création de l'offre
            </template>
          </p>
          <SimulationNote
            v-if="etapeEnCours?.id === e.id && state.statut === 'a_valider'"
            :titre="`Simuler la réponse de ${personne(e.personneId).nom}`"
          >
            <CspButton
              label="Valider"
              size="sm"
              icon="ri:check-line"
              is-icon-left
              @click="valider"
            />
            <CspButton
              label="Demander des corrections"
              size="sm"
              variant="secondary"
              @click="reponseOuverte = !reponseOuverte"
            />
          </SimulationNote>
          <form
            v-if="reponseOuverte && etapeEnCours?.id === e.id && state.statut === 'a_valider'"
            class="correction"
            @submit.prevent="demanderCorrections"
          >
            <CspSelect
              v-model="etapeCorrection"
              label="Partie concernée"
              size="sm"
              :options="stepsOptions"
            />
            <CspTextarea
              v-model="texteCorrection"
              label="Remarque"
              :rows="2"
              :error="Boolean(erreurCorrection)"
              :error-message="erreurCorrection"
            />
            <div>
              <CspButton
                type="submit"
                label="Envoyer la demande de correction"
                size="sm"
              />
            </div>
          </form>
        </div>
        <CspButton
          v-if="!e.obligatoire && modifiable"
          icon="ri:close-line"
          variant="tertiary-no-outline"
          size="sm"
          :aria-label="`Retirer l'étape ${e.libelle}`"
          @click="state.circuit = state.circuit.filter(x => x.id !== e.id)"
        />
      </li>
    </ol>
    <div
      v-if="modifiable && ajoutables.length"
      class="inline-add"
    >
      <CspSelect
        v-model="etapeAAjouter"
        label="Ajouter une étape facultative"
        placeholder="Choisir…"
        size="sm"
        :options="ajoutables"
      />
      <CspButton
        label="Ajouter"
        variant="secondary"
        size="sm"
        :disabled="!etapeAAjouter"
        @click="ajouterEtape"
      />
    </div>
    <p class="muted">
      Hypothèse : les étapes obligatoires viennent du paramétrage de l'organisation ; la personne qui crée l'offre peut seulement ajouter des relectures facultatives. Une étape facultative ne bloque pas la publication.
    </p>
  </section>

  <section
    class="block"
    aria-labelledby="remarques-title"
  >
    <h3
      id="remarques-title"
      class="block__title"
    >
      Remarques et demandes de correction
    </h3>
    <p
      v-if="!remarques.length"
      class="muted"
    >
      Aucune remarque pour l'instant.
    </p>
    <ul
      v-else
      class="remarques"
    >
      <li
        v-for="r in remarques"
        :key="r.id"
        :class="{ remarques__done: r.resolue }"
      >
        <p class="remarques__meta">
          <strong>{{ personne(r.auteurId).nom }}</strong> · {{ r.date }} · {{ stepLibelle(r.stepId) }}
          <span class="remarques__status">{{ r.resolue ? 'Traitée' : 'À traiter' }}</span>
        </p>
        <p class="remarques__text">
          {{ r.texte }}
        </p>
        <div
          v-if="!r.resolue"
          class="remarques__actions"
        >
          <CspButton
            :label="`Aller à « ${stepLibelle(r.stepId)} »`"
            size="sm"
            variant="tertiary"
            @click="aller(r.stepId)"
          />
          <CspButton
            label="Marquer comme traitée"
            size="sm"
            variant="tertiary-no-outline"
            @click="r.resolue = true"
          />
        </div>
      </li>
    </ul>
  </section>

  <section
    class="block"
    aria-labelledby="contrib-title"
  >
    <h3
      id="contrib-title"
      class="block__title"
    >
      Contributions demandées
    </h3>
    <p
      v-if="!state.contributions.length"
      class="muted"
    >
      Aucune. Vous pouvez demander à un collègue de compléter une partie depuis l'étape « Fiche de poste ».
    </p>
    <ul
      v-else
      class="remarques"
    >
      <li
        v-for="c in state.contributions"
        :key="c.id"
        :class="{ remarques__done: c.statut === 'faite' }"
      >
        <p class="remarques__meta">
          <strong>{{ personne(c.personneId).nom }}</strong> · {{ stepLibelle(c.stepId) }}
          <span class="remarques__status">{{ c.statut === 'faite' ? 'Faite' : 'En attente' }}</span>
        </p>
        <p class="remarques__text">
          {{ c.demande }}
        </p>
        <SimulationNote v-if="c.statut === 'en_attente'">
          <CspButton
            :label="`Simuler la réponse de ${personne(c.personneId).nom.split(' ')[0]}`"
            size="sm"
            variant="tertiary"
            @click="simulerContribution(c.id)"
          />
        </SimulationNote>
      </li>
    </ul>
  </section>

  <section
    class="block"
    aria-labelledby="equipe-title"
  >
    <h3
      id="equipe-title"
      class="block__title"
    >
      Équipe de recrutement
    </h3>
    <p class="muted">
      Ces personnes auront accès aux candidatures une fois l'offre publiée.
    </p>
    <table class="team">
      <thead>
        <tr>
          <th scope="col">
            Personne
          </th>
          <th scope="col">
            Rôle dans ce recrutement
          </th>
          <th scope="col">
            <span class="sr-only">Actions</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="m in state.equipe"
          :key="m.personneId"
        >
          <td>
            {{ personne(m.personneId).nom }}<template v-if="m.personneId === 'camille'">
              (vous)
            </template>
            <small>{{ personne(m.personneId).role }}</small>
          </td>
          <td>
            <select
              v-model="m.acces"
              class="team__select"
              :aria-label="`Rôle de ${personne(m.personneId).nom}`"
              :disabled="m.personneId === 'camille'"
            >
              <option
                v-for="a in ACCES"
                :key="a.value"
                :value="a.value"
              >
                {{ a.label }}
              </option>
            </select>
          </td>
          <td class="team__act">
            <CspButton
              v-if="m.personneId !== 'camille'"
              icon="ri:user-unfollow-line"
              variant="tertiary-no-outline"
              size="sm"
              :aria-label="`Retirer ${personne(m.personneId).nom} de l'équipe`"
              @click="state.equipe = state.equipe.filter(x => x.personneId !== m.personneId)"
            />
          </td>
        </tr>
      </tbody>
    </table>
    <div
      v-if="ajoutablesEquipe.length"
      class="inline-add"
    >
      <CspSelect
        v-model="membreAAjouter"
        label="Ajouter un membre"
        placeholder="Choisir…"
        size="sm"
        :options="ajoutablesEquipe"
      />
      <CspButton
        label="Ajouter"
        variant="secondary"
        size="sm"
        :disabled="!membreAAjouter"
        @click="ajouterMembre"
      />
    </div>
  </section>

  <StepFooter id="validation" />
</template>

<style scoped lang="scss">
.state {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
  padding: var(--csp-space-4) var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  border-left: 4px solid var(--border-plain-info);
  background: var(--background-default-grey);

  &--a_valider {
    border-left-color: var(--border-plain-blue-france);
  }

  &--a_corriger {
    border-left-color: var(--border-plain-error);
  }

  &--validee,
  &--publiee {
    border-left-color: var(--border-plain-success);
  }
}

.state__label {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.state__value {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  font-weight: var(--csp-font-weight-bold);
}

.state__detail {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
}

.state__actions {
  display: flex;
  gap: var(--csp-space-2);
  flex-shrink: 0;
}

.err-intro {
  margin: 0 0 var(--csp-space-1);
}

.err-list {
  margin: 0;
  padding-left: var(--csp-space-5);
}

.link {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.muted {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.block {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4) var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.block__head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: var(--csp-space-3);
}

.block__title {
  margin: 0;
  font-size: var(--csp-font-size-md);
}

.circuit {
  margin: 0;
  padding: 0;
  list-style: none;
}

.circuit__step {
  position: relative;
  display: flex;
  gap: var(--csp-space-3);
  padding-bottom: var(--csp-space-4);

  &:not(:last-child)::before {
    content: '';
    position: absolute;
    left: 0.5rem;
    top: 1.5rem;
    bottom: 0;
    width: 2px;
    background: var(--border-default-grey);
  }
}

.circuit__marker {
  flex-shrink: 0;
  color: var(--text-mention-grey);

  .circuit__step--ok & {
    color: var(--text-default-success);
  }

  .circuit__step--wait & {
    color: var(--text-action-high-blue-france);
  }

  .circuit__step--ko & {
    color: var(--text-default-error);
  }
}

.circuit__body {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-1);

  p {
    margin: 0;
  }
}

.circuit__name {
  font-weight: var(--csp-font-weight-bold);
}

.circuit__tag {
  margin-left: var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}

.circuit__who,
.circuit__status {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.circuit__step--ko .circuit__status {
  color: var(--text-default-error);
}

.correction {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  width: 100%;
  margin-top: var(--csp-space-2);
  padding: var(--csp-space-3);
  border: 1px dashed var(--border-default-grey);
}

.inline-add {
  display: flex;
  align-items: flex-end;
  gap: var(--csp-space-2);
  max-width: 32rem;

  > :first-child {
    flex: 1;
  }
}

.remarques {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;

  li {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: var(--csp-space-1);
    padding: var(--csp-space-3) 0;
    border-top: 1px solid var(--border-default-grey);
  }

  p {
    margin: 0;
  }
}

.remarques__meta {
  font-size: var(--csp-font-size-sm);
}

.remarques__status {
  margin-left: var(--csp-space-2);
  padding: 0 var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  background: var(--background-contrast-warning);

  .remarques__done & {
    background: var(--background-contrast-success);
  }
}

.remarques__done .remarques__text {
  color: var(--text-mention-grey);
}

.remarques__actions {
  display: flex;
  gap: var(--csp-space-2);
}

.team {
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
    padding: var(--csp-space-2);
    border-bottom: 1px solid var(--border-default-grey);
  }

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.team__select {
  padding: var(--csp-space-1) var(--csp-space-2);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  font: inherit;
  color: var(--text-default-grey);
}

.team__act {
  width: 2.5rem;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
