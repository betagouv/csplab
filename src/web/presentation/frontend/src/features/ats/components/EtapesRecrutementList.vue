<script setup lang="ts">
import type { EtapeRecrutement } from '../api/recrutement'
import { onMounted } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'
import { useEtapesRecrutement } from '../composables/useEtapesRecrutement'
import { CATEGORIE_BADGE } from '../constants/etape-recrutement'

const TEMP_ORGANISME_UUID = '00000000-0000-0000-0000-000000000000'

const {
  etapes,
  loading,
  saving,
  error,
  isEtapeLocked,
  fetchEtapes,
  reorderEtapes,
  addEtape,
  removeEtape,
} = useEtapesRecrutement(TEMP_ORGANISME_UUID)

onMounted(fetchEtapes)

function getMenuSections(
  item: EtapeRecrutement,
  canMoveUp: boolean,
  canMoveDown: boolean,
  moveUp: () => void,
  moveDown: () => void,
) {
  return [
    {
      items: [
        { label: 'Monter', icon: 'ri:arrow-up-s-line', disabled: !canMoveUp, onSelect: moveUp },
        { label: 'Descendre', icon: 'ri:arrow-down-s-line', disabled: !canMoveDown, onSelect: moveDown },
      ],
    },
    {
      items: [
        {
          label: 'Supprimer',
          icon: 'ri:delete-bin-line',
          destructive: true,
          disabled: isEtapeLocked(item),
          onSelect: () => removeEtape(item.etape_uuid),
        },
      ],
    },
  ]
}
</script>

<template>
  <div class="etapes-list">
    <header class="etapes-list__header">
      <h2 class="etapes-list__title">
        Étapes de recrutement
      </h2>
      <CspButton
        label="Ajouter une étape"
        icon="ri:add-line"
        variant="secondary"
        is-icon-left
        :disabled="saving"
        @click="addEtape"
      />
    </header>

    <div
      v-if="loading"
      class="etapes-list__loading"
    >
      Chargement...
    </div>

    <div
      v-else-if="error"
      class="etapes-list__error"
    >
      Une erreur est survenue lors du chargement des étapes.
    </div>

    <CspSortableList
      v-else
      :items="[...etapes]"
      :get-item-key="(etape) => etape.etape_uuid"
      :get-item-label="(etape) => etape.nom"
      :is-item-draggable="(etape) => !isEtapeLocked(etape)"
      :get-item-variant="(etape) => isEtapeLocked(etape) ? 'alt' : 'default'"
      show-position
      @reorder="reorderEtapes"
    >
      <template #header>
        <span class="etapes-list__header-spacer" />
        <span class="etapes-list__header-ordre">Ordre</span>
        <span class="etapes-list__header-nom">Nom de l'étape</span>
        <span class="etapes-list__header-statut">Statut visible par le candidat</span>
        <span class="etapes-list__header-actions" />
      </template>
      <template #item="{ item, canMoveUp, canMoveDown, moveUp, moveDown }">
        <span class="etapes-list__item-nom">{{ item.nom }}</span>
        <CspBadge
          class="etapes-list__item-badge"
          size="md"
          :icon="CATEGORIE_BADGE[item.categorie].icon"
          :type="CATEGORIE_BADGE[item.categorie].type"
          :label="CATEGORIE_BADGE[item.categorie].label"
        />
        <CspDropdownMenu
          :sections="getMenuSections(item, canMoveUp, canMoveDown, moveUp, moveDown)"
          side="bottom"
          align="end"
        >
          <template #trigger>
            <CspButton
              icon="ri:more-2-fill"
              variant="tertiary-no-outline"
              size="sm"
              :aria-label="`Actions pour ${item.nom}`"
            />
          </template>
        </CspDropdownMenu>
      </template>
    </CspSortableList>
  </div>
</template>

<style scoped lang="scss">
.etapes-list__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--csp-space-6);
}

.etapes-list__title {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.etapes-list__loading,
.etapes-list__error {
  padding: var(--csp-space-4);
  color: var(--text-mention-grey);
}

.etapes-list__error {
  color: var(--text-default-error);
}

.etapes-list__item-nom {
  flex: 1;
}

.etapes-list__item-badge {
  align-self: center;
}

.etapes-list__header-spacer {
  width: 1rem;
  flex-shrink: 0;
}

.etapes-list__header-ordre {
  width: 3rem;
  text-align: center;
  flex-shrink: 0;
}

.etapes-list__header-nom {
  flex: 1;
}

.etapes-list__header-statut {
  flex-shrink: 0;
}

.etapes-list__header-actions {
  width: 2rem;
  flex-shrink: 0;
}
</style>
