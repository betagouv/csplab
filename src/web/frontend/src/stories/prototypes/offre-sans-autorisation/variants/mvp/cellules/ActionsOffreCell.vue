<script setup lang="ts">
import type { Offre } from '../store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { dupliquer } from '../dupliquer'
import { useNav } from '../nav'
import { db, retirer, sauvegarder, UTILISATEUR } from '../store'

// Menu « … » d'une offre. Une seule action pour arrêter la diffusion (retour PO, point 6) : pas de distinction
// entre « mettre en pause » et « retirer » ; on remet l'offre en ligne en prolongeant sa date de fin.
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const { aller, notifier } = useNav()

const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)
const retrait = ref(false)
function confirmerRetrait() {
  retirer(props.row, 'manuel')
  sauvegarder()
  retrait.value = false
  notifier('Offre retirée : elle n\'est plus visible des candidats. Les candidatures reçues restent à traiter.')
}

const sections = computed(() => [{
  items: [
    { label: 'Voir l’offre', icon: 'ri:file-list-3-line', onSelect: () => aller({ nom: 'offre', id: props.row.id }) },
    { label: 'Dupliquer l’offre', icon: 'ri:file-copy-2-line', onSelect: () => dupliquer(props.row, { aller, notifier }) },
    ...(props.row.etat === 'publiee' && peutPublier.value
      ? [{ label: 'Retirer l’offre', icon: 'ri:stop-circle-line', onSelect: () => {
          retrait.value = true
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
      v-model:open="retrait"
      title="Retirer l'offre ?"
      size="sm"
    >
      <p class="texte">
        L'offre « {{ row.titre }} » ne sera plus visible des candidats. Les candidatures reçues restent à traiter.
        Vous pourrez la remettre en ligne en prolongeant sa date de fin.
      </p>
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="retrait = false"
        />
        <CspButton
          label="Retirer l'offre"
          @click="confirmerRetrait"
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
