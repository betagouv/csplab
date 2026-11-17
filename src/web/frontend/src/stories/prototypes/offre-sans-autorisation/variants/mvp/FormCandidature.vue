<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import ListEditor from '../../shared/ListEditor.vue'
import { PIECES } from './store'

// Section « Formulaire de candidature » : pièces demandées, questions libres. Les candidats postulent
// toujours dans l'ATS (plus de choix « par courriel » ni « sur un site externe »).
// Une fois l'offre publiée, ce qui est demandé aux candidats est verrouillé (des candidats ont déjà postulé).
const props = defineProps<{ offre: Offre, verrouille?: boolean }>()
const o = computed(() => props.offre)

const EXIGENCES = [
  { value: 'non', label: 'Non demandé' },
  { value: 'facultatif', label: 'Facultatif' },
  { value: 'obligatoire', label: 'Obligatoire' },
]
</script>

<template>
  <p
    v-if="verrouille"
    class="verrou"
  >
    Offre publiée : les pièces demandées ne peuvent plus changer, des candidats ont déjà postulé.
  </p>
  <div class="groupe">
    <h3 class="groupe__titre">
      Mode de candidature
    </h3>
    <p class="groupe__desc">
      Les candidats postulent dans l'ATS : les candidatures arrivent directement dans le suivi du recrutement.
    </p>
  </div>

  <div class="groupe">
    <h3 class="groupe__titre">
      Pièces demandées
    </h3>
    <p class="groupe__desc">
      Pour chaque pièce : non demandée, facultative ou obligatoire.
    </p>
    <div class="pieces">
      <div
        v-for="p in PIECES"
        :key="p.id"
        class="piece"
      >
        <span class="piece__nom">{{ p.label }}</span>
        <span
          v-if="verrouille"
          class="piece__valeur"
        >{{ EXIGENCES.find(e => e.value === o.pieces[p.id])?.label }}</span>
        <CspSegmentedControl
          v-else
          v-model="o.pieces[p.id]"
          :legend="p.label"
          hide-legend
          size="sm"
          :options="EXIGENCES"
        />
      </div>
    </div>
  </div>

  <div class="groupe">
    <h3 class="groupe__titre">
      Questions aux candidats
    </h3>
    <p class="groupe__desc">
      Réponse en texte libre, au moment de la candidature.
    </p>
    <ListEditor
      v-model="o.questions"
      label="Questions libres"
      placeholder="Ex. : Quelle expérience avez-vous de la paie publique ?"
      add-label="Ajouter une question"
    />
  </div>
</template>

<style scoped lang="scss">
.groupe {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  max-width: 60rem;

  & + & {
    margin-top: var(--csp-space-3);
    padding-top: var(--csp-space-6);
    border-top: 1px solid var(--border-default-grey);
  }
}

.groupe__titre {
  margin: 0;
  font-size: 1.125rem;
  font-weight: var(--csp-font-weight-bold);
  line-height: 1.4;
  color: var(--text-title-grey);
}

.groupe__desc {
  margin: calc(-1 * var(--csp-space-2)) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.verrou {
  margin: 0;
  padding: var(--csp-space-3) var(--csp-space-4);
  border-left: 3px solid var(--border-plain-grey);
  background: var(--background-alt-grey);
  font-size: var(--csp-font-size-sm);
}

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

.piece__valeur {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.piece__nom {
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-bold);
}
</style>
