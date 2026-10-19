import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { createLocalStorageMock } from '@/test/browser'
import { initUiTheme, UI_THEMES, useUiTheme } from './useUiTheme'

function setServerDefault(id: string) {
  document.documentElement.setAttribute('data-csp-theme-default', id)
}

describe('useUiTheme', () => {
  let localStorageMock: ReturnType<typeof createLocalStorageMock>

  beforeEach(() => {
    localStorageMock = createLocalStorageMock()
    vi.stubGlobal('localStorage', localStorageMock)
  })

  afterEach(() => {
    vi.unstubAllGlobals()
    window.history.replaceState(null, '', '/')
    document.documentElement.removeAttribute('data-csp-theme-default')
    document.documentElement.removeAttribute('data-csp-theme')
  })

  it('does nothing without a server default', () => {
    window.history.replaceState(null, '', '?theme=greige')

    initUiTheme()

    expect(document.documentElement.hasAttribute('data-csp-theme')).toBe(false)
    expect(useUiTheme().isEnabled).toBe(false)
  })

  it('applies the server default', () => {
    setServerDefault('dsfr')

    initUiTheme()

    expect(document.documentElement.getAttribute('data-csp-theme')).toBe('dsfr')
    expect(useUiTheme().isEnabled).toBe(true)
  })

  it('applies and stores the theme requested in the URL', () => {
    setServerDefault('dsfr')
    window.history.replaceState(null, '', '?theme=lasuite')

    initUiTheme()

    expect(document.documentElement.getAttribute('data-csp-theme')).toBe('lasuite')
    expect(localStorageMock.getItem('csp_ui_theme')).toBe('lasuite')
  })

  it('prefers the stored theme over the server default', () => {
    setServerDefault('dsfr')
    localStorageMock.setItem('csp_ui_theme', 'greige')

    initUiTheme()

    expect(document.documentElement.getAttribute('data-csp-theme')).toBe('greige')
  })

  it('falls back to kit when URL, storage and server default hold an unknown value', () => {
    setServerDefault('unknown')
    localStorageMock.setItem('csp_ui_theme', 'unknown')
    window.history.replaceState(null, '', '?theme=unknown')

    initUiTheme()

    expect(document.documentElement.hasAttribute('data-csp-theme')).toBe(false)
    expect(useUiTheme().currentName.value).toBe('Kit')
  })

  it('selectNext cycles through the themes, stores each one and returns to kit', () => {
    setServerDefault('kit')
    initUiTheme()
    const { selectNext, currentName } = useUiTheme()

    UI_THEMES.slice(1).forEach((theme) => {
      selectNext()
      expect(currentName.value).toBe(theme.name)
      expect(document.documentElement.getAttribute('data-csp-theme')).toBe(theme.id)
      expect(localStorageMock.getItem('csp_ui_theme')).toBe(theme.id)
    })

    selectNext()
    expect(currentName.value).toBe(UI_THEMES[0].name)
    expect(document.documentElement.hasAttribute('data-csp-theme')).toBe(false)
    expect(localStorageMock.getItem('csp_ui_theme')).toBe('kit')
  })
})
