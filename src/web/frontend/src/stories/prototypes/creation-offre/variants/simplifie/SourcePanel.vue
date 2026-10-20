<script setup lang="ts">
import type { Preset } from '../../data/scenario'
import type { OffreState } from '../../data/types'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { BESOINS, BROUILLONS, depuisBesoin, depuisFiche, depuisOffre, etatInitial, FICHES, OFFRES_PRECEDENTES } from '../../data/scenario'
import { useOffre } from '../../data/useOffre'

// Reprise d'informations existantes, intégrée à l'étape 1 (plus d'écran de démarrage séparé).
// Une fois la source appliquée, il ne reste qu'une ligne de rappel.
const emit = defineEmits<{ reprendre: [preset: Preset] }>()
const { state, notifier, completerAvecFiche } = useOffre()

type Mode = 'besoin' | 'fiche' | 'duplication' | 'brouillon'
const mode = ref<Mode | null>(null)
const sourceId = ref<string | null>(null)
const ouvert = computed({
  get: () => mode.value !== null,
  set: (v) => {
    if (!v) {
      mode.value = null
    }
  },
})

const TITRES: Record<Mode, string> = {
  besoin: 'Partir d\'un besoin validé',
  fiche: 'Partir d\'une fiche de poste',
  duplication: 'Dupliquer une offre',
  brouillon: 'Reprendre un brouillon',
}

const sources = computed(() => {
  switch (mode.value) {
    case 'besoin': return BESOINS.map(b => ({ id: b.id, libelle: b.libelle, detail: `${b.id} · ${b.statut}` }))
    case 'fiche': return FICHES.map(f => ({ id: f.id, libelle: f.libelle, detail: `${f.id} · ${f.detail}` }))
    case 'duplication': return OFFRES_PRECEDENTES.map(o => ({ id: o.id, libelle: o.libelle, detail: `${o.id} · ${o.detail}` }))
    case 'brouillon': return BROUILLONS.map(b => ({ id: b.id, libelle: b.libelle, detail: `${b.id} · ${b.detail}` }))
    default: return []
  }
})

function ouvrir(m: Mode) {
  mode.value = m
  sourceId.value = sources.value[0]?.id ?? null
}

function appliquer(s: OffreState) {
  if (mode.value === 'besoin') {
    depuisBesoin(s, BESOINS.find(b => b.id === sourceId.value)!)
  }
  else if (mode.value === 'fiche') {
    depuisFiche(s, FICHES.find(f => f.id === sourceId.value)!)
  }
  else if (mode.value === 'duplication') {
    depuisOffre(s, OFFRES_PRECEDENTES.find(o => o.id === sourceId.value)!)
  }
}

const NB_CHAMPS = (s: OffreState) => Object.keys(s.origines).length
const apercu = computed(() => {
  if (!sourceId.value || mode.value === 'brouillon' || !mode.value) {
    return null
  }
  const essai = etatInitial()
  appliquer(essai)
  const repris = [
    essai.besoin.intitule && 'intitulé et service',
    essai.besoin.categories.length && 'catégorie',
    essai.besoin.darRef && 'autorisation de recrutement',
    essai.poste.missions && 'missions et compétences (fiche de poste)',
    essai.offre.poste.texte && 'texte de l\'offre',
    essai.conditions.indispensables.length && 'critères de sélection',
  ].filter(Boolean)
  return { n: NB_CHAMPS(essai), repris }
})

function valider() {
  if (mode.value === 'brouillon') {
    emit('reprendre', BROUILLONS.find(b => b.id === sourceId.value)!.preset)
    return
  }
  appliquer(state)
  notifier(`${NB_CHAMPS(state)} informations préremplies. Elles sont signalées par « Repris de… ».`)
  mode.value = null
}

const ficheProposee = computed(() => state.startMode && state.startMode !== 'fiche' && !state.besoin.ficheRef && !state.poste.missions)
</script>

<template>
  <section
    v-if="!state.startMode && state.statut === 'brouillon'"
    class="source"
    aria-labelledby="source-title"
  >
    <div>
      <h2
        id="source-title"
        class="source__title"
      >
        Gagnez du temps : partez de l'existant
      </h2>
      <p class="source__desc">
        Les informations reprises restent modifiables. Vous pouvez aussi saisir directement ci-dessous.
      </p>
    </div>
    <div class="source__actions">
      <CspButton
        label="Besoin validé (DAR)"
        variant="secondary"
        size="sm"
        icon="ri:shield-check-line"
        is-icon-left
        @click="ouvrir('besoin')"
      />
      <CspButton
        label="Fiche de poste"
        variant="secondary"
        size="sm"
        icon="ri:file-text-line"
        is-icon-left
        @click="ouvrir('fiche')"
      />
      <CspButton
        label="Dupliquer une offre"
        variant="secondary"
        size="sm"
        icon="ri:file-copy-2-line"
        is-icon-left
        @click="ouvrir('duplication')"
      />
      <CspButton
        :label="`Reprendre un brouillon (${BROUILLONS.length})`"
        variant="tertiary-no-outline"
        size="sm"
        @click="ouvrir('brouillon')"
      />
    </div>
  </section>

  <p
    v-else-if="state.sourceLibelle"
    class="source-line"
  >
    <CspIcon
      name="ri:file-copy-2-line"
      :size="14"
    />
    <span>Prérempli depuis <strong>{{ state.sourceLibelle.split(' — ')[0] }}</strong>.</span>
    <button
      v-if="ficheProposee && state.statut === 'brouillon'"
      type="button"
      class="link"
      @click="completerAvecFiche"
    >
      Compléter avec la fiche de poste FP-SECL-2024-012
    </button>
  </p>

  <CspDialog
    v-model:open="ouvert"
    :title="mode ? TITRES[mode] : ''"
    size="md"
  >
    <fieldset class="dlg__list">
      <legend class="sr-only">
        Source
      </legend>
      <label
        v-for="s in sources"
        :key="s.id"
        class="dlg__item"
        :class="{ 'dlg__item--on': sourceId === s.id }"
      >
        <input
          v-model="sourceId"
          type="radio"
          name="src"
          :value="s.id"
        >
        <span>
          <strong>{{ s.libelle }}</strong>
          <small>{{ s.detail }}</small>
        </span>
      </label>
    </fieldset>
    <p
      v-if="apercu"
      class="dlg__preview"
    >
      Seront repris : {{ apercu.repris.join(', ') }}.
      <template v-if="mode === 'duplication'">
        Les dates, la DAR et les intervenants ne sont pas dupliqués.
      </template>
    </p>
    <template #footer>
      <CspButton
        label="Annuler"
        variant="secondary"
        @click="mode = null"
      />
      <CspButton
        :label="mode === 'brouillon' ? 'Ouvrir le brouillon' : 'Préremplir'"
        :disabled="!sourceId"
        @click="valider"
      />
    </template>
  </CspDialog>
</template>

<style scoped lang="scss">
.source {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-4) var(--csp-space-5);
  background: var(--background-alt-blue-france);
}

.source__title {
  margin: 0;
  font-size: var(--csp-font-size-base);
}

.source__desc {
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.source__actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
}

.source-line {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
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

.dlg__list {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  border: 0;
}

.dlg__item {
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

  &--on {
    border-color: var(--border-active-blue-france);
  }
}

.dlg__preview {
  margin: var(--csp-space-4) 0 0;
  font-size: var(--csp-font-size-sm);
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
