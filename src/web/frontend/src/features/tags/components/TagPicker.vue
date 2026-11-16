<script setup lang="ts">
import type { TagCategory } from '../types'
import { computed, ref } from 'vue'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspLabel from '@/components/base/CspLabel/CspLabel.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useTags } from '../composables/useTags'
import { tagPaletteColor } from '../format'

const props = defineProps<{
  organismeUuid: string
  category: TagCategory
  appliedTagUuids: string[]
  addingTagUuid?: string | null
}>()

const emit = defineEmits<{
  add: [tagUuid: string]
}>()

const { tags, pending, error } = useTags(props.organismeUuid)
const showSkeleton = useMinimumPending(pending)

const search = ref('')

const categoryTags = computed(() =>
  (tags.value ?? [])
    .filter(tag => tag.category === props.category)
    .sort((a, b) => a.name.localeCompare(b.name, 'fr')),
)

const visibleTags = computed(() => {
  const term = search.value.trim().toLocaleLowerCase('fr')
  return term
    ? categoryTags.value.filter(tag => tag.name.toLocaleLowerCase('fr').includes(term))
    : categoryTags.value
})

function isApplied(tagUuid: string): boolean {
  return props.appliedTagUuids.includes(tagUuid)
}
</script>

<template>
  <div class="tag-picker">
    <p class="tag-picker__title">
      Ajouter une étiquette
    </p>
    <CspSearchBar
      v-model="search"
      mode="live"
      label="Rechercher une étiquette"
      hide-label
      placeholder="Rechercher une étiquette"
    />
    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement des étiquettes"
      error-title="Impossible de charger les étiquettes"
    >
      <ul
        v-if="visibleTags.length > 0"
        class="tag-picker__list"
        aria-label="Étiquettes"
      >
        <li
          v-for="tag in visibleTags"
          :key="tag.uuid"
          class="tag-picker__item"
        >
          <CspLabel
            :label="tag.name"
            :color="tagPaletteColor(tag)"
          />
          <CspButton
            :label="isApplied(tag.uuid) ? 'Déjà ajoutée' : 'Ajouter'"
            variant="tertiary-no-outline"
            size="sm"
            :aria-label="isApplied(tag.uuid) ? `L'étiquette ${tag.name} est déjà ajoutée` : `Ajouter l'étiquette ${tag.name}`"
            :disabled="isApplied(tag.uuid) || addingTagUuid === tag.uuid"
            @click="emit('add', tag.uuid)"
          />
        </li>
      </ul>
      <p
        v-else
        class="tag-picker__empty"
      >
        {{ categoryTags.length > 0 ? 'Aucune étiquette ne correspond.' : 'Aucune étiquette.' }}
      </p>
    </CspAsyncSection>
  </div>
</template>

<style scoped lang="scss">
.tag-picker {
  display: flex;
  width: var(--csp-popover-width);
  max-width: 100%;
  flex-direction: column;
  gap: var(--csp-space-3);
}

.tag-picker__title {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
}

.tag-picker__list {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  list-style: none;
}

.tag-picker__item {
  display: flex;
  gap: var(--csp-space-2);
  align-items: center;
  justify-content: space-between;
}

.tag-picker__empty {
  margin: 0;
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}
</style>
