<script setup lang="ts">
import type { Etiquette } from '@/features/candidatures/etiquettes'
import type { PaletteColor } from '@/styles/palette'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'
import CspLabelList from '@/components/base/CspLabel/CspLabelList.vue'
import { ETIQUETTES_CANDIDATURE, ETIQUETTES_EQUIPE, ETIQUETTES_NOTE } from '@/features/candidatures/__mocks__/demo'
import { etiquettesOf } from '@/features/candidatures/etiquettes'
import { CATEGORIE_CONFIG } from '@/features/etapes-recrutement/constants/etape-recrutement'
import { DEMO_ETAPES } from '@/features/recrutements/__mocks__/demo'
import { proposeColor } from '@/styles/etiquettes/kit'
import { paletteVar } from '@/styles/palette'
import EtiquettePanel from './EtiquettePanel.vue'

const ETIQUETTES_PAR_TYPE: Record<string, Etiquette[]> = {
  candidature: Object.values(ETIQUETTES_CANDIDATURE),
  membre: Object.values(ETIQUETTES_EQUIPE),
  note: Object.values(ETIQUETTES_NOTE),
}

function proposerCouleur(type: string): PaletteColor {
  return proposeColor((ETIQUETTES_PAR_TYPE[type] ?? []).map(({ couleur }) => couleur))
}

const NOTE_LABELS = etiquettesOf({ etiquettes: ETIQUETTES_PAR_TYPE.note }).sort((a, b) => a.label.localeCompare(b.label, 'fr'))

// An étape is grey until the supervisor picks a color for it
const ETAPE_COLORS: Record<string, PaletteColor> = {
  'Entretien RH': 'purple',
  'Entretien avec le service': 'teal',
}

const ETAPES = DEMO_ETAPES.map(etape => ({
  ...etape,
  couleur: ETAPE_COLORS[etape.nom] ?? 'grey',
  statut: CATEGORIE_CONFIG[etape.categorie],
}))

// The avatar takes the color of the member's function on this offer, grey without one
const MEMBRES: { uuid: string, nom: string, poste: string, etiquette?: Etiquette }[] = [
  { uuid: '70000000-0000-4000-8000-000000000001', nom: 'Camille Bernard', poste: 'Cheffe du bureau des ressources humaines', etiquette: ETIQUETTES_EQUIPE.gestionnaire },
  { uuid: '70000000-0000-4000-8000-000000000002', nom: 'Julien Moreau', poste: 'Chef du service des affaires générales', etiquette: ETIQUETTES_EQUIPE.manager },
  { uuid: '70000000-0000-4000-8000-000000000003', nom: 'Sophie Lefèvre', poste: 'Conseillère mobilité carrière', etiquette: ETIQUETTES_EQUIPE.expert },
  { uuid: '70000000-0000-4000-8000-000000000004', nom: 'Nathalie Roche', poste: 'Adjointe à la cheffe de bureau', etiquette: ETIQUETTES_EQUIPE.jury },
  { uuid: '70000000-0000-4000-8000-000000000005', nom: 'Marc Dubois', poste: 'Gestionnaire de paie' },
]
</script>

<template>
  <div class="palette-kit">
    <section class="palette-kit__section">
      <h2 class="palette-kit__caption">
        Ajout d'une étiquette de note
      </h2>
      <div class="palette-kit__ajout">
        <div class="palette-kit__bloc">
          <h3 class="palette-kit__bloc-titre">
            Note
          </h3>
          <CspLabelList
            :labels="NOTE_LABELS"
            size="md"
          />
        </div>
        <EtiquettePanel
          title="Ajouter une étiquette"
          libelle=""
          type="note"
          :couleur="proposerCouleur('note')"
          :proposer-couleur="proposerCouleur"
        />
      </div>
    </section>

    <section class="palette-kit__section">
      <h2 class="palette-kit__caption">
        Équipe de recrutement
      </h2>
      <ul class="palette-kit__membres">
        <li
          v-for="membre in MEMBRES"
          :key="membre.uuid"
          class="palette-kit__membre"
        >
          <CspAvatar
            :name="membre.nom"
            :color="membre.etiquette?.couleur"
          />
          <div class="palette-kit__membre-identite">
            <span class="palette-kit__membre-nom">{{ membre.nom }}</span>
            <span class="palette-kit__membre-poste">{{ membre.poste }}</span>
          </div>
          <CspLabel
            v-if="membre.etiquette"
            :label="membre.etiquette.libelle"
            :color="membre.etiquette.couleur"
          />
        </li>
      </ul>
    </section>

    <section class="palette-kit__section">
      <h2 class="palette-kit__caption">
        Étapes de recrutement
      </h2>
      <ol class="palette-kit__etapes">
        <li
          v-for="etape in ETAPES"
          :key="etape.uuid"
          class="palette-kit__etape"
        >
          <span
            class="palette-kit__etape-pastille"
            :style="{ backgroundColor: paletteVar(etape.couleur, 'dot') }"
            aria-hidden="true"
          />
          <span class="palette-kit__etape-nom">{{ etape.nom }}</span>
          <CspBadge
            size="sm"
            :icon="etape.statut.icon"
            :type="etape.statut.type"
            :label="etape.statut.label"
          />
        </li>
      </ol>
    </section>
  </div>
</template>

<style scoped lang="scss">
@use '@/styles/breakpoints' as bp;

.palette-kit {
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

.palette-kit__section {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.palette-kit__caption {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-medium);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.palette-kit__ajout {
  display: grid;
  grid-template-columns: minmax(0, 24rem) minmax(0, 34rem);
  gap: var(--csp-space-8);
  align-items: start;

  @include bp.below(bp.$lg) {
    grid-template-columns: minmax(0, 1fr);
  }
}

.palette-kit__bloc {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-6);
  border: 1px solid var(--border-default-grey);
}

.palette-kit__bloc-titre {
  margin: 0;
  font-size: var(--csp-font-size-md);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.palette-kit__membres,
.palette-kit__etapes {
  display: flex;
  flex-direction: column;
  max-width: 48rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.palette-kit__membre,
.palette-kit__etape {
  display: flex;
  align-items: center;
  gap: var(--csp-space-3);
  padding: var(--csp-space-3) 0;
  border-bottom: 1px solid var(--border-default-grey);
}

.palette-kit__membre-identite {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.palette-kit__membre-nom,
.palette-kit__etape-nom {
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.palette-kit__membre-poste {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.palette-kit__etape-nom {
  flex: 1;
}

.palette-kit__etape-pastille {
  flex-shrink: 0;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
}
</style>
