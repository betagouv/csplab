<script setup lang="ts">
import type { MembreEquipe, RecrutementRole } from '../../types'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { useMembreEquipeActions } from '../../composables/useMembreEquipeActions'
import { RECRUTEMENT_ROLE_LABELS } from '../../constants/equipe-recrutement'
import { formatMembreLabel } from '../../format'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: MembreEquipe
}>()

const { revocation, roleChange } = useMembreEquipeActions()

const ROLE_ICONS: Record<RecrutementRole, string> = {
  responsable: 'ri:shield-user-line',
  recruteur: 'ri:user-star-line',
  contributeur: 'ri:user-line',
}

const membreLabel = computed(() => formatMembreLabel(props.row))

const rolesProposes = computed(() =>
  (Object.keys(RECRUTEMENT_ROLE_LABELS) as RecrutementRole[])
    .filter(role => role !== props.row.recrutement_role),
)

const sections = computed(() => [
  {
    items: rolesProposes.value.map(role => ({
      label: `Passer ${RECRUTEMENT_ROLE_LABELS[role].toLowerCase()}`,
      icon: ROLE_ICONS[role],
      onSelect: () => roleChange.request({ membre: props.row, role }),
    })),
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
