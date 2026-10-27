<script setup lang="ts">
import type { Membre, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import Panel from '../../shared/Panel.vue'
import { db } from './store'

// Étape 5 — équipe : facultative, puisque le créateur de l'offre en est Responsable.
const props = defineProps<{ offre: Offre }>()
const o = computed(() => props.offre)

const disponibles = computed(() => db.organisme.agents.map(a => a.nom).filter(n => !o.value.equipe.some(m => m.nom === n)))
const choix = ref('aucun')
const role = ref<Membre['role']>('Recruteur')
const ROLES = [{ value: 'Recruteur', label: 'Recruteur' }, { value: 'Contributeur', label: 'Contributeur' }]
function ajouter() {
  if (choix.value !== 'aucun') {
    o.value.equipe = [...o.value.equipe, { nom: choix.value, role: role.value }]
    choix.value = 'aucun'
  }
}
function retirer(nom: string) {
  o.value.equipe = o.value.equipe.filter(m => m.nom !== nom)
}
</script>

<template>
  <Panel
    titre="Qui suit ce recrutement ?"
    description="Facultatif : en créant l'offre, vous en êtes Responsable. Les membres voient les candidatures."
  >
    <ul class="membres">
      <li
        v-for="m in o.equipe"
        :key="m.nom"
        class="membre"
      >
        <span><strong>{{ m.nom }}</strong><small>{{ m.role }}</small></span>
        <CspButton
          v-if="m.role !== 'Responsable'"
          label="Retirer"
          size="sm"
          variant="tertiary-no-outline"
          @click="retirer(m.nom)"
        />
      </li>
    </ul>
    <div class="ajout">
      <CspSelect
        v-model="choix"
        label="Ajouter un agent"
        :options="[{ value: 'aucun', label: 'Choisir un agent' }, ...disponibles.map(n => ({ value: n, label: n }))]"
      />
      <CspSelect
        v-model="role"
        label="Rôle"
        :options="ROLES"
      />
      <CspButton
        label="Ajouter"
        variant="secondary"
        icon="ri:add-line"
        is-icon-left
        @click="ajouter"
      />
    </div>
  </Panel>
</template>

<style scoped lang="scss">
.membres {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-2);
  margin: 0;
  padding: 0;
  list-style: none;
}

.membre {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--csp-space-2) var(--csp-space-3);
  border: 1px solid var(--border-default-grey);
  font-size: var(--csp-font-size-sm);

  small {
    display: block;
    font-size: var(--csp-font-size-xs);
    color: var(--text-mention-grey);
  }
}

.ajout {
  display: grid;
  grid-template-columns: 2fr 1fr auto;
  gap: var(--csp-space-3);
  align-items: end;
}
</style>
