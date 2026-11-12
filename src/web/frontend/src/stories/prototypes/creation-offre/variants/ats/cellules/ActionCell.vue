<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import { useNav } from '../nav'
import { actionAFaire } from '../suivi'

// « Action à faire » : la prochaine étape pour la personne qui suit l'offre ; une simple mention si rien n'est à faire.
defineOptions({ inheritAttrs: false })

const props = defineProps<{ row: Offre }>()
const { aller } = useNav()
const a = computed(() => actionAFaire(props.row))
</script>

<template>
  <button
    v-if="a?.ecran"
    type="button"
    class="action"
    @click="aller(a.ecran)"
  >
    {{ a.label }}
  </button>
  <span
    v-else-if="a"
    class="mention"
  >{{ a.label }}</span>
  <span
    v-else
    class="mention"
  >-</span>
</template>

<style scoped lang="scss">
.action {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-align: left;
  text-decoration: underline;
  text-underline-offset: 3px;
  cursor: pointer;

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.mention {
  color: var(--text-mention-grey);
}
</style>
