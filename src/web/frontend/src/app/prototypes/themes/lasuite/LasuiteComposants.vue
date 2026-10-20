<script setup lang="ts">
import { ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspRadioGroup from '@/components/base/CspRadioGroup/CspRadioGroup.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import CspTooltip from '@/components/base/CspTooltip/CspTooltip.vue'

const ONGLETS = [
  { value: 'apercu', label: 'Aperçu', icon: 'ri:eye-line' },
  { value: 'fichiers', label: 'Fichiers', icon: 'ri:file-list-line' },
  { value: 'historique', label: 'Historique', icon: 'ri:history-line' },
]
const onglet = ref('apercu')

const VUES = [
  { value: 'grille', label: 'Grille', icon: 'ri:layout-grid-line' },
  { value: 'liste', label: 'Liste', icon: 'ri:list-unordered' },
]
const vue = ref('grille')

const OPTIONS = [
  { value: 'a', label: 'Première option' },
  { value: 'b', label: 'Deuxième option' },
]
const choix = ref('a')
const radio = ref('a')
const recherche = ref('')
const coche = ref(true)
const nonCoche = ref(false)
const actif = ref(true)

const MENU = [{
  items: [
    { label: 'Renommer', icon: 'ri:edit-line' },
    { label: 'Dupliquer', icon: 'ri:file-copy-line' },
    { label: 'Archiver', icon: 'ri:archive-line' },
  ],
}]
</script>

<template>
  <div class="lasuite-composants">
    <div class="lasuite-composants__grille">
      <section class="lasuite-composants__colonne">
        <CspTabs
          v-model="onglet"
          class="lasuite-composants__onglets"
          :tabs="ONGLETS"
        >
          <template #apercu />
          <template #fichiers />
          <template #historique />
        </CspTabs>
        <div class="lasuite-composants__rangee">
          <CspButton
            label="Valider"
            icon="ri:check-line"
            is-icon-left
          />
          <CspButton
            label="Ajouter"
            variant="secondary"
            icon="ri:add-line"
            is-icon-left
          />
          <CspButton
            label="Filtrer"
            variant="tertiary"
            icon="ri:filter-3-line"
            is-icon-left
          />
        </div>
        <div class="lasuite-composants__rangee">
          <CspButton
            label="Valider"
            disabled
          />
          <CspButton
            label="Ajouter"
            variant="secondary"
            disabled
          />
          <CspButton
            label="Filtrer"
            variant="tertiary"
            disabled
          />
        </div>
        <div class="lasuite-composants__rangee">
          <CspSegmentedControl
            v-model="vue"
            :options="VUES"
            legend="Affichage"
            hide-legend
          />
          <CspSearchBar
            v-model="recherche"
            class="lasuite-composants__recherche"
            mode="live"
            label="Rechercher"
            hide-label
            placeholder="Rechercher…"
          />
        </div>
        <CspSelect
          v-model="choix"
          class="lasuite-composants__champ"
          label="Liste de choix"
          :options="OPTIONS"
        />
        <div class="lasuite-composants__rangee lasuite-composants__rangee--haut">
          <CspRadioGroup
            v-model="radio"
            label="Boutons radio"
            :options="OPTIONS"
          />
          <div class="lasuite-composants__pile">
            <CspCheckbox
              v-model="coche"
              label="Case cochée"
            />
            <CspCheckbox
              v-model="nonCoche"
              label="Case vide"
            />
            <CspSwitch
              v-model="actif"
              label="Interrupteur"
            />
          </div>
        </div>
      </section>

      <section class="lasuite-composants__colonne">
        <div class="lasuite-composants__rangee">
          <CspBadge label="Brouillon" />
          <CspBadge
            type="info"
            label="En cours"
          />
          <CspBadge
            type="success"
            label="Validé"
          />
          <CspBadge
            type="error"
            label="Refusé"
          />
        </div>
        <CspCallout
          variant="info"
          title="Information"
          description="Les modifications s’appliquent à cet espace."
        />
        <CspCallout
          variant="success"
          title="Enregistré"
          description="Le document est à jour."
        />
        <div class="lasuite-composants__rangee lasuite-composants__rangee--couches">
          <CspDropdownMenu
            :sections="MENU"
            :open="true"
            side="bottom"
            align="start"
          >
            <template #trigger>
              <CspButton
                icon="ri:more-fill"
                variant="tertiary"
                aria-label="Actions"
              />
            </template>
          </CspDropdownMenu>
          <CspTooltip
            class="lasuite-composants__bulle"
            content="Copier le lien"
            side="right"
            :open="true"
          >
            <CspButton
              icon="ri:file-copy-line"
              variant="tertiary"
              aria-label="Copier le lien"
            />
          </CspTooltip>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped lang="scss">
/* Controls on the left, feedback and floating layers on the right, on the background of a page */
.lasuite-composants {
  display: grid;
  place-content: center;
  height: 100vh;
  background-color: var(--csp-canvas-background);
  color: var(--text-default-grey);
}

.lasuite-composants__grille {
  display: grid;
  grid-template-columns: 30rem 26rem;
  align-items: start;
  gap: var(--csp-space-12);
  zoom: 1.15;
}

.lasuite-composants__colonne {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
}

.lasuite-composants__onglets {
  align-self: stretch;
}

.lasuite-composants__rangee {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
}

.lasuite-composants__rangee--haut {
  align-items: flex-start;
  gap: var(--csp-space-12);
}

/* room under the menu and beside the tooltip, which open over the plate */
.lasuite-composants__rangee--couches {
  height: 9rem;
  align-items: flex-start;
  gap: var(--csp-space-16);
}

.lasuite-composants__pile {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.lasuite-composants__recherche {
  flex: 1;
}

.lasuite-composants__champ {
  width: 20rem;
}
</style>
