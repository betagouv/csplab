<script setup lang="ts">
// La colonne trie sur une clé de date ; la cellule affiche le libellé lisible.
defineOptions({ inheritAttrs: false })

defineProps<{ row: { modifieLe: string } }>()
</script>

<template>
  {{ row.modifieLe }}
</template>
