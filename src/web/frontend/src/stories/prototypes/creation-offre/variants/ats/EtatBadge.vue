<script setup lang="ts">
import type { EtatOffre } from './store'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import { LIBELLES_ETAT } from './store'

// État d'une offre, toujours présenté de la même façon (listes, détail, en-tête).
defineProps<{ etat: EtatOffre, size?: 'sm' | 'md' }>()

const TYPES: Record<EtatOffre, 'info' | 'new' | 'warning' | 'error' | 'success'> = {
  redaction: 'info',
  validation: 'new',
  a_publier: 'warning',
  publiee: 'success',
  archivee: 'info',
}
</script>

<template>
  <CspBadge
    :label="LIBELLES_ETAT[etat]"
    :type="TYPES[etat]"
    :variant="etat === 'archivee' ? 'outline' : 'soft'"
    :size="size ?? 'sm'"
  />
</template>
