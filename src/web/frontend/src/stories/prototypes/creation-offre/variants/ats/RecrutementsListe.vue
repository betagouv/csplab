<script setup lang="ts">
import type { Offre } from './store'
import type { CspColumnDef } from '@/components/base/CspDataTable/table'
import { computed, ref, watch } from 'vue'
import CspButton from '@/components/base/CspButton/CspButton.vue'
import CspCheckbox from '@/components/base/CspCheckbox/CspCheckbox.vue'
import CspDataTable from '@/components/base/CspDataTable/CspDataTable.vue'
import CspDialog from '@/components/base/CspDialog/CspDialog.vue'
import CspInput from '@/components/base/CspInput/CspInput.vue'
import CspSearchBar from '@/components/base/CspSearchBar/CspSearchBar.vue'
import CspTableToolbar from '@/components/base/CspTableToolbar/CspTableToolbar.vue'
import { useTableSelection } from '@/composables/data/useTableSelection'
import { useTextSearch } from '@/composables/data/useTextSearch'
import ActionsRecrutementCell from './cellules/ActionsRecrutementCell.vue'
import FinCell from './cellules/FinCell.vue'
import ModifieCell from './cellules/ModifieCell.vue'
import NouvellesCell from './cellules/NouvellesCell.vue'
import ResponsableCell from './cellules/ResponsableCell.vue'
import TitreCell from './cellules/TitreCell.vue'
import { useNav } from './nav'
import PageAts from './PageAts.vue'
import { aProlonger, aRetirer, candidatures, ilYa } from './recrutement'
import { aujourdhui, dateLongue, dateTri, db, plusJours, plusUnMois, prolonger, retirer, sauvegarder } from './store'
import { referenceCsp } from './suivi'

// « Mes recrutements », reprise de l'écran actuel de l'outil : une offre publiée devient un recrutement.
// Ajout : la fin de publication, et dans le menu « … » la prolongation et le retrait de l'offre.
const props = defineProps<{ ongletDepart?: 'en_cours' | 'clos' }>()
const { aller, notifier } = useNav()

type Onglet = 'en_cours' | 'clos'
const ONGLETS = [
  { value: 'en_cours' as const, label: 'Recrutements en cours' },
  { value: 'clos' as const, label: 'Recrutements clos' },
]
const onglet = ref<Onglet>(props.ongletDepart ?? 'en_cours')

const COLONNES: CspColumnDef<Offre>[] = [
  { id: 'titre', header: 'Intitulé de l\'offre', accessor: o => o.titre, cellComponent: TitreCell, width: '16rem' },
  { id: 'reference', header: 'Référence CSP', wrapHeader: true, accessor: o => referenceCsp(o), width: '7rem' },
  { id: 'publication', header: 'Publication', accessor: o => ilYa(o.dateDebut), width: '7rem' },
  { id: 'fin', header: 'Fin de diffusion', wrapHeader: true, sortable: true, accessor: o => o.dateFin, cellComponent: FinCell, width: '7.5rem' },
  { id: 'responsable', header: 'Responsable', accessor: o => o.responsables?.join(' ; ') ?? '', cellComponent: ResponsableCell },
  { id: 'modifie', header: 'Dernière activité', wrapHeader: true, sortable: true, accessor: o => dateTri(o.modifieLe), cellComponent: ModifieCell, width: '7.5rem' },
  { id: 'total', header: 'Candidatures', wrapHeader: true, accessor: o => candidatures(o).total, align: 'end', width: '6.5rem' },
  { id: 'nouvelles', header: 'Nouvelles', wrapHeader: true, accessor: o => candidatures(o).nouvelles, cellComponent: NouvellesCell, width: '6rem' },
  { id: 'actions', header: '', align: 'end', width: '3.5rem', cellComponent: ActionsRecrutementCell },
]

// En cours : offre en ligne, ou retirée mais candidatures encore à traiter. Clos : archivé.
const deLOnglet = computed(() => db.offres.filter(o => onglet.value === 'clos' ? o.etat === 'archivee' : (o.etat === 'publiee' || o.etat === 'retiree')))
const { search, filtered: lignes } = useTextSearch(deLOnglet, o => [o.titre, o.id, referenceCsp(o)])
const compte = computed(() => {
  const n = lignes.value.length
  return `${n} recrutement${n > 1 ? 's' : ''} ${onglet.value === 'clos' ? 'clos' : 'en cours'}`
})
const selection = useTableSelection(lignes, o => o.id)
const page = ref(1)

// --- Prolonger la publication (depuis le menu « … ») ---
const nouvelleFin = ref('')
const ouvertProlongation = computed({
  get: () => Boolean(aProlonger.value),
  set: (v) => {
    if (!v) {
      aProlonger.value = null
    }
  },
})
watch(aProlonger, (o) => {
  if (o) {
    nouvelleFin.value = plusJours(o.dateFin, 15)
  }
})
function confirmerProlongation() {
  const o = aProlonger.value
  if (!o || !/^\d{4}-\d{2}-\d{2}$/.test(nouvelleFin.value) || nouvelleFin.value <= o.dateFin) {
    return
  }
  prolonger(o, nouvelleFin.value)
  sauvegarder()
  aProlonger.value = null
  notifier(`Publication prolongée jusqu'au ${dateLongue(nouvelleFin.value)}, sans nouvelle validation.`)
}

// --- Retirer l'offre : le recrutement continue (candidatures à traiter) ---
const urgence = ref(false)
const ouvertRetrait = computed({
  get: () => Boolean(aRetirer.value),
  set: (v) => {
    if (!v) {
      aRetirer.value = null
      urgence.value = false
    }
  },
})
const avantUnMois = computed(() => Boolean(aRetirer.value?.dateDebut) && plusUnMois(aRetirer.value!.dateDebut) > aujourdhui())
function confirmerRetrait() {
  const o = aRetirer.value
  if (!o || (avantUnMois.value && !urgence.value)) {
    return
  }
  retirer(o, avantUnMois.value ? 'urgence' : 'manuel')
  sauvegarder()
  ouvertRetrait.value = false
  notifier('Offre retirée. Le recrutement continue : les candidatures reçues restent à traiter.')
}
</script>

<template>
  <PageAts
    v-model:onglet="onglet"
    actif="recrutements"
    titre="Mes recrutements"
    :fil="[{ label: 'Mes recrutements' }]"
    :onglets="ONGLETS"
  >
    <div>
      <CspTableToolbar
        :bordered="false"
        :selection-count="selection.count.value"
        :selection-label="`${selection.count.value} recrutement${selection.count.value > 1 ? 's sélectionnés' : ' sélectionné'}`"
      >
        <template #selection-actions>
          <CspButton
            label="Assigner un responsable"
            size="sm"
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
          label="Rechercher un recrutement"
          hide-label
          placeholder="Rechercher un intitulé d'offre, une référence"
          class="recherche"
        />
        <CspButton
          label="Filtres"
          size="sm"
          variant="tertiary"
          icon="ri:filter-line"
          is-icon-left
          @click="notifier('Simulation : filtres de l\'outil existant.')"
        />
      </CspTableToolbar>
      <CspDataTable
        :key="onglet"
        v-model:page="page"
        :rows="lignes"
        :columns="COLONNES"
        :row-key="o => o.id"
        selection-mode="checkbox"
        :selected-ids="selection.selectedIds.value"
        :selection-label="o => `Sélectionner ${o.titre}`"
        activation-mode="cell"
        :caption="onglet === 'clos' ? 'Recrutements clos' : 'Recrutements en cours'"
        :empty-label="search ? 'Aucun recrutement ne correspond à votre recherche.' : 'Aucun recrutement.'"
        :page-size="8"
        @activate="id => aller({ nom: 'offre', id })"
        @toggle-row="selection.toggle"
        @toggle-all="selection.toggleVisible"
      />
    </div>

    <CspDialog
      v-model:open="ouvertProlongation"
      title="Prolonger la publication"
      size="sm"
    >
      <p class="texte">
        {{ aProlonger?.titre }} : en ligne jusqu'au {{ aProlonger ? dateLongue(aProlonger.dateFin) : '' }}.
        La nouvelle date est aussi la date limite de candidature. Pas de nouvelle validation.
      </p>
      <CspInput
        v-model="nouvelleFin"
        label="Nouvelle date limite"
        placeholder="AAAA-MM-JJ"
        :hint="nouvelleFin ? dateLongue(nouvelleFin) : ''"
      />
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="ouvertProlongation = false"
        />
        <CspButton
          label="Prolonger"
          @click="confirmerProlongation"
        />
      </template>
    </CspDialog>

    <CspDialog
      v-model:open="ouvertRetrait"
      title="Retirer l'offre ?"
      size="sm"
    >
      <p class="texte">
        L'offre ne sera plus visible des candidats. Le recrutement reste en cours : les candidatures déjà reçues restent à traiter.
      </p>
      <CspCheckbox
        v-if="avantUnMois"
        v-model="urgence"
        label="L'offre est en ligne depuis moins d'un mois : je confirme qu'il s'agit d'une urgence"
      />
      <template #footer>
        <CspButton
          label="Annuler"
          variant="secondary"
          @click="ouvertRetrait = false"
        />
        <CspButton
          label="Retirer l'offre"
          :disabled="avantUnMois && !urgence"
          @click="confirmerRetrait"
        />
      </template>
    </CspDialog>
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

.texte {
  margin: 0 0 var(--csp-space-4);
}
</style>
