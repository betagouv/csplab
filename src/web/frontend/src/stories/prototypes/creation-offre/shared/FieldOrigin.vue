<script setup lang="ts">
import { computed } from 'vue'
import CspIcon from '@/components/base/CspIcon/CspIcon.vue'
import { useOffre } from '../data/useOffre'

// Indique qu'une valeur a été reprise d'une source (DAR, fiche de poste, offre dupliquée)
// et si elle a été modifiée depuis. Permet de revenir à la valeur d'origine.
const props = defineProps<{ path: string }>()

const { origine, restaurer, verrouille } = useOffre()
const info = computed(() => origine(props.path))
</script>

<template>
  <span
    v-if="info"
    class="field-origin"
    :class="{ 'field-origin--modifie': info.modifie }"
  >
    <CspIcon
      :name="info.modifie ? 'ri:edit-2-line' : 'ri:file-copy-2-line'"
      :size="12"
    />
    {{ info.libelle }}<template v-if="info.modifie">
      · modifié
    </template>
    <button
      v-if="info.modifie && !verrouille"
      type="button"
      class="field-origin__restore"
      @click="restaurer(path)"
    >
      Rétablir
    </button>
  </span>
</template>

<style scoped lang="scss">
.field-origin {
  display: inline-flex;
  align-items: center;
  gap: var(--csp-space-1);
  font-size: var(--csp-font-size-xs);
  color: var(--text-action-high-blue-france);
  background: var(--background-alt-blue-france);
  padding: 0 var(--csp-space-2);
  border-radius: 2px;
  line-height: 1.5rem;
  white-space: nowrap;

  &--modifie {
    color: var(--text-mention-grey);
    background: var(--background-alt-grey);
  }
}

.field-origin__restore {
  margin-inline-start: var(--csp-space-1);
  padding: 0;
  border: 0;
  background: none;
  color: var(--text-action-high-blue-france);
  font-size: inherit;
  text-decoration: underline;
  cursor: pointer;
}
</style>
