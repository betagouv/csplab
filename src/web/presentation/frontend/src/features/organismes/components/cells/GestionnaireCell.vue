<script setup lang="ts">
import type { OrganismeAdmin } from '../../types'
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: OrganismeAdmin
}>()

const gestionnaireLabel = computed(() => {
  const g = props.row.gestionnaire
  return g ? `${g.prenom} ${g.nom}` : null
})
</script>

<template>
  <CspBadge
    v-if="gestionnaireLabel"
    variant="soft"
    size="sm"
    :label="gestionnaireLabel"
  />
  <CspButton
    v-else
    variant="secondary"
    size="sm"
    label="Assigner un gestionnaire"
    disabled
  />
</template>
