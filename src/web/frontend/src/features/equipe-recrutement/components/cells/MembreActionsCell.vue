<script setup lang="ts">
import type { MembreEquipe } from '../../types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { useMembreEquipeActions } from '../../composables/useMembreEquipeActions'
import { formatMembreLabel } from '../../format'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: MembreEquipe
}>()

const { requestRevocation } = useMembreEquipeActions()

const membreLabel = computed(() => formatMembreLabel(props.row))

const sections = computed(() => [
  {
    items: [
      {
        label: 'Retirer de l\'équipe',
        icon: 'ri:user-unfollow-line',
        destructive: true,
        onSelect: () => requestRevocation(props.row),
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
