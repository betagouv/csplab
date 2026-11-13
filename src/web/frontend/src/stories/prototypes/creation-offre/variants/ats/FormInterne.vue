<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import FieldRow from '../../shared/FieldRow.vue'
import ChampOffre from './ChampOffre.vue'
import { db, MOTIFS_DEPART, MOTIFS_RECRUTEMENT } from './store'

// Section « Informations internes » (retour PO) : séparée de l'annonce pour qu'on voie d'un coup d'œil
// ce que le candidat ne verra jamais. Ces informations alimentent le résumé pour les valideurs.
// Jamais publiées, jamais reprises d'une fiche ni d'une offre dupliquée.
const props = defineProps<{ offre: Offre }>()
const o = computed(() => props.offre)

function modele(cle: 'motifRecrutement' | 'motifDepart' | 'groupeRifseep') {
  return computed({
    get: () => o.value[cle] || 'aucun',
    set: (v: string) => (o.value[cle] = v === 'aucun' ? '' : v),
  })
}
const motif = modele('motifRecrutement')
const depart = modele('motifDepart')
const rifseep = modele('groupeRifseep')
const avecAgent = computed(() => ['Remplacement', 'Renouvellement'].includes(o.value.motifRecrutement))
// Validation : qui va valider l'offre (circuit de l'organisme) et un commentaire facultatif,
// adressé à tous les services validateurs ou seulement à certains.
const avecValidation = computed(() => db.organisme.validationActive && db.organisme.groupes.length > 0)
const OPTIONS_SERVICES = computed(() => db.organisme.groupes.map(g => ({ value: g.nom, label: g.nom })))
const pour = computed({
  get: () => o.value.commentairePour?.length ? o.value.commentairePour : db.organisme.groupes.map(g => g.nom),
  set: (v: string[]) => (o.value.commentairePour = v.length === db.organisme.groupes.length ? [] : v),
})
function joindre(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (f) {
    o.value.ficheJointe = f.name
  }
}
const optsInternes = (l: string[]) => [{ value: 'aucun', label: 'Non renseigné' }, ...l.map(v => ({ value: v, label: v }))]
</script>

<template>
  <div class="interne">
    <FieldRow :cols="2">
      <CspInput
        v-model="o.referenceInterne"
        label="Référence interne (facultatif)"
      />
      <CspInput
        v-model="o.referenceFranceTravail"
        label="Référence France Travail (facultatif)"
      />
    </FieldRow>
    <FieldRow :cols="2">
      <CspInput
        v-model="o.codePoste"
        label="Code poste (facultatif)"
      />
    </FieldRow>
    <FieldRow :cols="2">
      <CspSelect
        v-model="motif"
        label="Motif de recrutement (facultatif)"
        :options="optsInternes(MOTIFS_RECRUTEMENT)"
      />
      <CspSelect
        v-model="depart"
        label="Motif de départ (facultatif)"
        :options="optsInternes(MOTIFS_DEPART)"
      />
    </FieldRow>
    <CspInput
      v-if="avecAgent"
      v-model="o.agentRemplace"
      label="Agent remplacé ou renouvelé (facultatif)"
    />
    <FieldRow :cols="2">
      <CspSelect
        v-model="rifseep"
        label="Groupe RIFSEEP (facultatif)"
        :options="optsInternes(['Groupe 1', 'Groupe 2', 'Groupe 3', 'Groupe 4'])"
      />
      <ChampOffre
        :offre="o"
        champ="cycleTravail"
        label="Cycle de travail (facultatif)"
        for-id="a-cycle"
      >
        <CspInput
          id="a-cycle"
          v-model="o.cycleTravail"
          placeholder="Ex. : 38 h 30 sur 5 jours"
        />
      </ChampOffre>
    </FieldRow>

    <div
      v-if="avecValidation"
      class="validation"
    >
      <h3 class="validation__titre">
        Validation
      </h3>
      <div>
        <p class="validation__label">
          Qui va valider l'offre
        </p>
        <ul class="validation__liste">
          <li
            v-for="g in db.organisme.groupes"
            :key="g.nom"
          >
            <strong>{{ g.nom }}</strong> : {{ g.valideurs.join(', ') || 'aucun valideur désigné' }}
          </li>
        </ul>
        <p class="validation__aide">
          Circuit défini dans les paramètres de l'organisme. L'accord d'un seul valideur suffit pour chaque service.
        </p>
      </div>
      <CspTextarea
        v-model="o.commentaireValideurs"
        label="Commentaire pour les valideurs (facultatif)"
        hint="Contexte utile pour décider, par ex. « Remplacement à l'identique, poste budgété »."
        :rows="3"
      />
      <CspCheckboxGroup
        v-if="o.commentaireValideurs.trim() && OPTIONS_SERVICES.length > 1"
        v-model="pour"
        label="Commentaire adressé à"
        :options="OPTIONS_SERVICES"
        size="sm"
      />
      <label class="ajout">
        <CspIcon
          name="ri:attachment-2"
          :size="14"
        /> {{ o.ficheJointe ? `Document joint : ${o.ficheJointe} · remplacer` : 'Joindre un document pour les valideurs (facultatif)' }}
        <input
          type="file"
          class="sr-only"
          @change="joindre"
        >
      </label>
    </div>
  </div>
</template>

<style scoped lang="scss">
.interne {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  max-width: 48rem;
}
.validation {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
  padding-top: var(--csp-space-5);
  border-top: 1px solid var(--border-default-grey);
}

.validation__titre {
  margin: 0;
  font-size: var(--csp-font-size-lg);
}

.validation__label {
  margin: 0 0 var(--csp-space-2);
  font-weight: var(--csp-font-weight-bold);
  font-size: var(--csp-font-size-sm);
}

.validation__liste {
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
}

.validation__aide {
  margin: var(--csp-space-2) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.ajout {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-sm);
  color: var(--text-action-high-blue-france);
  cursor: pointer;

  &:has(:focus-visible) {
    outline: 2px solid var(--csp-focus-ring-color, #0a76f6);
  }
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}
</style>
