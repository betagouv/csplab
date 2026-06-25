<script setup lang="ts">
import type { EtapePrototype } from '../../data/pipelineMock'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'
import { createPipeline, isObligatoire } from '../../data/pipelineMock'
import { useDirtyState } from '../../data/useDirtyState'
import ConfirmDeleteDialog from '../../shared/ConfirmDeleteDialog.vue'
import RenameEtapeDialog from '../../shared/RenameEtapeDialog.vue'

interface Props {
  // 'commit'  = brouillon + barre contextuelle dirty (Enregistrer / Annuler)
  // 'auto'    = chaque modif persiste, indicateur d'état, undo ponctuel
  // 'hybride' = chaque action structurante est atomique + undo en ligne
  model: 'commit' | 'auto' | 'hybride'
}

const props = defineProps<Props>()

const { draft: etapes, isDirty, changeCount, commit, reset } = useDirtyState(createPipeline())

const renameTarget = ref<EtapePrototype | null>(null)
const renameOpen = ref(false)
const deleteTarget = ref<EtapePrototype | null>(null)
const deleteOpen = ref(false)

const noms = computed(() => etapes.value.map(e => e.nom))

// --- Indicateur d'état (auto-save) ---
const saveState = ref<'idle' | 'saving' | 'saved'>('idle')
let saveTimer: ReturnType<typeof setTimeout> | null = null

// --- Undo ponctuel (auto / hybride) ---
const lastAction = ref<{ label: string, undo: () => void } | null>(null)
let undoTimer: ReturnType<typeof setTimeout> | null = null

function flashUndo(label: string, undo: () => void) {
  lastAction.value = { label, undo }
  if (undoTimer)
    clearTimeout(undoTimer)
  undoTimer = setTimeout(() => (lastAction.value = null), 6000)
}

// En auto-save, on simule une persistance après chaque modif.
function persistAuto() {
  if (props.model !== 'auto')
    return
  saveState.value = 'saving'
  if (saveTimer)
    clearTimeout(saveTimer)
  saveTimer = setTimeout(() => {
    commit()
    saveState.value = 'saved'
  }, 600)
}

// En hybride, chaque action structurante est immédiatement persistée.
function persistHybride() {
  if (props.model === 'hybride')
    commit()
}

function afterMutation(action?: { label: string, undo: () => void }) {
  persistAuto()
  persistHybride()
  if (action && props.model !== 'commit')
    flashUndo(action.label, action.undo)
}

function variantOf(etape: EtapePrototype): 'default' | 'alt' {
  return isObligatoire(etape) ? 'alt' : 'default'
}

function onReorder(items: EtapePrototype[]) {
  const before = [...etapes.value]
  etapes.value = items
  afterMutation({
    label: 'Étape déplacée',
    undo: () => {
      etapes.value = before
      afterMutation()
    },
  })
}

function openRename(etape: EtapePrototype) {
  renameTarget.value = etape
  renameOpen.value = true
}

function applyRename(nom: string) {
  if (!renameTarget.value)
    return
  const target = renameTarget.value
  const before = target.nom
  etapes.value = etapes.value.map(e =>
    e.identifiant === target.identifiant ? { ...e, nom } : e,
  )
  afterMutation({
    label: `« ${before} » renommée`,
    undo: () => {
      etapes.value = etapes.value.map(e =>
        e.identifiant === target.identifiant ? { ...e, nom: before } : e,
      )
      afterMutation()
    },
  })
}

function askRemove(etape: EtapePrototype) {
  deleteTarget.value = etape
  deleteOpen.value = true
}

function confirmRemove() {
  if (!deleteTarget.value)
    return
  const removed = deleteTarget.value
  const at = etapes.value.findIndex(e => e.identifiant === removed.identifiant)
  etapes.value = etapes.value.filter(e => e.identifiant !== removed.identifiant)
  afterMutation({
    label: `« ${removed.nom} » supprimée`,
    undo: () => {
      const next = [...etapes.value]
      next.splice(at, 0, removed)
      etapes.value = next
      afterMutation()
    },
  })
}

function addEtape() {
  const lastEnCours = etapes.value.map(e => e.categorie).lastIndexOf('EN_COURS')
  const at = lastEnCours === -1 ? etapes.value.length : lastEnCours + 1
  const etape: EtapePrototype = {
    identifiant: `e-${crypto.randomUUID()}`,
    categorie: 'EN_COURS',
    nom: 'Nouvelle étape',
    statutCandidat: 'EN_COURS',
  }
  const next = [...etapes.value]
  next.splice(at, 0, etape)
  etapes.value = next
  afterMutation({
    label: 'Étape ajoutée',
    undo: () => {
      etapes.value = etapes.value.filter(e => e.identifiant !== etape.identifiant)
      afterMutation()
    },
  })
}

function onSave() {
  commit()
  saveState.value = 'saved'
}
</script>

<template>
  <section
    class="etat"
    :class="`etat--${model}`"
  >
    <!-- En-tête : indicateur d'état selon le modèle -->
    <header class="etat__head">
      <span class="etat__title">Étapes de recrutement</span>

      <span
        v-if="model === 'auto'"
        class="etat__status"
        :class="`etat__status--${saveState}`"
        aria-live="polite"
      >
        <template v-if="saveState === 'saving'">
          <CspIcon
            name="ri:loader-2-line"
            :size="14"
            class="etat__spin"
          /> Enregistrement…
        </template>
        <template v-else-if="saveState === 'saved'">
          <CspIcon
            name="ri:check-line"
            :size="14"
          /> Enregistré
        </template>
        <template v-else>
          Modifications enregistrées automatiquement
        </template>
      </span>
    </header>

    <CspSortableList
      :items="etapes"
      :get-item-key="(e: EtapePrototype) => e.identifiant"
      :get-item-label="(e: EtapePrototype) => e.nom"
      :is-item-draggable="(e: EtapePrototype) => !isObligatoire(e)"
      :get-item-variant="variantOf"
      @reorder="onReorder"
    >
      <template #item="{ item, isDraggable }">
        <span class="etat__name">{{ item.nom }}</span>
        <span
          v-if="!isDraggable"
          class="etat__flag"
        >Obligatoire</span>

        <div class="etat__actions">
          <CspButton
            icon="ri:pencil-line"
            variant="tertiary-no-outline"
            size="sm"
            :aria-label="`Renommer ${item.nom}`"
            @click="openRename(item)"
          />
          <CspButton
            v-if="isDraggable"
            icon="ri:delete-bin-line"
            variant="tertiary-no-outline"
            size="sm"
            :aria-label="`Supprimer ${item.nom}`"
            @click="askRemove(item)"
          />
        </div>
      </template>
    </CspSortableList>

    <CspButton
      class="etat__add"
      label="Ajouter une étape"
      icon="ri:add-line"
      variant="tertiary"
      is-icon-left
      size="sm"
      @click="addEtape"
    />

    <!-- Undo ponctuel (auto / hybride) -->
    <div
      v-if="model !== 'commit' && lastAction"
      class="etat__undo"
      role="status"
    >
      <CspIcon
        name="ri:check-line"
        :size="16"
      />
      <span>{{ lastAction.label }}</span>
      <button
        type="button"
        class="etat__undo-btn"
        @click="lastAction.undo()"
      >
        Annuler
      </button>
    </div>

    <!-- Barre contextuelle dirty (commit explicite) -->
    <Transition name="etat-bar">
      <div
        v-if="model === 'commit' && isDirty"
        class="etat__bar"
        role="region"
        aria-label="Modifications non enregistrées"
      >
        <span class="etat__bar-info">
          <CspIcon
            name="ri:error-warning-line"
            :size="18"
          />
          {{ changeCount }} modification{{ changeCount > 1 ? 's' : '' }} non enregistrée{{ changeCount > 1 ? 's' : '' }}
        </span>
        <span class="etat__bar-actions">
          <CspButton
            label="Annuler"
            variant="secondary"
            size="sm"
            @click="reset"
          />
          <CspButton
            label="Enregistrer"
            variant="primary"
            size="sm"
            @click="onSave"
          />
        </span>
      </div>
    </Transition>

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
.etat {
  max-width: 40rem;
  // Réserve l'espace pour la barre sticky afin qu'elle ne masque pas le dernier élément.
  padding-bottom: 4.5rem;
}

.etat__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-3);
  margin-bottom: var(--csp-space-4);
}

.etat__title {
  font-size: var(--csp-font-size-lg, 1.125rem);
  font-weight: 700;
  color: var(--text-title-grey);
}

.etat__status {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: 0.8125rem;
  color: var(--text-mention-grey);
}

.etat__status--saved {
  color: var(--text-default-success);
}

.etat__spin {
  animation: etat-spin 0.8s linear infinite;
}

@keyframes etat-spin {
  to {
    transform: rotate(360deg);
  }
}

.etat__name {
  flex: 1;
  min-width: 0;
}

.etat__flag {
  flex: 0 0 auto;
  font-size: 0.6875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--text-mention-grey);
}

.etat__actions {
  display: flex;
  align-items: center;
  gap: var(--csp-space-1);
}

.etat__add {
  margin-top: var(--csp-space-3);
}

/* --- Undo ponctuel --- */
.etat__undo {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
  margin-top: var(--csp-space-4);
  padding: var(--csp-space-2) var(--csp-space-3);
  border-radius: 0.25rem;
  background: var(--background-contrast-grey);
  font-size: 0.8125rem;
  color: var(--text-default-grey);
}

.etat__undo-btn {
  border: none;
  background: none;
  padding: 0;
  font: inherit;
  font-weight: 500;
  color: var(--text-action-high-blue-france);
  cursor: pointer;
  text-decoration: underline;
}

/* --- Barre contextuelle dirty --- */
.etat__bar {
  position: sticky;
  bottom: var(--csp-space-4);
  margin-top: var(--csp-space-5);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-4);
  padding: var(--csp-space-3) var(--csp-space-4);
  border-radius: 0.25rem;
  background: var(--background-overlap-grey, var(--background-default-grey));
  box-shadow:
    inset 0 0 0 1px var(--border-default-grey),
    var(--csp-shadow-lg);
}

.etat__bar-info {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-2);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-default-warning, var(--text-default-grey));
}

.etat__bar-actions {
  display: inline-flex;
  gap: var(--csp-space-2);
}

.etat-bar-enter-active,
.etat-bar-leave-active {
  transition:
    opacity 160ms ease,
    transform 160ms ease;
}

.etat-bar-enter-from,
.etat-bar-leave-to {
  opacity: 0;
  transform: translateY(0.5rem);
}
</style>
