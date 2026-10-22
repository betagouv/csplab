<script setup lang="ts">
import type { Fiche } from '../store'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { useNav } from '../nav'

defineOptions({ inheritAttrs: false })

const props = defineProps<{ row: Fiche }>()
const { aller } = useNav()

const sections = [{
  items: [
    { label: 'Voir la fiche de poste', icon: 'ri:eye-line', onSelect: () => aller({ nom: 'fiche', id: props.row.id }) },
    { label: 'Lancer un recrutement', icon: 'ri:add-line', onSelect: () => aller({ nom: 'creation', mode: 'fiche', ficheId: props.row.id }) },
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
          :aria-label="`Actions pour ${row.intitule || row.id}`"
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
