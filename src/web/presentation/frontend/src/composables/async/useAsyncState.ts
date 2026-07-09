import type { Ref } from 'vue'
import { readonly, ref } from 'vue'

export async function runAsyncAction(
  pending: Ref<boolean>,
  error: Ref<Error | null>,
  action: () => Promise<void>,
): Promise<void> {
  pending.value = true
  error.value = null
  try {
    await action()
  }
  catch (err) {
    error.value = err as Error
  }
  finally {
    pending.value = false
  }
}

export function useAsyncState(initialPending = false) {
  const pending = ref(initialPending)
  const error = ref<Error | null>(null)

  async function run(action: () => Promise<void>): Promise<void> {
    await runAsyncAction(pending, error, action)
  }

  return {
    pending: readonly(pending),
    error: readonly(error),
    run,
  }
}
