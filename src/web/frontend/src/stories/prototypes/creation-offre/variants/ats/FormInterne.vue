<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import FieldRow from '../../shared/FieldRow.vue'
import ChampOffre from './ChampOffre.vue'
import { MOTIFS_DEPART, MOTIFS_RECRUTEMENT } from './store'

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
  </div>
</template>

<style scoped lang="scss">
.interne {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  max-width: 48rem;
}
</style>
