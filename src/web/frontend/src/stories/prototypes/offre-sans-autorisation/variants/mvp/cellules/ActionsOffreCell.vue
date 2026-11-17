<script setup lang="ts">
import type { Offre } from '../store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { useNav } from '../nav'
import { db, retirer, sauvegarder, UTILISATEUR } from '../store'

defineOptions({ inheritAttrs: false })

const props = defineProps<{ row: Offre }>()
const { aller, notifier } = useNav()

// « Mettre l'offre en pause » (retour Alice) : pour une offre en ligne, avec le droit « Publier ».
// Dans le proto, la pause dépublie l'offre ; on la relance avec « Prolonger et remettre en ligne ».
const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)
const pause = ref(false)
function confirmerPause() {
  retirer(props.row, 'pause')
  sauvegarder()
  pause.value = false
  notifier('Offre mise en pause : elle n\'est plus visible des candidats. Les candidatures reçues restent à traiter.')
}

const sections = computed(() => [{
  items: [
    { label: 'Voir l’offre', icon: 'ri:file-list-3-line', onSelect: () => aller({ nom: 'offre', id: props.row.id }) },
    { label: 'Dupliquer l’offre', icon: 'ri:file-copy-2-line', onSelect: () => aller({ nom: 'creation', mode: 'duplication', offreId: props.row.id }) },
    ...(props.row.etat === 'publiee' && peutPublier.value
      ? [{ label: 'Mettre l’offre en pause', icon: 'ri:stop-circle-line', onSelect: () => {
          pause.value = true
        } }]
      : []),
  ],
}])
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

    <CspDialog
      v-model:open="pause"
      title="Mettre l'offre en pause ?"
      size="sm"
    >
      <p class="texte">
        L'offre « {{ row.titre }} » ne sera plus visible des candidats. Les candidatures reçues restent à traiter.
        Vous pourrez la remettre en ligne depuis la page de l'offre.
      </p>
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="pause = false"
        />
        <CspButton
          label="Mettre en pause"
          icon="ri:stop-circle-line"
          is-icon-left
          @click="confirmerPause"
        />
      </template>
    </CspDialog>
  </div>
</template>

<style scoped lang="scss">
.actions-cell {
  display: flex;
  justify-content: flex-end;
}

.texte {
  margin: 0;
}
</style>
