<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspCheckboxGroup from '@/components/base/CspCheckboxGroup/CspCheckboxGroup.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import { db, UTILISATEUR } from './store'

// « Paramétrer le recrutement », 2e étape de la publication (retour PO) : responsable, équipe et notifications
// concernent le recrutement qui s'ouvre, pas la rédaction de l'offre. On ne les demande donc qu'ici.
const props = defineProps<{ offre: Offre }>()
const o = computed(() => props.offre)

const AGENTS = computed(() => db.organisme.agents.map(a => a.nom))
const responsable = computed({
  get: () => o.value.equipe.find(m => m.role === 'Responsable')?.nom ?? UTILISATEUR,
  set: (nom: string) => {
    o.value.equipe = [{ nom, role: 'Responsable' as const }, ...o.value.equipe.filter(m => m.role !== 'Responsable' && m.nom !== nom)]
  },
})
const recruteurs = computed({
  get: () => o.value.equipe.filter(m => m.role !== 'Responsable').map(m => m.nom),
  set: (noms: string[]) => {
    o.value.equipe = [{ nom: responsable.value, role: 'Responsable' as const }, ...noms.filter(n => n !== responsable.value).map(nom => ({ nom, role: 'Recruteur' as const }))]
  },
})
const OPTIONS_RESPONSABLE = computed(() => AGENTS.value.map(n => ({ value: n, label: n })))
const OPTIONS_EQUIPE = computed(() => AGENTS.value.filter(n => n !== responsable.value).map(n => ({ value: n, label: n })))
const FREQ = [
  { value: 'chaque', label: 'À chaque candidature' },
  { value: 'cinq', label: 'Toutes les 5 candidatures' },
  { value: 'quotidien', label: 'Un récapitulatif par jour' },
  { value: 'aucune', label: 'Jamais' },
]
</script>

<template>
  <div class="parametres">
    <CspSelect
      v-model="responsable"
      label="Responsable du recrutement"
      hint="Reçoit les candidatures et suit le recrutement."
      :options="OPTIONS_RESPONSABLE"
    />
    <CspCheckboxGroup
      v-model="recruteurs"
      label="Équipe de recrutement (facultatif)"
      hint="Ces personnes pourront consulter et évaluer les candidatures."
      :options="OPTIONS_EQUIPE"
      size="sm"
    />
    <CspRadioGroup
      v-model="o.notifications"
      label="Notifications par courriel pour les nouvelles candidatures"
      :options="FREQ"
      size="sm"
    />
  </div>
</template>

<style scoped lang="scss">
.parametres {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}
</style>
