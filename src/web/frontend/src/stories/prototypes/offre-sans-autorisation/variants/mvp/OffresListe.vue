<script setup lang="ts">
import type { CarteAFaire } from './AFaire.vue'
import type { Offre } from './store'
import type { CategorieOffre } from './suivi'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import type { CspTabItem } from '@/components/base/CspTabs/CspTabs.vue'
import { computed, ref } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspFiltersDrawer from '@/components/base/CspFiltersDrawer/CspFiltersDrawer.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspSelect from '@/components/base/CspSelect/CspSelect.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import { useTextSearch } from '@/composables/data/useTextSearch'
import { useDraft } from '@/composables/storage/useDraft'
import { useDisclosure } from '@/composables/ui/useDisclosure'
import AFaire from './AFaire.vue'
import { champsObligatoires } from './aide'
import ActionsOffreCell from './cellules/ActionsOffreCell.vue'
import ActiviteOffreCell from './cellules/ActiviteOffreCell.vue'
import CandidaturesCell from './cellules/CandidaturesCell.vue'
import CompletionCell from './cellules/CompletionCell.vue'
import DepublicationCell from './cellules/DepublicationCell.vue'
import EtatPreparationCell from './cellules/EtatPreparationCell.vue'
import IntituleCell from './cellules/IntituleCell.vue'
import ResponsablesCell from './cellules/ResponsablesCell.vue'
import StatutDepuisCell from './cellules/StatutDepuisCell.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { candidatures } from './recrutement'
import { aujourdhui, dateTri, db, fiche, joursRestants, plusJours, UTILISATEUR } from './store'
import { actionOffre, categorieOffre, CATEGORIES_OFFRE, etatPreparation, horsAts, PHASES, responsable, responsables } from './suivi'

// « Mes offres d'emploi » (sans autorisation) : onglets par statut, recherche, filtres, colonnes selon l'onglet (Alice, 25/11/2026).
const props = defineProps<{ filtre?: string }>()
const { aller } = useNav()

const offres = computed(() => db.offres)
const { search, filtered: trouvees } = useTextSearch(offres, o => [o.titre, o.id, o.lieu, fiche(o.ficheId)?.service])

const ORDRE = CATEGORIES_OFFRE.map(c => c.id)

// Onglets par statut (voir plus bas).
type Onglet = CategorieOffre | 'toutes'
// Accès direct depuis le tableau de bord. À l'ouverture, on arrive sur les offres en ligne (retour Alice).
const DEPUIS_ACCUEIL: Record<string, CategorieOffre> = { brouillon: 'brouillon', en_ligne: 'en_ligne', depubliee: 'en_pause', en_pause: 'en_pause', archivee: 'archivee' }
const onglet = ref<Onglet>((props.filtre && DEPUIS_ACCUEIL[props.filtre]) || 'en_ligne')

// --- Filtres (retour PO, L3), dans un tiroir et appliqués au clic, comme sur les autres listes ---
// Adaptés aux colonnes de chaque onglet (retour PO, 27/11/2026) : partout Date de publication, Fin de publication,
// Responsable et Lieu ; Statut là où la colonne existe. Pas de dates dans « En préparation » : rien n'est encore publié.
const TOUS = 'tous'
type CleFiltre = 'statut' | 'publication' | 'fin' | 'responsable' | 'lieu'
const filtres = useDraft<Record<CleFiltre, string>>(() => ({ statut: TOUS, publication: TOUS, fin: TOUS, responsable: TOUS, lieu: TOUS }))
const peutPublier = computed(() => Boolean(db.organisme.agents.find(a => a.nom === UTILISATEUR)?.publier))
const tiroir = useDisclosure()
function ouvrirFiltres() {
  filtres.syncDraft()
  tiroir.open()
}
function appliquer() {
  filtres.apply()
  tiroir.close()
}
function options(tous: string, valeurs: string[]) {
  return [{ value: TOUS, label: tous }, ...[...new Set(valeurs.filter(Boolean))].sort().map(v => ({ value: v, label: v }))]
}
const OPTIONS_RESPONSABLE = computed(() => options('Tous les responsables', offres.value.flatMap(responsables)))
const OPTIONS_LIEU = computed(() => options('Tous les lieux', offres.value.flatMap(o => o.lieu.split(',').map(l => l.trim()))))
// Filtre « Statut » : les statuts, avec les deux sous-statuts d'une offre en préparation.
const OPTIONS_STATUT_TOUS = [
  { value: TOUS, label: 'Tous les statuts' },
  { value: 'brouillon', label: 'En préparation · Brouillon' },
  { value: 'prete', label: 'En préparation · Prête à publier' },
  { value: 'en_ligne', label: 'En ligne' },
  { value: 'en_pause', label: 'En pause' },
  { value: 'archivee', label: 'Archivée' },
]
const OPTIONS_STATUT = computed(() => onglet.value === 'brouillon'
  ? [{ value: TOUS, label: 'Tous les statuts' }, { value: 'brouillon', label: 'Brouillon' }, { value: 'prete', label: 'Prête à publier' }]
  : OPTIONS_STATUT_TOUS)
function statutFiltre(o: Offre): string {
  const c = categorieOffre(o)
  return c === 'brouillon' ? (etatPreparation(o) === 'Brouillon' ? 'brouillon' : 'prete') : c
}
// Filtre « Date de publication » : publiée depuis moins de 7 ou 30 jours, ou depuis plus longtemps.
const OPTIONS_PUBLICATION = [
  { value: TOUS, label: 'Toutes les dates' },
  { value: '7', label: 'Depuis moins de 7 jours' },
  { value: '30', label: 'Depuis moins de 30 jours' },
  { value: 'plus', label: 'Depuis plus de 30 jours' },
]
function publicationFiltre(o: Offre, v: string): boolean {
  if (o.etat === 'brouillon' || !o.dateDebut) {
    return false
  }
  return v === 'plus' ? o.dateDebut < plusJours(aujourdhui(), -30) : o.dateDebut >= plusJours(aujourdhui(), -Number(v))
}
// Filtre « Fin de publication » : fin dans moins de 7 ou 30 jours, ou déjà passée.
const OPTIONS_FIN = [
  { value: TOUS, label: 'Toutes les dates' },
  { value: '7', label: 'Dans moins de 7 jours' },
  { value: '30', label: 'Dans moins de 30 jours' },
  { value: 'passee', label: 'Date passée' },
]
function finFiltre(o: Offre, v: string): boolean {
  if (o.etat === 'brouillon' || !o.dateFin) {
    return false
  }
  return v === 'passee' ? o.dateFin < aujourdhui() : o.dateFin >= aujourdhui() && joursRestants(o.dateFin) <= Number(v)
}
// Filtres proposés dans l'onglet affiché ; ceux d'un autre onglet ne s'appliquent pas.
const FILTRES_ONGLET = computed<CleFiltre[]>(() => [
  ...(['brouillon', 'toutes'].includes(onglet.value) ? ['statut' as const] : []),
  ...(onglet.value !== 'brouillon' ? ['publication' as const, 'fin' as const] : []),
  'responsable',
  'lieu',
])
const actif = (cle: CleFiltre) => FILTRES_ONGLET.value.includes(cle) && filtres.applied[cle] !== TOUS
const nbFiltres = computed(() => FILTRES_ONGLET.value.filter(actif).length)
// Filtres appliqués, annoncés au-dessus du tableau (« Vue filtrée »), chacun supprimable.
const LIBELLES_FILTRES: Record<CleFiltre, string> = { statut: 'Statut', publication: 'Date de publication', fin: 'Fin de publication', responsable: 'Responsable', lieu: 'Lieu' }
const OPTIONS_PAR_CLE: Partial<Record<CleFiltre, { value: string, label: string }[]>> = { statut: OPTIONS_STATUT_TOUS, publication: OPTIONS_PUBLICATION, fin: OPTIONS_FIN }
const filtresActifs = computed(() => FILTRES_ONGLET.value.filter(actif).map((cle) => {
  const v = filtres.applied[cle]
  return { cle, label: `${LIBELLES_FILTRES[cle]} : ${OPTIONS_PAR_CLE[cle]?.find(x => x.value === v)?.label ?? v}` }
}))
function retirerFiltre(cle: CleFiltre) {
  filtres.syncDraft()
  filtres.draft[cle] = TOUS
  filtres.apply()
}
function reinitialiser() {
  filtres.syncDraft()
  for (const cle of FILTRES_ONGLET.value) {
    filtres.draft[cle] = TOUS
  }
  filtres.apply()
}
const filtrees = computed(() => trouvees.value.filter((o) => {
  const f = filtres.applied
  return (!actif('responsable') || responsables(o).includes(f.responsable))
    && (!actif('lieu') || o.lieu.split(',').map(l => l.trim()).includes(f.lieu))
    && (!actif('statut') || statutFiltre(o) === f.statut)
    && (!actif('publication') || publicationFiltre(o, f.publication))
    && (!actif('fin') || finFiltre(o, f.fin))
}))

// --- Onglets par statut : En préparation, En ligne, En pause, Archivée, puis Toutes ---
// Les compteurs des onglets restent les totaux, même quand la vue est filtrée (Alice).
const parPhase = computed(() => {
  const m = new Map<CategorieOffre, number>()
  for (const o of offres.value) {
    m.set(categorieOffre(o), (m.get(categorieOffre(o)) ?? 0) + 1)
  }
  return m
})
const onglets = computed<CspTabItem<Onglet>[]>(() => [
  ...PHASES.map(p => ({ value: p.id, label: `${p.label} (${parPhase.value.get(p.id) ?? 0})` })),
  { value: 'toutes', label: `Toutes (${offres.value.length})` },
])

// Tri par défaut : en ligne, les fins les plus proches d'abord (L4) ; ailleurs, l'activité la plus récente d'abord.
function dateActivite(o: Offre) {
  const d = { brouillon: o.modifieLe, en_ligne: o.publieeLe ?? o.dateDebut, en_pause: o.retireeLe ?? o.dateFin, archivee: o.archiveeLe ?? '' }[categorieOffre(o)]
  return /^\d{4}-/.test(d) ? d : dateTri(d)
}
// --- Encart « À faire » (prolonger, publier) : un clic applique un filtre et ouvre l'onglet concerné ---
const offresAFaire = computed(() => {
  const c: Record<CarteAFaire, Offre[]> = { prolonger: [], publier: [] }
  for (const o of offres.value) {
    const a = actionOffre(o, peutPublier.value)
    if (a && a.type !== 'continuer') {
      c[a.type].push(o)
    }
  }
  return c
})
// Les cartes appliquent les filtres existants : Statut « Prête à publier », Fin de publication « moins de 7 jours ».
const ONGLET_ACTION: Record<CarteAFaire, CategorieOffre> = { prolonger: 'en_ligne', publier: 'brouillon' }
function choisirAction(t: CarteAFaire) {
  filtres.syncDraft()
  filtres.draft.statut = t === 'publier' ? 'prete' : TOUS
  filtres.draft.fin = t === 'prolonger' ? '7' : TOUS
  filtres.draft.publication = TOUS
  filtres.apply()
  onglet.value = ONGLET_ACTION[t]
}

const lignes = computed(() => {
  const l = filtrees.value.filter(o => onglet.value === 'toutes' || categorieOffre(o) === onglet.value)
  if (onglet.value === 'en_ligne') {
    return [...l].sort((a, b) => a.dateFin.localeCompare(b.dateFin))
  }
  if (onglet.value === 'toutes') {
    return [...l].sort((a, b) => ORDRE.indexOf(categorieOffre(a)) - ORDRE.indexOf(categorieOffre(b)) || dateActivite(b).localeCompare(dateActivite(a)))
  }
  return [...l].sort((a, b) => dateActivite(b).localeCompare(dateActivite(a)))
})

// Socle commun (Alice, 25/11/2026) : Offre d'emploi, Statut, Responsable, Activité sur l'offre, puis
// Fin de publication et Candidatures seulement là où elles existent (pas pour un brouillon ; pas de fin pour une archivée).
const COLONNES = computed<CspColumnDef<Offre>[]>(() => {
  const avecFin = ['en_ligne', 'en_pause', 'toutes'].includes(onglet.value)
  const avecCandidatures = onglet.value !== 'brouillon'
  return [
    { id: 'intitule', header: 'Offre d\'emploi', accessor: o => o.titre, cellComponent: IntituleCell },
    // Champs obligatoires remplis, dans « En préparation » (retour PO, 26/11/2026).
    ...(onglet.value === 'brouillon' ? [{ id: 'completion', header: 'Champs obligatoires remplis', wrapHeader: true, sortable: true, accessor: (o: Offre) => champsObligatoires(o).filter(c => c.ok).length / Math.max(1, champsObligatoires(o).length), cellComponent: CompletionCell, width: '8.5rem' }] : []),
    // Statut : badge dans « Toutes » ; texte simple dans « En préparation » (Brouillon, Prête à publier) ; rien ailleurs.
    ...(onglet.value === 'toutes' ? [{ id: 'statut', header: 'Statut', sortable: true, accessor: (o: Offre) => ORDRE.indexOf(categorieOffre(o)), cellComponent: StatutDepuisCell, width: '7.5rem' }] : []),
    ...(onglet.value === 'brouillon' ? [{ id: 'statut', header: 'Statut', sortable: true, accessor: (o: Offre) => etatPreparation(o), cellComponent: EtatPreparationCell, width: '8rem' }] : []),
    { id: 'responsable', header: 'Responsable', accessor: o => responsable(o), cellComponent: ResponsablesCell, width: '11rem' },
    { id: 'activite', header: 'Activité sur l\'offre', wrapHeader: true, sortable: true, accessor: (o: Offre) => dateActivite(o), cellComponent: ActiviteOffreCell, width: '11rem' },
    ...(avecFin ? [{ id: 'fin', header: 'Fin de publication', wrapHeader: true, sortable: true, accessor: (o: Offre) => (o.etat === 'publiee' || o.etat === 'retiree' ? o.dateFin : ''), cellComponent: DepublicationCell, width: '8rem' }] : []),
    ...(avecCandidatures ? [{ id: 'candidatures', header: 'Candidatures', wrapHeader: true, sortable: true, accessor: (o: Offre) => (o.etat === 'brouillon' ? -2 : horsAts(o) ? -1 : candidatures(o).total), cellComponent: CandidaturesCell, width: '9rem' }] : []),
    { id: 'actions', header: '', align: 'end', width: '9rem', cellComponent: ActionsOffreCell },
  ]
})

const compte = computed(() => {
  const n = lignes.value.length
  return `${n} offre${n > 1 ? 's' : ''}`
})
const page = ref(1)

// Sous-titre sur deux lignes (Alice, 27/11/2026) : le \n est respecté par PageAts.
const SOUS_TITRE = 'Créez et gérez vos offres d\'emploi, de leur préparation à leur publication.\nCertaines peuvent être associées à un recrutement pour traiter les candidatures.'
</script>

<template>
  <PageAts
    v-model:onglet="onglet"
    actif="offres"
    titre="Mes offres d'emploi"
    :sous-titre="SOUS_TITRE"
    :fil="[{ label: 'Mes offres d\'emploi' }]"
    :onglets="onglets"
  >
    <template #avant-onglets>
      <AFaire
        :offres="offresAFaire"
        @choisir="choisirAction"
      />
    </template>
    <template #actions>
      <CspButton
        label="Créer une offre"
        icon="ri:add-line"
        is-icon-left
        @click="aller({ nom: 'creation' })"
      />
    </template>

    <div>
      <CspTableToolbar :bordered="false">
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
          placeholder="Intitulé, lieu, référence"
          class="recherche"
        />
        <CspButton
          :label="nbFiltres ? `Filtres (${nbFiltres})` : 'Filtres'"
          variant="tertiary"
          icon="ri:filter-line"
          is-icon-left
          @click="ouvrirFiltres"
        />
      </CspTableToolbar>
      <div
        v-if="filtresActifs.length"
        class="vue-filtree"
        role="status"
      >
        <span class="vue-filtree__label">Vue filtrée :</span>
        <CspTag
          v-for="f in filtresActifs"
          :key="f.cle"
          variant="dismissible"
          size="sm"
          :label="f.label"
          :dismiss-label="`Retirer le filtre ${f.label}`"
          @dismiss="retirerFiltre(f.cle)"
        />
        <CspButton
          label="Supprimer les filtres"
          variant="tertiary-no-outline"
          size="sm"
          icon="ri:close-circle-line"
          is-icon-left
          @click="reinitialiser"
        />
      </div>
      <CspDataTable
        :key="onglet"
        v-model:page="page"
        :rows="lignes"
        :columns="COLONNES"
        :row-key="o => o.id"
        activation-mode="cell"
        caption="Mes offres d'emploi"
        :empty-label="search || nbFiltres ? 'Aucune offre ne correspond à votre recherche.' : 'Aucune offre.'"
        :page-size="10"
        @activate="id => aller({ nom: 'offre', id })"
      />
    </div>

    <CspFiltersDrawer
      v-model:open="tiroir.isOpen.value"
      :can-reset="filtres.canReset.value"
      @apply="appliquer"
      @reset="filtres.reset()"
    >
      <CspSelect
        v-if="FILTRES_ONGLET.includes('statut')"
        v-model="filtres.draft.statut"
        label="Statut"
        :options="OPTIONS_STATUT"
      />
      <template v-if="FILTRES_ONGLET.includes('publication')">
        <CspSelect
          v-model="filtres.draft.publication"
          label="Date de publication"
          :options="OPTIONS_PUBLICATION"
        />
        <CspSelect
          v-model="filtres.draft.fin"
          label="Fin de publication"
          :options="OPTIONS_FIN"
        />
      </template>
      <CspSelect
        v-model="filtres.draft.responsable"
        label="Responsable"
        :options="OPTIONS_RESPONSABLE"
      />
      <CspSelect
        v-model="filtres.draft.lieu"
        label="Lieu"
        :options="OPTIONS_LIEU"
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

.vue-filtree {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--csp-space-2);
  margin-bottom: var(--csp-space-3);
}

.vue-filtree__label {
  font-size: var(--csp-font-size-sm);
  font-weight: 700;
  color: var(--text-title-grey);
}

.recherche {
  min-width: 20rem;
}
</style>
