export function pluralize(count: number, singular: string, plural?: string): string {
  return count > 1 ? (plural ?? `${singular}s`) : singular
}

export function getInitials(name?: string | null): string | null {
  name = (name ?? '').trim()

  if (!name) {
    return null
  }

  const parts = name
    .split(/[\s\-]+/)
    .map(p => p.trim())
    .filter(Boolean)

  if (parts.length === 0) {
    return null
  }

  if (parts.length === 1) {
    return parts[0]
      .slice(0, 2)
      .toUpperCase()
  }

  const first = parts[0][0] ?? ''
  const last = parts.at(-1)?.[0] ?? ''

  return `${first}${last}`.toUpperCase()
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1000) {
    return `${bytes} o`
  }
  if (bytes < 1_000_000) {
    return `${Math.round(bytes / 1000)} ko`
  }
  return `${(bytes / 1_000_000).toFixed(1).replace('.', ',')} Mo`
}
