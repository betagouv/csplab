import type { ComputedRef, InjectionKey } from 'vue'
import { computed, inject, onScopeDispose, provide, shallowRef } from 'vue'

export interface CandidaturesToolbarAction {
  label: string
  icon: string
  onClick: () => void
}

export interface CandidaturesToolbarState {
  count: string
  pending: boolean
  selectionCount: number
  selectionLabel?: string
  selectionActions: CandidaturesToolbarAction[]
}

type ToolbarSource = () => Partial<CandidaturesToolbarState>

interface CandidaturesToolbarContext {
  state: ComputedRef<CandidaturesToolbarState>
  register: (source: ToolbarSource) => () => void
}

const KEY: InjectionKey<CandidaturesToolbarContext> = Symbol('candidatures-toolbar')

export function provideCandidaturesToolbar(): void {
  const source = shallowRef<ToolbarSource | null>(null)

  const state = computed<CandidaturesToolbarState>(() => ({
    count: '',
    pending: true,
    selectionCount: 0,
    selectionActions: [],
    ...source.value?.(),
  }))

  function register(next: ToolbarSource): () => void {
    source.value = next
    return () => {
      if (source.value === next) {
        source.value = null
      }
    }
  }

  provide(KEY, { state, register })
}

function injectContext(): CandidaturesToolbarContext {
  const context = inject(KEY)
  if (!context) {
    throw new Error('useCandidaturesToolbar must be used within provideCandidaturesToolbar')
  }
  return context
}

export function useCandidaturesToolbar(): ComputedRef<CandidaturesToolbarState> {
  return injectContext().state
}

export function publishCandidaturesToolbar(source: ToolbarSource): void {
  onScopeDispose(injectContext().register(source))
}
