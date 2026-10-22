<script setup lang="ts">
import type { Fiche, OrigineFiche } from './store'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspFiltersDrawer from '@/components/base/CspFiltersDrawer/CspFiltersDrawer.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useTableSelection } from '@/composables/data/useTableSelection'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { useDraft } from '@/composables/storage/useDraft'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import ActionsFicheCell from './cellules/ActionsFicheCell.vue'
import ModifieCell from './cellules/ModifieCell.vue'
import TagCell from './cellules/TagCell.vue'
import TitreCell from './cellules/TitreCell.vue'
import Colonnes from './Colonnes.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { CATEGORIES, dateTri, db, nouvelleFiche, offresDe, reinitialiser } from './store'

// Écran 2 — liste des fiches de poste, sur le modèle de la page « Recrutements » de l'application :
// onglets actives / archivées, recherche, filtres dans un tiroir, sélection, tri, pagination.
const { aller, notifier } = useNav()

const ORIGINES: Record<OrigineFiche, string> = { ats: 'ATS', sirh: 'SIRH', document: 'Document' }
function offresTexte(f: Fiche) {
  const liste = offresDe(f.id)
  if (!liste.length) {
    return 'Aucune'
  }
  const actives = liste.filter(o => o.etat !== 'archivee').length
  return actives ? `${liste.length} (${actives} active${actives > 1 ? 's' : ''})` : `${liste.length} archivée(s)`
}

type Onglet = 'actives' | 'archivees'
const ONGLETS = [
  { value: 'actives' as const, label: 'Fiches actives', icon: 'ri:file-text-line' },
  { value: 'archivees' as const, label: 'Fiches archivées', icon: 'ri:archive-line' },
]
const onglet = ref<Onglet>('actives')

type Col = CspColumnDef<Fiche> & { verrouillee?: boolean }
const TOUTES: Col[] = [
  { id: 'intitule', header: 'Intitulé du poste', accessor: f => f.intitule || 'Sans intitulé', cellComponent: TitreCell, verrouillee: true },
  { id: 'reference', header: 'Référence', accessor: f => f.id, width: '10rem' },
  { id: 'origine', header: 'Origine', sortable: true, accessor: f => ORIGINES[f.origine], cellComponent: TagCell, width: '8rem' },
  { id: 'service', header: 'Service', accessor: f => f.service.replace('Secrétariat général — ', 'SG — ') || '-' },
  { id: 'localisation', header: 'Localisation', accessor: f => f.localisation || '-' },
  { id: 'categorie', header: 'Catégorie', sortable: true, accessor: f => f.categories.join(', '), cellComponent: TagCell, width: '7rem' },
  { id: 'code', header: 'Code poste', accessor: f => f.codePoste || '-', width: '8rem' },
  { id: 'offres', header: 'Offres associées', accessor: f => offresTexte(f), width: '10rem' },
  { id: 'modifie', header: 'Dernière modification', sortable: true, accessor: f => dateTri(f.modifieLe), cellComponent: ModifieCell, width: '11rem' },
]
const ACTIONS: Col = { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: ActionsFicheCell, verrouillee: true }
const DEFAUT = ['reference', 'origine', 'service', 'categorie', 'offres', 'modifie']
const visiblesIds = ref([...DEFAUT])
const visibles = computed(() => [...TOUTES, ACTIONS].filter(c => c.verrouillee || visiblesIds.value.includes(c.id)))

// --- Recherche et filtres (brouillon dans le tiroir, appliqués au clic) ---
const TOUS = 'tous'
const filtres = useDraft(() => ({ origine: TOUS, categorie: TOUS, service: TOUS }))
const tiroir = useDisclosure()
function ouvrirFiltres() {
  filtres.syncDraft()
  tiroir.open()
}
function appliquer() {
  filtres.apply()
  tiroir.close()
}
const nbFiltres = computed(() => Object.values(filtres.applied).filter(v => v !== TOUS).length)
const OPTIONS_ORIGINE = [
  { value: TOUS, label: 'Toutes les origines' },
  { value: 'ats', label: 'Créées dans l\'ATS' },
  { value: 'sirh', label: 'Récupérées du SIRH' },
  { value: 'document', label: 'Issues d\'un document' },
]
const OPTIONS_CATEGORIE = [{ value: TOUS, label: 'Toutes les catégories' }, ...CATEGORIES.map(c => ({ value: c, label: `Catégorie ${c}` }))]
const OPTIONS_SERVICE = computed(() => [{ value: TOUS, label: 'Tous les services' }, ...[...new Set(db.fiches.map(f => f.service).filter(Boolean))].map(s => ({ value: s, label: s }))])

const deLOnglet = computed(() => db.fiches.filter(f => f.statut === (onglet.value === 'actives' ? 'active' : 'archivee')))
const { search, filtered: trouvees } = useTextSearch(deLOnglet, f => [f.intitule, f.codePoste, f.id, f.missions, f.service])
const lignes = computed(() => trouvees.value.filter(f =>
  (filtres.applied.origine === TOUS || f.origine === filtres.applied.origine)
  && (filtres.applied.categorie === TOUS || f.categories.includes(filtres.applied.categorie))
  && (filtres.applied.service === TOUS || f.service === filtres.applied.service)))

const compte = computed(() => {
  const n = lignes.value.length
  return `${n} fiche${n > 1 ? 's' : ''} ${onglet.value === 'actives' ? `active${n > 1 ? 's' : ''}` : `archivée${n > 1 ? 's' : ''}`}`
})

const selection = useTableSelection(lignes, f => f.id)
const page = ref(1)

function creer() {
  const f = nouvelleFiche({}, 'ats', 'Fiche créée dans l\'ATS par Camille Moreau')
  aller({ nom: 'fiche', id: f.id, edition: true })
}
</script>

<template>
  <PageAts
    v-model:onglet="onglet"
    actif="fiches"
    titre="Fiches de poste"
    sous-titre="Le référentiel des postes. Une fiche décrit durablement un poste et peut servir de base à plusieurs offres."
    :fil="[{ label: 'Fiches de poste' }]"
    :onglets="ONGLETS"
  >
    <template #actions>
      <CspButton
        label="Nouvelle fiche de poste"
        icon="ri:add-line"
        is-icon-left
        @click="creer"
      />
    </template>

    <div>
      <CspTableToolbar
        :bordered="false"
        :selection-count="selection.count.value"
        :selection-label="`${selection.count.value} fiche${selection.count.value > 1 ? 's sélectionnées' : ' sélectionnée'}`"
      >
        <template #selection-actions>
          <CspButton
            label="Archiver"
            variant="secondary"
            @click="notifier('Simulation : archivage groupé non prototypé.')"
          />
        </template>
        <template #status>
          <p class="compte">
            {{ compte }}
          </p>
        </template>
        <CspSearchBar
          v-model="search"
          mode="live"
          label="Rechercher une fiche de poste"
          hide-label
          placeholder="Rechercher un intitulé, un code poste,…"
          class="recherche"
        />
        <CspButton
          :label="nbFiltres ? `Filtres (${nbFiltres})` : 'Filtres'"
          variant="tertiary"
          icon="ri:filter-line"
          is-icon-left
          @click="ouvrirFiltres"
        />
        <Colonnes
          v-model="visiblesIds"
          :colonnes="TOUTES"
          :defaut="DEFAUT"
          cle="csplab-proto-ats-colonnes-fiches"
        />
      </CspTableToolbar>
      <CspDataTable
        :key="onglet"
        v-model:page="page"
        :rows="lignes"
        :columns="visibles"
        :row-key="f => f.id"
        selection-mode="checkbox"
        :selected-ids="selection.selectedIds.value"
        :selection-label="f => `Sélectionner ${f.intitule || f.id}`"
        activation-mode="cell"
        :caption="onglet === 'actives' ? 'Fiches de poste actives' : 'Fiches de poste archivées'"
        :empty-label="search || nbFiltres ? 'Aucune fiche ne correspond à votre recherche.' : 'Aucune fiche.'"
        :page-size="8"
        @activate="id => aller({ nom: 'fiche', id })"
        @toggle-row="selection.toggle"
        @toggle-all="selection.toggleVisible"
      />
    </div>

    <CspFiltersDrawer
      v-model:open="tiroir.isOpen.value"
      :can-reset="filtres.canReset.value"
      @apply="appliquer"
      @reset="filtres.reset()"
    >
      <CspSelect
        v-model="filtres.draft.origine"
        label="Origine"
        :options="OPTIONS_ORIGINE"
      />
      <CspSelect
        v-model="filtres.draft.categorie"
        label="Catégorie"
        :options="OPTIONS_CATEGORIE"
      />
      <CspSelect
        v-model="filtres.draft.service"
        label="Service"
        :options="OPTIONS_SERVICE"
      />
    </CspFiltersDrawer>

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
.compte {
  margin: 0;
  font-size: 0.9375rem;
  color: var(--text-mention-grey);
}

.recherche {
  min-width: 20rem;
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
