<script setup lang="ts">
import type { Offre } from './store'
import type { CategorieOffre } from './suivi'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import CspTag from '@/components/base/CspTag/CspTag.vue'
import CspTagGroup from '@/components/base/CspTag/CspTagGroup.vue'
import { useTextSearch } from '@/composables/data/useTextSearch'
import ActionsOffreCell from './cellules/ActionsOffreCell.vue'
import CandidaturesCell from './cellules/CandidaturesCell.vue'
import DepublicationCell from './cellules/DepublicationCell.vue'
import EtapeCell from './cellules/EtapeCell.vue'
import IntituleCell from './cellules/IntituleCell.vue'
import StatutDepuisCell from './cellules/StatutDepuisCell.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { candidatures } from './recrutement'
import { db, fiche } from './store'
import { categorieOffre, CATEGORIES_OFFRE, dateCourte, prochaineEtape, responsable } from './suivi'

// « Mes offres d'emploi » (retour PO) : retour à un tableau, offres en préparation et en ligne.
// Les puces au-dessus filtrent le tableau par statut ; « Toutes » garde l'ordre d'urgence.
const props = defineProps<{ filtre?: string }>()
const { aller } = useNav()

const offres = computed(() => db.offres.filter(o => o.etat === 'brouillon' || o.etat === 'publiee'))
const { search, filtered: trouvees } = useTextSearch(offres, o => [o.titre, o.id, o.lieu, fiche(o.ficheId)?.service])

const ORDRE = CATEGORIES_OFFRE.map(c => c.id)
const parCategorie = computed(() => {
  const m = new Map<CategorieOffre, Offre[]>()
  for (const o of trouvees.value) {
    const c = categorieOffre(o)
    m.set(c, [...(m.get(c) ?? []), o])
  }
  return m
})
const puces = computed(() => CATEGORIES_OFFRE.filter(c => parCategorie.value.has(c.id)))

// Accès direct depuis le tableau de bord.
const DEPUIS_ACCUEIL: Record<string, CategorieOffre> = { a_publier: 'validee', en_attente: 'en_attente', brouillon: 'brouillon', validation_refusee: 'validation_refusee', bientot: 'en_ligne' }
const puce = ref<string | undefined>((props.filtre && DEPUIS_ACCUEIL[props.filtre]) || 'toutes')
// Recliquer la puce active la désélectionne : on revient à « Toutes ».
watch(puce, (v) => {
  if (!v) {
    puce.value = 'toutes'
  }
})

const lignes = computed(() => trouvees.value
  .filter(o => !puce.value || puce.value === 'toutes' || categorieOffre(o) === puce.value)
  .sort((a, b) => ORDRE.indexOf(categorieOffre(a)) - ORDRE.indexOf(categorieOffre(b))))

const COLONNES: CspColumnDef<Offre>[] = [
  { id: 'intitule', header: 'Intitulé', accessor: o => o.titre, cellComponent: IntituleCell },
  { id: 'statut', header: 'Statut', sortable: true, accessor: o => ORDRE.indexOf(categorieOffre(o)), cellComponent: StatutDepuisCell, width: '11rem' },
  { id: 'etape', header: 'Prochaine étape', accessor: o => prochaineEtape(o).label, cellComponent: EtapeCell, width: '12rem' },
  { id: 'responsable', header: 'Responsable', accessor: o => responsable(o), width: '9rem' },
  { id: 'enligne', header: 'Mise en ligne', wrapHeader: true, sortable: true, accessor: o => (o.etat === 'publiee' ? dateCourte(o.dateDebut) : '—'), width: '7.5rem' },
  { id: 'depublication', header: 'Dépublication', wrapHeader: true, sortable: true, accessor: o => (o.etat === 'publiee' ? o.dateFin : ''), cellComponent: DepublicationCell, width: '7.5rem' },
  { id: 'candidatures', header: 'Candidatures', wrapHeader: true, sortable: true, accessor: o => (o.etat === 'publiee' ? candidatures(o).total : -1), cellComponent: CandidaturesCell, width: '6.5rem' },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: ActionsOffreCell },
]

const compte = computed(() => {
  const n = lignes.value.length
  return `${n} offre${n > 1 ? 's' : ''}`
})
const page = ref(1)
</script>

<template>
  <PageAts
    actif="offres"
    titre="Mes offres d'emploi"
    sous-titre="Retrouvez toutes vos offres d'emploi en ligne et en préparation."
    :fil="[{ label: 'Mes offres d\'emploi' }]"
  >
    <template #actions>
      <CspButton
        label="Créer une offre"
        variant="secondary"
        size="sm"
        icon="ri:add-line"
        is-icon-left
        @click="aller({ nom: 'creation' })"
      />
    </template>

    <CspTagGroup
      v-model="puce"
      type="single"
      size="sm"
      aria-label="Filtrer les offres par statut"
    >
      <CspTag
        variant="selectable"
        value="toutes"
        :label="`Toutes (${trouvees.length})`"
      />
      <CspTag
        v-for="c in puces"
        :key="c.id"
        variant="selectable"
        :value="c.id"
        :label="`${c.label} (${parCategorie.get(c.id)!.length})`"
      />
    </CspTagGroup>

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
          placeholder="Rechercher un intitulé, un lieu, une référence"
          class="recherche"
        />
      </CspTableToolbar>
      <CspDataTable
        :key="puce"
        v-model:page="page"
        :rows="lignes"
        :columns="COLONNES"
        :row-key="o => o.id"
        activation-mode="cell"
        caption="Mes offres d'emploi"
        :empty-label="search ? 'Aucune offre ne correspond à votre recherche.' : 'Aucune offre.'"
        :page-size="10"
        @activate="id => aller({ nom: 'offre', id })"
      />
    </div>
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
