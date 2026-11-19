<script setup lang="ts">
import type { Membre, Offre } from './store'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspDrawer from '@/components/base/CspDrawer/CspDrawer.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useTextSearch } from '@/composables/data/useTextSearch'
import RetirerMembreCell from './cellules/RetirerMembreCell.vue'
import { db } from './store'

// Reprise de l'écran existant « Équipe de recrutement » (EquipeRecrutementSection, retour PO point 4) :
// mêmes textes, même tableau (Membre, Rôle, Poste, Courriel), « Ajouter un membre » dans un tiroir.
const props = defineProps<{ offre: Offre }>()
const o = computed(() => props.offre)

interface Ligne { nom: string, role: string, poste: string, email: string, offre: Offre }
const POSTES: Record<string, string> = { 'Camille Moreau': 'Chargée de recrutement', 'Julien Lefèvre': 'Chef du service Aménagement', 'Isabelle Fournier': 'Responsable RH' }
const courriel = (nom: string) => `${nom.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase().replace(/\s+/g, '.')}@developpement-durable.gouv.fr`
const lignes = computed<Ligne[]>(() => o.value.equipe.map(m => ({ nom: m.nom, role: m.role, poste: POSTES[m.nom] ?? 'Agent', email: courriel(m.nom), offre: o.value })))
const { search, filtered } = useTextSearch(lignes, l => [l.nom, l.email])
const compte = computed(() => `${filtered.value.length} membre${filtered.value.length > 1 ? 's' : ''}`)
const COLONNES: CspColumnDef<Ligne>[] = [
  { id: 'membre', header: 'Membre', sortable: true, width: '16rem', accessor: l => l.nom },
  { id: 'role', header: 'Rôle', sortable: true, width: '10rem', accessor: l => l.role },
  { id: 'poste', header: 'Poste', accessor: l => l.poste },
  { id: 'email', header: 'Courriel', accessor: l => l.email },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: RetirerMembreCell },
]
const page = ref(1)

const tiroir = ref(false)
const agent = ref('aucun')
const role = ref('Recruteur')
const OPTIONS_AGENT = computed(() => [{ value: 'aucun', label: 'Choisir un agent' }, ...db.organisme.agents.filter(a => !o.value.equipe.some(m => m.nom === a.nom)).map(a => ({ value: a.nom, label: a.nom }))])
const OPTIONS_ROLE = ['Responsable', 'Recruteur', 'Contributeur'].map(r => ({ value: r, label: r }))
function ajouter() {
  if (agent.value !== 'aucun') {
    o.value.equipe = [...o.value.equipe, { nom: agent.value, role: role.value as Membre['role'] }]
  }
  agent.value = 'aucun'
  tiroir.value = false
}
</script>

<template>
  <section class="equipe">
    <div class="equipe__intro">
      <h2 class="equipe__titre">
        Membres de l’équipe de recrutement
      </h2>
      <p class="equipe__description">
        L'équipe de recrutement regroupe les utilisateurs qui participent au traitement
        des candidatures sur cette offre.
      </p>
    </div>
    <CspTableToolbar :count="compte">
      <CspSearchBar
        v-model="search"
        mode="live"
        label="Rechercher un membre, un courriel"
        hide-label
        placeholder="Rechercher un membre, un courriel"
      />
      <CspButton
        label="Ajouter un membre"
        icon="ri:user-add-line"
        is-icon-left
        @click="tiroir = true"
      />
    </CspTableToolbar>
    <CspDataTable
      v-model:page="page"
      :rows="filtered"
      :columns="COLONNES"
      :row-key="l => l.nom"
      caption="Équipe de recrutement"
      :page-size="10"
      empty-label="Aucun membre rattaché à ce recrutement."
    />

    <CspDrawer
      v-model:open="tiroir"
      title="Ajouter un membre"
    >
      <div class="equipe__form">
        <CspSelect
          v-model="agent"
          label="Agent"
          :options="OPTIONS_AGENT"
        />
        <CspSelect
          v-model="role"
          label="Rôle"
          :options="OPTIONS_ROLE"
        />
        <CspButton
          label="Ajouter"
          @click="ajouter"
        />
      </div>
    </CspDrawer>
  </section>
</template>

<style scoped lang="scss">
.equipe {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}

.equipe__titre {
  margin: 0;
  font-size: var(--csp-font-size-lg);
  font-weight: var(--csp-font-weight-bold);
  color: var(--text-title-grey);
}

.equipe__description {
  margin: var(--csp-space-1) 0 0;
  color: var(--text-mention-grey);
}

.equipe__form {
  display: flex;
  flex-direction: column;
  gap: var(--csp-space-4);
}
</style>
