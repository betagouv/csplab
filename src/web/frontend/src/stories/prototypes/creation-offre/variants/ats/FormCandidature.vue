<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import ListEditor from '../../shared/ListEditor.vue'
import Panel from '../../shared/Panel.vue'
import { PIECES } from './store'

// Étape 3 — formulaire de candidature : mode de candidature, pièces demandées, questions libres.
const props = defineProps<{ offre: Offre }>()
const o = computed(() => props.offre)

const MODES = [
  { value: 'ats', label: 'Dans l\'ATS (par défaut)' },
  { value: 'courriel', label: 'Par courriel' },
  { value: 'externe', label: 'Sur un site externe' },
]
const EXIGENCES = [
  { value: 'non', label: 'Non demandé' },
  { value: 'facultatif', label: 'Facultatif' },
  { value: 'obligatoire', label: 'Obligatoire' },
]
</script>

<template>
  <Panel
    titre="Mode de candidature"
    description="Dans l'ATS, les candidatures arrivent directement dans le suivi du recrutement."
  >
    <CspRadioGroup
      v-model="o.modeCandidature"
      label="Les candidats postulent"
      :options="MODES"
    />
    <CspInput
      v-if="o.modeCandidature === 'courriel'"
      v-model="o.courrielCandidature"
      label="Adresse de réception des candidatures"
      placeholder="recrutement@exemple.gouv.fr"
    />
    <CspInput
      v-if="o.modeCandidature === 'externe'"
      v-model="o.urlCandidature"
      label="Lien du bouton « Postuler »"
      placeholder="https://"
    />
  </Panel>

  <Panel
    titre="Pièces demandées"
    description="Pour chaque pièce : non demandée, facultative ou obligatoire."
  >
    <div class="pieces">
      <div
        v-for="p in PIECES"
        :key="p.id"
        class="piece"
      >
        <span class="piece__nom">{{ p.label }}</span>
        <CspSegmentedControl
          v-model="o.pieces[p.id]"
          :legend="p.label"
          hide-legend
          size="sm"
          :options="EXIGENCES"
        />
      </div>
    </div>
  </Panel>

  <Panel
    titre="Questions aux candidats (facultatif)"
    :description="o.modeCandidature === 'ats' ? 'Réponse en texte libre, au moment de la candidature.' : 'Disponible seulement si la candidature se fait dans l\'ATS.'"
  >
    <ListEditor
      v-model="o.questions"
      label="Questions libres"
      placeholder="Ex. : Quelle expérience avez-vous de la paie publique ?"
      add-label="Ajouter une question"
      :disabled="o.modeCandidature !== 'ats'"
    />
  </Panel>
</template>

<style scoped lang="scss">
.pieces {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.piece {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--csp-space-4);
  padding-bottom: var(--csp-space-3);
  border-bottom: 1px solid var(--border-default-grey);

  &:last-child {
    border-bottom: 0;
    padding-bottom: 0;
  }
}

.piece__nom {
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}
</style>
