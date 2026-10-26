<script setup lang="ts">
import type { CreateTagPayload, Tag, TagCategory } from '../types'
import { computed, ref } from 'vue'
import { isHttpStatus } from '@/api/errors'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useToast } from '@/composables/ui/useToast'
import { pluralize } from '@/utils/format'
import { useTags } from '../composables/useTags'
import { DEFAULT_TAG_COLOR, TAG_CATEGORIES, TAG_CATEGORY_TEXTS, TAG_COLOR_ACCENTS } from '../constants/tag'
import TagForm from './TagForm.vue'

const props = defineProps<{
  organismeUuid: string
}>()

const { tags, pending, error, createTag, creatingTag } = useTags(props.organismeUuid)
const { addToast } = useToast()

const showSkeleton = useMinimumPending(pending)

const drawerOpen = ref(false)
const drawerCategory = ref<TagCategory>('candidature')
const duplicate = ref<CreateTagPayload | null>(null)

const tagsByCategory = computed(() => {
  const groups = Object.fromEntries(TAG_CATEGORIES.map(category => [category, [] as Tag[]])) as Record<TagCategory, Tag[]>
  for (const tag of tags.value ?? []) {
    groups[tag.category].push(tag)
  }
  return groups
})

function openDrawer(category: TagCategory): void {
  drawerCategory.value = category
  duplicate.value = null
  drawerOpen.value = true
}

async function handleCreate(payload: CreateTagPayload): Promise<void> {
  try {
    await createTag(payload)
    addToast({ variant: 'success', title: 'Étiquette ajoutée' })
    drawerOpen.value = false
  }
  catch (submitError) {
    if (isHttpStatus(submitError, 409)) {
      duplicate.value = payload
      return
    }
    addToast({ variant: 'error', title: 'L\'ajout de l\'étiquette a échoué' })
  }
}
</script>

<template>
  <section class="tags-section">
    <CspAsyncSection
      :pending="showSkeleton"
      :error="error"
      loading-label="Chargement des étiquettes"
      error-title="Impossible de charger les étiquettes"
    >
      <div class="tags-section__blocks">
        <section
          v-for="category in TAG_CATEGORIES"
          :key="category"
          class="tags-section__block"
          :aria-labelledby="`tags-${category}`"
        >
          <div class="tags-section__header">
            <h2
              :id="`tags-${category}`"
              class="tags-section__title"
            >
              {{ TAG_CATEGORY_TEXTS[category].title }}
            </h2>
            <p class="tags-section__count">
              {{ tagsByCategory[category].length }} {{ pluralize(tagsByCategory[category].length, 'étiquette') }}
            </p>
          </div>
          <p class="tags-section__description">
            {{ TAG_CATEGORY_TEXTS[category].description }}
          </p>

          <ul
            v-if="tagsByCategory[category].length > 0"
            class="tags-section__list"
          >
            <li
              v-for="tag in tagsByCategory[category]"
              :key="tag.uuid"
            >
              <CspTag
                :label="tag.name"
                :accent="TAG_COLOR_ACCENTS[tag.color ?? DEFAULT_TAG_COLOR]"
              />
            </li>
          </ul>
          <p
            v-else
            class="tags-section__empty"
          >
            Aucune étiquette.
          </p>

          <CspButton
            variant="tertiary"
            size="sm"
            label="Ajouter une étiquette"
            icon="ri:add-line"
            @click="openDrawer(category)"
          />
        </section>
      </div>
    </CspAsyncSection>

    <CspDrawer
      v-model:open="drawerOpen"
      title="Ajouter une étiquette"
      size="md"
    >
      <TagForm
        :category="drawerCategory"
        :saving="creatingTag"
        :duplicate="duplicate"
        @create="handleCreate"
        @cancel="drawerOpen = false"
      />
    </CspDrawer>
  </section>
</template>

<style scoped lang="scss">
.tags-section__blocks {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-8);
}

.tags-section__block {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--csp-space-3);
}

.tags-section__header {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: var(--csp-space-1) var(--csp-space-3);
}

.tags-section__title {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  font-weight: 600;
}

.tags-section__count,
.tags-section__description,
.tags-section__empty {
  margin: 0;
  font-size: var(--csp-font-size-base);
  color: var(--text-mention-grey);
}

.tags-section__count {
  white-space: nowrap;
}

.tags-section__description {
  max-width: 65ch;
}

.tags-section__list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}
</style>
