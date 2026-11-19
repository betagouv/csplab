<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { dupliquer } from '../dupliquer'
import { useNav } from '../nav'

// Menu « … » d'un recrutement. Prolonger et retirer se font depuis la page de l'offre.
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const { aller, notifier } = useNav()

const sections = computed(() => [
  {
    items: [
      { label: 'Voir les candidatures', icon: 'ri:team-line', onSelect: () => notifier('Simulation : écran des candidatures (outil existant).') },
      { label: 'Voir l’offre publiée', icon: 'ri:file-list-3-line', onSelect: () => aller({ nom: 'offre', id: props.row.id }) },
    ],
  },
  {
    items: [{ label: 'Dupliquer l’offre', icon: 'ri:file-copy-2-line', onSelect: () => dupliquer(props.row, { aller, notifier }) }],
  },
])
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
          icon="ri:more-fill"
          variant="tertiary-no-outline"
          size="sm"
          :aria-label="`Actions pour ${row.titre || row.id}`"
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
