import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { labelOptions } from '@/utils/options'

export function tabMetaFor<T extends string>(_labels: Record<T, string>) {
  return (tab: T): { tab: T } => ({ tab })
}

export function tabItems<T extends string>(
  labels: Record<T, string>,
  icons?: Record<T, string>,
): CspTabItem<T>[] {
  return labelOptions(labels).map(option => ({ ...option, icon: icons?.[option.value] }))
}
