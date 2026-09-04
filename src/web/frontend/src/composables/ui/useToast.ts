import { readonly, ref } from 'vue'

export type ToastVariant = 'default' | 'info' | 'success' | 'warning' | 'error'

export interface ToastOptions {
  variant?: ToastVariant
  title?: string
  description?: string
  duration?: number
}

export interface ToastItem extends ToastOptions {
  id: number
}

const toasts = ref<ToastItem[]>([])
let nextId = 0

function addToast(options: ToastOptions): number {
  const id = nextId++
  toasts.value = [...toasts.value, { id, variant: 'default', ...options }]
  return id
}

function dismissToast(id: number): void {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

export function useToast() {
  return {
    toasts: readonly(toasts),
    addToast,
    dismissToast,
  }
}
