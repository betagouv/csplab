<script setup lang="ts">
import type { ProtoRecrutement } from '../../data/mock'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import { useEquipePrototypeContext } from '../../shared/context'
import { formatAgentNom } from '../../shared/format'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: ProtoRecrutement
}>()

const proto = useEquipePrototypeContext()

const noms = computed(() => proto.responsablesDe(props.row).map(formatAgentNom))
</script>

<template>
  <span v-if="noms.length">{{ noms.join(', ') }}</span>
  <CspButton
    v-else-if="proto.peutAssignerResponsables.value && !row.archive"
    label="Assigner un responsable"
    variant="tertiary"
    size="sm"
    icon="ri:user-add-line"
    is-icon-left
    @click="proto.demanderAssignation([row.uuid])"
  />
  <span
    v-else
    class="responsables-cell__none"
  >Aucun responsable</span>
</template>

<style scoped lang="scss">
.responsables-cell__none {
  color: var(--text-mention-grey);
}
</style>
