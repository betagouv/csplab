<script setup lang="ts">
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import type { CspLabelItem } from '@/components/base/CspLabel/types'
import type { Etiquette } from '@/features/candidatures/etiquettes'
import type { MembreEquipe } from '@/features/equipe-recrutement/types'
import { ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'
import CspLabelList from '@/components/base/CspLabel/CspLabelList.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { ETIQUETTES_CANDIDATURE, ETIQUETTES_EQUIPE, ETIQUETTES_NOTE } from '@/features/candidatures/__mocks__/demo'
import { etiquettesOf } from '@/features/candidatures/etiquettes'
import { EQUIPE_RECRUTEMENT_COLUMNS } from '@/features/equipe-recrutement/columns'
import { scenarioDefaultColor } from '@/styles/etiquettes/scenarios'
import { PALETTE_COLORS } from '@/styles/palette'
import EquipeEtiquetteCell from './EquipeEtiquetteCell.vue'
import EtiquettePanel from './EtiquettePanel.vue'

function trier(etiquettes: Etiquette[]): CspLabelItem[] {
  return etiquettesOf({ etiquettes }).sort((a, b) => a.label.localeCompare(b.label, 'fr'))
}

const blocs = ref([
  {
    titre: 'Candidature',
    description: 'Affichée sur la candidature. Permet de qualifier rapidement les profils candidats.',
    etiquettes: trier(Object.values(ETIQUETTES_CANDIDATURE)),
  },
  {
    titre: 'Note',
    description: 'Affichée sur les notes d\'une candidature. Permet d\'identifier la nature des notes.',
    etiquettes: trier(Object.values(ETIQUETTES_NOTE)),
  },
  {
    titre: 'Équipe de recrutement de l\'offre',
    description: 'Affichée dans l\'équipe de recrutement d\'une offre. Permet d\'indiquer ce que fait chaque membre sur cette offre.',
    etiquettes: trier(Object.values(ETIQUETTES_EQUIPE)),
  },
])

function supprimer(bloc: { etiquettes: CspLabelItem[] }, etiquette: CspLabelItem): void {
  bloc.etiquettes = bloc.etiquettes.filter(({ label }) => label !== etiquette.label)
}

type MembreAvecEtiquette = MembreEquipe & { etiquette?: Etiquette }

const MEMBRES: MembreAvecEtiquette[] = [
  { uuid: '70000000-0000-4000-8000-000000000001', prenom: 'Camille', nom: 'Bernard', poste: 'Cheffe du bureau des ressources humaines', email: 'camille.bernard@example.gouv.fr', recrutement_role: 'responsable', etiquette: ETIQUETTES_EQUIPE.gestionnaire },
  { uuid: '70000000-0000-4000-8000-000000000002', prenom: 'Julien', nom: 'Moreau', poste: 'Chef du service des affaires générales', email: 'julien.moreau@example.gouv.fr', recrutement_role: 'recruteur', etiquette: ETIQUETTES_EQUIPE.manager },
  { uuid: '70000000-0000-4000-8000-000000000003', prenom: 'Sophie', nom: 'Lefèvre', poste: 'Conseillère mobilité carrière', email: 'sophie.lefevre@example.gouv.fr', recrutement_role: 'contributeur', etiquette: ETIQUETTES_EQUIPE.expert },
  { uuid: '70000000-0000-4000-8000-000000000004', prenom: 'Nathalie', nom: 'Roche', poste: 'Adjointe à la cheffe de bureau', email: 'nathalie.roche@example.gouv.fr', recrutement_role: 'contributeur', etiquette: ETIQUETTES_EQUIPE.jury },
  { uuid: '70000000-0000-4000-8000-000000000005', prenom: 'Marc', nom: 'Dubois', poste: 'Gestionnaire de paie', email: 'marc.dubois@example.gouv.fr', recrutement_role: 'recruteur' },
]

const ETIQUETTE_COLUMN: CspColumnDef<MembreAvecEtiquette> = { id: 'etiquette', header: 'Étiquette', width: '12rem', cellComponent: EquipeEtiquetteCell }

const EQUIPE_COLUMNS: CspColumnDef<MembreAvecEtiquette>[] = EQUIPE_RECRUTEMENT_COLUMNS.flatMap(column =>
  column.id === 'role' ? [column, ETIQUETTE_COLUMN] : [column])

const ETIQUETTE_PAR_COULEUR = PALETTE_COLORS.map(couleur =>
  Object.values(ETIQUETTES_CANDIDATURE).find(etiquette => etiquette.couleur === couleur)!)

const COMPARAISONS = [
  { id: 'carte', size: 'sm', surface: 'default' },
  { id: 'colonne', size: 'sm', surface: 'alt' },
  { id: 'panneau', size: 'md', surface: 'default' },
] as const
</script>

<template>
  <div class="contextes">
    <section class="contextes__section">
      <h2 class="contextes__caption">
        Paramètres de l'organisme
      </h2>
      <div class="contextes__parametres">
        <h3 class="contextes__parametres-titre">
          Étiquettes
        </h3>
        <p class="contextes__parametres-intro">
          Créez des étiquettes pour qualifier vos candidatures, identifier les rôles de votre équipe et catégoriser vos notes.
        </p>
        <div
          v-for="bloc in blocs"
          :key="bloc.titre"
          class="contextes__bloc"
        >
          <div class="contextes__bloc-meta">
            <h4 class="contextes__bloc-titre">
              {{ bloc.titre }}
            </h4>
            <p class="contextes__bloc-description">
              {{ bloc.description }}
            </p>
            <p class="contextes__bloc-compteur">
              {{ bloc.etiquettes.length }} étiquettes
            </p>
            <CspButton
              class="contextes__bloc-ajouter"
              variant="tertiary-no-outline"
              size="sm"
              icon="ri:add-line"
              label="Ajouter une étiquette"
            />
          </div>
          <CspLabelList
            :labels="bloc.etiquettes"
            size="md"
            removable
            @remove="etiquette => supprimer(bloc, etiquette)"
          />
        </div>
      </div>
    </section>

    <section class="contextes__section">
      <h2 class="contextes__caption">
        Panneaux d'ajout et de modification
      </h2>
      <div class="contextes__panneaux">
        <EtiquettePanel
          title="Ajouter une étiquette"
          libelle=""
          type="candidature"
          :couleur="scenarioDefaultColor()"
        />
        <EtiquettePanel
          title="Modifier l'étiquette"
          :libelle="ETIQUETTES_CANDIDATURE.laureate.libelle"
          type="candidature"
          :couleur="ETIQUETTES_CANDIDATURE.laureate.couleur"
        />
      </div>
    </section>

    <section class="contextes__section">
      <h2 class="contextes__caption">
        Équipe de recrutement
      </h2>
      <CspDataTable
        :rows="MEMBRES"
        :columns="EQUIPE_COLUMNS"
        :row-key="row => row.uuid"
        caption="Membres de l'équipe de recrutement"
      />
    </section>

    <section class="contextes__section">
      <h2 class="contextes__caption">
        Étiquettes, statuts, filtres et boutons
      </h2>
      <div class="contextes__comparaisons">
        <div
          v-for="comparaison in COMPARAISONS"
          :key="comparaison.id"
          class="contextes__comparaison"
          :class="`contextes__comparaison--${comparaison.surface}`"
        >
          <div class="contextes__groupe contextes__groupe--etiquettes">
            <CspLabel
              v-for="etiquette in ETIQUETTE_PAR_COULEUR"
              :key="etiquette.libelle"
              :label="etiquette.libelle"
              :color="etiquette.couleur"
              :size="comparaison.size"
            />
          </div>
          <div class="contextes__groupe">
            <CspBadge
              type="success"
              label="Acceptée"
              :size="comparaison.size"
            />
            <CspBadge
              type="error"
              label="Refusée"
              :size="comparaison.size"
            />
            <CspBadge
              type="info"
              label="En cours"
              :size="comparaison.size"
            />
            <CspBadge
              type="warning"
              label="Incomplète"
              :size="comparaison.size"
            />
          </div>
          <div class="contextes__groupe">
            <CspTag
              variant="clickable"
              label="Présélection"
              :size="comparaison.size"
            />
            <CspTag
              variant="selectable"
              label="Entretien RH"
              :pressed="true"
              :size="comparaison.size"
            />
            <CspTag
              variant="dismissible"
              label="Titulaire"
              :size="comparaison.size"
            />
            <CspButton
              variant="secondary"
              label="Ajouter une note"
              :size="comparaison.size"
            />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/breakpoints' as bp;

.contextes {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-12);
  padding: var(--csp-space-8);
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);

  @include bp.below(bp.$lg) {
    gap: var(--csp-space-8);
    padding: var(--csp-space-4);
  }
}

.contextes__section {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.contextes__caption {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-medium);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.contextes__parametres {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.contextes__parametres-titre {
  margin: 0;
  font-size: var(--csp-font-size-xl);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.contextes__parametres-intro {
  margin: 0 0 var(--csp-space-2);
  color: var(--text-mention-grey);
}

.contextes__bloc {
  display: grid;
  grid-template-columns: 20rem minmax(0, 1fr);
  gap: var(--csp-space-8);
  padding: var(--csp-space-6);
  border: 1px solid var(--border-default-grey);

  @include bp.below(bp.$lg) {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--csp-space-4);
    padding: var(--csp-space-4);
  }
}

.contextes__bloc-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-2);
}

.contextes__bloc-titre {
  margin: 0;
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.contextes__bloc-description,
.contextes__bloc-compteur {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

/* the content of the button lines up with the text above */
.contextes__bloc-ajouter {
  margin-inline-start: calc(-1 * var(--csp-btn-padding-x));
}

.contextes__panneaux {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 34rem));
  gap: var(--csp-space-8);
  align-items: start;

  @include bp.below(bp.$lg) {
    grid-template-columns: minmax(0, 1fr);
  }
}

.contextes__comparaisons {
  display: flex;
  flex-direction: column;
}

.contextes__comparaison {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-4) var(--csp-space-8);
  padding: var(--csp-space-5);
}

.contextes__comparaison--alt {
  background-color: var(--background-alt-grey);
}

.contextes__groupe {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2);
}

.contextes__groupe--etiquettes {
  gap: var(--csp-space-1);
}
</style>
