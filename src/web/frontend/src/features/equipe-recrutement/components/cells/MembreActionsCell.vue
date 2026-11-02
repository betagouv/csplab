<script setup lang="ts">
import type { MembreEquipe } from '../../types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { formatAgentLabel } from '@/features/agents/format'
import { useMembreEquipeActions } from '../../composables/useMembreEquipeActions'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: MembreEquipe
}>()

const { revocation, roleChange } = useMembreEquipeActions()

const membreLabel = computed(() => formatAgentLabel(props.row))

const sections = computed(() => [
  {
    items: [
      {
        label: 'Modifier les droits d\'accès',
        icon: 'ri:shield-user-line',
        onSelect: () => roleChange.request(props.row),
      },
    ],
  },
  {
    items: [
      {
        label: 'Retirer de l\'équipe',
        icon: 'ri:user-unfollow-line',
        destructive: true,
        onSelect: () => revocation.request(props.row),
      },
    ],
  },
])
</script>

<template>
  <div class="membre-actions-cell">
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
          :aria-label="`Actions pour ${membreLabel}`"
        />
      </template>
    </CspDropdownMenu>
  </div>
</template>

<style scoped lang="scss">
.membre-actions-cell {
  display: flex;
  justify-content: flex-end;
}
</style>
