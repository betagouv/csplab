<script setup lang="ts">
import { activite } from '../recrutement'

// La colonne trie sur la date ; la cellule l'affiche en relatif (« Il y a 2 jours »), comme dans l'outil.
defineOptions({ inheritAttrs: false })
defineProps<{ row: { modifieLe: string } }>()
</script>

<template>
  {{ activite(row.modifieLe) }}
</template>
