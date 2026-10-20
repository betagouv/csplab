<script setup lang="ts">
import type { SectionOffreId } from '../data/types'
import { computed, reactive, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import { ORGANISMES, SECTIONS_OFFRE } from '../data/referentiels'
import { OFFRE_REDIGEE, SUGGESTIONS } from '../data/scenario'
import { useOffre } from '../data/useOffre'
import OffrePreview from '../shared/OffrePreview.vue'
import StepFooter from '../shared/StepFooter.vue'
import StepHeader from '../shared/StepHeader.vue'

// Écran 4 — rédiger l'offre destinée aux candidats, section par section.
// Rien n'est remplacé sans action explicite : reprise et reformulation passent par une confirmation.
const { state, verrouille, alertes, afficherErreurs } = useOffre()

type Vue = 'edition' | 'cote' | 'apercu'
const vue = ref<Vue>('edition')
const VUES = [
  { value: 'edition' as const, label: 'Rédaction', icon: 'ri:edit-line' },
  { value: 'cote' as const, label: 'Côte à côte', icon: 'ri:layout-column-line' },
  { value: 'apercu' as const, label: 'Aperçu candidat', icon: 'ri:eye-line' },
]

/** Texte proposé à partir des étapes précédentes (fiche de poste, besoin). */
function depuisEtapes(id: SectionOffreId): string {
  const b = state.besoin
  const p = state.poste
  switch (id) {
    case 'organisme':
      return b.organisme === 'dreal-occ' ? OFFRE_REDIGEE.organisme : `${ORGANISMES.find(o => o.value === b.organisme)?.label ?? ''} — présentation à compléter.`
    case 'poste':
      return [p.environnement, b.service ? `Poste rattaché au ${b.service}.` : ''].filter(Boolean).join(' ')
    case 'missions':
      return [p.missions, ...p.activites.map(a => `- ${a}`)].filter(Boolean).join('\n')
    case 'profil':
      return [p.qualifications, p.profil, ...p.competences.map(c => `- ${c}`)].filter(Boolean).join('\n')
    case 'conditions': {
      const statuts = b.statuts.length === 2 ? 'aux fonctionnaires et aux contractuels' : b.statuts[0] === 'titulaire' ? 'aux fonctionnaires' : 'aux contractuels'
      const contrat = b.statuts.includes('contractuel') && b.typeContrat === 'cdd' ? ` (CDD${b.dureeContrat ? ` de ${b.dureeContrat}` : ''})` : ''
      return b.statuts.length ? `Poste de catégorie ${b.categories.join(' ou ') || '?'} ouvert ${statuts}${contrat}.` : ''
    }
    case 'pratique':
      return [b.localisation && `Poste basé à ${b.localisation}.`, b.teletravail && `Télétravail : ${b.teletravail}.`, p.aDesConditions && p.conditionsParticulieres].filter(Boolean).join(' ')
    case 'candidature':
      return OFFRE_REDIGEE.candidature
  }
}

const SOURCE_LIBELLE: Record<SectionOffreId, string> = {
  organisme: 'présentation type de l\'organisme',
  poste: 'environnement et service',
  missions: 'missions et activités',
  profil: 'qualifications, profil et compétences',
  conditions: 'catégorie, statuts et contrat',
  pratique: 'localisation, télétravail, conditions',
  candidature: 'modèle de l\'organisme',
}

// État d'interface par section : confirmation de reprise, suggestion affichée.
const ui = reactive<Record<string, { confirmer?: string, suggestion?: string, chargement?: boolean }>>({})
function uiDe(id: string) {
  ui[id] ??= {}
  return ui[id]!
}

function saisir(id: SectionOffreId, texte: string) {
  state.offre[id].texte = texte
  state.offre[id].etat = texte.trim() ? 'redige' : 'vide'
}

function reprendre(id: SectionOffreId) {
  const texte = depuisEtapes(id)
  if (!state.offre[id].texte.trim()) {
    state.offre[id] = { texte, etat: 'reprise' }
    return
  }
  uiDe(id).confirmer = texte
}

function confirmerReprise(id: SectionOffreId, mode: 'remplacer' | 'ajouter') {
  const texte = uiDe(id).confirmer ?? ''
  state.offre[id] = mode === 'remplacer'
    ? { texte, etat: 'reprise' }
    : { texte: `${state.offre[id].texte}\n${texte}`, etat: 'redige' }
  uiDe(id).confirmer = undefined
}

function proposer(id: SectionOffreId) {
  uiDe(id).chargement = true
  setTimeout(() => {
    uiDe(id).chargement = false
    uiDe(id).suggestion = SUGGESTIONS[id]
  }, 900)
}

function accepterSuggestion(id: SectionOffreId) {
  state.offre[id] = { texte: uiDe(id).suggestion ?? '', etat: 'redige' }
  uiDe(id).suggestion = undefined
}

const ETATS = {
  vide: { label: 'À rédiger', icon: 'ri:checkbox-blank-circle-line', cls: 'vide' },
  reprise: { label: 'Repris — à retravailler pour les candidats', icon: 'ri:file-copy-2-line', cls: 'reprise' },
  redige: { label: 'Rédigé', icon: 'ri:checkbox-circle-fill', cls: 'redige' },
}

const alertesOffre = computed(() => alertes.value.filter(a => a.stepId === 'offre'))
const sectionsCompletes = computed(() => SECTIONS_OFFRE.filter(s => state.offre[s.id].texte.trim()).length)

function allerA(id: string) {
  document.getElementById(`section-${id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  document.getElementById(`ta-${id}`)?.focus({ preventScroll: true })
}
</script>

<template>
  <StepHeader
    id="offre"
    description="Le texte que liront les candidats. Il part des informations du poste mais se rédige pour être compris et donner envie : évitez le jargon interne. Les reprises et suggestions ne remplacent jamais votre texte sans votre accord."
  />

  <div class="offre-toolbar">
    <CspSegmentedControl
      v-model="vue"
      legend="Affichage"
      hide-legend
      size="sm"
      :options="VUES"
    />
    <span class="offre-toolbar__count">{{ sectionsCompletes }}/{{ SECTIONS_OFFRE.length }} sections rédigées</span>
  </div>

  <nav
    v-if="vue !== 'apercu'"
    class="offre-index"
    aria-label="Sections de l'offre"
  >
    <button
      v-for="s in SECTIONS_OFFRE"
      :key="s.id"
      type="button"
      class="offre-index__item"
      :class="`offre-index__item--${state.offre[s.id].etat}`"
      @click="allerA(s.id)"
    >
      <CspIcon
        :name="ETATS[state.offre[s.id].etat].icon"
        :size="12"
      />
      {{ s.libelle }}<span
        v-if="s.requise"
        aria-hidden="true"
      > *</span>
    </button>
  </nav>

  <div
    class="offre-layout"
    :class="`offre-layout--${vue}`"
  >
    <div
      v-if="vue !== 'apercu'"
      class="offre-editor"
    >
      <section
        v-for="s in SECTIONS_OFFRE"
        :id="`section-${s.id}`"
        :key="s.id"
        class="sec"
        :class="{ 'sec--error': afficherErreurs && s.requise && !state.offre[s.id].texte.trim() }"
      >
        <header class="sec__head">
          <label
            :for="`ta-${s.id}`"
            class="sec__title"
          >
            {{ s.libelle }}<span
              v-if="s.requise"
              class="sec__req"
            > *</span>
          </label>
          <span
            class="sec__state"
            :class="`sec__state--${ETATS[state.offre[s.id].etat].cls}`"
          >
            <CspIcon
              :name="ETATS[state.offre[s.id].etat].icon"
              :size="12"
            />
            {{ ETATS[state.offre[s.id].etat].label }}
          </span>
        </header>
        <textarea
          :id="`ta-${s.id}`"
          class="sec__ta"
          :value="state.offre[s.id].texte"
          :rows="state.offre[s.id].texte.length > 260 ? 7 : 4"
          :disabled="verrouille"
          :placeholder="`Rédigez la section « ${s.libelle} » pour un candidat qui ne connaît pas votre service.`"
          :aria-describedby="`aide-${s.id}`"
          :aria-invalid="(afficherErreurs && s.requise && !state.offre[s.id].texte.trim()) || undefined"
          @input="saisir(s.id, ($event.target as HTMLTextAreaElement).value)"
        />
        <p
          :id="`aide-${s.id}`"
          class="sec__aide"
        >
          <template v-if="afficherErreurs && s.requise && !state.offre[s.id].texte.trim()">
            <span class="sec__err">Cette section est requise pour soumettre l'offre.</span>
          </template>
          {{ state.offre[s.id].texte.length }} caractères · Une ligne commençant par « - » devient une puce.
        </p>

        <div
          v-if="uiDe(s.id).confirmer"
          class="sec__confirm"
          role="group"
          aria-label="Confirmer la reprise"
        >
          <p><strong>Cette section contient déjà du texte.</strong> Que faire du texte repris ({{ SOURCE_LIBELLE[s.id] }}) ?</p>
          <blockquote>{{ uiDe(s.id).confirmer }}</blockquote>
          <div class="sec__actions">
            <CspButton
              label="Remplacer mon texte"
              size="sm"
              variant="secondary"
              @click="confirmerReprise(s.id, 'remplacer')"
            />
            <CspButton
              label="Ajouter à la suite"
              size="sm"
              variant="secondary"
              @click="confirmerReprise(s.id, 'ajouter')"
            />
            <CspButton
              label="Annuler"
              size="sm"
              variant="tertiary-no-outline"
              @click="uiDe(s.id).confirmer = undefined"
            />
          </div>
        </div>

        <div
          v-if="uiDe(s.id).suggestion"
          class="sec__suggest"
        >
          <p class="sec__suggest-title">
            <CspIcon
              name="ri:magic-line"
              :size="14"
            />
            Proposition de reformulation (facultative)
          </p>
          <div class="sec__diff">
            <div>
              <p class="sec__diff-label">
                Votre texte
              </p>
              <p class="sec__diff-text">
                {{ state.offre[s.id].texte || '—' }}
              </p>
            </div>
            <div>
              <p class="sec__diff-label">
                Proposition
              </p>
              <p class="sec__diff-text sec__diff-text--new">
                {{ uiDe(s.id).suggestion }}
              </p>
            </div>
          </div>
          <div class="sec__actions">
            <CspButton
              label="Utiliser la proposition"
              size="sm"
              @click="accepterSuggestion(s.id)"
            />
            <CspButton
              label="Garder mon texte"
              size="sm"
              variant="tertiary-no-outline"
              @click="uiDe(s.id).suggestion = undefined"
            />
          </div>
        </div>

        <div
          v-if="!verrouille && !uiDe(s.id).confirmer && !uiDe(s.id).suggestion"
          class="sec__tools"
        >
          <CspButton
            :label="`Reprendre : ${SOURCE_LIBELLE[s.id]}`"
            size="sm"
            variant="tertiary-no-outline"
            icon="ri:download-2-line"
            is-icon-left
            :disabled="!depuisEtapes(s.id)"
            @click="reprendre(s.id)"
          />
          <CspButton
            v-if="SUGGESTIONS[s.id] && state.offre[s.id].texte.trim()"
            :label="uiDe(s.id).chargement ? 'Préparation…' : 'Proposer une reformulation'"
            size="sm"
            variant="tertiary-no-outline"
            :icon="uiDe(s.id).chargement ? 'ri:loader-4-line' : 'ri:magic-line'"
            is-icon-left
            :disabled="uiDe(s.id).chargement"
            @click="proposer(s.id)"
          />
        </div>
      </section>
    </div>

    <div
      v-if="vue !== 'edition'"
      class="offre-preview"
    >
      <OffrePreview />
    </div>
  </div>

  <section
    class="checks"
    aria-labelledby="checks-title"
  >
    <h3
      id="checks-title"
      class="checks__title"
    >
      Relecture éditoriale
    </h3>
    <ul
      v-if="alertesOffre.length"
      class="checks__list"
    >
      <li
        v-for="a in alertesOffre"
        :key="a.libelle"
        :class="`checks__item--${a.niveau}`"
      >
        <CspIcon
          :name="a.niveau === 'warning' ? 'ri:alert-line' : 'ri:information-line'"
          :size="14"
        />
        {{ a.libelle }}
      </li>
    </ul>
    <p
      v-else
      class="checks__ok"
    >
      <CspIcon
        name="ri:checkbox-circle-line"
        :size="14"
      />
      Aucun point d'attention détecté. Ces vérifications sont indicatives et ne remplacent pas une relecture.
    </p>
  </section>

  <StepFooter id="offre" />
</template>

<style scoped lang="scss">
.offre-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
}

.offre-toolbar__count {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.offre-index {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin-top: calc(-1 * var(--csp-space-2));
}

.offre-index__item {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  padding: var(--csp-space-1) var(--csp-space-2);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  font: inherit;
  font-size: var(--csp-font-size-xs);
  color: var(--text-default-grey);
  cursor: pointer;

  &--redige :deep(.csp-icon) {
    color: var(--text-default-success);
  }

  &--reprise :deep(.csp-icon) {
    color: var(--text-default-info);
  }

  &:hover {
    background: var(--background-default-grey-hover);
  }
}

.offre-layout {
  display: grid;
  gap: var(--csp-space-4);

  &--cote {
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    align-items: start;
  }
}

.offre-preview {
  .offre-layout--cote & {
    position: sticky;
    top: 0;
    max-height: calc(100vh - 10rem);
    overflow-y: auto;
  }
}

.offre-editor {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.sec {
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  border-left: 3px solid var(--border-plain-blue-france);
  background: var(--background-default-grey);
  scroll-margin-top: var(--csp-space-4);

  &--error {
    border-left-color: var(--border-plain-error);
  }
}

.sec__head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-3);
  margin-bottom: var(--csp-space-2);
}

.sec__title {
  font-weight: var(--csp-font-weight-bold);
}

.sec__req {
  color: var(--text-default-error);
}

.sec__state {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
  text-align: right;

  &--reprise {
    color: var(--text-default-info);
  }

  &--redige {
    color: var(--text-default-success);
  }
}

.sec__ta {
  width: 100%;
  padding: var(--csp-space-2) var(--csp-space-3);
  border: 0;
  border-radius: 0.25rem 0.25rem 0 0;
  box-shadow: inset 0 -2px 0 0 var(--border-plain-grey);
  background: var(--background-contrast-grey);
  font: inherit;
  line-height: var(--csp-line-height-relaxed);
  color: var(--text-default-grey);
  resize: vertical;

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
    outline-offset: 2px;
  }

  .sec--error & {
    box-shadow: inset 0 -2px 0 0 var(--border-plain-error);
  }
}

.sec__aide {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.sec__err {
  display: block;
  color: var(--text-default-error);
}

.sec__tools {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin-top: var(--csp-space-2);
  margin-left: calc(-1 * var(--csp-space-2));
}

.sec__confirm,
.sec__suggest {
  margin-top: var(--csp-space-3);
  padding: var(--csp-space-3);
  background: var(--background-alt-blue-france);
  font-size: var(--csp-font-size-sm);

  p {
    margin: 0 0 var(--csp-space-2);
  }

  blockquote {
    margin: 0 0 var(--csp-space-3);
    padding-left: var(--csp-space-3);
    border-left: 2px solid var(--border-default-blue-france);
    white-space: pre-line;
    color: var(--text-mention-grey);
  }
}

.sec__suggest-title {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-weight: var(--csp-font-weight-bold);
}

.sec__diff {
  display: grid;
  grid-template-columns: 1fr 1fr;

  .offre-layout--cote & {
    grid-template-columns: 1fr;
  }

  gap: var(--csp-space-3);
  margin-bottom: var(--csp-space-3);
}

.sec__diff-label {
  font-size: var(--csp-font-size-xs);
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.sec__diff-text {
  padding: var(--csp-space-2);
  background: var(--background-default-grey);
  white-space: pre-line;

  &--new {
    box-shadow: inset 3px 0 0 var(--border-plain-blue-france);
  }
}

.sec__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}

.checks {
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.checks__title {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-base);
}

.checks__list {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  li {
    display: flex;
    gap: var(--csp-space-2);
    align-items: baseline;
  }
}

.checks__item--warning :deep(.csp-icon) {
  color: var(--text-default-warning);
}

.checks__item--info :deep(.csp-icon) {
  color: var(--text-default-info);
}

.checks__ok {
  display: flex;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-success);
}
</style>
