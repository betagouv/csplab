export function labelOptions<T extends string>(labels: Record<T, string>): { value: T, label: string }[] {
  return (Object.keys(labels) as T[]).map(value => ({ value, label: labels[value] }))
}
