<script setup lang="ts">
import type { StepId } from '../../data/types'
import { computed, nextTick, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import { nomOrganisme } from '../../data/redaction'
import { libelleMetier, personne, SECTIONS_OFFRE } from '../../data/referentiels'
import { useOffre } from '../../data/useOffre'
import OffrePreview from '../../shared/OffrePreview.vue'
import Panel from '../../shared/Panel.vue'
import { ETAPE_DE, useEtapes } from './useEtapes'

// Étape 4 — vérifier et finaliser. Tous les points à traiter sont regroupés ici, classés
// (bloquant / avant publication / suggestion) ; l'action proposée dépend de l'organisation et de l'état.
const emit = defineEmits<{ dupliquer: [] }>()

const {
  state,
  manques,
  alertes,
  circuit,
  validationRestante,
  etapeEnCours,
  peutPublier,
  verrouille,
  afficherErreurs,
  soumettre,
  publier,
  retirerDeValidation,
  enregistrer,
  notifier,
  canaux,
  dirty,
  saving,
} = useOffre()
const { aller } = useEtapes()

// --- Points à traiter, en trois niveaux ---
const avecValidation = computed(() => validationRestante.value.length > 0)
const ANCRES: Record<string, string> = {
  intitule: 'champ-intitule',
  service: 'champ-service',
  localisation: 'champ-localisation',
  categories: 'champ-categories',
  statuts: 'champ-statuts',
  contrat: 'champ-contrat',
  canaux: 'fin-canaux',
  dateLimite: 'fin-dates',
}
/** Sans validation, la diffusion bloque la publication au même titre que le reste : une seule liste. */
const bloquants = computed(() => manques.value.filter(m => m.stepId !== 'diffusion' || !avecValidation.value))
const avantPublication = computed(() => [
  ...manques.value.filter(m => m.stepId === 'diffusion' && avecValidation.value).map(m => ({ libelle: m.libelle, stepId: m.stepId as StepId, cle: m.cle })),
  ...state.remarques.filter(r => !r.resolue).map(r => ({ libelle: `Correction demandée par ${personne(r.auteurId).nom}`, stepId: r.stepId, cle: '' })),
])
/** Les remarques non traitées apparaissent déjà au-dessus : on ne les répète pas en suggestion. */
const suggestions = computed(() => alertes.value.filter(a => !a.libelle.startsWith('Remarque de')))

function corriger(stepId: StepId, cle: string) {
  if (cle.startsWith('offre.')) {
    aller('offre', `offre-${cle.slice(6)}`)
  }
  else if (ETAPE_DE[stepId] === 'finaliser') {
    document.getElementById(ANCRES[cle] ?? '')?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
  else {
    aller(stepId, ANCRES[cle])
  }
}

// --- Synthèse ---
const b = state.besoin
const sectionsRedigees = computed(() => SECTIONS_OFFRE.filter(s => state.offre[s.id].texte.trim()).length)
const apercu = ref(false)

// --- Diffusion ---
const lignes = computed(() => canaux.map(c => ({ ...c, etat: state.canaux.find(x => x.id === c.id)! })))
const ISO = /^\d{4}-\d{2}-\d{2}$/
const erreurLimite = computed(() => {
  if (state.dateLimite && !ISO.test(state.dateLimite)) {
    return 'Format attendu : AAAA-MM-JJ'
  }
  if (state.dateLimite && state.dateDebutDiffusion && state.dateLimite <= state.dateDebutDiffusion) {
    return 'La date limite doit suivre le début de diffusion.'
  }
  return undefined
})

// --- Action principale selon l'état ---
const action = computed<'soumettre' | 'publier' | 'attente' | 'aucune'>(() => {
  if (state.statut === 'a_valider') {
    return 'attente'
  }
  if (state.statut === 'publiee') {
    return 'aucune'
  }
  if ((state.statut === 'brouillon' || state.statut === 'a_corriger') && avecValidation.value) {
    return 'soumettre'
  }
  return 'publier'
})

const pointsRef = ref<HTMLElement>()
function montrerPoints(message: string) {
  afficherErreurs.value = true
  notifier(message, 'info')
  nextTick(() => pointsRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
}

function agir() {
  if (action.value === 'soumettre') {
    if (!soumettre()) {
      montrerPoints(`${bloquants.value.length} information(s) à compléter avant de soumettre.`)
    }
  }
  else if (action.value === 'publier') {
    if (!peutPublier.value) {
      montrerPoints('Quelques informations manquent encore pour publier.')
      return
    }
    publier()
    notifier('Offre publiée. Le suivi des candidatures est ouvert.')
  }
}

const libelleAction = computed(() => {
  if (action.value === 'soumettre') {
    return state.statut === 'a_corriger' ? 'Renvoyer en validation' : 'Soumettre à validation'
  }
  return 'Publier l\'offre'
})

const circuitTexte = computed(() => {
  const etapes = circuit.value.filter(e => e.statut !== 'approuve')
  return etapes.map(e => `${personne(e.personneId).nom} (${personne(e.personneId).role.split(' — ')[0]!.toLowerCase()})`).join(', puis ')
})

async function sauver() {
  await enregistrer()
  notifier('Brouillon enregistré.')
}

// --- Après publication ---
const choisis = computed(() => lignes.value.filter(l => l.etat.selectionne))
function basculer(id: string, action: string) {
  const c = state.canaux.find(x => x.id === id)!
  c.fait = c.fait.includes(action) ? c.fait.filter(a => a !== action) : [...c.fait, action]
}
</script>

<template>
  <!-- ===== Publiée ===== -->
  <template v-if="state.statut === 'publiee'">
    <Panel>
      <div class="pub">
        <CspIcon
          name="ri:checkbox-circle-fill"
          :size="28"
          class="pub__icon"
        />
        <div>
          <h2 class="pub__title">
            Offre publiée
          </h2>
          <p class="muted">
            Candidatures ouvertes jusqu'au {{ state.dateLimite }}.
          </p>
        </div>
      </div>
    </Panel>
    <Panel
      v-if="choisis.some(c => c.actionsManuelles.length)"
      titre="Diffusion à terminer"
    >
      <ul class="todo">
        <template
          v-for="c in choisis"
          :key="c.id"
        >
          <li
            v-for="a in c.actionsManuelles"
            :key="a"
          >
            <label>
              <input
                type="checkbox"
                :checked="c.etat.fait.includes(a)"
                @change="basculer(c.id, a)"
              >
              <span :class="{ done: c.etat.fait.includes(a) }"><strong>{{ c.nom }}</strong> — {{ a }}</span>
            </label>
          </li>
        </template>
      </ul>
    </Panel>
    <Panel
      titre="Prêt pour la suite"
      description="Ce qui a été défini ici est repris dans le suivi des candidatures."
    >
      <ul class="cont">
        <li>Profils acceptés et critères de sélection affichés sur chaque candidature</li>
        <li v-if="state.conditions.questions.length">
          {{ state.conditions.questions.length }} question(s) de présélection posée(s) aux candidats
        </li>
        <li>{{ state.evaluation.criteres.length ? `Grille d'évaluation de ${state.evaluation.criteres.length} critère(s)` : 'Grille d\'évaluation à préparer au moment du tri' }}</li>
        <li>Équipe : {{ state.equipe.map(m => personne(m.personneId).nom).join(', ') }}</li>
      </ul>
      <div>
        <CspButton
          label="Dupliquer cette offre"
          variant="secondary"
          icon="ri:file-copy-2-line"
          is-icon-left
          @click="emit('dupliquer')"
        />
      </div>
    </Panel>
  </template>

  <!-- ===== Vérifier et finaliser ===== -->
  <template v-else>
    <header>
      <h2 class="title">
        Vérifier et finaliser
      </h2>
    </header>

    <section
      ref="pointsRef"
      class="points"
      aria-labelledby="points-title"
    >
      <h3
        id="points-title"
        class="sr-only"
      >
        Points à traiter
      </h3>
      <p
        v-if="!bloquants.length && !avantPublication.length"
        class="points__ok"
      >
        <CspIcon
          name="ri:checkbox-circle-line"
          :size="16"
        />
        Toutes les informations nécessaires sont renseignées.
      </p>
      <div
        v-if="bloquants.length"
        class="group"
        :class="{ 'group--alert': afficherErreurs }"
      >
        <p class="group__title">
          À compléter pour {{ avecValidation ? 'soumettre' : 'publier' }}
        </p>
        <ul>
          <li
            v-for="m in bloquants"
            :key="m.cle"
          >
            <span>{{ m.libelle }}</span>
            <button
              type="button"
              class="link"
              @click="corriger(m.stepId, m.cle)"
            >
              Compléter
            </button>
          </li>
        </ul>
      </div>
      <div
        v-if="avantPublication.length"
        class="group"
      >
        <p class="group__title">
          À compléter avant publication (peut attendre la validation)
        </p>
        <ul>
          <li
            v-for="m in avantPublication"
            :key="m.libelle"
          >
            <span>{{ m.libelle }}</span>
            <button
              type="button"
              class="link"
              @click="corriger(m.stepId, m.cle)"
            >
              Voir
            </button>
          </li>
        </ul>
      </div>
      <details
        v-if="suggestions.length"
        class="group group--sugg"
      >
        <summary class="group__title">
          {{ suggestions.length }} suggestion(s) pour améliorer l'offre
        </summary>
        <ul>
          <li
            v-for="a in suggestions"
            :key="a.libelle"
          >
            <span>{{ a.libelle }}</span>
            <button
              type="button"
              class="link"
              @click="aller(a.stepId)"
            >
              Voir
            </button>
          </li>
        </ul>
      </details>
    </section>

    <Panel titre="Synthèse">
      <dl class="syn">
        <div class="syn__row">
          <dt>Poste</dt>
          <dd>
            <strong>{{ b.intitule || 'Intitulé à renseigner' }}</strong>
            <span>{{ [nomOrganisme(state), b.service, b.localisation].filter(Boolean).join(' · ') }}</span>
            <span>{{ [b.categories.length ? `Catégorie ${b.categories.join(', ')}` : '', libelleMetier(b.metier), b.darRef].filter(Boolean).join(' · ') }}</span>
          </dd>
          <button
            type="button"
            class="link"
            @click="aller('poste')"
          >
            Modifier
          </button>
        </div>
        <div class="syn__row">
          <dt>Offre</dt>
          <dd>
            <span>{{ sectionsRedigees }} section(s) rédigée(s) sur {{ SECTIONS_OFFRE.length }}</span>
            <button
              type="button"
              class="link link--inline"
              :aria-expanded="apercu"
              @click="apercu = !apercu"
            >
              {{ apercu ? 'Masquer l\'aperçu' : 'Voir l\'aperçu candidat' }}
            </button>
          </dd>
          <button
            type="button"
            class="link"
            @click="aller('offre')"
          >
            Modifier
          </button>
        </div>
        <OffrePreview v-if="apercu" />
        <div class="syn__row">
          <dt>Candidatures</dt>
          <dd>
            <span>{{ state.conditions.profils.length }} profil(s) accepté(s) · {{ state.conditions.indispensables.length }} critère(s) indispensable(s) · {{ state.conditions.souhaites.length }} souhaité(s)</span>
            <span v-if="state.conditions.questions.length || state.evaluation.criteres.length">
              {{ [state.conditions.questions.length && `${state.conditions.questions.length} question(s) de présélection`, state.evaluation.criteres.length && 'grille d\'évaluation préparée'].filter(Boolean).join(' · ') }}
            </span>
          </dd>
          <button
            type="button"
            class="link"
            @click="aller('candidature')"
          >
            Modifier
          </button>
        </div>
      </dl>
    </Panel>

    <Panel
      titre="Diffusion"
      description="Le même texte est utilisé partout ; seule la mise en forme change selon le canal."
    >
      <fieldset
        id="fin-canaux"
        class="canaux"
        :disabled="state.statut === 'a_valider'"
      >
        <legend class="sr-only">
          Canaux de diffusion
        </legend>
        <label
          v-for="l in lignes"
          :key="l.id"
          class="canal"
        >
          <input
            v-model="l.etat.selectionne"
            type="checkbox"
          >
          <span>
            {{ l.nom }}
            <small v-if="l.etat.selectionne && l.mode === 'connecteur'">Transmission automatique (hypothèse){{ l.attendus.some(a => !a.ok(state)) ? ` · manque : ${l.attendus.filter(a => !a.ok(state)).map(a => a.libelle.toLowerCase()).join(', ')}` : '' }}</small>
            <small v-else-if="l.etat.selectionne && l.actionsManuelles.length">Ensuite : {{ l.actionsManuelles.join(', ').toLowerCase() }}</small>
          </span>
        </label>
      </fieldset>
      <div
        id="fin-dates"
        class="dates"
      >
        <CspInput
          v-model="state.dateDebutDiffusion"
          label="Début de diffusion (facultatif)"
          placeholder="AAAA-MM-JJ"
          hint="Vide : dès la publication"
          :disabled="state.statut === 'a_valider'"
        />
        <CspInput
          v-model="state.dateLimite"
          label="Date limite de candidature"
          placeholder="AAAA-MM-JJ"
          :disabled="state.statut === 'a_valider'"
          :error="Boolean(erreurLimite) || (afficherErreurs && !state.dateLimite && action === 'publier')"
          :error-message="erreurLimite ?? (afficherErreurs && !state.dateLimite && action === 'publier' ? 'Indiquez la date limite pour publier.' : undefined)"
        />
      </div>
    </Panel>

    <div class="final">
      <p class="final__info">
        <template v-if="action === 'attente'">
          <CspIcon
            name="ri:time-line"
            :size="16"
          />
          En validation<template v-if="etapeEnCours">
            auprès de {{ personne(etapeEnCours.personneId).nom }}
          </template>. Vous recevrez une notification de la décision.
        </template>
        <template v-else-if="action === 'soumettre'">
          <CspIcon
            name="ri:route-line"
            :size="16"
          />
          Validation prévue par votre organisation : {{ circuitTexte }}.
        </template>
        <template v-else-if="!circuit.length">
          <CspIcon
            name="ri:information-line"
            :size="16"
          />
          Pas de validation prévue pour ce recrutement : vous pouvez publier directement.
        </template>
        <template v-else>
          <CspIcon
            name="ri:checkbox-circle-line"
            :size="16"
          />
          Validation obtenue.
        </template>
      </p>
      <div class="final__actions">
        <CspButton
          v-if="!verrouille"
          label="Enregistrer le brouillon"
          variant="tertiary-no-outline"
          :disabled="saving || !dirty"
          @click="sauver"
        />
        <CspButton
          v-if="action === 'attente'"
          label="Retirer de la validation"
          variant="secondary"
          @click="retirerDeValidation"
        />
        <CspButton
          v-else-if="action !== 'aucune'"
          :label="libelleAction"
          :icon="action === 'publier' ? 'ri:send-plane-line' : 'ri:arrow-right-line'"
          @click="agir"
        />
      </div>
    </div>
  </template>
</template>

<style scoped lang="scss">
.title,
.pub__title {
  margin: 0;
  font-size: var(--csp-font-size-2xl);
}

.muted {
  margin: 0;
  color: var(--text-mention-grey);
}

.points {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  scroll-margin-top: var(--csp-space-4);
}

.points__ok {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  color: var(--text-default-success);
  font-size: var(--csp-font-size-sm);
}

.group {
  padding: var(--csp-space-3) var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);

  &--alert {
    border-left-color: var(--border-plain-error);
  }

  &--sugg {
    border-left-color: var(--border-default-grey);
  }

  ul {
    display: flex;
    flex-direction: column;
    gap: var(--csp-space-1);
    margin: var(--csp-space-2) 0 0;
    padding: 0;
    list-style: none;
  }

  li {
    display: flex;
    justify-content: space-between;
    gap: var(--csp-space-3);
  }
}

.group__title {
  margin: 0;
  font-weight: var(--csp-font-weight-bold);
}

summary.group__title {
  cursor: pointer;
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}

.syn {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  margin: 0;
}

.syn__row {
  display: grid;
  grid-template-columns: 8rem 1fr auto;
  gap: var(--csp-space-3);
  font-size: var(--csp-font-size-sm);

  dt {
    color: var(--text-mention-grey);
  }

  dd {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 2px;
    margin: 0;
  }

  & + & {
    padding-top: var(--csp-space-4);
    border-top: 1px solid var(--border-default-grey);
  }
}

.canaux {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  border: 0;
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

.dates {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--csp-space-4);
  max-width: 36rem;
  scroll-margin-top: var(--csp-space-6);
}

.final {
  position: sticky;
  bottom: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
  padding: var(--csp-space-3) var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  box-shadow: var(--csp-shadow-md);
}

.final__info {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.final__actions {
  display: flex;
  gap: var(--csp-space-2);
  flex-shrink: 0;
}

.link {
  flex-shrink: 0;
  align-self: flex-start;
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}

.pub {
  display: flex;
  gap: var(--csp-space-3);
  align-items: flex-start;
}

.pub__icon {
  color: var(--text-default-success);
}

.todo,
.cont {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  label {
    display: flex;
    gap: var(--csp-space-2);
    cursor: pointer;
  }

  input {
    accent-color: var(--background-action-high-blue-france);
  }
}

.cont {
  list-style: disc;
  padding-left: var(--csp-space-5);
}

.done {
  text-decoration: line-through;
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
