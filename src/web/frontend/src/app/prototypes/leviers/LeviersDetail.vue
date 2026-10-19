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
import CandidatureKanbanCard from '@/features/candidatures/components/CandidatureKanbanCard.vue'
import CandidatureKanbanColumn from '@/features/candidatures/components/CandidatureKanbanColumn.vue'
import CandidatureNoteMessage from '@/features/candidatures/components/CandidatureNoteMessage.vue'
import { formatCandidatNom } from '@/features/candidatures/utils/candidat'
import { formatDateTime } from '@/utils/date'

defineProps<{
  // arrondis: a kanban column as the board draws it; ombres: three cards at rest, hovered and dragged
  variante: 'arrondis' | 'ombres'
}>()

const BOARD_ID = 'leviers'

const ETAPES = demoKanban().etapes
const PREMIERE_ETAPE = ETAPES[0]!
const COLONNE = { ...PREMIERE_ETAPE, candidatures: PREMIERE_ETAPE.candidatures.slice(0, 3) }

const ETATS = [
  { id: 'repos', legende: 'Au repos' },
  { id: 'survol', legende: 'Au survol' },
  { id: 'glisser', legende: 'Pendant le glisser' },
] as const

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
      v-if="variante === 'arrondis'"
      class="leviers-detail__colonne"
      :etape="COLONNE"
      :board-id="BOARD_ID"
    />
    <div
      v-else
      class="leviers-detail__etats"
    >
      <div
        v-for="(etat, index) in ETATS"
        :key="etat.id"
        class="leviers-detail__etat"
      >
        <span class="leviers-detail__legende">{{ etat.legende }}</span>
        <div :class="`leviers-detail__carte leviers-detail__carte--${etat.id}`">
          <CandidatureKanbanCard
            :candidature="COLONNE.candidatures[index]!"
            :board-id="BOARD_ID"
            :column-id="COLONNE.uuid"
            :card-index="index"
          />
        </div>
      </div>
    </div>

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
      :title="formatCandidatNom(CANDIDATURE.candidat)"
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

.leviers-detail__etats {
  display: flex;
  flex: 0 0 var(--csp-kanban-column-width);
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-kanban-column-padding);
  background-color: var(--csp-region-background);
  box-shadow: inset 0 0 0 1px var(--csp-region-border-color);
  border-radius: var(--csp-radius-region);
}

.leviers-detail__etat {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-1);
}

.leviers-detail__legende {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

/* Variables of the hover and drag states, set on an ancestor of a card that the pointer does not reach */
.leviers-detail__carte--survol {
  --csp-raised-shadow: var(--csp-raised-shadow-hover);
  --csp-raised-background: var(--csp-raised-background-hover);
  --csp-raised-border: var(--csp-raised-border-hover);
}

.leviers-detail__carte--glisser {
  --csp-raised-shadow: var(--csp-raised-shadow-drag);

  opacity: var(--csp-raised-drag-opacity);
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
