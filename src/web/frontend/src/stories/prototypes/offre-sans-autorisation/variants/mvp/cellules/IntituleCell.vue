<script setup lang="ts">
import type { Offre } from '../store'
import { computed } from 'vue'
import { useNav } from '../nav'
import { fiche } from '../store'

// Intitulé, puis service · lieu · référence pour distinguer des offres au même intitulé.
defineOptions({ inheritAttrs: false })
const props = defineProps<{ row: Offre }>()
const { aller } = useNav()
const service = computed(() => props.row.service ?? fiche(props.row.ficheId)?.service.split(' — ').at(-1) ?? '')
const sous = computed(() => [service.value, props.row.lieu, props.row.id].filter(Boolean).join(' · '))
</script>

<template>
  <div class="intitule">
    <button
      type="button"
      class="intitule__titre"
      @click="aller({ nom: 'offre', id: row.id })"
    >
      {{ row.titre || 'Sans titre' }}
    </button>
    <span class="intitule__sous">{{ sous }}</span>
  </div>
</template>

<style scoped lang="scss">
.intitule {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.intitule__titre {
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-weight: 600;
  color: var(--text-title-grey);
  text-align: left;
  cursor: pointer;

  &:hover {
    text-decoration: underline;
  }

  &:focus-visible {
    outline: 2px solid var(--csp-focus-ring-color);
    outline-offset: 2px;
  }
}

.intitule__sous {
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
