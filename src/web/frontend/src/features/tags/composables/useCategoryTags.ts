import type { TagCategory } from '../types'
import { computed } from 'vue'
import { useTags } from './useTags'

export function useCategoryTags(organismeUuid: string, category: TagCategory) {
  const { tags, pending, error } = useTags(organismeUuid)

  const categoryTags = computed(() =>
    (tags.value ?? [])
      .filter(tag => tag.category === category)
      .sort((a, b) => a.name.localeCompare(b.name, 'fr')),
  )

  return { tags: categoryTags, pending, error }
}
