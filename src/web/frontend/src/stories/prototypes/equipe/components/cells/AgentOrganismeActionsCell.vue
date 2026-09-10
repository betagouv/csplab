<script setup lang="ts">
import type { ProtoAgent } from '../../data/mock'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { useEquipePrototypeContext } from '../../shared/context'
import { formatAgentNom } from '../../shared/format'
import { useMembreActions } from '../useMembreActions'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: ProtoAgent
}>()

const proto = useEquipePrototypeContext()
const { demanderRevocation } = useMembreActions()

const isMoi = computed(() => proto.agentCourant.value?.uuid === props.row.uuid)

const sections = computed(() => {
  const roleItem = props.row.roleOrganisme === 'gestionnaire'
    ? {
        label: 'Passer agent',
        icon: 'ri:user-line',
        onSelect: () => proto.modifierRoleOrganisme(props.row.uuid, 'agent'),
      }
    : {
        label: proto.peutPromouvoirGestionnaire.value ? 'Passer gestionnaire' : 'Passer gestionnaire (administrateur uniquement)',
        icon: 'ri:shield-user-line',
        disabled: !proto.peutPromouvoirGestionnaire.value,
        onSelect: () => proto.modifierRoleOrganisme(props.row.uuid, 'gestionnaire'),
      }
  const invitationItems = props.row.statut === 'en_attente'
    ? [{
        label: 'Renvoyer l\'invitation',
        icon: 'ri:mail-send-line',
        onSelect: () => proto.renvoyerInvitation(props.row.uuid),
      }]
    : []
  return [
    { items: [roleItem, ...invitationItems] },
    {
      items: [{
        label: 'Révoquer les accès',
        icon: 'ri:user-unfollow-line',
        destructive: true,
        onSelect: () => demanderRevocation(props.row),
      }],
    },
  ]
})
</script>

<template>
  <div
    v-if="!isMoi"
    class="agent-actions-cell"
  >
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
          :aria-label="`Actions pour ${formatAgentNom(row)}`"
        />
      </template>
    </CspDropdownMenu>
  </div>
</template>

<style scoped lang="scss">
.agent-actions-cell {
  display: flex;
  justify-content: flex-end;
}
</style>
