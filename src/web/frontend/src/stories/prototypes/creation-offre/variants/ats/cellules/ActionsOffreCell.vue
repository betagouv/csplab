<script setup lang="ts">
import type { Offre } from '../store'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { useNav } from '../nav'

defineOptions({ inheritAttrs: false })

const props = defineProps<{ row: Offre }>()
const { aller } = useNav()

const sections = [{
  items: [
    { label: 'Voir l’offre', icon: 'ri:file-list-3-line', onSelect: () => aller({ nom: 'offre', id: props.row.id }) },
    { label: 'Afficher comme les candidats', icon: 'ri:eye-line', onSelect: () => aller({ nom: 'apercu', id: props.row.id }) },
    { label: 'Voir la fiche de poste', icon: 'ri:file-text-line', onSelect: () => aller({ nom: 'fiche', id: props.row.ficheId }) },
    { label: 'Dupliquer l’offre', icon: 'ri:file-copy-2-line', onSelect: () => aller({ nom: 'creation', mode: 'duplication', offreId: props.row.id }) },
  ],
}]
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
