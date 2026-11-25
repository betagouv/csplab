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
import ActionsOffreCell from './cellules/ActionsOffreCell.vue'
import ActiviteOffreCell from './cellules/ActiviteOffreCell.vue'
import CandidaturesCell from './cellules/CandidaturesCell.vue'
import DepublicationCell from './cellules/DepublicationCell.vue'
import EtatPreparationCell from './cellules/EtatPreparationCell.vue'
import IntituleCell from './cellules/IntituleCell.vue'
import ResponsablesCell from './cellules/ResponsablesCell.vue'
import StatutDepuisCell from './cellules/StatutDepuisCell.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { candidatures } from './recrutement'
import { dateTri, db, fiche, UTILISATEUR } from './store'
import { actionOffre, categorieOffre, CATEGORIES_OFFRE, etatPreparation, PHASES, responsable, responsables } from './suivi'

// « Mes offres d'emploi » (sans autorisation) : onglets par statut, recherche, filtres, colonnes selon l'onglet (Alice, 25/11/2026).
const props = defineProps<{ filtre?: string }>()
const { aller } = useNav()

const offres = computed(() => db.offres)
const { search, filtered: trouvees } = useTextSearch(offres, o => [o.titre, o.id, o.lieu, fiche(o.ficheId)?.service])

const ORDRE = CATEGORIES_OFFRE.map(c => c.id)

// --- Filtres (retour PO, L3), dans un tiroir et appliqués au clic, comme sur les autres listes ---
const TOUS = 'tous'
const filtres = useDraft(() => ({ aFaire: TOUS as string, responsable: TOUS, service: TOUS, lieu: TOUS, categorie: TOUS }))
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
const nbFiltres = computed(() => Object.values(filtres.applied).filter(v => v !== TOUS).length)
const service = (o: Offre) => o.service ?? fiche(o.ficheId)?.service.split(' — ').at(-1) ?? ''
function options(tous: string, valeurs: string[]) {
  return [{ value: TOUS, label: tous }, ...[...new Set(valeurs.filter(Boolean))].sort().map(v => ({ value: v, label: v }))]
}
const OPTIONS_RESPONSABLE = computed(() => options('Tous les responsables', offres.value.flatMap(responsables)))
const OPTIONS_SERVICE = computed(() => options('Tous les services', offres.value.map(service)))
const OPTIONS_LIEU = computed(() => options('Tous les lieux', offres.value.flatMap(o => o.lieu.split(',').map(l => l.trim()))))
const OPTIONS_A_FAIRE = [
  { value: TOUS, label: 'Toutes les offres' },
  { value: 'prolonger', label: 'Se terminent dans moins de 7 jours' },
  { value: 'publier', label: 'Prêtes à publier' },
]
// Filtres appliqués, annoncés au-dessus du tableau (« Vue filtrée »), chacun supprimable.
const LIBELLES_FILTRES: Record<string, string> = { aFaire: 'À faire', responsable: 'Responsable', service: 'Service', lieu: 'Lieu', categorie: 'Catégorie' }
const filtresActifs = computed(() => Object.entries(filtres.applied)
  .filter(([, v]) => v !== TOUS)
  .map(([cle, v]) => ({ cle, label: `${LIBELLES_FILTRES[cle]} : ${cle === 'aFaire' ? OPTIONS_A_FAIRE.find(x => x.value === v)?.label : v}` })))
function retirerFiltre(cle: string) {
  filtres.syncDraft()
  ;(filtres.draft as Record<string, string>)[cle] = TOUS
  filtres.apply()
}
const OPTIONS_CATEGORIE = computed(() => options('Toutes les catégories', offres.value.map(o => o.categorie ? `Catégorie ${o.categorie}` : '')))
const filtrees = computed(() => trouvees.value.filter((o) => {
  const f = filtres.applied
  return (f.responsable === TOUS || responsables(o).includes(f.responsable))
    && (f.service === TOUS || service(o) === f.service)
    && (f.lieu === TOUS || o.lieu.split(',').map(l => l.trim()).includes(f.lieu))
    && (f.categorie === TOUS || `Catégorie ${o.categorie}` === f.categorie)
    && (f.aFaire === TOUS || actionOffre(o, peutPublier.value)?.type === f.aFaire)
}))

// --- Onglets par statut : En préparation, En ligne, En pause, Archivée, puis Toutes ---
type Onglet = CategorieOffre | 'toutes'
const parPhase = computed(() => {
  const m = new Map<CategorieOffre, number>()
  for (const o of filtrees.value) {
    m.set(categorieOffre(o), (m.get(categorieOffre(o)) ?? 0) + 1)
  }
  return m
})
const onglets = computed<CspTabItem<Onglet>[]>(() => [
  ...PHASES.map(p => ({ value: p.id, label: `${p.label} (${parPhase.value.get(p.id) ?? 0})` })),
  { value: 'toutes', label: `Toutes (${filtrees.value.length})` },
])
// Accès direct depuis le tableau de bord. À l'ouverture, on arrive sur les offres en ligne (retour Alice).
const DEPUIS_ACCUEIL: Record<string, CategorieOffre> = { brouillon: 'brouillon', en_ligne: 'en_ligne', depubliee: 'en_pause', en_pause: 'en_pause', archivee: 'archivee' }
const onglet = ref<Onglet>((props.filtre && DEPUIS_ACCUEIL[props.filtre]) || 'en_ligne')

// Tri par défaut : en ligne, les fins les plus proches d'abord (L4) ; ailleurs, l'activité la plus récente d'abord.
function dateActivite(o: Offre) {
  const d = { brouillon: o.modifieLe, en_ligne: o.publieeLe ?? o.dateDebut, en_pause: o.retireeLe ?? o.dateFin, archivee: o.archiveeLe ?? '' }[categorieOffre(o)]
  return /^\d{4}-/.test(d) ? d : dateTri(d)
}
// --- Encart « À faire » (prolonger, publier) : un clic applique le filtre « À faire » et ouvre l'onglet concerné ---
const compteAFaire = computed(() => {
  const c: Record<CarteAFaire, number> = { prolonger: 0, publier: 0 }
  for (const o of offres.value) {
    const a = actionOffre(o, peutPublier.value)
    if (a && a.type !== 'continuer') {
      c[a.type]++
    }
  }
  return c
})
const ONGLET_ACTION: Record<CarteAFaire, CategorieOffre> = { prolonger: 'en_ligne', publier: 'brouillon' }
function choisirAction(t: CarteAFaire) {
  filtres.syncDraft()
  filtres.draft.aFaire = filtres.applied.aFaire === t ? TOUS : t
  filtres.apply()
  if (filtres.applied.aFaire !== TOUS) {
    onglet.value = ONGLET_ACTION[t]
  }
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
    // Statut : badge dans « Toutes » ; texte simple dans « En préparation » (Brouillon, Prête à publier) ; rien ailleurs.
    ...(onglet.value === 'toutes' ? [{ id: 'statut', header: 'Statut', sortable: true, accessor: (o: Offre) => ORDRE.indexOf(categorieOffre(o)), cellComponent: StatutDepuisCell, width: '7.5rem' }] : []),
    ...(onglet.value === 'brouillon' ? [{ id: 'statut', header: 'Statut', sortable: true, accessor: (o: Offre) => etatPreparation(o), cellComponent: EtatPreparationCell, width: '8rem' }] : []),
    { id: 'responsable', header: 'Responsable', accessor: o => responsable(o), cellComponent: ResponsablesCell, width: '11rem' },
    { id: 'activite', header: 'Activité sur l\'offre', wrapHeader: true, sortable: true, accessor: (o: Offre) => dateActivite(o), cellComponent: ActiviteOffreCell, width: '11rem' },
    ...(avecFin ? [{ id: 'fin', header: 'Fin de publication', wrapHeader: true, sortable: true, accessor: (o: Offre) => (o.etat === 'publiee' || o.etat === 'retiree' ? o.dateFin : ''), cellComponent: DepublicationCell, width: '8rem' }] : []),
    ...(avecCandidatures ? [{ id: 'candidatures', header: 'Candidatures', wrapHeader: true, sortable: true, accessor: (o: Offre) => (o.etat !== 'brouillon' ? candidatures(o).total : -1), cellComponent: CandidaturesCell, width: '6.5rem' }] : []),
    { id: 'actions', header: '', align: 'end', width: '9rem', cellComponent: ActionsOffreCell },
  ]
})

const compte = computed(() => {
  const n = lignes.value.length
  return `${n} offre${n > 1 ? 's' : ''}`
})
const page = ref(1)
</script>

<template>
  <PageAts
    v-model:onglet="onglet"
    actif="offres"
    titre="Mes offres d'emploi"
    sous-titre="Retrouvez toutes vos offres d'emploi : en préparation, en ligne, en pause et archivées."
    :fil="[{ label: 'Mes offres d\'emploi' }]"
    :onglets="onglets"
  >
    <template #avant-onglets>
      <AFaire
        :compte="compteAFaire"
        :actif="filtres.applied.aFaire === TOUS ? null : filtres.applied.aFaire as CarteAFaire"
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
          @click="filtres.reset()"
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
        v-model="filtres.draft.aFaire"
        label="À faire"
        :options="OPTIONS_A_FAIRE"
      />
      <CspSelect
        v-model="filtres.draft.responsable"
        label="Responsable"
        :options="OPTIONS_RESPONSABLE"
      />
      <CspSelect
        v-model="filtres.draft.service"
        label="Service"
        :options="OPTIONS_SERVICE"
      />
      <CspSelect
        v-model="filtres.draft.lieu"
        label="Lieu"
        :options="OPTIONS_LIEU"
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
