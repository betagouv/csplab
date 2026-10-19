<script setup lang="ts">
import type { PaletteColor } from '@/styles/palette'
import CspAvatar from '@/components/base/CspAvatar/CspAvatar.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import { CATEGORIE_CONFIG } from '@/features/etapes-recrutement/constants/etape-recrutement'
import { paletteVar } from '@/styles/palette'

const MEMBRES: { nom: string, couleur: PaletteColor }[] = [
  { nom: 'Camille Bernard', couleur: 'teal' },
  { nom: 'Julien Moreau', couleur: 'purple' },
  { nom: 'Sophie Lefèvre', couleur: 'yellow' },
  { nom: 'Nathalie Roche', couleur: 'brown' },
  { nom: 'Marc Dubois', couleur: 'blue' },
  { nom: 'Inès Moreau', couleur: 'red' },
  { nom: 'Thomas Leroy', couleur: 'green' },
  { nom: 'Clara Fontaine', couleur: 'orange' },
  { nom: 'Léa Chevalier', couleur: 'pink' },
  { nom: 'Paul Dumas', couleur: 'grey' },
]

const ETAPES: { nom: string, couleur: PaletteColor, candidatures: number }[] = [
  { nom: 'Présélection', couleur: 'blue', candidatures: 4 },
  { nom: 'Entretien RH', couleur: 'teal', candidatures: 3 },
  { nom: 'Entretien avec le manager', couleur: 'purple', candidatures: 2 },
]

const EN_COURS = CATEGORIE_CONFIG.EN_COURS
</script>

<template>
  <div class="palette-usages">
    <section class="palette-usages__section">
      <h2 class="palette-usages__caption">
        Membres de l'équipe de recrutement
      </h2>
      <ul class="palette-usages__membres">
        <li
          v-for="membre in MEMBRES"
          :key="membre.nom"
          class="palette-usages__membre"
        >
          <CspAvatar
            class="palette-usages__avatar"
            :name="membre.nom"
            :style="{
              '--palette-usages-background': paletteVar(membre.couleur, 'background'),
              '--palette-usages-text': paletteVar(membre.couleur, 'text'),
            }"
          />
          {{ membre.nom }}
        </li>
      </ul>
    </section>

    <section class="palette-usages__section">
      <h2 class="palette-usages__caption">
        Étapes du recrutement
      </h2>
      <div class="palette-usages__colonnes">
        <section
          v-for="etape in ETAPES"
          :key="etape.nom"
          class="palette-usages__colonne"
        >
          <h3 class="palette-usages__etape">
            <CspCheckbox
              variant="checkbox-only"
              size="sm"
              :label="`Sélectionner la colonne ${etape.nom}`"
            />
            <span
              class="palette-usages__pastille"
              :style="{ backgroundColor: paletteVar(etape.couleur, 'dot') }"
              aria-hidden="true"
            />
            <span class="palette-usages__etape-nom">{{ etape.nom }}</span>
            <CspBadge
              size="md"
              :label="String(etape.candidatures)"
            />
          </h3>
          <footer class="palette-usages__statut">
            <p class="palette-usages__statut-titre">
              Statut visible par le candidat
            </p>
            <CspBadge
              size="sm"
              :icon="EN_COURS.icon"
              :type="EN_COURS.type"
              :label="EN_COURS.label"
            />
          </footer>
        </section>
      </div>
    </section>
  </div>
</template>

<style scoped lang="scss">
.palette-usages {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-10);
  padding: var(--csp-space-8);
  background-color: var(--background-default-grey);
  color: var(--text-default-grey);
}

.palette-usages__section {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.palette-usages__caption {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  font-weight: var(--csp-font-weight-medium);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text-mention-grey);
}

.palette-usages__membres {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-3) var(--csp-space-6);
  margin: 0;
  padding: 0;
  list-style: none;
}

.palette-usages__membre {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
}

.palette-usages .palette-usages__avatar {
  background-color: var(--palette-usages-background);
  color: var(--palette-usages-text);
  box-shadow: none;
}

.palette-usages__colonnes {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-kanban-gap);
}

/* Same frame as the header and the footer of a kanban column (CandidatureKanbanColumn) */
.palette-usages__colonne {
  display: flex;
  flex-direction: column;
  gap: var(--csp-kanban-column-gap);
  width: var(--csp-kanban-column-width);
  padding: var(--csp-kanban-column-padding);
  border-top: var(--csp-kanban-column-accent-width) solid var(--border-plain-info);
  background-color: var(--background-alt-grey);
  box-shadow: inset 0 0 0 1px var(--border-default-grey);
}

.palette-usages__etape {
  display: flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0 var(--csp-kanban-column-header-padding-inline);
  font-size: 0.9375rem;
  font-weight: 700;
  line-height: 1.3;
  color: var(--text-title-grey);
}

.palette-usages__pastille {
  flex-shrink: 0;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
}

.palette-usages__etape-nom {
  min-width: 0;
}

.palette-usages__etape :deep(.badge) {
  margin: 0;
}

.palette-usages__statut {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-2);
  padding: var(--csp-space-3) var(--csp-space-1) 0;
  border-top: 1px solid var(--border-default-grey);
}

.palette-usages__statut-titre {
  margin: 0;
  font-size: 0.75rem;
  color: var(--text-mention-grey);
}

.palette-usages__statut :deep(.badge) {
  margin: 0;
}
</style>
