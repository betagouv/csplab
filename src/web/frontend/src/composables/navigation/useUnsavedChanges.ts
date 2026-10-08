import type { InjectionKey } from 'vue'
import type { RouteLocationNormalized } from 'vue-router'
import { computed, inject, onMounted, onScopeDispose, onUnmounted, provide, shallowReactive, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

type NavigationPredicate = (to: RouteLocationNormalized, from: RouteLocationNormalized) => boolean

interface UnsavedInput {
  isDirty: () => boolean
  discard: () => void
  isLeftBy?: NavigationPredicate
}

interface UnsavedChangesGuardOptions {
  ignore?: NavigationPredicate
}

interface PendingConfirmation {
  resolve: (leave: boolean) => void
  inputs: UnsavedInput[]
}

const UNSAVED_INPUTS: InjectionKey<Set<UnsavedInput>> = Symbol('unsavedInputs')

export function useUnsavedChangesGuard({ ignore }: UnsavedChangesGuardOptions = {}) {
  const inputs = shallowReactive(new Set<UnsavedInput>())
  provide(UNSAVED_INPUTS, inputs)

  const hasUnsavedChanges = computed(() => [...inputs].some(input => input.isDirty()))
  const pending = shallowRef<PendingConfirmation | null>(null)

  function settle(leave: boolean): void {
    const confirmation = pending.value
    pending.value = null
    if (leave) {
      confirmation?.inputs.forEach(input => input.discard())
    }
    confirmation?.resolve(leave)
  }

  async function confirmLeave(leftInputs: UnsavedInput[] = [...inputs]): Promise<boolean> {
    const dirtyInputs = leftInputs.filter(input => input.isDirty())
    if (dirtyInputs.length === 0) {
      return true
    }
    settle(false)
    return new Promise((resolve) => {
      pending.value = { resolve, inputs: dirtyInputs }
    })
  }

  function isLeftBy(input: UnsavedInput, to: RouteLocationNormalized, from: RouteLocationNormalized): boolean {
    return input.isLeftBy?.(to, from) ?? !ignore?.(to, from)
  }

  const removeGuard = useRouter().beforeEach((to, from) =>
    confirmLeave([...inputs].filter(input => isLeftBy(input, to, from))),
  )
  onScopeDispose(removeGuard)

  function warnBeforeUnload(event: BeforeUnloadEvent): void {
    if (hasUnsavedChanges.value) {
      event.preventDefault()
    }
  }
  onMounted(() => window.addEventListener('beforeunload', warnBeforeUnload))
  onUnmounted(() => window.removeEventListener('beforeunload', warnBeforeUnload))

  return {
    confirmLeave: () => confirmLeave(),
    isConfirming: computed(() => pending.value !== null),
    keepEditing: () => settle(false),
    leave: () => settle(true),
  }
}

interface UnsavedChangesOptions {
  isLeftBy?: NavigationPredicate
}

export function useUnsavedChanges(
  isDirty: () => boolean,
  discard: () => void,
  { isLeftBy }: UnsavedChangesOptions = {},
): void {
  const inputs = inject(UNSAVED_INPUTS, null)
  if (!inputs) {
    return
  }
  const input: UnsavedInput = { isDirty, discard, isLeftBy }
  inputs.add(input)
  onScopeDispose(() => inputs.delete(input))
}
