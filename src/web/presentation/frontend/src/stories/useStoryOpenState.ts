import { computed, ref, watch } from 'vue'

interface StoryOpenArgs {
  open?: boolean
}

export function useStoryOpenState(args: StoryOpenArgs) {
  const open = ref(Boolean(args.open))

  watch(
    () => args.open,
    (value) => {
      if (value === undefined) {
        return
      }

      open.value = value
    },
  )

  const controlledOpen = computed(() => (args.open === undefined ? undefined : open.value))

  function handleUpdateOpen(value: boolean) {
    open.value = value
  }

  return {
    open,
    controlledOpen,
    handleUpdateOpen,
  }
}
