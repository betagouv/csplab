<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import ListEditor from '../../shared/ListEditor.vue'
import { PIECES } from './store'

// Paramétrage des candidatures, en deux étapes : « Formulaire » (questions) et « Documents » (pièces demandées). Les candidats postulent
// toujours dans l'ATS (plus de choix « par courriel » ni « sur un site externe »).
// Une fois l'offre publiée, ce qui est demandé aux candidats est verrouillé (des candidats ont déjà postulé).
const props = defineProps<{ offre: Offre, partie: 'formulaire' | 'documents', verrouille?: boolean }>()
const o = computed(() => props.offre)

// Posées au candidat au moment où il postule : pas de profil candidat à remplir (retour PO, 26/11/2026).
// Posées par défaut. Le switch n'était pas compris (revue UI, 27/11/2026) : deux choix, présentés comme les documents.
const QUESTIONS_FIXES = [
  { id: 'rqth' as const, question: 'Êtes-vous bénéficiaire d\'une RQTH ?', reponses: 'Oui / Non' },
  { id: 'fonctionnaire' as const, question: 'Êtes-vous fonctionnaire ?', reponses: 'Oui / Non' },
]
function affichee(id: 'rqth' | 'fonctionnaire') {
  return o.value.questionsFixes?.[id] !== false
}
function choisir(id: 'rqth' | 'fonctionnaire', v: string) {
  o.value.questionsFixes = { ...o.value.questionsFixes, [id]: v === 'posee' }
}
const AFFICHAGES = [
  { value: 'non', label: 'Non posée' },
  { value: 'posee', label: 'Posée' },
]
// Partie 3 « Diffusion » : si les candidatures sont gérées hors de l'ATS, il n'y a rien à paramétrer ici.
const horsAts = computed(() => o.value.modeCandidature !== 'ats')

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
    Offre publiée : ce qui est demandé aux candidats ne peut plus changer, des candidats ont déjà postulé.
  </p>
  <p
    v-if="horsAts"
    class="verrou"
  >
    Candidatures gérées hors de l'ATS (choix fait dans la partie « Diffusion ») : ces paramètres ne s'appliquent pas.
  </p>

  <div
    v-if="partie === 'documents'"
    class="groupe"
  >
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

  <div
    v-if="partie === 'formulaire'"
    class="groupe"
  >
    <h3 class="groupe__titre">
      Questions oui / non
    </h3>
    <p class="groupe__desc">
      Posées par défaut. Pour chaque question : non posée ou posée. Le candidat répond par oui ou par non.
    </p>
    <div class="pieces">
      <div
        v-for="q in QUESTIONS_FIXES"
        :key="q.question"
        class="piece"
      >
        <span class="piece__nom">{{ q.question }}</span>
        <span
          v-if="verrouille"
          class="piece__valeur"
        >{{ affichee(q.id) ? 'Posée' : 'Non posée' }}</span>
        <CspSegmentedControl
          v-else
          :model-value="affichee(q.id) ? 'posee' : 'non'"
          :legend="q.question"
          hide-legend
          size="sm"
          :options="AFFICHAGES"
          @update:model-value="(v: string) => choisir(q.id, v)"
        />
      </div>
    </div>
  </div>

  <div
    v-if="partie === 'formulaire'"
    class="groupe"
  >
    <h3 class="groupe__titre">
      Questions aux candidats
    </h3>
    <p class="groupe__desc">
      Réponse en texte libre, au moment de la candidature.
    </p>
    <p
      v-if="verrouille"
      class="piece__valeur"
    >
      {{ o.questions.length ? o.questions.join(' · ') : 'Aucune question' }}
    </p>
    <ListEditor
      v-else
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
