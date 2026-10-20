<script setup lang="ts">
import type { SectionOffreId } from '../../data/types'
import { computed, reactive, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import { texteDepuisPoste } from '../../data/redaction'
import { SECTIONS_OFFRE } from '../../data/referentiels'
import { SUGGESTIONS } from '../../data/scenario'
import { useOffre } from '../../data/useOffre'
import OffrePreview from '../../shared/OffrePreview.vue'
import EtapeFooter from './EtapeFooter.vue'
import RemarquesSection from './RemarquesSection.vue'

// Étape 2 — rédiger l'offre pour les candidats, sur une seule page.
// Un seul geste pour partir des informations du poste ; la reformulation reste une proposition.
const { state, verrouille, afficherErreurs, notifier } = useOffre()

const vue = ref<'edition' | 'apercu'>('edition')
const VUES = [
  { value: 'edition' as const, label: 'Rédaction', icon: 'ri:edit-line' },
  { value: 'apercu' as const, label: 'Aperçu candidat', icon: 'ri:eye-line' },
]

const sectionsVides = computed(() => SECTIONS_OFFRE.filter(s => !state.offre[s.id].texte.trim() && texteDepuisPoste(state, s.id)))
function preremplir() {
  const n = sectionsVides.value.length
  for (const s of sectionsVides.value) {
    state.offre[s.id] = { texte: texteDepuisPoste(state, s.id), etat: 'reprise' }
  }
  notifier(`${n} section(s) préremplie(s) à partir du poste. Adaptez-les pour les candidats.`)
}

function saisir(id: SectionOffreId, texte: string) {
  state.offre[id] = { texte, etat: texte.trim() ? 'redige' : 'vide' }
}

const suggestion = reactive<Record<string, { texte?: string, chargement?: boolean }>>({})
function proposer(id: SectionOffreId) {
  suggestion[id] = { chargement: true }
  setTimeout(() => (suggestion[id] = { texte: SUGGESTIONS[id] }), 800)
}
function accepter(id: SectionOffreId) {
  saisir(id, suggestion[id]?.texte ?? '')
  delete suggestion[id]
}

const enErreur = (id: SectionOffreId, requise: boolean) => afficherErreurs.value && requise && !state.offre[id].texte.trim()
</script>

<template>
  <header class="head">
    <div>
      <h2 class="head__title">
        Rédiger l'offre
      </h2>
      <p class="head__desc">
        Le texte que liront les candidats. Écrivez pour quelqu'un qui ne connaît pas votre service.
      </p>
    </div>
    <CspSegmentedControl
      v-model="vue"
      legend="Affichage"
      hide-legend
      size="sm"
      :options="VUES"
    />
  </header>

  <RemarquesSection :step-ids="['offre']" />

  <OffrePreview v-if="vue === 'apercu'" />

  <template v-else>
    <div
      v-if="sectionsVides.length && !verrouille"
      class="prefill"
    >
      <span>{{ sectionsVides.length }} section(s) peuvent être préremplies avec les informations du poste.</span>
      <CspButton
        label="Préremplir"
        variant="secondary"
        size="sm"
        icon="ri:download-2-line"
        is-icon-left
        @click="preremplir"
      />
    </div>

    <div class="editor">
      <section
        v-for="s in SECTIONS_OFFRE"
        :id="`offre-${s.id}`"
        :key="s.id"
        class="sec"
      >
        <div class="sec__head">
          <label
            :for="`ta-${s.id}`"
            class="sec__label"
          >
            {{ s.libelle }}<span
              v-if="!s.requise"
              class="sec__opt"
            > (facultatif)</span>
          </label>
          <span
            v-if="state.offre[s.id].etat === 'reprise'"
            class="sec__tag"
          >Repris du poste — à adapter</span>
        </div>
        <textarea
          :id="`ta-${s.id}`"
          class="sec__ta"
          :class="{ 'sec__ta--error': enErreur(s.id, s.requise) }"
          :value="state.offre[s.id].texte"
          :rows="state.offre[s.id].texte.length > 260 ? 6 : 3"
          :disabled="verrouille"
          :aria-invalid="enErreur(s.id, s.requise) || undefined"
          :aria-describedby="enErreur(s.id, s.requise) ? `err-${s.id}` : undefined"
          @input="saisir(s.id, ($event.target as HTMLTextAreaElement).value)"
        />
        <p
          v-if="enErreur(s.id, s.requise)"
          :id="`err-${s.id}`"
          class="sec__error"
        >
          <CspIcon
            name="ri:error-warning-fill"
            :size="14"
          />
          Rédigez cette section pour pouvoir soumettre l'offre.
        </p>

        <div
          v-if="suggestion[s.id]?.texte"
          class="sugg"
        >
          <p class="sugg__title">
            Proposition de reformulation
          </p>
          <p class="sugg__text">
            {{ suggestion[s.id]!.texte }}
          </p>
          <div class="sugg__actions">
            <CspButton
              label="Remplacer mon texte"
              size="sm"
              @click="accepter(s.id)"
            />
            <CspButton
              label="Garder mon texte"
              size="sm"
              variant="tertiary-no-outline"
              @click="delete suggestion[s.id]"
            />
          </div>
        </div>
        <div
          v-else-if="!verrouille && SUGGESTIONS[s.id] && state.offre[s.id].texte.trim()"
          class="sec__tools"
        >
          <CspButton
            :label="suggestion[s.id]?.chargement ? 'Préparation…' : 'Proposer une reformulation'"
            size="sm"
            variant="tertiary-no-outline"
            :icon="suggestion[s.id]?.chargement ? 'ri:loader-4-line' : 'ri:magic-line'"
            is-icon-left
            :disabled="suggestion[s.id]?.chargement"
            @click="proposer(s.id)"
          />
        </div>
      </section>
    </div>
  </template>

  <EtapeFooter />
</template>

<style scoped lang="scss">
.head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: var(--csp-space-4);
}

.head__title {
  margin: 0;
  font-size: var(--csp-font-size-2xl);
}

.head__desc {
  margin: var(--csp-space-1) 0 0;
  color: var(--text-mention-grey);
}

.prefill {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-alt-blue-france);
  font-size: var(--csp-font-size-sm);
}

.editor {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
  padding: var(--csp-space-5) var(--csp-space-6);
  border: 1px solid var(--border-default-grey);
  box-shadow: inset 3px 0 0 var(--border-plain-blue-france);
  background: var(--background-default-grey);
}

.sec {
  scroll-margin-top: var(--csp-space-4);
}

.sec__head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: var(--csp-space-3);
  margin-bottom: var(--csp-space-2);
}

.sec__label {
  font-weight: var(--csp-font-weight-bold);
}

.sec__opt {
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}

.sec__tag {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
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

  &--error {
    box-shadow: inset 0 -2px 0 0 var(--border-plain-error);
  }
}

.sec__error {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
  margin: var(--csp-space-1) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-default-error);
}

.sec__tools {
  margin: var(--csp-space-1) 0 0 calc(-1 * var(--csp-space-2));
}

.sugg {
  margin-top: var(--csp-space-2);
  padding: var(--csp-space-3) var(--csp-space-4);
  background: var(--background-alt-blue-france);
  font-size: var(--csp-font-size-sm);

  p {
    margin: 0;
  }
}

.sugg__title {
  font-weight: var(--csp-font-weight-bold);
}

.sugg__text {
  margin: var(--csp-space-2) 0 var(--csp-space-3) !important;
  white-space: pre-line;
}

.sugg__actions {
  display: flex;
  gap: var(--csp-space-2);
}
</style>
