<script setup lang="ts">
import type { ProtoRecrutement } from '../../data/mock'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { useEquipePrototypeContext } from '../../shared/context'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: ProtoRecrutement
}>()

const proto = useEquipePrototypeContext()

const sections = computed(() => {
  const equipeItem = {
    label: proto.peutGererEquipe(props.row.uuid) ? 'Gérer l\'équipe de recrutement' : 'Voir l\'équipe de recrutement',
    icon: 'ri:team-line',
    onSelect: () => proto.goParametresRecrutement(props.row.uuid),
  }
  const assignationItems = proto.peutAssignerResponsables.value && !props.row.archive
    ? [{
        label: 'Assigner un responsable',
        icon: 'ri:user-add-line',
        onSelect: () => proto.demanderAssignation([props.row.uuid]),
      }]
    : []
  return [{ items: [equipeItem, ...assignationItems] }]
})
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
