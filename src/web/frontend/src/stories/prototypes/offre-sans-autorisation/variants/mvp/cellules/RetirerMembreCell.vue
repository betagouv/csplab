<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'

// Menu « … » d'un membre de l'équipe : le retirer (le dernier Responsable reste).
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: { nom: string, role: string, offre: Offre } }>()
const seulResponsable = computed(() => props.row.role === 'Responsable' && props.row.offre.equipe.filter(m => m.role === 'Responsable').length === 1)
const sections = computed(() => [{
  items: [{
    label: 'Retirer de l’équipe',
    icon: 'ri:user-unfollow-line',
    disabled: seulResponsable.value,
    onSelect: () => {
      const offre = props.row.offre
      offre.equipe = offre.equipe.filter(m => m.nom !== props.row.nom)
    },
  }],
}])
</script>

<template>
  <div class="actions-cell">
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
          :aria-label="`Actions pour ${row.nom}`"
        />
      </template>
    </CspDropdownMenu>
  </div>
</template>

<style scoped lang="scss">
.actions-cell {
  display: flex;
  justify-content: flex-end;
}
</style>
