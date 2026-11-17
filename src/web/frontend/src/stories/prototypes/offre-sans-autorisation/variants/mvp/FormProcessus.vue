<script setup lang="ts">
import type { Offre } from './store'
import { computed } from 'vue'
import CspSwitch from '@/components/base/CspSwitch/CspSwitch.vue'
import ListEditor from '../../shared/ListEditor.vue'
import { db } from './store'

// Étape « Processus » (facultative) : par défaut, le processus de l'organisme s'applique.
// On peut l'adapter pour cette offre ; ça ne bloque pas la publication et se modifie plus tard.
const props = defineProps<{ offre: Offre, lectureSeule?: boolean }>()
const o = computed(() => props.offre)

const personnalise = computed({
  get: () => o.value.processusPersonnalise,
  set: (v: boolean) => {
    o.value.processusPersonnalise = v
    if (v && !o.value.etapesProcessus.length) {
      o.value.etapesProcessus = [...db.organisme.etapesRecrutement]
    }
    if (!v) {
      o.value.etapesProcessus = [...db.organisme.etapesRecrutement]
    }
  },
})
</script>

<template>
  <div class="processus">
    <CspSwitch
      v-model="personnalise"
      label="Adapter les étapes de recrutement pour cette offre"
      :disabled="lectureSeule"
    />
    <div v-if="!personnalise">
      <p class="processus__label">
        Processus de l'organisme
      </p>
      <ol class="processus__etapes">
        <li
          v-for="e in db.organisme.etapesRecrutement"
          :key="e"
        >
          {{ e }}
        </li>
      </ol>
      <p class="processus__aide">
        Défini dans les paramètres de l'organisme. Il s'applique tant que vous ne l'adaptez pas.
      </p>
    </div>
    <ListEditor
      v-else
      v-model="o.etapesProcessus"
      label="Étapes de recrutement pour cette offre"
      add-label="Ajouter une étape"
      placeholder="Ex. : Mise en situation"
    />
  </div>
</template>

<style scoped lang="scss">
.processus {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  max-width: 40rem;
}

.processus__label {
  margin: 0 0 var(--csp-space-2);
  font-size: 0.875rem;
  font-weight: 600;
}

.processus__etapes {
  display: flex;
  flex-wrap: wrap;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
  counter-reset: etape;

  li {
    padding: var(--csp-space-1) var(--csp-space-3);
    border: 1px solid var(--border-default-grey);
    font-size: var(--csp-font-size-sm);
    counter-increment: etape;

    &::before {
      content: counter(etape) '. ';
      color: var(--text-mention-grey);
    }
  }
}

.processus__aide {
  margin: var(--csp-space-2) 0 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}
</style>
