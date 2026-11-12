<script setup lang="ts">
import type { Offre } from './store'
import type { StatutListe } from './suivi'
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
import ActionCell from './cellules/ActionCell.vue'
import ActionsOffreCell from './cellules/ActionsOffreCell.vue'
import ModifieCell from './cellules/ModifieCell.vue'
import StatutCell from './cellules/StatutCell.vue'
import TagCell from './cellules/TagCell.vue'
import TitreCell from './cellules/TitreCell.vue'
import Colonnes from './Colonnes.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { CATEGORIES, dateTri, db, fiche, LIBELLES_CONTENU, termineBientot } from './store'
import { actionAFaire, dateCourte, referenceCsp, statutListe, STATUTS } from './suivi'

// « Mes offres d'emploi », d'après la maquette d'Alice : onglets en cours / archivées, recherche, filtres,
// sélection, tri, pagination. Un seul statut (publication et validation réunies) et une colonne
// « Action à faire » qui donne la prochaine étape de chaque offre.
const props = defineProps<{ filtre?: string }>()
const { aller, notifier } = useNav()

type Onglet = 'en_cours' | 'archivees'
const ONGLETS = [
  { value: 'en_cours' as const, label: 'Offres en cours', icon: 'ri:megaphone-line' },
  { value: 'archivees' as const, label: 'Offres archivées', icon: 'ri:archive-line' },
]
const onglet = ref<Onglet>(props.filtre === 'archivee' ? 'archivees' : 'en_cours')

type Col = CspColumnDef<Offre> & { verrouillee?: boolean }
const ORDRE: StatutListe[] = ['validation_refusee', 'prete', 'brouillon', 'validation_attente', 'publiee', 'retiree', 'archivee']
const TOUTES: Col[] = [
  { id: 'titre', header: 'Intitulé de l\'offre', accessor: o => o.titre || 'Sans titre', cellComponent: TitreCell, verrouillee: true },
  { id: 'reference', header: 'Référence CSP', accessor: o => referenceCsp(o), width: '7.5rem' },
  { id: 'statut', header: 'Statut', sortable: true, accessor: o => ORDRE.indexOf(statutListe(o)), cellComponent: StatutCell, width: '10.5rem' },
  { id: 'debut', header: 'Début', sortable: true, accessor: o => dateCourte(o.dateDebut), width: '7.5rem' },
  { id: 'fin', header: 'Fin de publication', sortable: true, accessor: o => dateCourte(o.dateFin), width: '8rem' },
  { id: 'modifie', header: 'Dernière activité', sortable: true, accessor: o => dateTri(o.modifieLe), cellComponent: ModifieCell, width: '8.5rem' },
  { id: 'action', header: 'Action à faire', accessor: o => actionAFaire(o)?.label ?? '', cellComponent: ActionCell, width: '11rem' },
  { id: 'fiche', header: 'Fiche de poste', accessor: o => fiche(o.ficheId)?.intitule ?? '—' },
  { id: 'categorie', header: 'Catégorie', accessor: o => o.categorie, cellComponent: TagCell, width: '7rem' },
  { id: 'postes', header: 'Postes', sortable: true, accessor: o => Number(o.nbPostes), align: 'end', width: '6rem' },
  { id: 'contenu', header: 'Origine du contenu', accessor: o => LIBELLES_CONTENU[o.origineContenu] },
]
const ACTIONS: Col = { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: ActionsOffreCell, verrouillee: true }
const DEFAUT = ['reference', 'statut', 'fin', 'modifie', 'action']
const visiblesIds = ref([...DEFAUT])
const visibles = computed(() => [...TOUTES, ACTIONS].filter(c => c.verrouillee || visiblesIds.value.includes(c.id)))

// --- Recherche et filtres (brouillon dans le tiroir, appliqués au clic) ---
const TOUS = 'tous'
// Filtres rapides depuis l'accueil : « À valider », « À publier », « Se terminent sous 7 jours ».
const filtres = useDraft(() => ({ statut: TOUS, delai: TOUS, categorie: TOUS }))
if (props.filtre && props.filtre !== 'archivee') {
  if (props.filtre === 'bientot') {
    filtres.draft.delai = props.filtre
  }
  else if (props.filtre === 'a_publier') {
    filtres.draft.statut = 'prete'
  }
  else if (props.filtre === 'en_attente') {
    filtres.draft.statut = 'validation_attente'
  }
  else if (props.filtre in STATUTS) {
    filtres.draft.statut = props.filtre
  }
  filtres.apply()
}
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

const STATUTS_EN_COURS: StatutListe[] = ['brouillon', 'validation_attente', 'validation_refusee', 'prete', 'publiee', 'retiree']
const OPTIONS_STATUT = [{ value: TOUS, label: 'Tous les statuts' }, ...STATUTS_EN_COURS.map(e => ({ value: e, label: STATUTS[e].label }))]
const OPTIONS_DELAI = [{ value: TOUS, label: 'Toutes' }, { value: 'bientot', label: 'Se terminent sous 7 jours' }]
const OPTIONS_CATEGORIE = [{ value: TOUS, label: 'Toutes les catégories' }, ...CATEGORIES.map(c => ({ value: c, label: `Catégorie ${c}` }))]

const deLOnglet = computed(() => db.offres.filter(o => (onglet.value === 'archivees') === (o.etat === 'archivee')))
const { search, filtered: trouvees } = useTextSearch(deLOnglet, o => [o.titre, o.id, o.ficheId, fiche(o.ficheId)?.intitule])
const lignes = computed(() => trouvees.value.filter(o =>
  (filtres.applied.statut === TOUS || statutListe(o) === filtres.applied.statut)
  && (filtres.applied.delai !== 'bientot' || termineBientot(o))
  && (filtres.applied.categorie === TOUS || o.categorie === filtres.applied.categorie)))

const compte = computed(() => {
  const n = lignes.value.length
  return onglet.value === 'archivees' ? `${n} offre${n > 1 ? 's' : ''} archivée${n > 1 ? 's' : ''}` : `${n} offre${n > 1 ? 's' : ''} en cours`
})

const selection = useTableSelection(lignes, o => o.id)
const page = ref(1)
</script>

<template>
  <PageAts
    v-model:onglet="onglet"
    actif="offres"
    titre="Mes offres d'emploi"
    :fil="[{ label: 'Mes offres d\'emploi' }]"
    :onglets="ONGLETS"
  >
    <template #actions>
      <CspButton
        label="Créer une offre"
        icon="ri:add-line"
        is-icon-left
        @click="aller({ nom: 'creation' })"
      />
    </template>

    <div>
      <CspTableToolbar
        :bordered="false"
        :selection-count="selection.count.value"
        :selection-label="`${selection.count.value} offre${selection.count.value > 1 ? 's sélectionnées' : ' sélectionnée'}`"
      >
        <template #selection-actions>
          <CspButton
            label="Assigner un responsable"
            @click="notifier('Simulation : assignation d\'un responsable non prototypée.')"
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
          label="Rechercher une offre"
          hide-label
          placeholder="Rechercher un intitulé d'offre, une référence"
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
          cle="csplab-proto-ats-colonnes-offres-v2"
        />
      </CspTableToolbar>
      <CspDataTable
        :key="onglet"
        v-model:page="page"
        :rows="lignes"
        :columns="visibles"
        :row-key="o => o.id"
        selection-mode="checkbox"
        :selected-ids="selection.selectedIds.value"
        :selection-label="o => `Sélectionner ${o.titre || o.id}`"
        activation-mode="cell"
        :caption="onglet === 'archivees' ? 'Offres archivées' : 'Offres en cours'"
        :empty-label="search || nbFiltres ? 'Aucune offre ne correspond à votre recherche.' : 'Aucune offre.'"
        :page-size="8"
        @activate="id => aller({ nom: 'offre', id })"
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
        v-if="onglet === 'en_cours'"
        v-model="filtres.draft.statut"
        label="Statut"
        :options="OPTIONS_STATUT"
      />
      <CspSelect
        v-if="onglet === 'en_cours'"
        v-model="filtres.draft.delai"
        label="Échéance"
        :options="OPTIONS_DELAI"
      />
      <CspSelect
        v-model="filtres.draft.categorie"
        label="Catégorie"
        :options="OPTIONS_CATEGORIE"
      />
    </CspFiltersDrawer>
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
</style>
