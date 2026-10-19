<script setup lang="ts">
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'
import { ETIQUETTES_CANDIDATURE, ETIQUETTES_EQUIPE } from '@/features/candidatures/__mocks__/demo'
import { PALETTE_COLORS } from '@/styles/palette'

const FONDS = [
  { id: 'blanc', titre: 'Fond blanc' },
  { id: 'colonne', titre: 'Colonne du kanban' },
  { id: 'note', titre: 'Note' },
  { id: 'panneau', titre: 'Panneau' },
] as const

const BORDURES = [
  { id: 'sans', titre: 'Sans bordure' },
  { id: 'filet', titre: 'Filet de 1 px' },
  { id: 'lisere', titre: 'Liseré, forme ronde' },
] as const

const ETIQUETTE_PAR_COULEUR = PALETTE_COLORS.map(couleur =>
  [...Object.values(ETIQUETTES_CANDIDATURE), ...Object.values(ETIQUETTES_EQUIPE)].find(etiquette => etiquette.couleur === couleur)!)

const TAILLES = ['sm', 'md'] as const
</script>

<template>
  <div class="bordures">
    <div
      class="bordures__entete"
      aria-hidden="true"
    />
    <h2
      v-for="bordure in BORDURES"
      :key="bordure.id"
      class="bordures__caption"
    >
      {{ bordure.titre }}
    </h2>
    <div
      v-for="fond in FONDS"
      :key="fond.id"
      class="bordures__rangee"
      :class="`bordures__rangee--${fond.id}`"
    >
      <h2 class="bordures__caption bordures__caption--fond">
        {{ fond.titre }}
      </h2>
      <div
        v-for="bordure in BORDURES"
        :key="bordure.id"
        class="bordures__cellule"
        :class="[`bordures__cellule--${fond.id}`, `bordures__cellule--${bordure.id}`]"
        :data-fond="fond.id"
        :data-bordure="bordure.id"
      >
        <div
          v-for="taille in TAILLES"
          :key="taille"
          class="bordures__ligne"
        >
          <CspLabel
            v-for="etiquette in ETIQUETTE_PAR_COULEUR"
            :key="etiquette.libelle"
            :label="etiquette.libelle"
            :color="etiquette.couleur"
            :size="taille"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.bordures {
  display: grid;
  grid-template-columns: 10rem repeat(3, minmax(0, 1fr));
  gap: var(--csp-space-4) var(--csp-space-6);
  align-items: stretch;
  padding: var(--csp-space-8);
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
}

.bordures__rangee {
  display: grid;
  grid-column: 1 / -1;
  grid-template-columns: subgrid;
}

.bordures__caption {
  align-self: end;
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-medium);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.bordures__caption--fond {
  align-self: center;
}

.bordures__cellule {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-3);
  padding: var(--csp-space-5);
}

.bordures__cellule--blanc {
  background-color: var(--background-default-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
}

.bordures__cellule--colonne {
  background-color: var(--background-alt-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
}

.bordures__cellule--note {
  background-color: var(--background-alt-grey);
}

.bordures__cellule--panneau {
  background-color: var(--background-overlap-grey);
  border-left: 1px solid var(--border-default-grey);
}

.bordures__ligne {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-1);
}

.bordures .bordures__cellule--sans :deep(.csp-label.csp-label) {
  --csp-label-border-color: transparent;
}

/* the rule of the « libre » scenario, on every scenario */
.bordures .bordures__cellule--filet :deep(.csp-label.csp-label) {
  --csp-label-border-color: color-mix(in oklab, var(--csp-label-dot) 26%, transparent);
}

/* the round label of the shape plates */
.bordures__cellule--lisere {
  --csp-label-radius: 999px;
}

.bordures .bordures__cellule--lisere :deep(.csp-label.csp-label) {
  --csp-label-border-color: color-mix(in srgb, currentColor 20%, transparent);
}
</style>
