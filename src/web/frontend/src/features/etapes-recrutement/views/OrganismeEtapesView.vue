<script setup lang="ts">
import EtapesRecrutementSection from '../components/EtapesRecrutementSection.vue'
import { ETAPES_TEXTS_ORGANISME } from '../constants/etape-recrutement'

defineProps<{
  organismeUuid: string
}>()
</script>

<template>
  <EtapesRecrutementSection
    :params="{ type: 'organisme', organismeUuid }"
    :texts="ETAPES_TEXTS_ORGANISME"
  />
</template>
