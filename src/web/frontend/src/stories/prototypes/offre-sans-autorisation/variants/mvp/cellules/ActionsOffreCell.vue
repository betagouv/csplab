<script setup lang="ts">
import type { Offre } from '../store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import { dupliquer } from '../dupliquer'
import { useNav } from '../nav'
import { db, retirer, sauvegarder, UTILISATEUR } from '../store'
import { actionOffre } from '../suivi'

// Menu « … » d'une offre. Une seule action pour arrêter la diffusion (retour PO, point 6), appelée « Mettre en pause »
// comme le statut ; une offre en pause se remet en ligne, sans forcément la prolonger (Alice, 25/11/2026).
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const { aller, notifier } = useNav()

const peutPublier = computed(() => db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier)
// Action à faire sur la ligne (Continuer, Publier, Prolonger), avant le menu (Alice, 25/11/2026).
const action = computed(() => actionOffre(props.row, Boolean(peutPublier.value)))
const retrait = ref(false)
function confirmerRetrait() {
  retirer(props.row, 'pause')
  sauvegarder()
  retrait.value = false
  notifier('Offre mise en pause : elle n\'est plus visible des candidats. Les candidatures reçues restent à traiter.')
}

const sections = computed(() => [{
  items: [
    { label: 'Voir l’offre', icon: 'ri:file-list-3-line', onSelect: () => aller({ nom: 'offre', id: props.row.id }) },
    { label: 'Dupliquer l’offre', icon: 'ri:file-copy-2-line', onSelect: () => dupliquer(props.row, { aller, notifier }) },
    ...(props.row.etat === 'publiee' && peutPublier.value
      ? [{ label: 'Mettre en pause', icon: 'ri:stop-circle-line', onSelect: () => {
          retrait.value = true
        } }]
      : []),
    ...(props.row.etat === 'retiree' && peutPublier.value
      ? [{ label: 'Remettre en ligne', icon: 'ri:play-circle-line', onSelect: () => aller({ nom: 'offre', id: props.row.id, section: 'remettre' }) }]
      : []),
  ],
}])
</script>

<template>
  <div class="actions-cell">
    <CspButton
      v-if="action"
      :label="action.label"
      size="sm"
      :variant="action.type === 'continuer' ? 'secondary' : 'primary'"
      @click.stop="aller(action.ecran)"
    />
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
      title="Mettre l'offre en pause ?"
      size="sm"
    >
      <p class="texte">
        L'offre « {{ row.titre }} » ne sera plus visible des candidats et ne recevra plus de candidatures.
        Les candidatures reçues restent à traiter. Vous pourrez la remettre en ligne à tout moment.
      </p>
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="retrait = false"
        />
        <CspButton
          label="Mettre en pause"
          @click="confirmerRetrait"
        />
      </template>
    </CspDialog>
  </div>
</template>

<style scoped lang="scss">
.actions-cell {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--csp-space-2);
}

.texte {
  margin: 0;
}
</style>
