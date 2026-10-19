import { computed, ref } from 'vue'

// Each id but kit has its file styles/themes/<id>.css, imported by styles/themes/index.css
export const UI_THEMES = [
  { id: 'kit', name: 'Kit' },
  { id: 'dsfr', name: 'DSFR' },
  { id: 'greige', name: 'Greige' },
  { id: 'lasuite', name: 'La Suite' },
] as const

type UiThemeId = typeof UI_THEMES[number]['id']

const STORAGE_KEY = 'csp_ui_theme'
const URL_PARAMETER = 'theme'

const current = ref<UiThemeId>('kit')

function isUiTheme(id: string | null | undefined): id is UiThemeId {
  return UI_THEMES.some(theme => theme.id === id)
}

// The server sets data-csp-theme-default only where WEB_UI_THEME is set: without it, no theme and no choice
function serverDefault(): string | undefined {
  return document.documentElement.dataset.cspThemeDefault
}

function apply(id: UiThemeId): void {
  current.value = id
  if (id === 'kit') {
    document.documentElement.removeAttribute('data-csp-theme')
  }
  else {
    document.documentElement.setAttribute('data-csp-theme', id)
  }
}

export function initUiTheme(): void {
  const fallback = serverDefault()
  if (fallback === undefined) {
    return
  }
  const requested = new URLSearchParams(window.location.search).get(URL_PARAMETER)
  if (isUiTheme(requested)) {
    localStorage.setItem(STORAGE_KEY, requested)
  }
  const stored = localStorage.getItem(STORAGE_KEY)
  apply(isUiTheme(stored) ? stored : isUiTheme(fallback) ? fallback : 'kit')
}

export function useUiTheme() {
  const isEnabled = serverDefault() !== undefined
  const currentName = computed(() => UI_THEMES.find(theme => theme.id === current.value)!.name)

  function selectNext(): void {
    const index = UI_THEMES.findIndex(theme => theme.id === current.value)
    const next = UI_THEMES[(index + 1) % UI_THEMES.length]!.id
    localStorage.setItem(STORAGE_KEY, next)
    apply(next)
  }

  return { isEnabled, currentName, selectNext }
}
