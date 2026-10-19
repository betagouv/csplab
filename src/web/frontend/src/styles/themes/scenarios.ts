// To add a theme: write styles/themes/<id>.css with every rule under :root[data-csp-theme='<id>'], import it in index.css, then list it in THEMES (DEFAULT_THEME applies it without the toolbar).

export interface Theme {
  id: string
  name: string
}

export const THEMES: Theme[] = [
  { id: 'dsfr', name: 'Rester dans le DSFR' },
  { id: 'greige', name: 'Greige chaleureux' },
  { id: 'lasuite', name: 'Rapprochement avec La Suite' },
]

export const DEFAULT_THEME: string | null = null

export const THEME_ATTRIBUTE = 'data-csp-theme'

export function applyTheme(element: HTMLElement, id: string | null | undefined): void {
  if (id && THEMES.some(theme => theme.id === id)) {
    element.setAttribute(THEME_ATTRIBUTE, id)
  }
  else {
    element.removeAttribute(THEME_ATTRIBUTE)
  }
}
