<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import FieldRow from '../../shared/FieldRow.vue'
import { manquesDates } from './aide'
import { dateLongue, plusUnMois, SITES_PARTENAIRES, SUPPORT_MAITRE } from './store'

// Dates et diffusion d'une offre : étape « Publication » du formulaire et page « Publier ».
// Une seule date de fin, qui est aussi la date limite de candidature : un mois minimum, un mois par défaut.
const props = defineProps<{ offre: Offre, tentative?: boolean, disabled?: boolean }>()
const o = computed(() => props.offre)

function changerDebut(v: string | undefined) {
  o.value.dateDebut = v ?? ''
  if (/^\d{4}-\d{2}-\d{2}$/.test(o.value.dateDebut) && !o.value.dateFin) {
    o.value.dateFin = plusUnMois(o.value.dateDebut)
  }
}
const erreurDates = computed(() => (props.tentative ? manquesDates(o.value)[0] : undefined))

const diffusion = computed({
  get: () => o.value.diffusion ?? 'simple',
  set: (v: 'simple' | 'multi') => (o.value.diffusion = v),
})
const DIFFUSIONS = [
  { value: 'simple', label: `Simple diffusion — ${SUPPORT_MAITRE.nom} uniquement` },
  { value: 'multi', label: `Multi-diffusion — ${SUPPORT_MAITRE.nom} et des sites partenaires` },
]
const partenaires = computed({
  get: () => o.value.canaux.filter(c => c !== SUPPORT_MAITRE.id),
  set: (v: string[]) => (o.value.canaux = [SUPPORT_MAITRE.id, ...v]),
})
const OPTIONS_PARTENAIRES = SITES_PARTENAIRES.map(s => ({ value: s.id, label: `${s.nom} — ${s.detail}` }))
const erreurSites = computed(() => props.tentative && diffusion.value === 'multi' && !partenaires.value.length)
defineExpose({ valide: () => !manquesDates(o.value).length && !(diffusion.value === 'multi' && !partenaires.value.length) })
</script>

<template>
  <div class="champs">
    <FieldRow :cols="2">
      <CspInput
        :model-value="o.dateDebut"
        label="Date de début de publication"
        placeholder="AAAA-MM-JJ"
        :disabled="disabled"
        @update:model-value="changerDebut"
      />
      <CspInput
        v-model="o.dateFin"
        label="Date de fin (date limite de candidature)"
        placeholder="AAAA-MM-JJ"
        :disabled="disabled"
        :error="Boolean(erreurDates)"
        :error-message="erreurDates ? `Indiquez les ${erreurDates}.` : undefined"
      />
    </FieldRow>
    <p class="mention">
      <template v-if="o.dateDebut && o.dateFin">
        Du {{ dateLongue(o.dateDebut) }} au {{ dateLongue(o.dateFin) }} : l'offre est retirée automatiquement ce jour-là.
      </template>
      <template v-else>
        La date de fin est aussi la date limite de candidature : un mois après le début par défaut.
      </template>
    </p>
    <CspCheckbox
      v-model="o.urgence"
      label="Recrutement urgent : publier moins d'un mois (article D311-2)"
      :disabled="disabled"
    />
    <CspRadioGroup
      v-model="diffusion"
      label="Type de diffusion"
      :options="DIFFUSIONS"
      :disabled="disabled"
    />
    <CspCheckboxGroup
      v-if="diffusion === 'multi'"
      v-model="partenaires"
      label="Sites partenaires"
      :options="OPTIONS_PARTENAIRES"
      :disabled="disabled"
      :error="erreurSites"
      :error-message="erreurSites ? 'Choisissez au moins un site partenaire.' : undefined"
    />
  </div>
</template>

<style scoped lang="scss">
.champs {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.mention {
  margin: calc(-1 * var(--csp-space-3)) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
