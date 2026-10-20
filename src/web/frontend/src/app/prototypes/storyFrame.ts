// Globals of the current story, which the preview decorator writes on the root element, for a story framed inside it
export function currentGlobals(): string {
  const root = document.documentElement
  return [
    `interfaceTheme:${root.getAttribute('data-csp-theme') ?? 'kit'}`,
    `theme:${root.getAttribute('data-fr-theme') ?? 'light'}`,
    `density:${root.getAttribute('data-csp-density') ?? 'compact'}`,
    `etiquettes:${root.getAttribute('data-csp-etiquettes') ?? 'repli'}`,
  ].join(';')
}

// Address of a story rendered with the globals of the current story
export function storyFrameSrc(id: string): string {
  return `${window.location.pathname}?id=${encodeURIComponent(id)}&viewMode=story&globals=${currentGlobals()}`
}
