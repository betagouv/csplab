<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { useNav } from '../nav'
import { aProlonger, aRetirer } from '../recrutement'
import { archiverOffre, sauvegarder } from '../store'

// Menu « … » d'un recrutement : la vie de l'annonce publiée (prolonger, retirer) se gère ici, plus sur l'offre.
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
    items: props.row.etat === 'publiee'
      ? [
          { label: 'Prolonger la publication', icon: 'ri:calendar-line', onSelect: () => (aProlonger.value = props.row) },
          { label: 'Retirer l’offre', icon: 'ri:stop-circle-line', onSelect: () => (aRetirer.value = props.row) },
        ]
      : props.row.etat === 'retiree'
        ? [{ label: 'Clore le recrutement', icon: 'ri:archive-line', onSelect: () => {
            archiverOffre(props.row)
            sauvegarder()
            notifier('Recrutement clos : il passe dans « Recrutements clos ».')
          } }]
        : [{ label: 'Dupliquer l’offre', icon: 'ri:file-copy-2-line', onSelect: () => aller({ nom: 'creation', mode: 'duplication', offreId: props.row.id }) }],
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
