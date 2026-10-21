<script setup lang="ts">
import type { Fiche, OrigineFiche } from './store'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import Colonnes from './Colonnes.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { db, nouvelleFiche, offresDe, reinitialiser } from './store'

// Écran 2 — liste des fiches de poste : recherche, origine, offres associées, sans ouvrir chaque fiche.
const { aller } = useNav()

const ORIGINES: Record<OrigineFiche, string> = { ats: 'ATS', sirh: 'SIRH', document: 'Document ajouté' }
function offresTexte(f: Fiche) {
  const liste = offresDe(f.id)
  if (!liste.length) {
    return 'Aucune'
  }
  const actives = liste.filter(o => o.etat !== 'archivee').length
  return actives ? `${liste.length} (${actives} active${actives > 1 ? 's' : ''})` : `${liste.length} archivée(s)`
}

type Col = CspColumnDef<Fiche> & { verrouillee?: boolean }
const TOUTES: Col[] = [
  { id: 'intitule', header: 'Fiche de poste', accessor: f => f.intitule || 'Sans intitulé', verrouillee: true },
  { id: 'origine', header: 'Origine', accessor: f => ORIGINES[f.origine], width: '9rem' },
  { id: 'service', header: 'Service', accessor: f => f.service.replace('Secrétariat général — ', 'SG — ') || '—' },
  { id: 'localisation', header: 'Localisation', accessor: f => f.localisation || '—' },
  { id: 'categorie', header: 'Catégorie', accessor: f => f.categories.join(', ') || '—', width: '6rem' },
  { id: 'code', header: 'Code poste', accessor: f => f.codePoste || '—', width: '8rem' },
  { id: 'reference', header: 'Référence', accessor: f => f.id, width: '9.5rem' },
  { id: 'offres', header: 'Offres associées', accessor: f => offresTexte(f), width: '10rem' },
  { id: 'modifie', header: 'Modifiée', accessor: f => f.modifieLe, width: '9rem' },
]
const DEFAUT = ['origine', 'service', 'categorie', 'offres', 'modifie']
const visiblesIds = ref([...DEFAUT])
const visibles = computed(() => TOUTES.filter(c => c.verrouillee || visiblesIds.value.includes(c.id)))

const recherche = ref('')
const origine = ref<'toutes' | OrigineFiche>('toutes')
const statut = ref<'active' | 'archivee'>('active')
const lignes = computed(() => {
  const q = recherche.value.toLowerCase().trim()
  return db.fiches.filter(f => f.statut === statut.value
    && (origine.value === 'toutes' || f.origine === origine.value)
    && (!q || [f.intitule, f.codePoste, f.id, f.missions, f.service].join(' ').toLowerCase().includes(q)))
})
const OPTIONS_ORIGINE = [
  { value: 'toutes', label: 'Toutes les origines' },
  { value: 'ats', label: 'Créées dans l\'ATS' },
  { value: 'sirh', label: 'Récupérées du SIRH' },
  { value: 'document', label: 'Issues d\'un document' },
]

function creer() {
  const f = nouvelleFiche({}, 'ats', 'Fiche créée dans l\'ATS par Camille Moreau')
  aller({ nom: 'fiche', id: f.id, edition: true })
}
</script>

<template>
  <PageAts
    actif="fiches"
    titre="Fiches de poste"
    sous-titre="Le référentiel des postes. Une fiche décrit durablement un poste et peut servir de base à plusieurs offres."
  >
    <template #actions>
      <CspButton
        label="Nouvelle fiche de poste"
        icon="ri:add-line"
        is-icon-left
        @click="creer"
      />
    </template>

    <div class="filtres">
      <CspInput
        v-model="recherche"
        type="search"
        label="Rechercher"
        placeholder="Intitulé, code poste, service, mot-clé…"
      />
      <CspSelect
        v-model="origine"
        label="Origine"
        :options="OPTIONS_ORIGINE"
      />
    </div>
    <div class="puces">
      <button
        type="button"
        class="puce"
        :aria-pressed="statut === 'active'"
        @click="statut = 'active'"
      >
        Actives ({{ db.fiches.filter(f => f.statut === 'active').length }})
      </button>
      <button
        type="button"
        class="puce"
        :aria-pressed="statut === 'archivee'"
        @click="statut = 'archivee'"
      >
        Archivées ({{ db.fiches.filter(f => f.statut === 'archivee').length }})
      </button>
    </div>

    <div>
      <CspTableToolbar :count="`${lignes.length} fiche${lignes.length > 1 ? 's' : ''}`">
        <Colonnes
          v-model="visiblesIds"
          :colonnes="TOUTES"
          :defaut="DEFAUT"
          cle="csplab-proto-ats-colonnes-fiches"
        />
      </CspTableToolbar>
      <CspDataTable
        :rows="lignes"
        :columns="visibles"
        :row-key="f => f.id"
        caption="Fiches de poste"
        activation-mode="row"
        size="sm"
        :empty-label="recherche ? 'Aucune fiche ne correspond.' : 'Aucune fiche dans cette vue.'"
        @activate="id => aller({ nom: 'fiche', id })"
      />
    </div>

    <p class="pied">
      Données fictives conservées pendant la session.
      <button
        type="button"
        class="lien"
        @click="reinitialiser"
      >
        Réinitialiser la démonstration
      </button>
    </p>
  </PageAts>
</template>

<style scoped lang="scss">
.filtres {
  display: grid;
  grid-template-columns: minmax(0, 2fr) minmax(0, 1fr);
  gap: var(--csp-space-4);
  max-width: 56rem;
}

.puces {
  display: flex;
  gap: var(--csp-space-2);
  margin-top: calc(-1 * var(--csp-space-2));
}

.puce {
  padding: var(--csp-space-1) var(--csp-space-3);
  border: 1px solid var(--border-default-grey);
  border-radius: 1rem;
  background: var(--background-default-grey);
  font: inherit;
  font-size: var(--csp-font-size-sm);
  color: var(--text-default-grey);
  cursor: pointer;

  &[aria-pressed='true'] {
    border-color: var(--border-active-blue-france);
    background: var(--background-action-low-blue-france);
    color: var(--text-action-high-blue-france);
  }
}

.pied {
  margin: 0;
  font-size: var(--csp-font-size-xs);
  color: var(--text-mention-grey);
}

.lien {
  margin-left: var(--csp-space-1);
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  color: var(--text-action-high-blue-france);
  text-decoration: underline;
  cursor: pointer;
}
</style>
