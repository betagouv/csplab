<script setup lang="ts">
import type { Preset, SourceFiche } from '../data/scenario'
import type { OffreState, StartMode } from '../data/types'
import { computed, ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { BESOINS, BROUILLONS, depuisBesoin, depuisFiche, depuisOffre, etatInitial, FICHES, OFFRES_PRECEDENTES } from '../data/scenario'
import { useOffre } from '../data/useOffre'

// Écran 1 — choisir comment démarrer. On montre avant de valider ce qui sera repris
// et ce qui restera à compléter.
const emit = defineEmits<{ reprendre: [preset: Preset] }>()

const { state, aller, notifier, journaliser, completerAvecFiche } = useOffre()

const MODES: { id: StartMode, titre: string, desc: string, icon: string, compte?: string }[] = [
  { id: 'besoin', titre: 'À partir d\'un besoin existant', desc: 'Une DAR ou une demande de recrutement déjà saisie.', icon: 'ri:shield-check-line', compte: `${BESOINS.length} besoins sans offre` },
  { id: 'fiche', titre: 'À partir d\'une fiche de poste', desc: 'Reprendre une fiche du SIRH ou importer un document.', icon: 'ri:file-text-line' },
  { id: 'duplication', titre: 'Dupliquer une offre précédente', desc: 'Repartir d\'une offre déjà publiée sur un poste proche.', icon: 'ri:file-copy-2-line' },
  { id: 'vierge', titre: 'Commencer une offre vierge', desc: 'Aucune information préremplie.', icon: 'ri:file-add-line' },
]

const mode = ref<StartMode | null>(null)
const sourceId = ref<string | null>(null)
const fiches = ref<SourceFiche[]>([...FICHES])
const importEnCours = ref(false)
const erreur = ref('')

const sources = computed(() => {
  if (mode.value === 'besoin') {
    return BESOINS.map(b => ({ id: b.id, libelle: b.libelle, detail: b.detail, statut: b.statut }))
  }
  if (mode.value === 'fiche') {
    return fiches.value.map(f => ({ id: f.id, libelle: f.libelle, detail: f.detail, statut: '' }))
  }
  if (mode.value === 'duplication') {
    return OFFRES_PRECEDENTES.map(o => ({ id: o.id, libelle: o.libelle, detail: o.detail, statut: '' }))
  }
  return []
})

function choisirMode(m: StartMode) {
  mode.value = m
  sourceId.value = null
  erreur.value = ''
}

function appliquer(s: OffreState) {
  if (mode.value === 'besoin') {
    depuisBesoin(s, BESOINS.find(b => b.id === sourceId.value)!)
  }
  else if (mode.value === 'fiche') {
    depuisFiche(s, fiches.value.find(f => f.id === sourceId.value)!)
  }
  else if (mode.value === 'duplication') {
    depuisOffre(s, OFFRES_PRECEDENTES.find(o => o.id === sourceId.value)!)
  }
  else {
    s.startMode = 'vierge'
  }
}

const CHAMPS: { libelle: string, get: (s: OffreState) => unknown }[] = [
  { libelle: 'Intitulé du poste', get: s => s.besoin.intitule },
  { libelle: 'Service recruteur', get: s => s.besoin.service },
  { libelle: 'Motif du recrutement', get: s => s.besoin.motif },
  { libelle: 'Localisation', get: s => s.besoin.localisation },
  { libelle: 'Métier du répertoire', get: s => s.besoin.metier },
  { libelle: 'Catégorie', get: s => s.besoin.categories },
  { libelle: 'Statuts ouverts', get: s => s.besoin.statuts },
  { libelle: 'Autorisation de recrutement (DAR)', get: s => s.besoin.darRef },
  { libelle: 'Missions et activités', get: s => s.poste.missions },
  { libelle: 'Compétences attendues', get: s => s.poste.competences },
  { libelle: 'Texte de l\'offre pour les candidats', get: s => s.offre.poste.texte },
  { libelle: 'Conditions de candidature', get: s => s.conditions.profils },
]

function rempli(v: unknown) {
  return Array.isArray(v) ? v.length > 0 : Boolean(v && String(v).trim())
}

/** Aperçu calculé en appliquant la source sur un brouillon jetable. */
const apercu = computed(() => {
  if (!mode.value || (mode.value !== 'vierge' && !sourceId.value)) {
    return null
  }
  const essai = etatInitial()
  appliquer(essai)
  return {
    repris: CHAMPS.filter(c => rempli(c.get(essai))),
    aCompleter: CHAMPS.filter(c => !rempli(c.get(essai))),
  }
})

function importer() {
  importEnCours.value = true
  setTimeout(() => {
    importEnCours.value = false
    const f: SourceFiche = {
      ...FICHES[0]!,
      id: 'FP-IMPORT-001',
      libelle: 'fiche-poste-charge-mission-PTRE.docx',
      detail: 'Document importé à l\'instant · extraction simulée, à vérifier',
    }
    if (!fiches.value.some(x => x.id === f.id)) {
      fiches.value.push(f)
    }
    sourceId.value = f.id
  }, 1400)
}

function creer() {
  if (mode.value !== 'vierge' && !sourceId.value) {
    erreur.value = 'Sélectionnez une source dans la liste pour continuer.'
    return
  }
  appliquer(state)
  const n = apercu.value?.repris.length ?? 0
  if (mode.value === 'vierge') {
    journaliser('Offre vierge créée')
  }
  notifier(n ? `Offre créée : ${n} informations reprises. Vérifiez-les étape par étape.` : 'Offre vierge créée.')
  aller('besoin')
}

// --- Offre déjà démarrée : on peut compléter avec une fiche de poste (champs vides uniquement) ---
const ficheAjoutee = ref(false)
function completer() {
  completerAvecFiche()
  ficheAjoutee.value = true
}
</script>

<template>
  <!-- Offre déjà démarrée -->
  <template v-if="state.startMode">
    <header class="start__head">
      <h2 class="start__title">
        Point de départ
      </h2>
      <p class="start__intro">
        Cette offre a été créée
        <template v-if="state.startMode === 'vierge'">
          sans source préremplie.
        </template>
        <template v-else>
          à partir de <strong>{{ state.sourceLibelle }}</strong>.
        </template>
      </p>
    </header>
    <CspCallout
      v-if="!state.besoin.ficheRef && !ficheAjoutee"
      variant="info"
      title="Une fiche de poste existe pour ce service"
      description="FP-SECL-2024-012 — Chargé·e de mission PTRE. Vous pouvez l'utiliser pour compléter les champs encore vides : les informations déjà saisies ne seront pas remplacées."
    >
      <CspButton
        label="Compléter avec cette fiche"
        variant="secondary"
        size="sm"
        @click="completer"
      />
    </CspCallout>
    <div>
      <CspButton
        label="Aller à la première étape"
        icon="ri:arrow-right-line"
        @click="aller('besoin')"
      />
    </div>
  </template>

  <!-- Démarrage -->
  <template v-else>
    <header class="start__head">
      <h2 class="start__title">
        Créer une offre
      </h2>
      <p class="start__intro">
        Partez de ce qui existe déjà : vous n'aurez qu'à vérifier et compléter ce qui manque.
        Vous pourrez enregistrer et reprendre à tout moment.
      </p>
    </header>

    <section
      class="start__drafts"
      aria-labelledby="drafts-title"
    >
      <h3
        id="drafts-title"
        class="start__h3"
      >
        Reprendre une offre en cours
      </h3>
      <ul class="start__draft-list">
        <li
          v-for="b in BROUILLONS"
          :key="b.id"
        >
          <button
            type="button"
            class="start__draft"
            @click="emit('reprendre', b.preset)"
          >
            <span class="start__draft-ref">{{ b.id }}</span>
            <span class="start__draft-main">
              <strong>{{ b.libelle }}</strong>
              <small>{{ b.detail }}</small>
            </span>
            <CspBadge
              :label="b.statut === 'brouillon' ? 'Brouillon' : 'À corriger'"
              :type="b.statut === 'brouillon' ? 'info' : 'error'"
              variant="soft"
              size="sm"
            />
            <CspIcon
              name="ri:arrow-right-s-line"
              :size="18"
            />
          </button>
        </li>
      </ul>
    </section>

    <section
      class="start__new"
      aria-labelledby="new-title"
    >
      <h3
        id="new-title"
        class="start__h3"
      >
        Nouvelle offre — comment voulez-vous démarrer ?
      </h3>
      <div
        class="start__modes"
        role="radiogroup"
        aria-labelledby="new-title"
      >
        <label
          v-for="m in MODES"
          :key="m.id"
          class="start__mode"
          :class="{ 'start__mode--checked': mode === m.id }"
        >
          <input
            type="radio"
            name="start-mode"
            :value="m.id"
            :checked="mode === m.id"
            class="start__radio"
            @change="choisirMode(m.id)"
          >
          <CspIcon
            :name="m.icon"
            :size="20"
            class="start__mode-icon"
          />
          <span class="start__mode-title">{{ m.titre }}</span>
          <span class="start__mode-desc">{{ m.desc }}</span>
          <span
            v-if="m.compte"
            class="start__mode-count"
          >{{ m.compte }}</span>
        </label>
      </div>

      <div
        v-if="mode"
        class="start__config"
      >
        <div
          v-if="mode !== 'vierge'"
          class="start__sources"
        >
          <fieldset class="start__fieldset">
            <legend class="start__legend">
              {{ mode === 'besoin' ? 'Besoin de recrutement' : mode === 'fiche' ? 'Fiche de poste' : 'Offre à dupliquer' }}
            </legend>
            <label
              v-for="s in sources"
              :key="s.id"
              class="start__source"
              :class="{ 'start__source--checked': sourceId === s.id }"
            >
              <input
                v-model="sourceId"
                type="radio"
                name="source"
                :value="s.id"
              >
              <span>
                <strong>{{ s.libelle }}</strong>
                <small>{{ s.id }} · {{ s.detail }}</small>
                <small
                  v-if="s.statut"
                  class="start__source-statut"
                  :class="{ 'start__source-statut--wait': !s.statut.includes('validée') }"
                >{{ s.statut }}</small>
              </span>
            </label>
          </fieldset>
          <div
            v-if="mode === 'fiche'"
            class="start__import"
          >
            <CspButton
              :label="importEnCours ? 'Lecture du document…' : 'Importer un document (.docx, .pdf, .odt)'"
              variant="tertiary"
              size="sm"
              :icon="importEnCours ? 'ri:loader-4-line' : 'ri:upload-2-line'"
              is-icon-left
              :disabled="importEnCours"
              @click="importer"
            />
            <small>Prototype : l'extraction du contenu est simulée.</small>
          </div>
          <p
            v-if="erreur"
            class="start__error"
            role="alert"
          >
            <CspIcon
              name="ri:error-warning-fill"
              :size="14"
            />
            {{ erreur }}
          </p>
        </div>

        <div
          class="start__preview"
          aria-live="polite"
        >
          <template v-if="apercu">
            <h4 class="start__preview-title">
              Ce que vous obtiendrez
            </h4>
            <div class="start__preview-cols">
              <div>
                <p class="start__preview-sub start__preview-sub--ok">
                  Déjà disponible ({{ apercu.repris.length }})
                </p>
                <ul>
                  <li
                    v-for="c in apercu.repris"
                    :key="c.libelle"
                  >
                    <CspIcon
                      name="ri:check-line"
                      :size="14"
                    />{{ c.libelle }}
                  </li>
                  <li
                    v-if="!apercu.repris.length"
                    class="start__muted"
                  >
                    Rien de prérempli
                  </li>
                </ul>
              </div>
              <div>
                <p class="start__preview-sub">
                  À compléter ({{ apercu.aCompleter.length }})
                </p>
                <ul>
                  <li
                    v-for="c in apercu.aCompleter"
                    :key="c.libelle"
                  >
                    <CspIcon
                      name="ri:edit-line"
                      :size="14"
                    />{{ c.libelle }}
                  </li>
                </ul>
              </div>
            </div>
            <p
              v-if="mode === 'duplication'"
              class="start__warn"
            >
              <CspIcon
                name="ri:alert-line"
                :size="14"
              />
              Pensez à vérifier les dates, la référence de la DAR et les intervenants : ils ne sont pas dupliqués.
            </p>
          </template>
          <p
            v-else
            class="start__muted"
          >
            Sélectionnez une source pour voir ce qui sera repris.
          </p>
          <CspButton
            class="start__cta"
            label="Créer l'offre"
            icon="ri:arrow-right-line"
            @click="creer"
          />
        </div>
      </div>
    </section>
  </template>
</template>

<style scoped lang="scss">
.start__head {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.start__title {
  margin: 0;
  font-size: var(--csp-font-size-2xl);
}

.start__intro {
  margin: 0;
  color: var(--text-mention-grey);
  max-width: 44rem;
}

.start__h3 {
  margin: 0 0 var(--csp-space-3);
  font-size: var(--csp-font-size-md);
}

.start__draft-list {
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
}

.start__draft-list li + li {
  border-top: 1px solid var(--border-default-grey);
}

.start__draft {
  display: flex;
  align-items: center;
  gap: var(--csp-space-4);
  width: 100%;
  padding: var(--csp-space-3) var(--csp-space-4);
  border: 0;
  background: none;
  font: inherit;
  text-align: left;
  color: var(--text-default-grey);
  cursor: pointer;

  &:hover {
    background: var(--background-default-grey-hover);
  }
}

.start__draft-ref {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
  font-variant-numeric: tabular-nums;
  width: 7rem;
}

.start__draft-main {
  flex: 1;

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.start__modes {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--csp-space-3);
}

.start__mode {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
  padding: var(--csp-space-4);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);
  cursor: pointer;

  &:hover {
    background: var(--background-default-grey-hover);
  }

  &:has(:focus-visible) {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
    outline-offset: 2px;
  }

  &--checked {
    border-color: var(--border-active-blue-france);
    box-shadow: inset 0 0 0 1px var(--border-active-blue-france);
  }
}

.start__radio {
  position: absolute;
  top: var(--csp-space-4);
  right: var(--csp-space-4);
  accent-color: var(--background-action-high-blue-france);
}

.start__mode-icon {
  color: var(--text-action-high-blue-france);
  margin-bottom: var(--csp-space-2);
}

.start__mode-title {
  font-weight: var(--csp-font-weight-bold);
  padding-right: var(--csp-space-5);
}

.start__mode-desc {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.start__mode-count {
  margin-top: var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  color: var(--text-action-high-blue-france);
  font-weight: var(--csp-font-weight-medium);
}

.start__config {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr);
  gap: var(--csp-space-4);
  margin-top: var(--csp-space-4);
  padding: var(--csp-space-5);
  border: 1px solid var(--border-default-grey);
  background: var(--background-default-grey);

  &:has(.start__preview:only-child) {
    grid-template-columns: 1fr;
  }
}

.start__fieldset {
  margin: 0;
  padding: 0;
  border: 0;
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
}

.start__legend {
  margin-bottom: var(--csp-space-2);
  font-weight: var(--csp-font-weight-bold);
}

.start__source {
  display: flex;
  gap: var(--csp-space-3);
  align-items: flex-start;
  padding: var(--csp-space-3);
  border: 1px solid var(--border-default-grey);
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

  &--checked {
    border-color: var(--border-active-blue-france);
    background: var(--background-alt-blue-france);
  }
}

.start__source-statut {
  color: var(--text-default-success) !important;

  &--wait {
    color: var(--text-default-warning) !important;
  }
}

.start__import {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  margin-top: var(--csp-space-3);

  small {
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.start__error {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: var(--csp-space-3) 0 0;
  color: var(--text-default-error);
  font-size: var(--csp-font-size-sm);
}

.start__preview {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4);
  background: var(--background-alt-grey);

  ul {
    margin: 0;
    padding: 0;
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: var(--csp-space-1);
    font-size: var(--csp-font-size-sm);
  }

  li {
    display: flex;
    gap: var(--csp-space-1);
    align-items: center;
  }
}

.start__preview-title {
  margin: 0;
  font-size: var(--csp-font-size-base);
}

.start__preview-cols {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--csp-space-4);
}

.start__preview-sub {
  margin: 0 0 var(--csp-space-2);
  font-size: var(--csp-font-size-xs);
  font-weight: var(--csp-font-weight-bold);
  text-transform: uppercase;
  color: var(--text-mention-grey);

  &--ok {
    color: var(--text-default-success);
  }
}

.start__warn {
  display: flex;
  gap: var(--csp-space-1);
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-default-warning);
}

.start__muted {
  margin: 0;
  color: var(--text-mention-grey);
  font-size: var(--csp-font-size-sm);
}

.start__cta {
  align-self: flex-start;
  margin-top: auto;
}
</style>
