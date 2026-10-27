<script setup lang="ts">
import type { Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import { useNav } from './nav'
import { db, demanderValidation } from './store'

// « Demander la validation » : disponible à toutes les étapes, dès le brouillon, sans champ obligatoire.
// On continue à rédiger l'offre pendant la validation.
const props = defineProps<{ offre: Offre, variant?: 'primary' | 'secondary' }>()
const emit = defineEmits<{ demandee: [] }>()
const { notifier } = useNav()

const visible = computed(() => db.organisme.validationActive && props.offre.etat === 'brouillon'
  && (props.offre.validationEtat === 'non_demandee' || props.offre.validationEtat === 'refusee'))
const ouvert = ref(false)
const acquis = computed(() => (props.offre.validations ?? []).filter(v => v.decision === 'accord').map(v => v.nom))

function confirmer() {
  ouvert.value = false
  demanderValidation(props.offre)
  notifier('Validation demandée. Vous pouvez continuer à modifier l\'offre.')
  emit('demandee')
}
</script>

<template>
  <template v-if="visible">
    <CspButton
      :label="offre.validationEtat === 'refusee' ? 'Redemander la validation' : 'Demander la validation'"
      :variant="variant ?? 'secondary'"
      icon="ri:send-plane-line"
      is-icon-left
      @click="ouvert = true"
    />
    <CspDialog
      v-model:open="ouvert"
      title="Demander la validation ?"
      size="sm"
    >
      <p class="texte">
        La demande part en parallèle à chaque validation du circuit ; l'accord d'un seul valideur suffit pour chacune.
        Vous pourrez continuer à modifier l'offre pendant la validation.
      </p>
      <ul class="liste">
        <li
          v-for="g in db.organisme.groupes"
          :key="g.nom"
        >
          <strong>{{ g.nom }}</strong> — {{ g.valideurs.join(', ') || 'aucun valideur désigné' }}
          <em v-if="acquis.includes(g.nom)"> (accord déjà acquis)</em>
        </li>
      </ul>
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="ouvert = false"
        />
        <CspButton
          label="Demander la validation"
          icon="ri:send-plane-line"
          is-icon-left
          @click="confirmer"
        />
      </template>
    </CspDialog>
  </template>
</template>

<style scoped lang="scss">
.texte {
  margin: 0 0 var(--csp-space-3);
  font-size: var(--csp-font-size-sm);
}

.liste {
  margin: 0;
  padding-left: var(--csp-space-5);
  font-size: var(--csp-font-size-sm);
}
</style>
