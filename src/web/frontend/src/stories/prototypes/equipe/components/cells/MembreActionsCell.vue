<script setup lang="ts">
import type { ProtoAgent, ProtoMembre, RoleOffre } from '../../data/mock'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { ROLE_OFFRE_LABELS } from '../../data/mock'
import { useEquipePrototypeContext } from '../../shared/context'
import { formatAgentNom } from '../../shared/format'
import { useMembreActions } from '../useMembreActions'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: { agent: ProtoAgent, membre: ProtoMembre, recrutementUuid: string }
}>()

const proto = useEquipePrototypeContext()
const { demanderRetrait } = useMembreActions()

const ROLE_ICONS: Record<RoleOffre, string> = {
  responsable: 'ri:shield-user-line',
  recruteur: 'ri:user-star-line',
  contributeur: 'ri:user-line',
}

const sections = computed(() => {
  const rolesProposes = (Object.keys(ROLE_OFFRE_LABELS) as RoleOffre[])
    .filter(role => role !== props.row.membre.roleOffre)
    .filter(role => role !== 'responsable' || proto.peutAssignerResponsables.value)
  const roleItems = rolesProposes.map(role => ({
    label: `Passer ${ROLE_OFFRE_LABELS[role].toLowerCase()}`,
    icon: ROLE_ICONS[role],
    onSelect: () => proto.modifierRoleOffre(props.row.recrutementUuid, props.row.agent.uuid, role),
  }))
  const invitationItems = props.row.agent.statut === 'en_attente'
    ? [{
        label: 'Renvoyer l\'invitation',
        icon: 'ri:mail-send-line',
        onSelect: () => proto.renvoyerInvitation(props.row.agent.uuid),
      }]
    : []
  return [
    { items: [...roleItems, ...invitationItems] },
    {
      items: [{
        label: 'Retirer de l\'équipe',
        icon: 'ri:user-unfollow-line',
        destructive: true,
        onSelect: () => demanderRetrait({ recrutementUuid: props.row.recrutementUuid, agent: props.row.agent }),
      }],
    },
  ]
})
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
          :aria-label="`Actions pour ${formatAgentNom(row.agent)}`"
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
