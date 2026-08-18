<script setup lang="ts">
import type { OrganismeAdmin } from '../../types'
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { useGestionnaireAssignation } from '../../composables/useGestionnaireAssignation'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: OrganismeAdmin
}>()

const { openAssignation } = useGestionnaireAssignation()

const gestionnaire = computed(() => props.row.gestionnaire)

const gestionnaireLabel = computed(() =>
  gestionnaire.value ? `${gestionnaire.value.prenom} ${gestionnaire.value.nom}` : null,
)
</script>

<template>
  <span
    v-if="gestionnaireLabel"
    class="gestionnaire-cell"
  >
    {{ gestionnaireLabel }}
    <CspBadge
      v-if="gestionnaire?.invitation_en_attente"
      variant="soft"
      size="sm"
      type="new"
      label="Invitation en attente"
    />
  </span>
  <CspButton
    v-else
    variant="secondary"
    size="sm"
    label="Assigner un gestionnaire"
    @click="openAssignation(props.row)"
  />
</template>

<style scoped lang="scss">
.gestionnaire-cell {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
}
</style>
