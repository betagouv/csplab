<script setup lang="ts">
import type { ProtoMembre } from '../../data/mock'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import { ROLE_OFFRE_LABELS } from '../../data/mock'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: { membre: ProtoMembre }
}>()
</script>

<template>
  <CspBadge
    v-if="row.membre.roleOffre === 'responsable'"
    size="sm"
    variant="soft"
    type="info"
    icon="ri:shield-user-line"
    :label="ROLE_OFFRE_LABELS[row.membre.roleOffre]"
  />
  <CspBadge
    v-else
    size="sm"
    variant="soft"
    :label="ROLE_OFFRE_LABELS[row.membre.roleOffre]"
  />
</template>
