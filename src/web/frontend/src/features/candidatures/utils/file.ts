export function formatFileSize(bytes: number): string {
  if (bytes < 1000)
    return `${bytes} o`
  if (bytes < 1_000_000)
    return `${Math.round(bytes / 1000)} ko`
  return `${(bytes / 1_000_000).toFixed(1).replace('.', ',')} Mo`
}
