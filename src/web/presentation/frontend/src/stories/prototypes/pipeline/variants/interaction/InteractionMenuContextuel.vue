<script setup lang="ts">
import type { EtapePrototype } from '../../data/pipelineMock'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'
import { createPipeline, isObligatoire } from '../../data/pipelineMock'
import ConfirmDeleteDialog from '../../shared/ConfirmDeleteDialog.vue'
import RenameEtapeDialog from '../../shared/RenameEtapeDialog.vue'

interface MenuItem {
  label: string
  icon?: string
  disabled?: boolean
  destructive?: boolean
  onSelect: () => void
}

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

function insertAt(index: number) {
  const next = [...etapes.value]
  next.splice(index, 0, {
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

interface MenuContext {
  item: EtapePrototype
  index: number
  obligatoire: boolean
  canMoveUp: boolean
  canMoveDown: boolean
  moveUp: () => void
  moveDown: () => void
}

function menuSections(ctx: MenuContext) {
  const { item, index, obligatoire, canMoveUp, canMoveDown, moveUp, moveDown } = ctx

  const sections: { items: MenuItem[] }[] = [
    {
      items: [
        { label: 'Renommer l\'étape', icon: 'ri:pencil-line', onSelect: () => openRename(item) },
      ],
    },
  ]

  if (!obligatoire) {
    sections.push(
      {
        items: [
          { label: 'Déplacer vers le haut', icon: 'ri:arrow-up-line', disabled: !canMoveUp, onSelect: moveUp },
          { label: 'Déplacer vers le bas', icon: 'ri:arrow-down-line', disabled: !canMoveDown, onSelect: moveDown },
        ],
      },
      {
        items: [
          { label: 'Ajouter une étape au-dessus', icon: 'ri:add-line', onSelect: () => insertAt(index) },
          { label: 'Ajouter une étape en dessous', icon: 'ri:add-line', onSelect: () => insertAt(index + 1) },
        ],
      },
      {
        items: [
          { label: 'Supprimer l\'étape', icon: 'ri:delete-bin-line', destructive: true, onSelect: () => askRemove(item) },
        ],
      },
    )
  }

  return sections
}
</script>

<template>
  <section class="proto-b">
    <CspSortableList
      :items="etapes"
      :get-item-key="(e: EtapePrototype) => e.identifiant"
      :get-item-label="(e: EtapePrototype) => e.nom"
      :is-item-draggable="(e: EtapePrototype) => !isObligatoire(e)"
      :get-item-variant="variantOf"
      @reorder="onReorder"
    >
      <template #item="{ item, index, isDraggable, canMoveUp, canMoveDown, moveUp, moveDown }">
        <span class="proto-b__name">{{ item.nom }}</span>
        <span
          v-if="!isDraggable"
          class="proto-b__flag"
        >Obligatoire</span>

        <CspDropdownMenu
          side="bottom"
          align="end"
          :sections="menuSections({ item, index, obligatoire: !isDraggable, canMoveUp, canMoveDown, moveUp, moveDown })"
        >
          <template #trigger>
            <CspButton
              icon="ri:more-2-fill"
              variant="tertiary-no-outline"
              size="sm"
              :aria-label="`Options pour ${item.nom}`"
            />
          </template>
        </CspDropdownMenu>
      </template>
    </CspSortableList>

    <CspButton
      class="proto-b__add"
      label="Ajouter une étape"
      icon="ri:add-line"
      variant="tertiary"
      is-icon-left
      size="sm"
      @click="insertAt(etapes.length - 1)"
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
.proto-b {
  max-width: 40rem;
}

.proto-b__name {
  flex: 1;
  min-width: 0;
}

.proto-b__flag {
  flex: 0 0 auto;
  font-size: 0.6875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--text-mention-grey);
}

.proto-b__add {
  margin-top: var(--csp-space-3);
}
</style>
