<script setup lang="ts">
import type { EtapePrototype } from '../../data/pipelineMock'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'
import { createPipeline, isObligatoire } from '../../data/pipelineMock'
import ConfirmDeleteDialog from '../../shared/ConfirmDeleteDialog.vue'
import RenameEtapeDialog from '../../shared/RenameEtapeDialog.vue'

const etapes = ref<EtapePrototype[]>(createPipeline())

const renameTarget = ref<EtapePrototype | null>(null)
const renameOpen = ref(false)

const deleteTarget = ref<EtapePrototype | null>(null)
const deleteOpen = ref(false)

const noms = computed(() => etapes.value.map(e => e.nom))

function onReorder(items: EtapePrototype[]) {
  etapes.value = items
}

function variantOf(etape: EtapePrototype): 'default' | 'alt' {
  return isObligatoire(etape) ? 'alt' : 'default'
}

function openRename(etape: EtapePrototype) {
  renameTarget.value = etape
  renameOpen.value = true
}

function applyRename(nom: string) {
  if (!renameTarget.value)
    return
  const target = renameTarget.value
  etapes.value = etapes.value.map(e =>
    e.identifiant === target.identifiant ? { ...e, nom } : e,
  )
}

function addEtape() {
  const lastEnCours = etapes.value.map(e => e.categorie).lastIndexOf('EN_COURS')
  const insertAt = lastEnCours === -1 ? etapes.value.length : lastEnCours + 1
  const next = [...etapes.value]
  next.splice(insertAt, 0, {
    identifiant: `e-${crypto.randomUUID()}`,
    categorie: 'EN_COURS',
    nom: 'Nouvelle étape',
    statutCandidat: 'EN_COURS',
  })
  etapes.value = next
}

function askRemove(etape: EtapePrototype) {
  deleteTarget.value = etape
  deleteOpen.value = true
}

function confirmRemove() {
  if (!deleteTarget.value)
    return
  const id = deleteTarget.value.identifiant
  etapes.value = etapes.value.filter(e => e.identifiant !== id)
}
</script>

<template>
  <section class="proto-a">
    <CspSortableList
      :items="etapes"
      :get-item-key="(e: EtapePrototype) => e.identifiant"
      :get-item-label="(e: EtapePrototype) => e.nom"
      :is-item-draggable="(e: EtapePrototype) => !isObligatoire(e)"
      :get-item-variant="variantOf"
      @reorder="onReorder"
    >
      <template #item="{ item, isDraggable, canMoveUp, canMoveDown, moveUp, moveDown }">
        <span class="proto-a__name">{{ item.nom }}</span>
        <span
          v-if="!isDraggable"
          class="proto-a__flag"
        >Obligatoire</span>

        <div class="proto-a__actions">
          <CspButton
            icon="ri:pencil-line"
            variant="tertiary-no-outline"
            size="sm"
            :aria-label="`Renommer ${item.nom}`"
            @click="openRename(item)"
          />
          <template v-if="isDraggable">
            <CspButton
              icon="ri:arrow-up-s-line"
              variant="tertiary-no-outline"
              size="sm"
              :disabled="!canMoveUp"
              :aria-label="`Monter ${item.nom}`"
              @click="moveUp"
            />
            <CspButton
              icon="ri:arrow-down-s-line"
              variant="tertiary-no-outline"
              size="sm"
              :disabled="!canMoveDown"
              :aria-label="`Descendre ${item.nom}`"
              @click="moveDown"
            />
            <CspButton
              icon="ri:delete-bin-line"
              variant="tertiary-no-outline"
              size="sm"
              :aria-label="`Supprimer ${item.nom}`"
              @click="askRemove(item)"
            />
          </template>
        </div>
      </template>
    </CspSortableList>

    <CspButton
      class="proto-a__add"
      label="Ajouter une étape"
      icon="ri:add-line"
      variant="tertiary"
      is-icon-left
      size="sm"
      @click="addEtape"
    />

    <RenameEtapeDialog
      v-model:open="renameOpen"
      :nom="renameTarget?.nom ?? ''"
      :noms="noms"
      @confirm="applyRename"
    />

    <ConfirmDeleteDialog
      v-model:open="deleteOpen"
      :nom="deleteTarget?.nom ?? ''"
      @confirm="confirmRemove"
    />
  </section>
</template>

<style scoped lang="scss">
.proto-a {
  max-width: 40rem;
}

.proto-a__name {
  flex: 1;
  min-width: 0;
}

.proto-a__flag {
  flex: 0 0 auto;
  font-size: 0.6875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--text-mention-grey);
}

.proto-a__actions {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
}

.proto-a__add {
  margin-top: var(--csp-space-3);
}
</style>
