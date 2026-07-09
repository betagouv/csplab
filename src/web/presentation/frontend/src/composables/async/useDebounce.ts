import type { Ref, WatchSource } from 'vue'
import { onScopeDispose, ref, watch } from 'vue'

export function useDebounce<T>(source: WatchSource<T>, delay = 250): Readonly<Ref<T>> {
  const debounced = ref(toValue(source)) as Ref<T>
  let timer: ReturnType<typeof setTimeout> | undefined

  watch(source, (value) => {
    clearTimeout(timer)
    timer = setTimeout(() => {
      debounced.value = value
    }, delay)
  })

  onScopeDispose(() => clearTimeout(timer))

  return debounced
}

function toValue<T>(source: WatchSource<T>): T {
  return typeof source === 'function' ? (source as () => T)() : source.value
}
