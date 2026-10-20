<script setup lang="ts">
import { ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspPagination from '@/components/base/CspPagination/CspPagination.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import CspTooltip from '@/components/base/CspTooltip/CspTooltip.vue'
import { demoKanban } from '@/features/candidatures/__mocks__/demo'
import CandidatureKanbanColumn from '@/features/candidatures/components/CandidatureKanbanColumn.vue'

// The components of the kanban and of its pages, in the interface theme applied to the page
const ETAPES = demoKanban().etapes
const PREMIERE_ETAPE = ETAPES[0]!
const COLONNE = { ...PREMIERE_ETAPE, candidatures: PREMIERE_ETAPE.candidatures.slice(0, 3) }

const MENU = [{
  items: [
    { label: 'Voir le détail de l’offre', icon: 'ri:eye-line' },
    { label: 'Personnaliser les étapes de recrutement', icon: 'ri:table-line' },
  ],
}]

const OPTIONS_ETAPES = ETAPES.map(etape => ({ value: etape.uuid, label: etape.nom }))
const VUES = [
  { value: 'kanban', label: 'Kanban', icon: 'ri:table-line' },
  { value: 'liste', label: 'Liste', icon: 'ri:list-unordered' },
]

const etape = ref(PREMIERE_ETAPE.uuid)
const vue = ref('kanban')
const recherche = ref('')
const page = ref(2)
const avertir = ref(true)
</script>

<template>
  <div class="composants-planche">
    <CandidatureKanbanColumn
      class="composants-planche__colonne"
      :etape="COLONNE"
      board-id="composants"
    />

    <div class="composants-planche__groupe">
      <div class="composants-planche__rangee">
        <CspBadge :label="PREMIERE_ETAPE.nom" />
        <CspBadge
          type="info"
          label="En cours"
        />
        <CspBadge
          type="success"
          label="Acceptée"
        />
        <CspBadge
          type="error"
          label="Refusée"
        />
      </div>
      <div class="composants-planche__rangee">
        <CspButton
          label="Changer d'étape"
          icon="ri:arrow-left-right-line"
          is-icon-left
        />
        <CspButton
          label="Ajouter une note"
          variant="secondary"
        />
        <CspButton
          label="Filtres"
          icon="ri:filter-3-line"
          is-icon-left
          variant="tertiary"
        />
      </div>
      <CspSearchBar
        v-model="recherche"
        mode="live"
        label="Rechercher un candidat"
        hide-label
        placeholder="Rechercher un candidat…"
      />
      <div class="composants-planche__rangee composants-planche__rangee--champs">
        <CspSelect
          v-model="etape"
          class="composants-planche__select"
          label="Étape"
          :options="OPTIONS_ETAPES"
        />
        <CspSegmentedControl
          v-model="vue"
          :options="VUES"
          legend="Affichage des candidatures"
          hide-legend
        />
      </div>
      <div class="composants-planche__rangee">
        <CspTag label="Titulaire" />
        <CspTag label="Contractuel" />
        <CspCheckbox
          v-model="avertir"
          label="M’avertir"
        />
      </div>
      <CspPagination
        v-model:page="page"
        :page-count="6"
      />
    </div>

    <div class="composants-planche__groupe">
      <CspCallout
        variant="info"
        title="Statut visible par le candidat"
        description="Le candidat voit l’étape « Candidatures reçues » comme « À traiter »."
      />
      <CspCallout
        variant="success"
        title="Étape modifiée"
        description="Clara Fontaine est passée à l’étape Entretien."
      />
      <div class="composants-planche__rangee composants-planche__rangee--couches">
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
              aria-label="Actions sur l’offre"
            />
          </template>
        </CspDropdownMenu>
        <CspTooltip
          content="Copier l’adresse électronique"
          side="right"
          :open="true"
        >
          <CspButton
            icon="ri:file-copy-line"
            variant="tertiary"
            aria-label="Copier l’adresse électronique"
          />
        </CspTooltip>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.composants-planche {
  display: grid;
  grid-template-columns: var(--csp-kanban-column-width) 30rem 26rem;
  place-content: center;
  align-items: start;
  gap: var(--csp-space-10);
  box-sizing: border-box;
  height: 100vh;
  padding: var(--csp-space-8);
  background-color: var(--csp-canvas-background);
  color: var(--text-default-grey);
}

.composants-planche__groupe {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-5);
}

.composants-planche__groupe :deep(.csp-search-bar),
.composants-planche__groupe :deep(.csp-callout) {
  align-self: stretch;
}

.composants-planche__rangee {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);

  > * {
    flex-shrink: 0;
  }
}

.composants-planche__rangee--champs {
  align-items: flex-end;
  align-self: stretch;
}

.composants-planche__select {
  flex: 1 1 auto;
}
</style>
