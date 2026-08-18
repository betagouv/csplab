<script setup lang="ts">
import type { OrganismeAdmin } from '../../types'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { useOrganismeEdition } from '../../composables/useOrganismeEdition'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: OrganismeAdmin
}>()

const { openEdition } = useOrganismeEdition()
</script>

<template>
  <CspButton
    variant="tertiary-no-outline"
    size="sm"
    icon="ri:pencil-line"
    :aria-label="`Modifier l'organisme ${props.row.nom}`"
    @click="openEdition(props.row)"
  />
</template>
