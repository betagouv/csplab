<script setup lang="ts">
import type { AgentOrganisme } from '../../types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { useAgentActions } from '../../composables/useAgentActions'
import { formatAgentName } from '../../format'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: AgentOrganisme
}>()

const { roleChange, revocation } = useAgentActions()

const sections = computed(() => [
  {
    items: [
      props.row.role === 'superviseur'
        ? {
            label: 'Passer membre',
            icon: 'ri:user-line',
            onSelect: () => roleChange.request({ agent: props.row, role: 'agent' }),
          }
        : {
            label: 'Passer responsable',
            icon: 'ri:shield-user-line',
            onSelect: () => roleChange.request({ agent: props.row, role: 'superviseur' }),
          },
    ],
  },
  {
    items: [
      {
        label: 'Révoquer',
        icon: 'ri:user-unfollow-line',
        destructive: true,
        onSelect: () => revocation.request(props.row),
      },
    ],
  },
])
</script>

<template>
  <div class="agent-actions-cell">
    <CspDropdownMenu
      :sections="sections"
      side="bottom"
      align="end"
    >
      <template #trigger>
        <CspButton
          icon="ri:more-2-fill"
          variant="tertiary-no-outline"
          size="sm"
          :aria-label="`Actions pour ${formatAgentName(row)}`"
        />
      </template>
    </CspDropdownMenu>
  </div>
</template>

<style scoped lang="scss">
.agent-actions-cell {
  display: flex;
  justify-content: flex-end;
}
</style>
