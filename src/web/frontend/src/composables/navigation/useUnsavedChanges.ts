import type { InjectionKey } from 'vue'
import type { RouteLocationNormalized } from 'vue-router'
import { computed, inject, onMounted, onScopeDispose, onUnmounted, provide, shallowReactive, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

interface UnsavedInput {
  isDirty: () => boolean
  discard: () => void
}

interface UnsavedChangesGuardOptions {
  ignore?: (to: RouteLocationNormalized, from: RouteLocationNormalized) => boolean
}

const UNSAVED_INPUTS: InjectionKey<Set<UnsavedInput>> = Symbol('unsavedInputs')

export function useUnsavedChangesGuard({ ignore }: UnsavedChangesGuardOptions = {}) {
  const inputs = shallowReactive(new Set<UnsavedInput>())
  provide(UNSAVED_INPUTS, inputs)

  const hasUnsavedChanges = computed(() => [...inputs].some(input => input.isDirty()))
  const pending = shallowRef<((leave: boolean) => void) | null>(null)

  function settle(leave: boolean): void {
    const resolve = pending.value
    pending.value = null
    if (leave)
      inputs.forEach(input => input.discard())
    resolve?.(leave)
  }

  async function confirmLeave(): Promise<boolean> {
    if (!hasUnsavedChanges.value)
      return true
    settle(false)
    return new Promise((resolve) => {
      pending.value = resolve
    })
  }

  const removeGuard = useRouter().beforeEach((to, from) => ignore?.(to, from) || confirmLeave())
  onScopeDispose(removeGuard)

  function warnBeforeUnload(event: BeforeUnloadEvent): void {
    if (hasUnsavedChanges.value)
      event.preventDefault()
  }
  onMounted(() => window.addEventListener('beforeunload', warnBeforeUnload))
  onUnmounted(() => window.removeEventListener('beforeunload', warnBeforeUnload))

  return {
    confirmLeave,
    isConfirming: computed(() => pending.value !== null),
    keepEditing: () => settle(false),
    leave: () => settle(true),
  }
}

export function useUnsavedChanges(isDirty: () => boolean, discard: () => void): void {
  const inputs = inject(UNSAVED_INPUTS, null)
  if (!inputs)
    return
  const input: UnsavedInput = { isDirty, discard }
  inputs.add(input)
  onScopeDispose(() => inputs.delete(input))
}
