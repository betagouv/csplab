<script setup lang="ts">
import type { CompteUtilisateur } from '../../types'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { useResendInvitation } from '../../composables/useResendInvitation'

defineOptions({ inheritAttrs: false })

const props = defineProps<{
  row: CompteUtilisateur
}>()

const { openResend } = useResendInvitation()
</script>

<template>
  <CspDropdownMenu
    v-if="props.row.invitation_en_attente"
    side="bottom"
    align="end"
    :sections="[{
      items: [{
        label: 'Renvoyer une invitation',
        icon: 'ri:mail-send-line',
        onSelect: () => openResend(props.row),
      }],
    }]"
  >
    <template #trigger>
      <CspButton
        variant="tertiary-no-outline"
        size="sm"
        icon="ri:more-2-fill"
        :aria-label="`Actions pour ${props.row.prenom} ${props.row.nom}`"
      />
    </template>
  </CspDropdownMenu>
</template>
