<script setup lang="ts">
import type { ProtoAgent } from '../../data/mock'
import { computed } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import { useEquipePrototypeContext } from '../../shared/context'
import { formatAgentNom } from '../../shared/format'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: ProtoAgent | { agent: ProtoAgent }
}>()

const proto = useEquipePrototypeContext()

const agent = computed(() => ('agent' in props.row ? props.row.agent : props.row))
const isMoi = computed(() => proto.agentCourant.value?.uuid === agent.value.uuid)
</script>

<template>
  <div class="membre-cell">
    <span class="membre-cell__name">
      {{ formatAgentNom(agent) }}
      <span
        v-if="isMoi"
        class="membre-cell__me"
      >(vous)</span>
    </span>
    <CspBadge
      v-if="agent.statut === 'en_attente'"
      size="sm"
      variant="soft"
      type="warning"
      label="Invitation en attente"
    />
  </div>
</template>

<style scoped lang="scss">
.membre-cell {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-1);
}

.membre-cell__name {
  font-weight: 600;
  color: var(--text-title-grey);
}

.membre-cell__me {
  font-weight: var(--csp-font-weight-regular);
  color: var(--text-mention-grey);
}
</style>
