import { computed, onMounted, onUnmounted, ref, watch } from 'vue'

export type ColorMode = 'light' | 'dark' | 'system'

const STORAGE_KEY = 'csp_color_mode'

const colorMode = ref<ColorMode>('system')
const systemPrefersDark = ref(false)

function getSystemPreference(): boolean {
  if (typeof window === 'undefined')
    return false
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

function applyTheme(isDark: boolean) {
  if (typeof document === 'undefined')
    return
  document.documentElement.setAttribute('data-fr-theme', isDark ? 'dark' : 'light')
}

export function useColorMode() {
  const isDark = computed(() => {
    if (colorMode.value === 'system') {
      return systemPrefersDark.value
    }
    return colorMode.value === 'dark'
  })

  function setColorMode(mode: ColorMode) {
    colorMode.value = mode
    localStorage.setItem(STORAGE_KEY, mode)
    applyTheme(isDark.value)
  }

  function toggle() {
    const newMode = isDark.value ? 'light' : 'dark'
    setColorMode(newMode)
  }

  let mediaQuery: MediaQueryList | null = null
  let handler: ((e: MediaQueryListEvent) => void) | null = null

  onMounted(() => {
    systemPrefersDark.value = getSystemPreference()

    const stored = localStorage.getItem(STORAGE_KEY) as ColorMode | null
    if (stored && ['light', 'dark', 'system'].includes(stored)) {
      colorMode.value = stored
    }

    applyTheme(isDark.value)

    mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    handler = (e: MediaQueryListEvent) => {
      systemPrefersDark.value = e.matches
      if (colorMode.value === 'system') {
        applyTheme(e.matches)
      }
    }
    mediaQuery.addEventListener('change', handler)
  })

  onUnmounted(() => {
    if (mediaQuery && handler) {
      mediaQuery.removeEventListener('change', handler)
    }
  })

  watch(isDark, (dark) => {
    applyTheme(dark)
  })

  return {
    colorMode,
    isDark,
    setColorMode,
    toggle,
  }
}
