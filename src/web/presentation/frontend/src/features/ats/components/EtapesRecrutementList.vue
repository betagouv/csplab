<script setup lang="ts">
import type { EtapeRecrutement } from '../api/recrutement'
import { onMounted, ref, watch } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'
import { useToast } from '@/composables/useToast'
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
  addEtapeAt,
  renameEtape,
  removeEtape,
} = useEtapesRecrutement(TEMP_ORGANISME_UUID)

const { addToast } = useToast()

watch(error, (err) => {
  if (!err) {
    return
  }
  addToast({
    variant: 'error',
    title: 'Erreur',
    description: 'Une erreur est survenue. Veuillez réessayer.',
  })
})

onMounted(fetchEtapes)

type ModalMode = 'add' | 'add-at' | 'rename'

const modalOpen = ref(false)
const modalMode = ref<ModalMode>('add')
const modalNom = ref('')
const modalEtapeUuid = ref<string | null>(null)
const modalInsertIndex = ref<number | null>(null)

const modalTitle: Record<ModalMode, string> = {
  'add': 'Ajouter une étape',
  'add-at': 'Ajouter une étape',
  'rename': 'Renommer l\'étape',
}

const deleteModalOpen = ref(false)
const deleteEtapeUuid = ref<string | null>(null)
const deleteEtapeNom = ref('')

function openDeleteModal(etape: EtapeRecrutement) {
  deleteEtapeUuid.value = etape.etape_uuid
  deleteEtapeNom.value = etape.nom
  deleteModalOpen.value = true
}

async function handleDeleteConfirm() {
  if (!deleteEtapeUuid.value) {
    return
  }

  await removeEtape(deleteEtapeUuid.value)
  deleteModalOpen.value = false
}

function openAddModal() {
  modalMode.value = 'add'
  modalNom.value = ''
  modalEtapeUuid.value = null
  modalInsertIndex.value = null
  modalOpen.value = true
}

function openAddAtModal(index: number) {
  modalMode.value = 'add-at'
  modalNom.value = ''
  modalEtapeUuid.value = null
  modalInsertIndex.value = index
  modalOpen.value = true
}

function openRenameModal(etape: EtapeRecrutement) {
  modalMode.value = 'rename'
  modalNom.value = etape.nom
  modalEtapeUuid.value = etape.etape_uuid
  modalInsertIndex.value = null
  modalOpen.value = true
}

async function handleModalConfirm() {
  const nom = modalNom.value.trim()
  if (!nom) {
    return
  }

  if (modalMode.value === 'add') {
    await addEtape(nom)
  }
  else if (modalMode.value === 'add-at' && modalInsertIndex.value !== null) {
    await addEtapeAt(nom, modalInsertIndex.value)
  }
  else if (modalMode.value === 'rename' && modalEtapeUuid.value) {
    await renameEtape(modalEtapeUuid.value, nom)
  }

  modalOpen.value = false
}

function getMenuSections(
  item: EtapeRecrutement,
  index: number,
  canMoveUp: boolean,
  canMoveDown: boolean,
  moveUp: () => void,
  moveDown: () => void,
) {
  return [
    {
      items: [
        {
          label: 'Renommer',
          icon: 'ri:edit-line',
          disabled: isEtapeLocked(item),
          onSelect: () => openRenameModal(item),
        },
      ],
    },
    {
      items: [
        {
          label: 'Ajouter une étape au-dessus',
          icon: 'ri:add-line',
          onSelect: () => openAddAtModal(index),
        },
        {
          label: 'Ajouter une étape en dessous',
          icon: 'ri:add-line',
          onSelect: () => openAddAtModal(index + 1),
        },
      ],
    },
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
          onSelect: () => openDeleteModal(item),
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
        @click="openAddModal"
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
      <template #item="{ item, index, canMoveUp, canMoveDown, moveUp, moveDown }">
        <span class="etapes-list__item-nom">{{ item.nom }}</span>
        <CspBadge
          class="etapes-list__item-badge"
          size="md"
          :icon="CATEGORIE_BADGE[item.categorie].icon"
          :type="CATEGORIE_BADGE[item.categorie].type"
          :label="CATEGORIE_BADGE[item.categorie].label"
        />
        <CspDropdownMenu
          :sections="getMenuSections(item, index, canMoveUp, canMoveDown, moveUp, moveDown)"
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

    <CspDialog
      v-model:open="modalOpen"
      :title="modalTitle[modalMode]"
      size="sm"
    >
      <CspInput
        v-model="modalNom"
        label="Nom de l'étape"
        placeholder="Ex: Entretien technique"
        @keydown.enter="handleModalConfirm"
      />
      <template #footer>
        <div class="etapes-list__modal-footer">
          <CspButton
            label="Annuler"
            variant="secondary"
            @click="modalOpen = false"
          />
          <CspButton
            :label="modalMode === 'add' ? 'Ajouter' : 'Renommer'"
            variant="primary"
            :disabled="!modalNom.trim() || saving"
            @click="handleModalConfirm"
          />
        </div>
      </template>
    </CspDialog>

    <CspDialog
      v-model:open="deleteModalOpen"
      title="Supprimer l'étape"
      :description="`Voulez-vous vraiment supprimer l'étape « ${deleteEtapeNom} » ? Cette action est irréversible.`"
      size="sm"
    >
      <template #footer>
        <div class="etapes-list__modal-footer">
          <CspButton
            label="Annuler"
            variant="secondary"
            @click="deleteModalOpen = false"
          />
          <CspButton
            label="Supprimer"
            variant="primary"
            :disabled="saving"
            @click="handleDeleteConfirm"
          />
        </div>
      </template>
    </CspDialog>
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

.etapes-list__modal-footer {
  display: flex;
  gap: var(--csp-space-3);
  justify-content: flex-end;
}
</style>
