<script setup lang="ts">
import type { EtatOffre, Offre } from './store'
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
import ActionsOffreCell from './cellules/ActionsOffreCell.vue'
import EtatCell from './cellules/EtatCell.vue'
import ModifieCell from './cellules/ModifieCell.vue'
import TagCell from './cellules/TagCell.vue'
import TitreCell from './cellules/TitreCell.vue'
import Colonnes from './Colonnes.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { CATEGORIES, dateTri, db, fiche, LIBELLES_CONTENU, LIBELLES_ETAT } from './store'

// Liste des offres d'emploi, sur le modèle de la page « Recrutements » de l'application :
// onglets en cours / archivées, nombre de résultats, recherche, filtres dans un tiroir, sélection, tri, pagination.
const props = defineProps<{ filtre?: string }>()
const { aller, notifier } = useNav()

type Onglet = 'en_cours' | 'archivees'
const ONGLETS = [
  { value: 'en_cours' as const, label: 'Offres en cours', icon: 'ri:megaphone-line' },
  { value: 'archivees' as const, label: 'Offres archivées', icon: 'ri:archive-line' },
]
const onglet = ref<Onglet>(props.filtre === 'archivee' ? 'archivees' : 'en_cours')

type Col = CspColumnDef<Offre> & { verrouillee?: boolean }
const TOUTES: Col[] = [
  { id: 'titre', header: 'Intitulé de l\'offre', accessor: o => o.titre || 'Sans titre', cellComponent: TitreCell, verrouillee: true },
  { id: 'reference', header: 'Référence', accessor: o => o.id, width: '9rem' },
  { id: 'etat', header: 'État', sortable: true, accessor: o => LIBELLES_ETAT[o.etat], cellComponent: EtatCell, width: '13rem' },
  { id: 'fiche', header: 'Fiche de poste', accessor: o => fiche(o.ficheId)?.intitule ?? '—' },
  { id: 'categorie', header: 'Catégorie', accessor: o => o.categorie, cellComponent: TagCell, width: '7rem' },
  { id: 'postes', header: 'Postes', sortable: true, accessor: o => Number(o.nbPostes), align: 'end', width: '6rem' },
  { id: 'contenu', header: 'Origine du contenu', accessor: o => LIBELLES_CONTENU[o.origineContenu] },
  { id: 'limite', header: 'Date limite', sortable: true, accessor: o => o.dateLimite || '-', width: '8rem' },
  { id: 'modifie', header: 'Dernière modification', sortable: true, accessor: o => dateTri(o.modifieLe), cellComponent: ModifieCell, width: '11rem' },
]
const ACTIONS: Col = { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: ActionsOffreCell, verrouillee: true }
const DEFAUT = ['reference', 'etat', 'fiche', 'postes', 'modifie']
const visiblesIds = ref([...DEFAUT])
const visibles = computed(() => [...TOUTES, ACTIONS].filter(c => c.verrouillee || visiblesIds.value.includes(c.id)))

// --- Recherche et filtres (brouillon dans le tiroir, appliqués au clic) ---
const TOUS = 'tous'
const filtres = useDraft(() => ({ etat: TOUS, categorie: TOUS, contenu: TOUS }))
if (props.filtre && props.filtre !== 'archivee') {
  filtres.draft.etat = props.filtre
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

const ETATS_EN_COURS: EtatOffre[] = ['redaction', 'validation', 'a_publier', 'publiee']
const OPTIONS_ETAT = [{ value: TOUS, label: 'Tous les états' }, ...ETATS_EN_COURS.map(e => ({ value: e, label: LIBELLES_ETAT[e] }))]
const OPTIONS_CATEGORIE = [{ value: TOUS, label: 'Toutes les catégories' }, ...CATEGORIES.map(c => ({ value: c, label: `Catégorie ${c}` }))]
const OPTIONS_CONTENU = [{ value: TOUS, label: 'Toutes les origines' }, ...Object.entries(LIBELLES_CONTENU).map(([value, label]) => ({ value, label }))]

const deLOnglet = computed(() => db.offres.filter(o => (onglet.value === 'archivees') === (o.etat === 'archivee')))
const { search, filtered: trouvees } = useTextSearch(deLOnglet, o => [o.titre, o.id, o.ficheId, fiche(o.ficheId)?.intitule])
const lignes = computed(() => trouvees.value.filter(o =>
  (filtres.applied.etat === TOUS || o.etat === filtres.applied.etat)
  && (filtres.applied.categorie === TOUS || o.categorie === filtres.applied.categorie)
  && (filtres.applied.contenu === TOUS || o.origineContenu === filtres.applied.contenu)))

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
    titre="Offres d'emploi"
    sous-titre="Chaque offre est une opération de recrutement rattachée à une fiche de poste."
    :fil="[{ label: 'Offres d\'emploi' }]"
    :onglets="ONGLETS"
  >
    <template #actions>
      <CspButton
        label="Lancer un recrutement"
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
          placeholder="Rechercher une offre, une référence,…"
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
          cle="csplab-proto-ats-colonnes-offres"
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
        v-model="filtres.draft.etat"
        label="État"
        :options="OPTIONS_ETAT"
      />
      <CspSelect
        v-model="filtres.draft.categorie"
        label="Catégorie"
        :options="OPTIONS_CATEGORIE"
      />
      <CspSelect
        v-model="filtres.draft.contenu"
        label="Origine du contenu"
        :options="OPTIONS_CONTENU"
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
