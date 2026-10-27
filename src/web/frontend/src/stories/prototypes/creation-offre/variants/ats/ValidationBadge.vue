<script setup lang="ts">
import type { EtatValidation, Offre } from './store'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import { LIBELLES_VALIDATION } from './store'

// État de la validation d'une offre, suivi à part de son statut.
defineProps<{ offre: Offre }>()

const TYPES: Record<EtatValidation, 'info' | 'new' | 'warning' | 'success'> = {
  non_demandee: 'info',
  en_attente: 'new',
  validee: 'success',
  refusee: 'warning',
}
</script>

<template>
  <CspBadge
    :label="`Validation : ${LIBELLES_VALIDATION[offre.validationEtat].toLowerCase()}${offre.modifieeDepuisValidation ? ' · modifiée depuis' : ''}`"
    :type="TYPES[offre.validationEtat]"
    :variant="offre.validationEtat === 'non_demandee' ? 'outline' : 'soft'"
    size="sm"
  />
</template>
