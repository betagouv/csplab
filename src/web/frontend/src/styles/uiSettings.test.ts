import { readdirSync, readFileSync } from 'node:fs'
import { dirname, join, relative } from 'node:path'
import { fileURLToPath } from 'node:url'
import { afterEach, describe, expect, it } from 'vitest'
import { applyUiSettings, initUiSettings } from './uiSettings'

const root = document.documentElement

function openPage({ preview = true, url = '/ats/', shape, density }: { preview?: boolean, url?: string, shape?: string, density?: string }) {
  window.history.replaceState(null, '', url)
  if (preview) {
    root.setAttribute('data-csp-ui-preview', '')
  }
  if (shape) {
    root.setAttribute('data-csp-shape', shape)
  }
  if (density) {
    root.setAttribute('data-csp-density', density)
  }
}

afterEach(() => {
  ['data-csp-ui-preview', 'data-csp-shape', 'data-csp-density'].forEach(attribute => root.removeAttribute(attribute))
  sessionStorage.clear()
  window.history.replaceState(null, '', '/')
})

describe('applyUiSettings', () => {
  it('sets the attribute of a value other than the default', () => {
    applyUiSettings({ shape: 'rounded', density: 'standard' })
    expect(root.getAttribute('data-csp-shape')).toBe('rounded')
    expect(root.hasAttribute('data-csp-density')).toBe(false)
  })

  it('removes the attribute of the default value', () => {
    root.setAttribute('data-csp-shape', 'rounded')
    applyUiSettings({ shape: 'dsfr', density: 'standard' })
    expect(root.hasAttribute('data-csp-shape')).toBe(false)
  })
})

describe('initUiSettings', () => {
  it('keeps the theme of the environment without the preview attribute', () => {
    sessionStorage.setItem('csp_ui_settings', JSON.stringify({ shape: 'dsfr' }))
    openPage({ preview: false, url: '/ats/?shape=dsfr', shape: 'rounded' })
    initUiSettings()
    expect(root.getAttribute('data-csp-shape')).toBe('rounded')
    expect(sessionStorage.getItem('csp_ui_settings')).toBe(JSON.stringify({ shape: 'dsfr' }))
  })

  it('applies the shape of the url and keeps it for the tab', () => {
    openPage({ url: '/ats/?shape=rounded' })
    initUiSettings()
    expect(root.getAttribute('data-csp-shape')).toBe('rounded')
    expect(JSON.parse(sessionStorage.getItem('csp_ui_settings')!)).toEqual({ shape: 'rounded' })
  })

  it('applies the shape kept for the tab after a reload', () => {
    sessionStorage.setItem('csp_ui_settings', JSON.stringify({ shape: 'rounded' }))
    openPage({})
    initUiSettings()
    expect(root.getAttribute('data-csp-shape')).toBe('rounded')
  })

  it('prefers the url to the tab and the tab to the environment', () => {
    sessionStorage.setItem('csp_ui_settings', JSON.stringify({ shape: 'rounded' }))
    openPage({ url: '/ats/?shape=dsfr', shape: 'rounded' })
    initUiSettings()
    expect(root.hasAttribute('data-csp-shape')).toBe(false)
  })

  it('keeps the theme of the environment without a choice', () => {
    openPage({ shape: 'rounded' })
    initUiSettings()
    expect(root.getAttribute('data-csp-shape')).toBe('rounded')
    expect(sessionStorage.getItem('csp_ui_settings')).toBeNull()
  })

  it('ignores an unknown value of the url and of the tab', () => {
    sessionStorage.setItem('csp_ui_settings', JSON.stringify({ density: 'dense' }))
    openPage({ url: '/ats/?shape=square&density=dense', shape: 'rounded' })
    initUiSettings()
    expect(root.getAttribute('data-csp-shape')).toBe('rounded')
    expect(root.hasAttribute('data-csp-density')).toBe(false)
    expect(JSON.parse(sessionStorage.getItem('csp_ui_settings')!)).toEqual({ density: 'dense' })
  })

  it('ignores a tab entry that is not json', () => {
    sessionStorage.setItem('csp_ui_settings', 'rounded')
    openPage({ url: '/ats/?density=standard' })
    initUiSettings()
    expect(root.hasAttribute('data-csp-density')).toBe(false)
  })
})

const FRONTEND = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const TEMPLATES = join(FRONTEND, '..', 'presentation', 'templates')
const ALLOWED = ['src/styles/uiSettings.ts', 'src/styles/shapes.css', 'src/styles/densities.css', '../presentation/templates/ats/base.html']

describe('theme attributes', () => {
  it('are mentioned only by uiSettings.ts, the theme sheets and the page of the ats', () => {
    const files = [join(FRONTEND, 'src'), join(FRONTEND, '.storybook'), TEMPLATES]
      .flatMap(folder => readdirSync(folder, { recursive: true, encoding: 'utf8' }).map(file => join(folder, file)))
      .filter(file => /\.(?:vue|ts|css|scss|html)$/.test(file) && !/\.test\.ts$/.test(file))
      .map(file => relative(FRONTEND, file))
    const writers = files
      .filter(file => !ALLOWED.includes(file) && /data-csp-(?:shape|density)/.test(readFileSync(join(FRONTEND, file), 'utf8')))
      .map(file => `${file}: read a role variable, uiSettings.ts owns the theme attributes`)
    expect(writers).toEqual([])
  })
})
