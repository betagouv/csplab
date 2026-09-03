import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'

export function tabMetaFor<T extends string>(_labels: Record<T, string>) {
  return (tab: T): { tab: T } => ({ tab })
}

export function tabItems<T extends string>(
  labels: Record<T, string>,
  icons?: Record<T, string>,
): CspTabItem<T>[] {
  return (Object.keys(labels) as T[]).map(value => ({ value, label: labels[value], icon: icons?.[value] }))
}
