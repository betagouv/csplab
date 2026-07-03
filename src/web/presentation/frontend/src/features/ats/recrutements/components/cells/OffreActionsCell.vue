<script setup lang="ts">
import type { RecrutementBase } from '../../types'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: RecrutementBase
  activate?: () => void
}>()

const sections = [{
  items: [{
    label: 'Voir le détail de l’offre',
    icon: 'ri:eye-line',
    onSelect: () => props.activate?.(),
  }],
}]
</script>

<template>
  <div class="offre-actions-cell">
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
          :aria-label="`Actions pour ${row.intitule}`"
        />
      </template>
    </CspDropdownMenu>
  </div>
</template>

<style scoped lang="scss">
.offre-actions-cell {
  display: flex;
  justify-content: flex-end;
}
</style>
