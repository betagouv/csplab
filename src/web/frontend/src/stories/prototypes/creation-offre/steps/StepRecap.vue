<script setup lang="ts">
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { CATEGORIES, libelleMetier, MOTIFS, ORGANISMES, personne, STATUTS } from '../data/referentiels'
import { LIBELLES_STATUT, STEPS, useOffre } from '../data/useOffre'
import OffrePreview from '../shared/OffrePreview.vue'

// Écran 9 — récapitulatif et actions finales, cohérentes avec l'état courant.
const emit = defineEmits<{ dupliquer: [] }>()

const {
  state,
  manques,
  alertes,
  circuit,
  validationRestante,
  bloquantsSoumission,
  peutPublier,
  statutStep,
  manquesDe,
  soumettre,
  publier,
  enregistrer,
  notifier,
  aller,
  canaux,
  dirty,
  saving,
  afficherErreurs,
} = useOffre()

const b = state.besoin
const infos = computed(() => [
  { k: 'Intitulé', v: b.intitule },
  { k: 'Organisme', v: ORGANISMES.find(o => o.value === b.organisme)?.label },
  { k: 'Service', v: b.service },
  { k: 'Motif', v: MOTIFS.find(m => m.value === b.motif)?.label },
  { k: 'Localisation', v: b.localisation },
  { k: 'Métier', v: libelleMetier(b.metier) || b.metierHorsReferentiel },
  { k: 'Catégorie(s)', v: b.categories.map(c => CATEGORIES.find(x => x.value === c)?.label).join(', ') },
  { k: 'Statuts', v: b.statuts.map(s => STATUTS.find(x => x.value === s)?.label).join(', ') },
  { k: 'DAR', v: b.darApplicable === 'oui' ? `${b.darRef || 'référence manquante'} (${{ 'validee': 'validée', 'en_cours': 'en cours', 'a_demander': 'à demander', '': 'état inconnu' }[b.darStatut]})` : b.darApplicable === 'non' ? 'Non requise' : 'À préciser' },
  { k: 'Date limite', v: state.dateLimite },
])

const LIBELLES_STEP = {
  complet: 'Complet',
  incomplet: 'À compléter',
  facultatif: 'Facultatif — non renseigné',
  a_faire: 'À faire',
  en_cours: 'En cours',
}

const canauxChoisis = computed(() => canaux.filter(c => state.canaux.find(x => x.id === c.id)?.selectionne))

const raisonPublication = computed(() => {
  if (state.statut === 'publiee') {
    return ''
  }
  if (bloquantsSoumission.value.length) {
    return 'Des informations requises manquent encore.'
  }
  if (validationRestante.value.length) {
    const e = validationRestante.value[0]!
    return state.statut === 'brouillon' || state.statut === 'a_corriger'
      ? `L'offre doit d'abord être validée (${validationRestante.value.length} validation(s) obligatoire(s)).`
      : `En attente de validation : ${e.libelle.toLowerCase()} — ${personne(e.personneId).nom}.`
  }
  if (manques.value.length) {
    return 'La diffusion n\'est pas complète (canal ou date limite).'
  }
  return ''
})

const confirmation = ref(false)
const echec = ref(false)

function onSoumettre() {
  echec.value = !soumettre()
}

function onPublier() {
  if (!peutPublier.value) {
    afficherErreurs.value = true
    echec.value = true
    return
  }
  confirmation.value = true
}

function confirmerPublication() {
  publier()
  confirmation.value = false
  notifier('Offre publiée. Le suivi des candidatures est ouvert.')
}

async function sauver() {
  await enregistrer()
  notifier('Brouillon enregistré.')
}

// --- Après publication ---
const actionsManuelles = computed(() => canauxChoisis.value.flatMap(c => c.actionsManuelles.map(a => ({ canalId: c.id, canal: c.nom, action: a }))))
function estFait(canalId: string, action: string) {
  return state.canaux.find(x => x.id === canalId)!.fait.includes(action)
}
function basculer(canalId: string, action: string) {
  const c = state.canaux.find(x => x.id === canalId)!
  c.fait = c.fait.includes(action) ? c.fait.filter(a => a !== action) : [...c.fait, action]
}
</script>

<template>
  <!-- ===== Offre publiée ===== -->
  <template v-if="state.statut === 'publiee'">
    <header class="pub">
      <CspIcon
        name="ri:checkbox-circle-fill"
        :size="32"
        class="pub__icon"
      />
      <div>
        <h2 class="pub__title">
          Offre publiée
        </h2>
        <p class="pub__desc">
          {{ state.reference }} — {{ b.intitule }}. Les candidatures peuvent être reçues jusqu'au {{ state.dateLimite }}.
        </p>
      </div>
    </header>

    <section class="block">
      <h3 class="block__title">
        Diffusion — actions restant à faire
      </h3>
      <ul class="todo">
        <li
          v-for="c in canauxChoisis.filter(x => x.mode === 'connecteur')"
          :key="c.id"
        >
          <CspIcon
            name="ri:send-plane-line"
            :size="16"
          />
          <span><strong>{{ c.nom }}</strong> — transmis automatiquement (simulation : aucun envoi réel)</span>
        </li>
        <li
          v-for="a in actionsManuelles"
          :key="a.action"
        >
          <label class="todo__check">
            <input
              type="checkbox"
              :checked="estFait(a.canalId, a.action)"
              @change="basculer(a.canalId, a.action)"
            >
            <span :class="{ todo__done: estFait(a.canalId, a.action) }"><strong>{{ a.canal }}</strong> — {{ a.action }}</span>
          </label>
        </li>
      </ul>
    </section>

    <section class="block">
      <h3 class="block__title">
        La suite du recrutement est prête
      </h3>
      <p class="muted">
        Ce qui a été défini à la création est repris dans le suivi des candidatures :
      </p>
      <ul class="continuity">
        <li>
          <CspIcon
            name="ri:shield-user-line"
            :size="16"
          />
          <span><strong>Éligibilité</strong> — {{ state.conditions.profils.length }} profil(s) autorisé(s), affichés sur chaque candidature</span>
        </li>
        <li>
          <CspIcon
            name="ri:question-answer-line"
            :size="16"
          />
          <span><strong>Questions de présélection</strong> — {{ state.conditions.questions.length }} question(s) posée(s) aux candidats</span>
        </li>
        <li>
          <CspIcon
            name="ri:list-check-3"
            :size="16"
          />
          <span><strong>Grille d'évaluation</strong> — {{ state.evaluation.active ? `${state.evaluation.criteres.length} critère(s), ${state.evaluation.premierTri.length} point(s) de premier tri` : 'à définir au moment du tri' }}</span>
        </li>
        <li>
          <CspIcon
            name="ri:team-line"
            :size="16"
          />
          <span><strong>Équipe</strong> — {{ state.equipe.map(m => personne(m.personneId).nom).join(', ') }}</span>
        </li>
        <li>
          <CspIcon
            name="ri:bar-chart-2-line"
            :size="16"
          />
          <span><strong>Pilotage</strong> — motif, catégorie, métier et canaux alimentent les indicateurs de recrutement</span>
        </li>
      </ul>
      <div class="actions">
        <CspButton
          label="Dupliquer cette offre"
          variant="secondary"
          icon="ri:file-copy-2-line"
          is-icon-left
          @click="emit('dupliquer')"
        />
      </div>
    </section>
  </template>

  <!-- ===== Récapitulatif avant soumission / publication ===== -->
  <template v-else>
    <header class="head">
      <h2 class="head__title">
        Récapitulatif
      </h2>
      <p class="muted">
        Vérifiez l'ensemble avant de soumettre ou de publier. Chaque partie peut être modifiée.
      </p>
    </header>

    <section class="state-row">
      <div>
        <span class="muted">État</span>
        <strong>{{ LIBELLES_STATUT[state.statut].label }}</strong>
      </div>
      <div>
        <span class="muted">Informations requises</span>
        <strong>{{ manques.length ? `${manques.length} manquante(s)` : 'Complètes' }}</strong>
      </div>
      <div>
        <span class="muted">Validations obligatoires</span>
        <strong>{{ circuit.filter(e => e.obligatoire && e.statut === 'approuve').length }}/{{ circuit.filter(e => e.obligatoire).length }} obtenue(s)</strong>
      </div>
      <div>
        <span class="muted">Points d'attention</span>
        <strong>{{ alertes.length }}</strong>
      </div>
    </section>

    <CspCallout
      v-if="echec && (bloquantsSoumission.length || manques.length)"
      variant="error"
      title="Action impossible pour l'instant"
    >
      <ul class="err-list">
        <li
          v-for="m in (state.statut === 'validee' ? manques : bloquantsSoumission)"
          :key="m.libelle"
        >
          <button
            type="button"
            class="link"
            @click="aller(m.stepId)"
          >
            {{ m.libelle }}
          </button>
        </li>
      </ul>
    </CspCallout>

    <div class="cols">
      <section class="block">
        <h3 class="block__title">
          Informations essentielles
        </h3>
        <dl class="dl">
          <template
            v-for="i in infos"
            :key="i.k"
          >
            <dt>{{ i.k }}</dt>
            <dd :class="{ 'dd--empty': !i.v }">
              {{ i.v || 'Non renseigné' }}
            </dd>
          </template>
        </dl>
      </section>

      <section class="block">
        <h3 class="block__title">
          Parties de l'offre
        </h3>
        <ul class="parts">
          <li
            v-for="s in STEPS.filter(x => x.id !== 'recap')"
            :key="s.id"
            :class="`parts__item--${statutStep(s.id)}`"
          >
            <CspIcon
              :name="statutStep(s.id) === 'complet' ? 'ri:checkbox-circle-fill' : statutStep(s.id) === 'incomplet' ? 'ri:error-warning-line' : 'ri:checkbox-blank-circle-line'"
              :size="16"
            />
            <span class="parts__name">
              {{ s.libelle }}
              <small>{{ LIBELLES_STEP[statutStep(s.id)] }}<template v-if="manquesDe(s.id).length"> · {{ manquesDe(s.id).map(m => m.libelle).join(', ') }}</template></small>
            </span>
            <CspButton
              label="Modifier"
              size="sm"
              variant="tertiary-no-outline"
              :aria-label="`Modifier ${s.libelle}`"
              @click="aller(s.id)"
            />
          </li>
        </ul>
      </section>
    </div>

    <section
      v-if="alertes.length"
      class="block"
    >
      <h3 class="block__title">
        Points d'attention <span class="muted">(non bloquants)</span>
      </h3>
      <ul class="alerts">
        <li
          v-for="a in alertes"
          :key="a.libelle"
        >
          <CspIcon
            :name="a.niveau === 'warning' ? 'ri:alert-line' : 'ri:information-line'"
            :size="14"
            :class="`alerts__icon--${a.niveau}`"
          />
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
    </section>

    <div class="cols">
      <section class="block">
        <h3 class="block__title">
          Validation
        </h3>
        <ol class="mini-circuit">
          <li
            v-for="e in circuit"
            :key="e.id"
          >
            <CspIcon
              :name="e.statut === 'approuve' ? 'ri:checkbox-circle-fill' : e.statut === 'corrections' ? 'ri:error-warning-fill' : e.statut === 'en_attente' ? 'ri:time-line' : 'ri:checkbox-blank-circle-line'"
              :size="14"
              :class="`mini-circuit__icon--${e.statut}`"
            />
            {{ e.libelle }} <small>— {{ personne(e.personneId).nom }}{{ e.obligatoire ? '' : ' (facultative)' }}</small>
          </li>
        </ol>
      </section>
      <section class="block">
        <h3 class="block__title">
          Diffusion envisagée
        </h3>
        <ul
          v-if="canauxChoisis.length"
          class="mini-list"
        >
          <li
            v-for="c in canauxChoisis"
            :key="c.id"
          >
            {{ c.nom }} <small>— {{ c.mode === 'connecteur' ? 'automatique (hypothèse)' : 'action manuelle' }}</small>
          </li>
        </ul>
        <p
          v-else
          class="muted"
        >
          Aucun canal sélectionné.
        </p>
        <p class="muted">
          {{ state.dateDebutDiffusion ? `Du ${state.dateDebutDiffusion}` : 'Dès publication' }} · {{ state.dateLimite ? `jusqu'au ${state.dateLimite}` : 'date limite à définir' }}
        </p>
      </section>
    </div>

    <details class="block details">
      <summary>Voir l'offre telle que la verront les candidats</summary>
      <OffrePreview />
    </details>

    <div class="final">
      <p
        v-if="raisonPublication"
        id="why"
        class="final__why"
      >
        <CspIcon
          name="ri:lock-line"
          :size="14"
        />
        Publication indisponible : {{ raisonPublication }}
      </p>
      <p
        v-else
        class="final__why final__why--ok"
      >
        <CspIcon
          name="ri:checkbox-circle-line"
          :size="14"
        />
        Toutes les conditions sont réunies pour publier.
      </p>
      <div class="final__actions">
        <CspButton
          label="Enregistrer le brouillon"
          variant="tertiary"
          :disabled="saving || !dirty"
          @click="sauver"
        />
        <CspButton
          v-if="state.statut === 'brouillon' || state.statut === 'a_corriger'"
          :label="state.statut === 'a_corriger' ? 'Renvoyer en validation' : 'Soumettre à validation'"
          :variant="validationRestante.length ? 'primary' : 'secondary'"
          icon="ri:send-plane-line"
          is-icon-left
          @click="onSoumettre"
        />
        <CspButton
          label="Publier l'offre"
          :variant="peutPublier ? 'primary' : 'secondary'"
          :disabled="!peutPublier"
          :aria-describedby="raisonPublication ? 'why' : undefined"
          @click="onPublier"
        />
      </div>
    </div>

    <CspDialog
      v-model:open="confirmation"
      title="Publier l'offre ?"
      description="L'offre sera visible des candidats sur les canaux choisis."
      size="md"
    >
      <ul class="mini-list">
        <li
          v-for="c in canauxChoisis"
          :key="c.id"
        >
          <strong>{{ c.nom }}</strong> <small>— {{ c.mode === 'connecteur' ? 'transmission automatique (simulée)' : `à faire ensuite : ${c.actionsManuelles.join(', ').toLowerCase()}` }}</small>
        </li>
      </ul>
      <p class="muted">
        Date limite de candidature : {{ state.dateLimite }}
      </p>
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="confirmation = false"
        />
        <CspButton
          label="Publier"
          icon="ri:send-plane-line"
          is-icon-left
          @click="confirmerPublication"
        />
      </template>
    </CspDialog>
  </template>
</template>

<style scoped lang="scss">
.head__title,
.pub__title {
  margin: 0;
  font-size: var(--csp-font-size-2xl);
}

.muted {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}

.state-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);

  > div {
    display: flex;
    flex-direction: column;
    padding: var(--csp-space-3) var(--csp-space-4);
  }

  > div + div {
    border-left: 1px solid var(--border-default-grey);
  }

  .muted {
    font-size: var(--csp-font-size-xs);
  }
}

.cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--csp-space-4);
}

.block {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4) var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.block__title {
  margin: 0;
  font-size: var(--csp-font-size-md);
}

.dl {
  display: grid;
  grid-template-columns: 7rem 1fr;
  gap: var(--csp-space-1) var(--csp-space-3);
  margin: 0;
  font-size: var(--csp-font-size-sm);

  dt {
    color: var(--text-mention-grey);
  }

  dd {
    margin: 0;
  }
}

.dd--empty {
  color: var(--text-default-warning);
  font-style: italic;
}

.parts,
.alerts,
.mini-circuit,
.mini-list,
.todo,
.continuity {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  small {
    color: var(--text-mention-grey);
  }
}

.parts li {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
}

.parts__name {
  flex: 1;

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
  }
}

.parts__item--complet :deep(.csp-icon) {
  color: var(--text-default-success);
}

.parts__item--incomplet :deep(.csp-icon) {
  color: var(--text-default-warning);
}

.alerts li {
  display: flex;
  align-items: baseline;
  gap: var(--csp-space-2);
}

.alerts__icon--warning {
  color: var(--text-default-warning);
}

.alerts__icon--info {
  color: var(--text-default-info);
}

.mini-circuit__icon--approuve {
  color: var(--text-default-success);
}

.mini-circuit__icon--corrections {
  color: var(--text-default-error);
}

.mini-circuit__icon--en_attente {
  color: var(--text-action-high-blue-france);
}

.details summary {
  cursor: pointer;
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-action-high-blue-france);
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

.err-list {
  margin: 0;
  padding-left: var(--csp-space-5);
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

.final__why {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);

  &--ok {
    color: var(--text-default-success);
  }
}

.final__actions {
  display: flex;
  gap: var(--csp-space-2);
  flex-shrink: 0;
}

.pub {
  display: flex;
  gap: var(--csp-space-4);
  align-items: flex-start;
  padding: var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  border-left: 4px solid var(--border-plain-success);
  background: var(--background-default-grey);
}

.pub__icon {
  color: var(--text-default-success);
}

.pub__desc {
  margin: var(--csp-space-1) 0 0;
}

.todo li,
.continuity li {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-2);
}

.todo__check {
  display: flex;
  gap: var(--csp-space-2);
  cursor: pointer;

  input {
    accent-color: var(--background-action-high-blue-france);
  }
}

.todo__done {
  text-decoration: line-through;
  color: var(--text-mention-grey);
}

.actions {
  display: flex;
  gap: var(--csp-space-2);
}
</style>
