<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import ListEditor from '../../shared/ListEditor.vue'
import Panel from '../../shared/Panel.vue'
import { db } from './store'

// Étape 4 — processus : la rédaction de l'offre est aussi le moment où l'on paramètre le recrutement.
// Par défaut, le processus de l'organisme ; on peut le personnaliser pour cette offre (facultatif).
const props = defineProps<{ offre: Offre }>()
const o = computed(() => props.offre)

function personnaliser(v: boolean) {
  o.value.processusPersonnalise = v
  if (!v) {
    o.value.etapesProcessus = [...db.organisme.etapesRecrutement]
  }
}
</script>

<template>
  <Panel
    titre="Étapes de recrutement"
    description="Les étapes que suivront les candidatures une fois l'offre publiée."
  >
    <ol class="etapes">
      <li
        v-for="e in (o.processusPersonnalise ? o.etapesProcessus : db.organisme.etapesRecrutement)"
        :key="e"
      >
        {{ e }}
      </li>
    </ol>
    <CspSwitch
      :model-value="o.processusPersonnalise"
      label="Personnaliser le processus pour cette offre (facultatif)"
      @update:model-value="personnaliser"
    />
    <ListEditor
      v-if="o.processusPersonnalise"
      v-model="o.etapesProcessus"
      label="Étapes de cette offre"
      add-label="Ajouter une étape"
    />
  </Panel>
</template>

<style scoped lang="scss">
.etapes {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: var(--csp-font-size-sm);

  li {
    padding: var(--csp-space-1) var(--csp-space-3);
    border: 1px solid var(--border-default-grey);
    background: var(--background-alt-grey);
  }

  li + li::before {
    content: '› ';
    color: var(--text-mention-grey);
  }
}
</style>
