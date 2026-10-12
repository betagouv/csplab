import type { MaybeRefOrGetter } from 'vue'
import { useHead } from '@unhead/vue'
import { toValue } from 'vue'

const SEPARATOR = ' - '

export function useDocumentTitle(...parts: MaybeRefOrGetter<string | null | undefined>[]): void {
  useHead({
    title: () => parts.map(part => toValue(part)).filter(Boolean).join(SEPARATOR),
  })
}
