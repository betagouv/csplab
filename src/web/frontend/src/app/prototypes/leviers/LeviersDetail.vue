<script setup lang="ts">
import { ref } from 'vue'
import { DEMO_CANDIDATURE } from '@/api/__mocks__/demo'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSegmentedControl from '@/components/base/CspSegmentedControl/CspSegmentedControl.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTextarea from '@/components/base/CspTextarea/CspTextarea.vue'
import CspTooltip from '@/components/base/CspTooltip/CspTooltip.vue'
import { demoCandidatureDetail, demoKanban, demoNotes } from '@/features/candidatures/__mocks__/demo'
import CandidatureKanbanColumn from '@/features/candidatures/components/CandidatureKanbanColumn.vue'
import CandidatureNoteMessage from '@/features/candidatures/components/CandidatureNoteMessage.vue'
import { formatCandidatName } from '@/features/candidatures/format'
import { formatDateTime } from '@/utils/date'

const BOARD_ID = 'leviers'

const ETAPES = demoKanban().etapes
const PREMIERE_ETAPE = ETAPES[0]!
const COLONNE = { ...PREMIERE_ETAPE, candidatures: PREMIERE_ETAPE.candidatures.slice(0, 3) }

const CANDIDATURE = demoCandidatureDetail(DEMO_CANDIDATURE.uuid)!
const NOTE = demoNotes(DEMO_CANDIDATURE.uuid)[0]!

const MENU = [{
  items: [
    { label: 'Voir le détail de l’offre', icon: 'ri:eye-line' },
    { label: 'Personnaliser les étapes de recrutement', icon: 'ri:table-line' },
  ],
}]

const OPTIONS_ETAPES = ETAPES.map(etape => ({ value: etape.uuid, label: etape.nom }))
const etape = ref(PREMIERE_ETAPE.uuid)

const VUES = [
  { value: 'kanban', label: 'Kanban', icon: 'ri:table-line' },
  { value: 'liste', label: 'Liste', icon: 'ri:list-unordered' },
]
const vue = ref('kanban')
const recherche = ref('')
const note = ref('')
</script>

<template>
  <div class="leviers-detail">
    <CandidatureKanbanColumn
      class="leviers-detail__colonne"
      :etape="COLONNE"
      :board-id="BOARD_ID"
    />

    <div class="leviers-detail__controles">
      <div class="leviers-detail__rangee">
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
      <div class="leviers-detail__rangee">
        <CspButton
          label="Changer d'étape"
          icon="ri:arrow-left-right-line"
          is-icon-left
        />
        <CspButton
          label="Ajouter une note"
          variant="secondary"
        />
      </div>
      <CspSearchBar
        v-model="recherche"
        mode="live"
        label="Rechercher un candidat"
        hide-label
        placeholder="Rechercher un candidat…"
      />
      <div class="leviers-detail__rangee leviers-detail__rangee--champs">
        <CspSelect
          v-model="etape"
          class="leviers-detail__select"
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
      <div class="leviers-detail__rangee">
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

    <CspDrawer
      :open="true"
      :modal="false"
      :overlay="false"
      :title="formatCandidatName(CANDIDATURE.candidat)"
      :description="CANDIDATURE.recrutement_intitule"
      aria-label="Candidature"
      close-label="Fermer la candidature"
    >
      <template #title-end>
        <CspBadge :label="PREMIERE_ETAPE.nom" />
      </template>
      <div class="leviers-detail__panneau">
        <CspTextarea
          v-model="note"
          label="Ajouter une note"
          :rows="2"
        />
        <CspCard
          as="div"
          variant="alt"
        >
          <template #start>
            <span class="leviers-detail__note-auteur">{{ NOTE.publie_par_prenom }} {{ NOTE.publie_par_nom }}</span>
            <time
              :datetime="NOTE.publie_le"
              class="leviers-detail__note-date"
            >
              {{ formatDateTime(NOTE.publie_le) }}
            </time>
          </template>
          <CandidatureNoteMessage :message="NOTE.message" />
        </CspCard>
      </div>
    </CspDrawer>
  </div>
</template>

<style scoped lang="scss">
.leviers-detail {
  display: flex;
  align-items: flex-start;
  gap: var(--csp-space-8);
  box-sizing: border-box;
  height: 100vh;
  padding: var(--csp-space-8);
  background-color: var(--csp-canvas-background);
  color: var(--text-default-grey);
}

.leviers-detail__colonne {
  flex: 0 0 var(--csp-kanban-column-width);
}

.leviers-detail__controles {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-5);
  width: 30rem;
}

.leviers-detail__controles :deep(.csp-search-bar) {
  align-self: stretch;
}

.leviers-detail__rangee {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);

  > * {
    flex-shrink: 0;
  }
}

.leviers-detail__rangee--champs {
  align-items: flex-end;
  align-self: stretch;
}

.leviers-detail__select {
  flex: 1 1 auto;
}

.leviers-detail__panneau {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-6);
}

.leviers-detail__note-auteur {
  font-weight: var(--csp-font-weight-medium);
}

.leviers-detail__note-date {
  margin-inline-start: var(--csp-space-2);
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}
</style>
