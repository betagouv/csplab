<script setup lang="ts">
import { ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import CspTabs from '@/components/base/CspTabs/CspTabs.vue'
import { demoKanban } from '@/features/candidatures/__mocks__/demo'
import CandidatureKanbanColumn from '@/features/candidatures/components/CandidatureKanbanColumn.vue'
import { IMBRICATIONS, SCENE } from './imbrications'

const ETAPES = demoKanban().etapes
const ETAPE = ETAPES.find(etape => etape.candidatures.length >= 2) ?? ETAPES[0]!
const COLONNE = { ...ETAPE, candidatures: ETAPE.candidatures.slice(0, 2) }

const MENU = [{
  items: [
    { label: 'Renommer l’étape', icon: 'ri:edit-line' },
    { label: 'Supprimer l’étape', icon: 'ri:delete-bin-line' },
  ],
}]

const VUES = [
  { value: 'kanban', label: 'Kanban', icon: 'ri:table-line' },
  { value: 'liste', label: 'Liste', icon: 'ri:list-unordered' },
]

const ONGLETS = [
  { value: 'cv', label: 'CV' },
  { value: 'notes', label: 'Notes' },
  { value: 'documents', label: 'Documents' },
]

const vue = ref('liste')
const recherche = ref('')
const selection = ref(true)

const DIMENSIONS = {
  '--imbrications-scene-largeur': `${SCENE.largeur}px`,
  '--imbrications-scene-hauteur': `${SCENE.hauteur}px`,
  '--imbrications-ecart': `${SCENE.ecart}px`,
  '--imbrications-marge': `${SCENE.marge}px`,
  '--imbrications-legende': `${SCENE.legende}px`,
}
</script>

<template>
  <div
    class="imbrications-planche"
    :style="DIMENSIONS"
  >
    <figure
      v-for="imbrication in IMBRICATIONS"
      :key="imbrication.id"
      class="imbrications-planche__cas"
    >
      <figcaption class="imbrications-planche__legende">
        {{ imbrication.legende }}
      </figcaption>
      <div
        class="imbrications-planche__scene"
        :class="`imbrications-planche__scene--${imbrication.id}`"
      >
        <CandidatureKanbanColumn
          v-if="imbrication.id === 'colonne'"
          class="imbrications-planche__colonne"
          :etape="COLONNE"
          board-id="imbrications"
        />

        <CspCard
          v-else-if="imbrication.id === 'carte'"
          as="div"
          class="imbrications-planche__carte"
          title="Chargée de mission"
        >
          <CspCheckbox
            v-model="selection"
            label="M’avertir"
          />
          <template #footer>
            <CspButton label="Ouvrir" />
            <CspButton
              label="Modifier"
              variant="secondary"
            />
          </template>
        </CspCard>

        <CspDropdownMenu
          v-else-if="imbrication.id === 'menu'"
          :sections="MENU"
          :open="true"
          side="bottom"
          align="start"
        >
          <template #trigger>
            <CspButton
              icon="ri:more-fill"
              variant="tertiary"
              aria-label="Actions pour l’étape Entretien"
            />
          </template>
        </CspDropdownMenu>

        <CspSearchBar
          v-else-if="imbrication.id === 'recherche'"
          v-model="recherche"
          class="imbrications-planche__recherche"
          label="Rechercher un candidat"
          hide-label
          placeholder="Rechercher"
        />

        <CspSegmentedControl
          v-else-if="imbrication.id === 'segmente'"
          v-model="vue"
          class="imbrications-planche__segmente"
          :options="VUES"
          legend="Affichage des candidatures"
          hide-legend
        />

        <CspTabs
          v-else-if="imbrication.id === 'onglet'"
          class="imbrications-planche__onglets"
          :tabs="ONGLETS"
          default-value="notes"
        >
          <template
            v-for="onglet in ONGLETS"
            :key="onglet.value"
            #[onglet.value]
          >
            <p class="imbrications-planche__contenu">
              Les notes sont visibles par l’équipe de recrutement.
            </p>
          </template>
        </CspTabs>

        <CspButton
          v-else-if="imbrication.id === 'focus'"
          class="imbrications-planche__focus"
          label="Valider"
        />
      </div>
    </figure>
  </div>
</template>

<style scoped lang="scss">
.imbrications-planche {
  /* the open menu turns off pointer events on the body: the other controls keep theirs */
  pointer-events: auto;
  display: grid;
  grid-template-columns: repeat(4, var(--imbrications-scene-largeur));
  align-content: start;
  gap: var(--imbrications-ecart);
  box-sizing: border-box;
  min-height: 100vh;
  padding: var(--imbrications-marge);
  background-color: var(--csp-canvas-background);
  color: var(--text-default-grey);
}

.imbrications-planche__cas {
  margin: 0;
}

.imbrications-planche__legende {
  height: var(--imbrications-legende);
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.imbrications-planche__scene {
  position: relative;
  height: var(--imbrications-scene-hauteur);
  overflow: hidden;

  > * {
    position: absolute;
    left: var(--csp-space-4);
  }
}

/* each case lies where the zone of imbrications.ts frames its corners */
.imbrications-planche__colonne,
.imbrications-planche__scene--menu > *,
.imbrications-planche__onglets {
  top: var(--csp-space-4);
}

.imbrications-planche__colonne {
  width: var(--csp-kanban-column-width);
  height: 26rem;
}

.imbrications-planche__carte {
  bottom: var(--csp-space-4);
  width: 17rem;
}

.imbrications-planche__recherche,
.imbrications-planche__segmente,
.imbrications-planche__focus {
  top: 50%;
  transform: translateY(-50%);
}

.imbrications-planche__recherche {
  width: 10rem;
}

.imbrications-planche__onglets {
  right: var(--csp-space-4);
}

.imbrications-planche__contenu {
  margin: var(--csp-space-4) 0 0;
  font-size: var(--csp-font-size-sm);
}

/* states that the pointer and the keyboard give, drawn on one element of each case */
.imbrications-planche__segmente :deep(.csp-segmented__element:nth-of-type(1) label::before) {
  background-color: var(--background-default-grey-hover);
}

.imbrications-planche__onglets :deep(.csp-tabs__trigger:nth-of-type(1)) {
  background-color: var(--csp-tabs-trigger-background-hover);
  border-bottom-color: var(--csp-tabs-trigger-border-color-hover);
}

.imbrications-planche__focus {
  outline: var(--focus-ring);
  outline-offset: var(--csp-focus-ring-offset);
}
</style>

<style lang="scss">
/* the menu lies in the body, out of reach of the scoped styles: its first item takes the highlight that the keyboard
   gives */
body:has(.imbrications-planche) .csp-dropdown__item:first-of-type {
  background-color: var(--background-default-grey-hover);
}
</style>
