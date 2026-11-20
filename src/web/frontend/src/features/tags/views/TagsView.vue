<script setup lang="ts">
import type { CreateTagPayload, Tag, TagCategory } from '../types'
import { computed, ref } from 'vue'
import { isHttpStatus } from '@/api/errors'
import CspAsyncSection from '@/components/base/CspAsyncSection/CspAsyncSection.vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import { useMinimumPending } from '@/composables/async/useMinimumPending'
import { useToast } from '@/composables/ui/useToast'
import { pluralize, quote } from '@/utils/format'
import TagForm from '../components/TagForm.vue'
import TagList from '../components/TagList.vue'
import { useTags } from '../composables/useTags'
import { TAG_CATEGORIES, TAG_CATEGORY_TEXTS } from '../constants/tag'

const props = defineProps<{
  organismeUuid: string
}>()

const { tags, pending, error, createTag, creatingTag, updateTag, updatingTag, deleteTag, deletingTag } = useTags(props.organismeUuid)
const { addToast } = useToast()

const showSkeleton = useMinimumPending(pending)

const drawerOpen = ref(false)
const drawerCategory = ref<TagCategory>('candidature')
const editedTag = ref<Tag | null>(null)
const duplicate = ref<CreateTagPayload | null>(null)
const deletedTag = ref<Tag | null>(null)
const deletionDialogOpen = ref(false)

const tagsByCategory = computed(() => {
  const groups = Object.fromEntries(TAG_CATEGORIES.map(category => [category, [] as Tag[]])) as Record<TagCategory, Tag[]>
  for (const tag of tags.value ?? []) {
    groups[tag.category].push(tag)
  }
  return groups
})

function openDrawer(category: TagCategory, tag: Tag | null = null): void {
  drawerCategory.value = category
  editedTag.value = tag
  duplicate.value = null
  drawerOpen.value = true
}

async function handleSave(payload: CreateTagPayload): Promise<void> {
  const tag = editedTag.value
  try {
    if (tag) {
      await updateTag({ tagUuid: tag.uuid, payload: { name: payload.name, color: payload.color } })
      addToast({ variant: 'success', title: 'Étiquette modifiée' })
    }
    else {
      await createTag(payload)
      addToast({ variant: 'success', title: 'Étiquette ajoutée' })
    }
    drawerOpen.value = false
  }
  catch (submitError) {
    if (isHttpStatus(submitError, 409)) {
      duplicate.value = payload
      return
    }
    if (tag && isHttpStatus(submitError, 404)) {
      addToast({ variant: 'warning', title: 'Cette étiquette a été supprimée' })
      drawerOpen.value = false
      return
    }
    addToast({ variant: 'error', title: tag ? 'La modification de l\'étiquette a échoué' : 'L\'ajout de l\'étiquette a échoué' })
  }
}

function usageText(tag: Tag): string {
  if (tag.usage_count === 0) {
    return 'Cette étiquette n\'est posée nulle part.'
  }
  const [singular, plural] = TAG_CATEGORY_TEXTS[tag.category].usage
  return `Cette étiquette est posée sur ${tag.usage_count} ${pluralize(tag.usage_count, singular, plural)}. Elle en sera retirée.`
}

function openDeletionDialog(tag: Tag): void {
  deletedTag.value = tag
  deletionDialogOpen.value = true
}

async function confirmDeletion(): Promise<void> {
  const tag = deletedTag.value
  if (!tag) {
    return
  }
  try {
    await deleteTag(tag.uuid)
  }
  catch (deletionError) {
    if (!isHttpStatus(deletionError, 404)) {
      addToast({ variant: 'error', title: 'La suppression de l\'étiquette a échoué' })
      return
    }
  }
  addToast({ variant: 'success', title: 'Étiquette supprimée' })
  deletionDialogOpen.value = false
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

          <TagList
            v-if="tagsByCategory[category].length > 0"
            :tags="tagsByCategory[category]"
            :edit-label="tag => `Modifier l'étiquette ${tag.name}`"
            :dismiss-label="tag => `Supprimer l'étiquette ${tag.name}`"
            @edit="tag => openDrawer(category, tag)"
            @dismiss="openDeletionDialog"
          />
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
      :title="editedTag ? 'Modifier l\'étiquette' : 'Ajouter une étiquette'"
      size="md"
    >
      <TagForm
        :category="drawerCategory"
        :tag="editedTag"
        :saving="creatingTag || updatingTag"
        :duplicate="duplicate"
        @save="handleSave"
        @cancel="drawerOpen = false"
      />
    </CspDrawer>

    <CspDialog
      v-model:open="deletionDialogOpen"
      :title="deletedTag ? `Supprimer l'étiquette ${quote(deletedTag.name)}` : null"
      size="sm"
    >
      <template v-if="deletedTag">
        {{ usageText(deletedTag) }}
      </template>

      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="deletionDialogOpen = false"
        />
        <CspButton
          label="Supprimer"
          :disabled="deletingTag"
          @click="confirmDeletion"
        />
      </template>
    </CspDialog>
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
</style>
