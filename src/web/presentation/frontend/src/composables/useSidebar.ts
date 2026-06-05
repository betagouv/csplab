import type { ComputedRef, InjectionKey, Ref } from 'vue'
import { computed, inject, onMounted, onUnmounted, provide, ref, watch } from 'vue'

export const SIDEBAR_COOKIE_NAME = 'csp_sidebar_state'
export const SIDEBAR_COOKIE_MAX_AGE = 60 * 60 * 24 * 30
export const SIDEBAR_KEYBOARD_SHORTCUT = 'b'
export const SIDEBAR_WIDTH = '15rem'
export const SIDEBAR_WIDTH_COLLAPSED = '4rem'
export const SIDEBAR_BREAKPOINT = 768

export interface SidebarContext {
  state: ComputedRef<'expanded' | 'collapsed'>
  isExpanded: Ref<boolean>
  isMobile: Ref<boolean>
  isMobileOpen: Ref<boolean>
  setExpanded: (value: boolean) => void
  setMobileOpen: (value: boolean) => void
  toggle: () => void
}

export const SIDEBAR_INJECTION_KEY = Symbol('sidebar') as InjectionKey<SidebarContext>

function getCookieValue(name: string): string | null {
  if (typeof document === 'undefined') {
    return null
  }
  const match = document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`))
  return match ? match[2] : null
}

function setCookieValue(name: string, value: string, maxAge: number): void {
  if (typeof document === 'undefined') {
    return
  }
  document.cookie = `${name}=${value}; path=/; max-age=${maxAge}`
}

function useMediaQuery(breakpoint: number) {
  const matches = ref(false)

  function updateMatch() {
    if (typeof window !== 'undefined') {
      matches.value = window.innerWidth <= breakpoint
    }
  }

  onMounted(() => {
    updateMatch()
    window.addEventListener('resize', updateMatch)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', updateMatch)
  })

  return matches
}

export function provideSidebar(options: {
  defaultExpanded?: boolean
  persistState?: boolean
}) {
  const { defaultExpanded = true, persistState = true } = options

  const storedState = getCookieValue(SIDEBAR_COOKIE_NAME)
  const initialExpanded = storedState !== null
    ? storedState === 'true'
    : defaultExpanded

  const isExpanded = ref(initialExpanded)
  const isMobile = useMediaQuery(SIDEBAR_BREAKPOINT)
  const isMobileOpen = ref(false)

  const state = computed<'expanded' | 'collapsed'>(() =>
    isExpanded.value ? 'expanded' : 'collapsed',
  )

  function setExpanded(value: boolean) {
    isExpanded.value = value
    if (persistState) {
      setCookieValue(SIDEBAR_COOKIE_NAME, String(value), SIDEBAR_COOKIE_MAX_AGE)
    }
  }

  function setMobileOpen(value: boolean) {
    isMobileOpen.value = value
  }

  function toggle() {
    if (isMobile.value) {
      setMobileOpen(!isMobileOpen.value)
    }
    else {
      setExpanded(!isExpanded.value)
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (
      event.key === SIDEBAR_KEYBOARD_SHORTCUT
      && (event.metaKey || event.ctrlKey)
    ) {
      event.preventDefault()
      toggle()
    }
  }

  onMounted(() => {
    window.addEventListener('keydown', handleKeydown)
  })

  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
  })

  watch(isMobile, (mobile) => {
    if (!mobile && isMobileOpen.value) {
      isMobileOpen.value = false
    }
  })

  const context: SidebarContext = {
    state,
    isExpanded,
    isMobile,
    isMobileOpen,
    setExpanded,
    setMobileOpen,
    toggle,
  }

  provide(SIDEBAR_INJECTION_KEY, context)

  return context
}

export function useSidebar(): SidebarContext {
  const context = inject(SIDEBAR_INJECTION_KEY)

  if (!context) {
    throw new Error('useSidebar must be used within a CspSidebar provider')
  }

  return context
}
