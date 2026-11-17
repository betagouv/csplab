<script setup lang="ts">
import type { Membre, Offre } from './store'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import FieldRow from '../../shared/FieldRow.vue'
import { db } from './store'

// Étape « Équipe » (facultative) : le créateur est déjà Responsable ; on ajoute des membres.
// Ça ne bloque pas la publication et se modifie plus tard avec les écrans existants.
const props = defineProps<{ offre: Offre, lectureSeule?: boolean }>()
const o = computed(() => props.offre)

const ROLES: { value: Membre['role'], label: string, aide: string }[] = [
  { value: 'Responsable', label: 'Responsable', aide: 'Gère l\'offre et le recrutement.' },
  { value: 'Recruteur', label: 'Recruteur', aide: 'Évalue les candidatures.' },
  { value: 'Contributeur', label: 'Contributeur', aide: 'Donne son avis sur les candidatures.' },
]
const disponibles = computed(() => db.organisme.agents.map(a => a.nom).filter(n => !o.value.equipe.some(m => m.nom === n)))
const nom = ref('')
const role = ref<Membre['role']>('Recruteur')
function ajouter() {
  if (!nom.value) {
    return
  }
  o.value.equipe = [...o.value.equipe, { nom: nom.value, role: role.value }]
  nom.value = ''
}
function retirer(n: string) {
  o.value.equipe = o.value.equipe.filter(m => m.nom !== n)
}
const responsables = computed(() => o.value.equipe.filter(m => m.role === 'Responsable').length)
</script>

<template>
  <div class="equipe">
    <ul class="equipe__liste">
      <li
        v-for="m in o.equipe"
        :key="m.nom"
      >
        <span class="equipe__nom">{{ m.nom }}</span>
        <span class="equipe__role">{{ m.role }}</span>
        <CspButton
          v-if="!lectureSeule && !(m.role === 'Responsable' && responsables === 1)"
          label="Retirer"
          size="sm"
          variant="tertiary-no-outline"
          @click="retirer(m.nom)"
        />
      </li>
    </ul>
    <FieldRow
      v-if="!lectureSeule"
      :cols="3"
      class="equipe__ajout"
    >
      <CspSelect
        v-model="nom"
        label="Ajouter un membre"
        placeholder="Choisir un agent"
        :options="disponibles.map(n => ({ value: n, label: n }))"
      />
      <CspSelect
        v-model="role"
        label="Rôle"
        :options="ROLES"
      />
      <div class="equipe__bouton">
        <CspButton
          label="Ajouter"
          variant="secondary"
          icon="ri:add-line"
          is-icon-left
          :disabled="!nom"
          @click="ajouter"
        />
      </div>
    </FieldRow>
  </div>
</template>

<style scoped lang="scss">
.equipe {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-5);
  max-width: 48rem;
}

.equipe__liste {
  margin: 0;
  padding: 0;
  list-style: none;
  border-top: 1px solid var(--border-default-grey);

  li {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 9rem 6rem;
    align-items: center;
    min-height: 2.75rem;
    border-bottom: 1px solid var(--border-default-grey);
  }
}

.equipe__nom {
  font-weight: 600;
}

.equipe__role {
  font-size: var(--csp-font-size-sm);
  color: var(--text-mention-grey);
}

.equipe__bouton {
  display: flex;
  align-items: flex-end;
}
</style>
