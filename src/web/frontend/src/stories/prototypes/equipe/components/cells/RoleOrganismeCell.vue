<script setup lang="ts">
import type { ProtoAgent } from '../../data/mock'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import { ROLE_ORGANISME_LABELS } from '../../data/mock'

defineOptions({ inheritAttrs: false })

defineProps<{
  row: ProtoAgent
}>()
</script>

<template>
  <CspBadge
    v-if="row.roleOrganisme === 'gestionnaire'"
    size="sm"
    variant="soft"
    type="info"
    icon="ri:shield-user-line"
    :label="ROLE_ORGANISME_LABELS[row.roleOrganisme]"
  />
  <CspBadge
    v-else
    size="sm"
    variant="soft"
    :label="ROLE_ORGANISME_LABELS[row.roleOrganisme]"
  />
</template>
