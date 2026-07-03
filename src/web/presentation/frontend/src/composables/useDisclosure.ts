import { ref } from 'vue'

export function useDisclosure(initialOpen = false) {
  const isOpen = ref(initialOpen)

  function open(): void {
    isOpen.value = true
  }

  function close(): void {
    isOpen.value = false
  }

  function toggle(): void {
    isOpen.value = !isOpen.value
  }

  return {
    isOpen,
    open,
    close,
    toggle,
  }
}
