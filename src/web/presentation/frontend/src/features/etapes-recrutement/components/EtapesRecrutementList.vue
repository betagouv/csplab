<script setup lang="ts">
import type { EtapeRecrutement } from '../types'
import { ref, watch } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSkeletonSortableList from '@/components/base/CspSkeleton/CspSkeletonSortableList.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useToast } from '@/composables/ui/useToast'
import { TEMP_ORGANISME_UUID } from '@/constants/organisme'
import { useEtapesRecrutement } from '../composables/useEtapesRecrutement'
import { CATEGORIE_CONFIG } from '../constants/etape-recrutement'

const {
  etapes,
  loading,
  saving,
  error,
  isEtapeLocked,
  reorderEtapes,
  addEtape,
  addEtapeAt,
  renameEtape,
  removeEtape,
  resetEtapes,
} = useEtapesRecrutement(TEMP_ORGANISME_UUID)

const showSkeleton = useMinimumPending(loading)

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

const resetModalOpen = ref(false)

async function handleResetConfirm() {
  await resetEtapes()
  resetModalOpen.value = false
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
  const isLocked = isEtapeLocked(item)
  return [
    {
      items: [
        {
          label: 'Renommer',
          icon: 'ri:edit-line',
          onSelect: () => openRenameModal(item),
        },
      ],
    },
    {
      items: [
        {
          label: 'Ajouter une étape au-dessus',
          icon: 'ri:add-line',
          disabled: isLocked,
          onSelect: () => openAddAtModal(index),
        },
        {
          label: 'Ajouter une étape en dessous',
          icon: 'ri:add-line',
          disabled: isLocked,
          onSelect: () => openAddAtModal(index + 1),
        },
      ],
    },
    {
      items: [
        { label: 'Monter', icon: 'ri:arrow-up-s-line', disabled: !canMoveUp || isLocked, onSelect: moveUp },
        { label: 'Descendre', icon: 'ri:arrow-down-s-line', disabled: !canMoveDown || isLocked, onSelect: moveDown },
      ],
    },
    {
      items: [
        {
          label: 'Supprimer',
          icon: 'ri:delete-bin-line',
          destructive: true,
          disabled: isLocked,
          onSelect: () => openDeleteModal(item),
        },
      ],
    },
  ]
}
</script>

<template>
  <div class="etapes-list">
    <div class="etapes-list__main">
      <header class="etapes-list__header">
        <h2 class="etapes-list__title">
          Étapes de recrutement
        </h2>
        <div class="etapes-list__actions">
          <CspButton
            label="Réinitialiser"
            icon="ri:restart-line"
            variant="tertiary"
            is-icon-left
            :disabled="saving || loading"
            @click="resetModalOpen = true"
          />
          <CspButton
            label="Ajouter une étape"
            icon="ri:add-line"
            variant="secondary"
            is-icon-left
            :disabled="saving"
            @click="openAddModal"
          />
        </div>
      </header>

      <CspAsyncSection
        :pending="showSkeleton"
        :error="error"
        loading-label="Chargement des étapes"
        error-title="Une erreur est survenue lors du chargement des étapes."
      >
        <template #skeleton>
          <CspSkeletonSortableList :rows="6" />
        </template>
        <CspSortableList
          :items="[...etapes]"
          :get-item-key="(etape) => etape.etape_uuid"
          :get-item-label="(etape) => etape.nom"
          :is-item-draggable="(etape) => !isEtapeLocked(etape)"
          :get-item-variant="(etape) => isEtapeLocked(etape) ? 'alt' : 'default'"
          show-position
          @reorder="reorderEtapes"
        >
          <template #header>
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
              :icon="CATEGORIE_CONFIG[item.categorie].icon"
              :type="CATEGORIE_CONFIG[item.categorie].type"
              :label="CATEGORIE_CONFIG[item.categorie].label"
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
      </CspAsyncSection>
    </div>

    <aside class="etapes-list__aside">
      <CspCallout
        variant="info"
        title="Modification des étapes de recrutement"
        description="Ce modèle d'étapes sera appliqué par défaut à tous les nouveaux recrutements. Les modifications apportées à ce modèle ne s'appliqueront qu'aux nouvelles offres."
      />
    </aside>

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

    <CspDialog
      v-model:open="resetModalOpen"
      title="Réinitialiser les étapes"
      description="Voulez-vous vraiment réinitialiser les étapes de recrutement ? Toutes vos personnalisations seront perdues et remplacées par la configuration par défaut."
      size="sm"
    >
      <template #footer>
        <div class="etapes-list__modal-footer">
          <CspButton
            label="Annuler"
            variant="secondary"
            @click="resetModalOpen = false"
          />
          <CspButton
            label="Réinitialiser"
            variant="primary"
            :disabled="saving"
            @click="handleResetConfirm"
          />
        </div>
      </template>
    </CspDialog>
  </div>
</template>

<style scoped lang="scss">
.etapes-list {
  display: flex;
  gap: var(--csp-space-8);
}

.etapes-list__main {
  flex: 1;
  min-width: 0;
}

.etapes-list__aside {
  flex-shrink: 0;
  width: 20rem;
}

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

.etapes-list__actions {
  display: flex;
  gap: var(--csp-space-3);
}

.etapes-list__item-nom {
  flex: 1;
}

.etapes-list__item-badge {
  align-self: center;
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
