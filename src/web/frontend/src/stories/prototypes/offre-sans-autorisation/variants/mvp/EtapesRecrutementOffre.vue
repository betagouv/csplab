<script setup lang="ts">
import type { Offre } from './store'
import { computed, ref } from 'vue'
import CspBadge from '@/components/base/CspBadge/CspBadge.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCallout from '@/components/base/CspCallout/CspCallout.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'
import { db } from './store'

// Reprise de l'écran existant « Personnaliser les étapes de recrutement de l'offre » (EtapesRecrutementList,
// retour PO point 4) : mêmes textes, même liste ordonnable, même encadré. Données simulées sur l'offre.
const props = defineProps<{ offre: Offre }>()
const o = computed(() => props.offre)
const etapes = computed(() => (o.value.etapesProcessus.length ? o.value.etapesProcessus : db.organisme.etapesRecrutement))

// Statut visible par le candidat : la première étape est « À traiter », la dernière « Acceptée ».
function statut(i: number) {
  if (i === 0) {
    return { label: 'À traiter', icon: 'ri:inbox-2-line', type: undefined }
  }
  if (i === etapes.value.length - 1) {
    return { label: 'Acceptée', icon: 'ri:checkbox-circle-line', type: 'success' as const }
  }
  return { label: 'En cours', icon: 'ri:loader-4-line', type: 'info' as const }
}
function enregistrer(liste: string[]) {
  o.value.etapesProcessus = liste
  o.value.processusPersonnalise = true
}

const ajout = ref(false)
const nom = ref('')
function ajouter() {
  if (nom.value.trim()) {
    const l = [...etapes.value]
    l.splice(l.length - 1, 0, nom.value.trim())
    enregistrer(l)
  }
  nom.value = ''
  ajout.value = false
}
function menu(i: number, canMoveUp: boolean, canMoveDown: boolean, moveUp: () => void, moveDown: () => void) {
  const verrou = i === 0 || i === etapes.value.length - 1
  return [{
    items: [
      { label: 'Monter', icon: 'ri:arrow-up-line', disabled: !canMoveUp, onSelect: moveUp },
      { label: 'Descendre', icon: 'ri:arrow-down-line', disabled: !canMoveDown, onSelect: moveDown },
      { label: 'Supprimer', icon: 'ri:delete-bin-line', disabled: verrou, onSelect: () => enregistrer(etapes.value.filter((_, j) => j !== i)) },
    ],
  }]
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
            @click="o.etapesProcessus = [...db.organisme.etapesRecrutement]; o.processusPersonnalise = false"
          />
          <CspButton
            label="Ajouter une étape"
            icon="ri:add-line"
            variant="secondary"
            is-icon-left
            @click="ajout = true"
          />
        </div>
      </header>
      <CspSortableList
        :items="[...etapes]"
        :get-item-key="(e: string) => e"
        :get-item-label="(e: string) => e"
        :is-item-draggable="(_e: string, i: number) => i !== 0 && i !== etapes.length - 1"
        :get-item-variant="(_e: string, i: number) => (i === 0 || i === etapes.length - 1 ? 'alt' : 'default')"
        show-position
        handle-placement="gutter"
        @reorder="enregistrer"
      >
        <template #header>
          <span class="etapes-list__header-ordre">Ordre</span>
          <span class="etapes-list__header-nom">Nom de l'étape</span>
          <span class="etapes-list__header-statut">Statut visible par le candidat</span>
          <span class="etapes-list__header-actions" />
        </template>
        <template #item="{ item, index, canMoveUp, canMoveDown, moveUp, moveDown }">
          <span class="etapes-list__item-nom">{{ item }}</span>
          <CspBadge
            class="etapes-list__item-badge"
            size="md"
            :icon="statut(index).icon"
            :type="statut(index).type"
            :label="statut(index).label"
          />
          <CspDropdownMenu
            :sections="menu(index, canMoveUp, canMoveDown, moveUp, moveDown)"
            side="bottom"
            align="end"
          >
            <template #trigger>
              <CspButton
                icon="ri:more-2-fill"
                variant="tertiary-no-outline"
                size="sm"
                :aria-label="`Actions pour ${item}`"
              />
            </template>
          </CspDropdownMenu>
        </template>
      </CspSortableList>
    </div>
    <aside class="etapes-list__aside">
      <CspCallout
        variant="info"
        title="Modification des étapes de recrutement"
        description="Ces étapes ne s'appliquent qu'à cette offre et remplacent le modèle défini dans les paramètres de l'organisme. Une étape ne doit pas contenir de candidature pour pouvoir être supprimée."
      />
    </aside>

    <CspDialog
      v-model:open="ajout"
      title="Ajouter une étape"
      size="sm"
    >
      <CspInput
        v-model="nom"
        label="Nom de l'étape"
        placeholder="Ex: Entretien technique"
        @keydown.enter="ajouter"
      />
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="ajout = false"
        />
        <CspButton
          label="Ajouter"
          @click="ajouter"
        />
      </template>
    </CspDialog>
  </div>
</template>

<style scoped lang="scss">
.etapes-list {
  display: flex;
  gap: var(--csp-space-10, 2.5rem);
}

.etapes-list__main {
  flex: 1;
  min-width: 0;
}

.etapes-list__aside {
  flex-shrink: 0;
  width: 18rem;
}

@media (width <= 75rem) {
  .etapes-list {
    flex-direction: column;
  }

  .etapes-list__aside {
    width: auto;
  }
}

.etapes-list__header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--csp-space-3);
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
  flex-shrink: 0;
  width: 3rem;
  text-align: center;
}

.etapes-list__header-nom {
  flex: 1;
}

.etapes-list__header-statut {
  flex-shrink: 0;
}

.etapes-list__header-actions {
  flex-shrink: 0;
  width: 2rem;
}
</style>
