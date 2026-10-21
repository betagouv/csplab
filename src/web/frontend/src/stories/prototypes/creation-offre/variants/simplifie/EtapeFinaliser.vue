<script setup lang="ts">
import type { StepId } from '../../data/types'
import { computed, nextTick, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import { quand } from '../../data/processus'
import { nomOrganisme } from '../../data/redaction'
import { personne, SECTIONS_OFFRE } from '../../data/referentiels'
import { useOffre } from '../../data/useOffre'
import OffrePreview from '../../shared/OffrePreview.vue'
import Panel from '../../shared/Panel.vue'
import { useEtapes } from './useEtapes'

// Étape 4 — vérifier et créer. Créer l'offre et activer sa publication sont deux actions distinctes :
// on peut créer l'offre sans la rendre visible. L'action proposée dépend de l'état de la DAR et de l'organisation.
const emit = defineEmits<{ dupliquer: [] }>()

const {
  state,
  manques,
  alertes,
  validationRestante,
  etapeEnCours,
  afficherErreurs,
  soumettre,
  retirerDeValidation,
  enregistrer,
  notifier,
  canaux,
  dirty,
  saving,
  soumettreDar,
  bloquantsCreation,
  creer,
  manquesPublication,
  activerPublication,
} = useOffre()
const { aller } = useEtapes()
const b = state.besoin

// --- Action principale ---
type Action = 'soumettreDar' | 'attenteDar' | 'soumettre' | 'attente' | 'creer' | 'creee'
const action = computed<Action>(() => {
  if (state.statut === 'creee' || state.statut === 'publiee') {
    return 'creee'
  }
  if (state.statut === 'a_valider') {
    return 'attente'
  }
  if (b.darApplicable === 'oui' && b.darRef && (b.darStatut === 'a_demander' || b.darStatut === '')) {
    return 'soumettreDar'
  }
  if (b.darApplicable === 'oui' && b.darStatut === 'en_cours') {
    return 'attenteDar'
  }
  // Organisation qui fait aussi valider l'offre (paramétrage) : soumission avant création.
  if (state.circuit.some(e => e.obligatoire && e.statut !== 'approuve') && state.statut !== 'validee') {
    return 'soumettre'
  }
  return 'creer'
})

// --- Points à traiter, en trois niveaux ---
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
const bloquants = computed(() => (action.value === 'soumettreDar'
  ? manques.value.filter(m => m.stepId === 'besoin' || m.stepId === 'poste')
  : bloquantsCreation.value))
const avantPublication = computed(() => [
  ...manquesPublication.value.map(m => ({ libelle: m.libelle, stepId: m.stepId as StepId, cle: m.cle })),
  ...state.remarques.filter(r => !r.resolue).map(r => ({ libelle: `Correction demandée par ${personne(r.auteurId).nom}`, stepId: r.stepId, cle: '' })),
])
const suggestions = computed(() => alertes.value.filter(a => !a.libelle.startsWith('Remarque de')))

function corriger(stepId: StepId, cle: string) {
  if (cle.startsWith('offre.')) {
    aller('offre', `offre-${cle.slice(6)}`)
  }
  else {
    aller(stepId, ANCRES[cle])
  }
}

const pointsRef = ref<HTMLElement>()
function montrerPoints(message: string) {
  afficherErreurs.value = true
  notifier(message, 'info')
  nextTick(() => pointsRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
}

function agir() {
  if (action.value === 'soumettreDar') {
    if (!soumettreDar()) {
      montrerPoints('Quelques informations manquent à la DAR.')
    }
  }
  else if (action.value === 'soumettre') {
    if (!soumettre()) {
      montrerPoints(`${bloquants.value.length} information(s) à compléter avant de soumettre.`)
    }
  }
  else if (action.value === 'creer') {
    if (creer()) {
      notifier('Offre créée. Elle n\'est pas encore visible des candidats.')
      nextTick(() => document.querySelector('.cs-main')?.scrollTo({ top: 0 }))
    }
    else {
      montrerPoints(`${bloquants.value.length} information(s) à compléter avant de créer l'offre.`)
    }
  }
}

const libelleAction = computed(() => ({
  soumettreDar: 'Soumettre la DAR à validation',
  soumettre: state.statut === 'a_corriger' ? 'Renvoyer en validation' : 'Soumettre l\'offre à validation',
  creer: 'Créer l\'offre',
}[action.value as 'soumettreDar' | 'soumettre' | 'creer']))

const circuitTexte = computed(() => validationRestante.value
  .map(e => `${personne(e.personneId).nom} (${personne(e.personneId).role.split(' — ')[0]!.toLowerCase()})`)
  .join(', puis '))

function attenteTexte(debut: string) {
  return `${debut}${etapeEnCours.value ? ` auprès de ${personne(etapeEnCours.value.personneId).nom}` : ''}.`
}

async function sauver() {
  await enregistrer()
  notifier('Brouillon enregistré.')
}

// --- Synthèse ---
const sectionsRedigees = computed(() => SECTIONS_OFFRE.filter(s => state.offre[s.id].texte.trim()).length)
const sectionsReprises = computed(() => SECTIONS_OFFRE.filter(s => state.offre[s.id].etat === 'reprise').length)
const apercu = ref(false)
const lignesCanaux = computed(() => canaux.map(c => ({ ...c, etat: state.canaux.find(x => x.id === c.id)! })))
const choisis = computed(() => lignesCanaux.value.filter(l => l.etat.selectionne))
const etatDar = computed(() => {
  if (b.darApplicable !== 'oui' || !b.darRef) {
    return ''
  }
  if (b.darStatut === 'validee') {
    return `validée${state.darContenu ? ` ${quand(state.darContenu.date)}` : ''} — inchangée`
  }
  return b.darStatut === 'en_cours' ? 'soumise, en attente de validation' : 'brouillon'
})

// --- Publication (après création) ---
const refusPublication = ref(false)
const publication = computed({
  get: () => state.statut === 'publiee',
  set: (v: boolean) => {
    refusPublication.value = !activerPublication(v)
    if (!refusPublication.value) {
      notifier(v ? 'Publication activée (simulation : rien n\'est envoyé).' : 'Publication désactivée : l\'offre n\'est plus visible.', v ? 'success' : 'info')
    }
  },
})
function basculerFait(id: string, a: string) {
  const c = state.canaux.find(x => x.id === id)!
  c.fait = c.fait.includes(a) ? c.fait.filter(x => x !== a) : [...c.fait, a]
}
const FREQUENCES = [
  { value: 'chaque', label: 'À chaque candidature' },
  { value: 'cinq', label: 'Toutes les 5 candidatures' },
  { value: 'quotidien', label: 'Un récapitulatif par jour' },
  { value: 'aucune', label: 'Jamais' },
]
</script>

<template>
  <!-- ===== Offre créée : publication à activer ou non ===== -->
  <template v-if="action === 'creee'">
    <Panel>
      <div class="done">
        <CspIcon
          name="ri:checkbox-circle-fill"
          :size="28"
          class="done__icon"
        />
        <div>
          <h2 class="done__title">
            Offre créée
          </h2>
          <p class="muted">
            {{ state.reference.replace('REC-', 'OFF-') }} · {{ state.titreAnnonce || b.intitule }} · {{ b.nbPostes }} poste(s) à pourvoir.
            <template v-if="etatDar">
              DAR {{ b.darRef }} {{ etatDar }}.
            </template>
          </p>
        </div>
      </div>
    </Panel>

    <Panel titre="Publication">
      <CspSwitch
        v-model="publication"
        :label="publication ? 'Publication activée' : 'Publication désactivée'"
      />
      <p class="muted">
        <template v-if="publication">
          Visible sur {{ choisis.map(c => c.nom).join(', ') }} jusqu'au {{ state.dateLimite }}. Simulation : aucune donnée n'est envoyée.
        </template>
        <template v-else>
          L'offre n'est pas visible des candidats. Vous pouvez l'activer maintenant, ou plus tard en rouvrant l'offre depuis la liste.
        </template>
      </p>
      <div
        v-if="refusPublication && manquesPublication.length"
        class="refus"
        role="alert"
      >
        Pour activer la publication, complétez :
        <ul>
          <li
            v-for="m in manquesPublication"
            :key="m.cle"
          >
            {{ m.libelle }}
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
      <ul
        v-if="publication && choisis.some(c => c.actionsManuelles.length)"
        class="todo"
      >
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
                @change="basculerFait(c.id, a)"
              >
              <span :class="{ done__strike: c.etat.fait.includes(a) }"><strong>{{ c.nom }}</strong> — {{ a }}</span>
            </label>
          </li>
        </template>
      </ul>
    </Panel>

    <Panel titre="Suivi des candidatures">
      <CspRadioGroup
        v-model="state.notifications"
        label="Me prévenir par courriel des nouvelles candidatures"
        :options="FREQUENCES"
        size="sm"
      />
      <p class="muted small">
        Modifiable à tout moment depuis « Suivi ». Prototype : aucun courriel envoyé.
      </p>
      <div>
        <CspButton
          label="Nouveau recrutement sur cette fiche"
          variant="secondary"
          size="sm"
          icon="ri:file-copy-2-line"
          is-icon-left
          @click="emit('dupliquer')"
        />
      </div>
    </Panel>
  </template>

  <!-- ===== Avant création ===== -->
  <template v-else>
    <header>
      <h2 class="title">
        Vérifier et créer
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
          {{ action === 'soumettreDar' ? 'À compléter pour soumettre la DAR' : action === 'soumettre' ? 'À compléter pour soumettre' : 'À compléter pour créer l\'offre' }}
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
        class="group group--soft"
      >
        <p class="group__title">
          Pourra être complété plus tard, avant d'activer la publication
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
  </template>

  <Panel titre="Synthèse">
    <dl class="syn">
      <div
        v-if="etatDar"
        class="syn__row"
      >
        <dt>DAR</dt>
        <dd>
          <strong>{{ b.darRef }}</strong>
          <span>{{ etatDar }}</span>
        </dd>
        <button
          type="button"
          class="link"
          @click="aller('poste')"
        >
          Consulter
        </button>
      </div>
      <div class="syn__row">
        <dt>Annonce</dt>
        <dd>
          <strong>{{ state.titreAnnonce || b.intitule || 'Titre à renseigner' }}</strong>
          <span>{{ [nomOrganisme(state), b.localisation].filter(Boolean).join(' · ') }}</span>
          <span>{{ sectionsRedigees }} section(s) rédigée(s) sur {{ SECTIONS_OFFRE.length }}<template v-if="sectionsReprises"> · {{ sectionsReprises }} encore reprise(s) telle(s) quelle(s)</template></span>
          <button
            type="button"
            class="link link--inline"
            :aria-expanded="apercu"
            @click="apercu = !apercu"
          >
            {{ apercu ? 'Masquer l\'aperçu candidat' : 'Voir l\'aperçu candidat' }}
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
        <dt>Offre</dt>
        <dd>
          <span>{{ Number(b.nbPostes) > 1 ? `${b.nbPostes} postes à pourvoir, une seule offre` : '1 poste à pourvoir' }}<template v-if="b.codesPostes.length"> · {{ b.codesPostes.join(', ') }}</template></span>
          <span>{{ state.dateLimite ? `Candidatures jusqu'au ${state.dateLimite}` : 'Date limite à définir' }} · {{ choisis.map(c => c.nom).join(', ') || 'aucun canal' }}</span>
          <span>{{ state.conditions.profils.length }} profil(s) accepté(s) · {{ state.conditions.indispensables.length + state.conditions.souhaites.length }} critère(s)</span>
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

  <div
    v-if="action !== 'creee'"
    class="final"
  >
    <p class="final__info">
      <template v-if="action === 'attente'">
        <CspIcon
          name="ri:time-line"
          :size="16"
        />
        {{ attenteTexte('Offre en validation') }}
      </template>
      <template v-else-if="action === 'attenteDar'">
        <CspIcon
          name="ri:time-line"
          :size="16"
        />
        {{ attenteTexte('DAR en attente de validation') }} L'offre pourra être créée ensuite ; votre travail est enregistré.
      </template>
      <template v-else-if="action === 'soumettreDar'">
        <CspIcon
          name="ri:information-line"
          :size="16"
        />
        La DAR doit être validée avant de créer l'offre. Vous pouvez continuer à rédiger l'offre en attendant.
      </template>
      <template v-else-if="action === 'soumettre'">
        <CspIcon
          name="ri:route-line"
          :size="16"
        />
        Votre organisation fait valider l'offre : {{ circuitTexte }}.
      </template>
      <template v-else>
        <CspIcon
          name="ri:information-line"
          :size="16"
        />
        L'offre sera créée sans être publiée. Vous activerez la publication quand vous le souhaitez.
      </template>
    </p>
    <div class="final__actions">
      <CspButton
        v-if="state.statut === 'brouillon' || state.statut === 'a_corriger'"
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
        v-else-if="action === 'soumettreDar' || action === 'soumettre' || action === 'creer'"
        :label="libelleAction"
        :icon="action === 'creer' ? 'ri:check-line' : 'ri:send-plane-line'"
        @click="agir"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">
.title,
.done__title {
  margin: 0;
  font-size: var(--csp-font-size-2xl);
}

.muted {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.small {
  font-size: var(--csp-font-size-xs);
}

.done {
  display: flex;
  gap: var(--csp-space-3);
  align-items: flex-start;
}

.done__icon {
  color: var(--text-default-success);
}

.done__strike {
  text-decoration: line-through;
  color: var(--text-mention-grey);
}

.refus {
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-error);
  background: var(--background-default-grey);
  font-size: var(--csp-font-size-sm);

  ul {
    margin: var(--csp-space-1) 0 0;
    padding-left: var(--csp-space-5);
  }
}

.todo {
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

  &--soft,
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

.group--soft .group__title,
summary.group__title {
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}

summary.group__title {
  cursor: pointer;
}

.syn {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  margin: 0;
}

.syn__row {
  display: grid;
  grid-template-columns: 7rem 1fr auto;
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

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
