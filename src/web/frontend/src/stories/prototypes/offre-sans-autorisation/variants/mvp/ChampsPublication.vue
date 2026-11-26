<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import { manquesDates } from './aide'
import ChampDate from './ChampDate.vue'
import { aujourdhui, dateLongue, plusUnMois, SUPPORT_MAITRE } from './store'

// Publication (doc PO) : l'offre est mise en ligne le jour où on publie (pas de programmation). Date de fin de
// publication, qui vaut date limite de candidature (au moins un mois, sauf urgence). Saisies au moment de
// publier, pas dans le formulaire de l'offre. La multidiffusion n'est pas annoncée (retour PO, F11).
const props = defineProps<{ offre: Offre, tentative?: boolean }>()
const o = computed(() => props.offre)
if (!o.value.dateFin) {
  o.value.dateFin = plusUnMois(aujourdhui())
}
const erreur = computed(() => (props.tentative ? manquesDates(o.value)[0] : undefined))
</script>

<template>
  <div class="champs">
    <p class="mention mention--haut">
      Publication sur {{ SUPPORT_MAITRE.nom }}. L'offre est mise en ligne dès que vous publiez.
    </p>
    <ChampDate
      v-model="o.dateFin"
      label="Date de fin de publication"
      hint="Champ obligatoire · au moins un mois après aujourd'hui"
      :error="Boolean(erreur)"
      :error-message="erreur"
    />
    <p
      v-if="o.dateFin"
      class="mention"
    >
      En ligne jusqu'au {{ dateLongue(o.dateFin) }}.
      C'est aussi la date limite de candidature : l'offre sera retirée automatiquement ce jour-là. Vous pourrez la prolonger.
    </p>
    <CspCheckbox
      v-model="o.urgence"
      label="Recrutement urgent : publier moins d'un mois (article D311-2)"
    />
  </div>
</template>

<style scoped lang="scss">
.champs {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.mention {
  margin: calc(-1 * var(--csp-space-2)) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);

  &--haut {
    margin: 0;
    font-size: var(--csp-font-size-sm);
  }
}
</style>
