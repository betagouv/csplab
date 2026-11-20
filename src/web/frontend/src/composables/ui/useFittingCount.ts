import type { MaybeRefOrGetter, Ref } from 'vue'
import { nextTick, onBeforeUnmount, onMounted, ref, toValue, watch } from 'vue'

// Counts the items of a wrapping row that fit in `maxLines` lines, keeping room for the
// trailing "more" element on the last line. The container renders every item, each one
// marked with `data-fitting-item`, then the "more" element marked with `data-fitting-more`.
// The count keeps at least the first item, which the container shrinks when it is too wide.
export function useFittingCount(
  container: Ref<HTMLElement | null>,
  items: MaybeRefOrGetter<readonly unknown[]>,
  maxLines: MaybeRefOrGetter<number | undefined>,
) {
  const count = ref(toValue(items).length)

  function measure(): void {
    const element = container.value
    const lines = toValue(maxLines)
    if (!element || !lines) {
      count.value = toValue(items).length
      return
    }
    const box = element.getBoundingClientRect()
    const rects = [...element.querySelectorAll<HTMLElement>('[data-fitting-item]')].map(item => item.getBoundingClientRect())
    const lineTops = [...new Set(rects.map(item => Math.round(item.top)))].sort((a, b) => a - b)
    if (lineTops.length <= lines && rects.every(item => item.right - box.left <= box.width)) {
      count.value = rects.length
      return
    }
    const lastLineTop = lineTops[Math.min(lines, lineTops.length) - 1] ?? 0
    const moreWidth = element.querySelector<HTMLElement>('[data-fitting-more]')?.getBoundingClientRect().width ?? 0
    const gap = Number.parseFloat(getComputedStyle(element).columnGap) || 0
    let fitting = rects.filter(item => Math.round(item.top) <= lastLineTop).length
    while (fitting > 1) {
      const last = rects[fitting - 1]
      if (!last || Math.round(last.top) < lastLineTop || last.right - box.left + gap + moreWidth <= box.width) {
        break
      }
      fitting -= 1
    }
    count.value = fitting
  }

  let observer: ResizeObserver | undefined

  onMounted(() => {
    measure()
    void document.fonts?.ready.then(measure)
    observer = new ResizeObserver(measure)
    if (container.value) {
      observer.observe(container.value)
    }
  })

  onBeforeUnmount(() => observer?.disconnect())

  watch(() => [toValue(items), toValue(maxLines)], () => nextTick(measure))

  return count
}
