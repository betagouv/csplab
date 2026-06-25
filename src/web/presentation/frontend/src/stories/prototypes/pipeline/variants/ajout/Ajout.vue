<script setup lang="ts">
import type { EtapePrototype } from '../../data/pipelineMock'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDropdownMenu from '@/components/base/CspDropdownMenu/CspDropdownMenu.vue'
import CspSortableList from '@/components/base/CspSortableList/CspSortableList.vue'
import { createPipeline, isObligatoire } from '../../data/pipelineMock'
import AddEtapeDialog from '../../shared/AddEtapeDialog.vue'

interface Props {
  // 'bottom'  = un bouton unique sous la liste (insère en fin de segment)
  // 'menu'    = via le menu « … » (au-dessus / en dessous d'une étape)
  // 'naming'  = bouton unique → modale (nom + position)
  approach: 'bottom' | 'menu' | 'naming'
}

const props = defineProps<Props>()

const etapes = ref<EtapePrototype[]>(createPipeline())

const addOpen = ref(false)

const noms = computed(() => etapes.value.map(e => e.nom))

function onReorder(items: EtapePrototype[]) {
  etapes.value = items
}

function variantOf(etape: EtapePrototype): 'default' | 'alt' {
  return isObligatoire(etape) ? 'alt' : 'default'
}

// Borne basse / haute du segment réordonnable (entre les étapes obligatoires).
function lastEnCoursIndex(): number {
  return etapes.value.map(e => e.categorie).lastIndexOf('EN_COURS')
}

function bottomInsertIndex(): number {
  return lastEnCoursIndex() === -1 ? etapes.value.length : lastEnCoursIndex() + 1
}

// Positions d'insertion valides : avant la 1re EN_COURS jusqu'après la dernière.
const positionOptions = computed(() => {
  const firstEnCours = etapes.value.findIndex(e => e.categorie === 'EN_COURS')
  const start = firstEnCours === -1 ? bottomInsertIndex() : firstEnCours
  const end = bottomInsertIndex()
  const options: { index: number, label: string }[] = []
  for (let i = start; i <= end; i++) {
    const before = etapes.value[i - 1]
    const after = etapes.value[i]
    let label: string
    if (i === end)
      label = before ? `Après « ${before.nom} »` : 'En dernier'
    else if (!before)
      label = `Avant « ${after.nom} »`
    else
      label = `Entre « ${before.nom} » et « ${after.nom} »`
    options.push({ index: i, label })
  }
  return options
})

function insertEtape(index: number, nom: string) {
  const next = [...etapes.value]
  next.splice(index, 0, {
    identifiant: `e-${crypto.randomUUID()}`,
    categorie: 'EN_COURS',
    nom,
    statutCandidat: 'EN_COURS',
  })
  etapes.value = next
}

// 'bottom' et 'menu' : étape « Nouvelle étape » à renommer ensuite.
function quickInsert(index: number) {
  insertEtape(index, 'Nouvelle étape')
}

// 'naming' : la modale fournit nom + position.
function onAddConfirm(payload: { nom: string, index: number }) {
  insertEtape(payload.index, payload.nom)
}

function onBottomClick() {
  if (props.approach === 'naming')
    addOpen.value = true
  else
    quickInsert(bottomInsertIndex())
}

function menuSections(index: number) {
  return [
    {
      items: [
        { label: 'Ajouter une étape au-dessus', icon: 'ri:insert-row-top', onSelect: () => quickInsert(index) },
        { label: 'Ajouter une étape en dessous', icon: 'ri:insert-row-bottom', onSelect: () => quickInsert(index + 1) },
      ],
    },
  ]
}
</script>

<template>
  <section class="ajout">
    <CspSortableList
      :items="etapes"
      :get-item-key="(e: EtapePrototype) => e.identifiant"
      :get-item-label="(e: EtapePrototype) => e.nom"
      :is-item-draggable="(e: EtapePrototype) => !isObligatoire(e)"
      :get-item-variant="variantOf"
      @reorder="onReorder"
    >
      <template #item="{ item, index, isDraggable }">
        <span class="ajout__name">{{ item.nom }}</span>
        <span
          v-if="!isDraggable"
          class="ajout__flag"
        >Obligatoire</span>

        <!-- approach 'menu' : ajout contextuel par étape -->
        <CspDropdownMenu
          v-if="approach === 'menu'"
          side="bottom"
          align="end"
          :sections="menuSections(index)"
        >
          <template #trigger>
            <CspButton
              icon="ri:add-line"
              variant="tertiary-no-outline"
              size="sm"
              :aria-label="`Ajouter une étape près de ${item.nom}`"
            />
          </template>
        </CspDropdownMenu>
      </template>
    </CspSortableList>

    <!-- approach 'bottom' et 'naming' : bouton unique sous la liste -->
    <CspButton
      v-if="approach !== 'menu'"
      class="ajout__add"
      label="Ajouter une étape"
      icon="ri:add-line"
      variant="tertiary"
      is-icon-left
      size="sm"
      @click="onBottomClick"
    />

    <!-- approach 'naming' : modale nom + position -->
    <AddEtapeDialog
      v-if="approach === 'naming'"
      v-model:open="addOpen"
      :noms="noms"
      :positions="positionOptions"
      :default-index="bottomInsertIndex()"
      @confirm="onAddConfirm"
    />
  </section>
</template>

<style scoped lang="scss">
.ajout {
  max-width: 40rem;
}

.ajout__name {
  flex: 1;
  min-width: 0;
}

.ajout__flag {
  flex: 0 0 auto;
  font-size: 0.6875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--text-mention-grey);
}

.ajout__add {
  margin-top: var(--csp-space-3);
}
</style>
