<script setup lang="ts">
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import type { CandidatureListe } from '@/features/candidatures/types'
import { DEMO_CANDIDATURE } from '@/api/__mocks__/demo'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCard from '@/components/base/CspCard/CspCard.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'
import CspLabelList from '@/components/base/CspLabel/CspLabelList.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { demoCandidatureDetail, demoKanban, demoListe, demoNotes, ETIQUETTES_CANDIDATURE, ETIQUETTES_EQUIPE } from '@/features/candidatures/__mocks__/demo'
import { CANDIDATURE_LISTE_COLUMNS } from '@/features/candidatures/columns'
import CandidatureEtiquettes from '@/features/candidatures/components/CandidatureEtiquettes.vue'
import CandidatureKanbanCard from '@/features/candidatures/components/CandidatureKanbanCard.vue'
import CandidatureNoteMessage from '@/features/candidatures/components/CandidatureNoteMessage.vue'
import { etiquettesOf } from '@/features/candidatures/etiquettes'
import { PALETTE_COLORS } from '@/styles/palette'
import { formatDateTime } from '@/utils/date'

const FORMES = [
  { id: 'tag', titre: 'Tag du DSFR' },
  { id: 'badge', titre: 'Badge du DSFR' },
  { id: 'etiquette', titre: 'Étiquette du kit' },
  { id: 'ronde', titre: 'Étiquette ronde' },
] as const

const PREMIERE_ETAPE = demoKanban().etapes[0]!
const CARTES = [0, 2, 4].map(index => PREMIERE_ETAPE.candidatures[index]!)

const ETIQUETTES_PANNEAU = etiquettesOf(demoCandidatureDetail(DEMO_CANDIDATURE.uuid) ?? {})

const NOTE = demoNotes(DEMO_CANDIDATURE.uuid)[0]!

const LIGNES = demoListe().slice(0, 4)

const COLONNES_LISTE: CspColumnDef<CandidatureListe>[] = CANDIDATURE_LISTE_COLUMNS.filter(({ id }) =>
  ['candidat', 'etiquettes', 'date_soumission'].includes(id))

const ETIQUETTE_PAR_COULEUR = PALETTE_COLORS.map(couleur =>
  [...Object.values(ETIQUETTES_CANDIDATURE), ...Object.values(ETIQUETTES_EQUIPE)].find(etiquette => etiquette.couleur === couleur)!)

const TAILLES = ['sm', 'md'] as const
</script>

<template>
  <div class="formes">
    <section
      v-for="forme in FORMES"
      :key="forme.id"
      class="formes__forme"
      :class="`formes__forme--${forme.id}`"
    >
      <h2 class="formes__caption">
        {{ forme.titre }}
      </h2>
      <div class="formes__contextes">
        <div class="formes__colonne">
          <CandidatureKanbanCard
            v-for="(candidature, index) in CARTES"
            :key="candidature.uuid"
            :candidature="candidature"
            :board-id="`formes-${forme.id}`"
            :column-id="PREMIERE_ETAPE.uuid"
            :card-index="index"
          />
        </div>
        <div class="formes__panneau">
          <CandidatureEtiquettes :etiquettes="ETIQUETTES_PANNEAU" />
        </div>
        <CspCard
          as="div"
          variant="alt"
          class="formes__note"
        >
          <template #start>
            <span class="formes__note-auteur">{{ NOTE.publie_par_prenom }} {{ NOTE.publie_par_nom }}</span>
            <span
              class="formes__note-separateur"
              aria-hidden="true"
            >•</span>
            <time
              :datetime="NOTE.publie_le"
              class="formes__note-horodatage"
            >
              {{ formatDateTime(NOTE.publie_le) }}
            </time>
          </template>
          <CspLabelList
            class="formes__note-etiquettes"
            :labels="etiquettesOf(NOTE)"
            removable
          />
          <CandidatureNoteMessage :message="NOTE.message" />
        </CspCard>
        <CspDataTable
          class="formes__liste"
          :rows="LIGNES"
          :columns="COLONNES_LISTE"
          :row-key="row => row.uuid"
          caption="Candidatures"
        />
      </div>
      <div class="formes__comparaisons">
        <div
          v-for="taille in TAILLES"
          :key="taille"
          class="formes__comparaison"
        >
          <div class="formes__groupe formes__groupe--etiquettes">
            <CspLabel
              v-for="etiquette in ETIQUETTE_PAR_COULEUR"
              :key="etiquette.libelle"
              :label="etiquette.libelle"
              :color="etiquette.couleur"
              :size="taille"
            />
          </div>
          <div class="formes__groupe">
            <CspBadge
              type="success"
              label="Acceptée"
              :size="taille"
            />
            <CspBadge
              type="error"
              label="Refusée"
              :size="taille"
            />
            <CspBadge
              type="info"
              label="En cours"
              :size="taille"
            />
          </div>
          <div class="formes__groupe">
            <CspTag
              variant="clickable"
              label="Présélection"
              :size="taille"
            />
            <CspTag
              variant="selectable"
              label="Entretien RH"
              :pressed="true"
              :size="taille"
            />
            <CspTag
              variant="dismissible"
              label="Titulaire"
              :size="taille"
            />
            <CspButton
              variant="secondary"
              label="Ajouter une note"
              :size="taille"
            />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
.formes {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-10);
  padding: var(--csp-space-8);
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
}

.formes__forme {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.formes__caption {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-medium);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.formes__contextes {
  display: grid;
  grid-template-columns: var(--csp-kanban-column-width) 20rem 28rem minmax(0, 1fr);
  gap: var(--csp-space-6);
  align-items: start;
}

.formes__colonne {
  display: flex;
  flex-direction: column;
  gap: var(--csp-kanban-column-gap);
  padding: var(--csp-kanban-column-padding);
  background-color: var(--background-alt-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
  border-top: var(--csp-kanban-column-accent-width) solid var(--border-default-grey);
}

.formes__panneau {
  padding: var(--csp-space-6);
  background-color: var(--background-overlap-grey);
  border-left: 1px solid var(--border-default-grey);
}

.formes__note {
  --csp-card-border: transparent;
}

.formes__note-auteur {
  font-size: var(--csp-font-size-base);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.formes__note-separateur,
.formes__note-horodatage {
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
}

.formes__note-etiquettes {
  margin-bottom: var(--csp-space-3);
}

.formes__comparaisons {
  display: flex;
  flex-direction: column;
}

.formes__comparaison {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-4) var(--csp-space-8);
  padding-block: var(--csp-space-3);
}

.formes__groupe {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2);
}

.formes__groupe--etiquettes {
  gap: var(--csp-space-1);
}

/* DSFR tag, fr-tag and fr-tag--sm of DSFR 1.15.4 */
.formes .formes__forme--tag :deep(.csp-label.csp-label--sm),
.formes .formes__forme--tag :deep(.csp-label-list__more.csp-label-list__more) {
  gap: 0.125rem;
  min-height: 1.5rem;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-size: 0.75rem;
  font-weight: var(--csp-font-weight-regular);
  line-height: 1.25rem;
}

.formes .formes__forme--tag :deep(.csp-label.csp-label--md),
.formes .formes__forme--tag :deep(.csp-label-list__more.csp-label-list__more--md) {
  gap: 0.25rem;
  min-width: 2.25rem;
  min-height: 2rem;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: var(--csp-font-weight-regular);
  line-height: 1.5rem;
}

.formes .formes__forme--tag :deep(.csp-label--sm .csp-label__remove) {
  margin-inline-end: -0.1875rem;
  padding: 0;
  font-size: 0.75rem;
}

.formes .formes__forme--tag :deep(.csp-label--md .csp-label__remove) {
  margin-inline-end: -0.25rem;
  padding: 0;
  font-size: 1rem;
}

/* DSFR badge, fr-badge and fr-badge--sm of DSFR 1.15.4 */
.formes .formes__forme--badge :deep(.csp-label.csp-label--sm),
.formes .formes__forme--badge :deep(.csp-label-list__more.csp-label-list__more) {
  min-height: 1.125rem;
  padding: 0 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: var(--csp-font-weight-bold);
  line-height: 1.25rem;
  text-transform: uppercase;
}

.formes .formes__forme--badge :deep(.csp-label.csp-label--md),
.formes .formes__forme--badge :deep(.csp-label-list__more.csp-label-list__more--md) {
  min-height: 1.5rem;
  padding: 0 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-weight: var(--csp-font-weight-bold);
  line-height: 1.5rem;
  text-transform: uppercase;
}

.formes .formes__forme--tag :deep(.csp-label.csp-label),
.formes .formes__forme--badge :deep(.csp-label.csp-label) {
  align-items: center;
  white-space: nowrap;
}

.formes .formes__forme--tag :deep(.csp-label .csp-label__remove),
.formes .formes__forme--badge :deep(.csp-label .csp-label__remove) {
  margin-block: 0;
}

.formes .formes__forme--tag :deep(.csp-label .csp-label__dot),
.formes .formes__forme--badge :deep(.csp-label .csp-label__dot) {
  display: none;
}

/* Round label with a light border, next to the status badge at the radius of a control */
.formes__forme--ronde {
  --csp-label-radius: 999px;
}

.formes .formes__forme--ronde :deep(.csp-label.csp-label) {
  --csp-label-border-color: color-mix(in srgb, currentColor 20%, transparent);
}

.formes .formes__forme--ronde :deep(.badge) {
  border-radius: 0.375rem;
}
</style>
